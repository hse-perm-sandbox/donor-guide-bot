import logging
from telebot import types
from src.database.database import get_session
from src.database.repositories.folder import FolderRepository
from src.database.repositories.question import QuestionRepository
import os
from src.config import settings

logger = logging.getLogger(__name__)

def _send_photo_from_path_and_update_db(bot, session, question, chat_id, caption, reply_markup, image_path, question_title_formatted, answer_text_for_display):

    try:
        logger.info(f"Отправка фото из файла: {image_path} для вопроса ID {question.id}")
        absolute_image_path = os.path.join(settings.ASSETS_DIR, image_path)

        with open(absolute_image_path, 'rb') as photo_file:
            sent_message = bot.send_photo(
                chat_id=chat_id,
                photo=photo_file,
                caption=caption,
                parse_mode="HTML",
                reply_markup=reply_markup
            )
        
        if sent_message and hasattr(sent_message, 'photo') and sent_message.photo:
            new_file_id = sent_message.photo[-1].file_id
            if question.answer_file_id != new_file_id:
                question.answer_file_id = new_file_id
                try:
                    session.commit()
                    logger.info(f"Сохранен новый file_id '{question.answer_file_id}' для вопроса ID {question.id}")
                except Exception as db_exc:
                    logger.error(f"Ошибка сохранения file_id '{question.answer_file_id}' в БД для вопроса ID {question.id}: {db_exc}")
                    session.rollback()

                    return False 
        return True
    except FileNotFoundError:
        logger.warning(f"Файл изображения не найден: {image_path} для вопроса ID {question.id}")
        error_text = f"{question_title_formatted}\n\n🖼 Изображение не найдено.\nПожалуйста, проверьте путь: {image_path}\n\n{answer_text_for_display}"
        bot.send_message(chat_id, error_text, parse_mode="HTML", reply_markup=reply_markup)
        return False
    except Exception as send_exc:
        logger.error(f"Ошибка при отправке фото из файла {image_path} (вопрос ID {question.id}): {send_exc}")
        error_text = f"{question_title_formatted}\n\n⚠️ Ошибка при отправке изображения.\n\n{answer_text_for_display}"
        bot.send_message(chat_id, error_text, parse_mode="HTML", reply_markup=reply_markup)
        return False

def register_folder_navigation_handlers(bot):
    session = next(get_session())
    folder_repo = FolderRepository(session)
    question_repo = QuestionRepository(session)

    @bot.message_handler(func=lambda msg: msg.text == "Ответы на часто задаваемые вопросы")
    def show_root_folders(message):
        show_folder_level(chat_id=message.chat.id, parent_id=None, message_id=None)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("folder_"))
    def folder_callback_handler(call):
        folder_id_str = call.data.split("_")[1]
        folder_id = None if folder_id_str == "root" else int(folder_id_str)

        subfolders = folder_repo.get_by_parent(folder_id)

        if subfolders:
            show_folder_level(call.message.chat.id, folder_id, call.message.message_id)
        else:
            questions = question_repo.get_by_folder(folder_id)
            if questions:
                show_question_list(call.message.chat.id, questions, call.message.message_id, folder_id)
            else:
                keyboard = types.InlineKeyboardMarkup()
                current_folder_obj = folder_repo.get_by_id(folder_id)

                if current_folder_obj and current_folder_obj.parent_id is not None:
                    back_target_id = current_folder_obj.parent_id
                    keyboard.add(types.InlineKeyboardButton(
                        text="⬅ Назад", callback_data=f"folder_{back_target_id}"
                    ))
                else:
                    keyboard.add(types.InlineKeyboardButton(
                        text="⬅ Назад к категориям", callback_data="folder_root"
                    ))
                
                try:
                    bot.edit_message_text(
                        chat_id=call.message.chat.id,
                        message_id=call.message.message_id,
                        text="🔍 В этой категории пока нет вопросов.",
                        reply_markup=keyboard
                    )
                except Exception as e_edit:
                    logger.warning(f"Ошибка редактирования сообщения в folder_callback_handler: {e_edit}. Отправка нового сообщения.")
                    bot.send_message(call.message.chat.id, "🔍 В этой категории пока нет вопросов.", reply_markup=keyboard)


    @bot.callback_query_handler(func=lambda call: call.data.startswith("question_"))
    def question_callback_handler(call):
        question_id = int(call.data.split("_")[1])
        question = question_repo.get_by_id(question_id)

        if not question:
            bot.answer_callback_query(call.id, "Вопрос не найден.")
            return

        keyboard = types.InlineKeyboardMarkup()
        back_callback_data = f"backtofolder_{question.folder_id}" if question.folder_id is not None else "folder_root"
        keyboard.add(types.InlineKeyboardButton(
            text="⬅ Назад", callback_data=back_callback_data
        ))

        question_title_formatted = f"❓ <b>{question.question}</b>"
        answer_text_for_display = question.answer_text or "Ответ пока не добавлен."

        if not question.answer_picture_path:

            logger.info(f"Отправка текстового ответа для вопроса ID {question.id}, т.к. answer_picture_path не указан.")
            text_to_send = f"{question_title_formatted}\n\n{answer_text_for_display}"
            try:
                bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    text=text_to_send,
                    parse_mode="HTML",
                    reply_markup=keyboard
                )
            except Exception as e_edit:
                logger.error(f"Ошибка редактирования сообщения для текстового ответа (вопрос ID {question.id}): {e_edit}. Попытка отправить как новое сообщение.")
   
                bot.send_message(call.message.chat.id, text_to_send, parse_mode="HTML", reply_markup=keyboard)

        else:
  
            full_caption = f"{question_title_formatted}\n\n{answer_text_for_display}".strip()


            try:
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                logger.debug(f"Сообщение {call.message.message_id} удалено перед отправкой фото для вопроса ID {question.id}")
            except Exception as e_delete:
                logger.warning(f"Не удалось удалить сообщение {call.message.message_id} (вопрос ID {question.id}): {e_delete}")

            photo_sent_successfully = False
            if question.answer_file_id:

                try:
                    logger.info(f"Попытка отправки фото по file_id: {question.answer_file_id} для вопроса ID {question.id}")
                    bot.send_photo(
                        chat_id=call.message.chat.id,
                        photo=question.answer_file_id,
                        caption=full_caption,
                        parse_mode="HTML",
                        reply_markup=keyboard
                    )
                    photo_sent_successfully = True
                except Exception as e_file_id:
                    logger.warning(f"Не удалось отправить фото по file_id '{question.answer_file_id}' (вопрос ID {question.id}): {e_file_id}. Попытка отправки как нового файла.")
                    question.answer_file_id = None

            
            if not photo_sent_successfully:
                image_full_path = question.answer_picture_path 
                
                _send_photo_from_path_and_update_db(
                    bot, session, question, call.message.chat.id, full_caption, keyboard,
                    image_full_path, question_title_formatted, answer_text_for_display
                )

    @bot.callback_query_handler(func=lambda call: call.data.startswith("backtofolder_"))
    def back_to_folder(call):
        folder_id_str = call.data.split("_")[1]

        try:
            folder_id = int(folder_id_str)
        except ValueError:
            logger.warning(f"Некорректный folder_id в backtofolder_: {folder_id_str}. Переход в корень.")
            try:

                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            except Exception as e_delete:
                logger.error(f"Ошибка удаления сообщения (backtofolder fallback to root, msg_id: {call.message.message_id}): {e_delete}")
            show_folder_level(chat_id=call.message.chat.id, parent_id=None, message_id=None)
            return

        try:
            bot.delete_message(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id
            )
        except Exception as e_delete:
            logger.warning(f"Ошибка удаления сообщения в back_to_folder (msg_id: {call.message.message_id}): {e_delete}")

        questions = question_repo.get_by_folder(folder_id)
        show_question_list(call.message.chat.id, questions, message_id=None, folder_id=folder_id)

    def show_folder_level(chat_id: int, parent_id: int | None, message_id: int | None = None):

        from typing import Optional 
        parent_id_typed: Optional[int] = parent_id
        message_id_typed: Optional[int] = message_id
        
        folders = folder_repo.get_by_parent(parent_id_typed)
        keyboard = types.InlineKeyboardMarkup(row_width=1)

        for folder in folders:
            keyboard.add(types.InlineKeyboardButton(
                text=folder.folder_name,
                callback_data=f"folder_{folder.id}"
            ))

        if parent_id_typed is not None:
            current_folder_obj = folder_repo.get_by_id(parent_id_typed)

            back_target_id_str = "root"
            if current_folder_obj:
                if current_folder_obj.parent_id is not None:
                    back_target_id_str = str(current_folder_obj.parent_id)

            
            keyboard.add(types.InlineKeyboardButton(
                text="⬅ Назад", callback_data=f"folder_{back_target_id_str}" 
            ))

        text = "📂 Выберите раздел:"
        if message_id_typed:
            try:
                bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=message_id_typed,
                    text=text,
                    reply_markup=keyboard
                )
            except Exception as e:
                logger.warning(f"Ошибка редактирования в show_folder_level (msg_id: {message_id_typed}), отправка нового: {e}")
                bot.send_message(chat_id, text, reply_markup=keyboard)
        else:
            bot.send_message(chat_id, text, reply_markup=keyboard)

    def show_question_list(chat_id: int, questions: list, message_id: int | None, folder_id: int):
        from typing import Optional
        message_id_typed: Optional[int] = message_id

        keyboard = types.InlineKeyboardMarkup(row_width=1)
        
        text_to_display = "📖 Выберите вопрос:"

        if not questions:
            text_to_display = "🔍 В этой папке пока нет вопросов."
        else:
            for q in questions:

                question_text_for_button = str(q.question)[:45] + ("..." if len(str(q.question)) > 45 else "")
                keyboard.add(types.InlineKeyboardButton(
                    text=question_text_for_button,  
                    callback_data=f"question_{q.id}"
                ))

        current_folder_obj = folder_repo.get_by_id(folder_id)
        back_target_id_str = "root"
        if current_folder_obj:
            if current_folder_obj.parent_id is not None:
                back_target_id_str = str(current_folder_obj.parent_id)

            keyboard.add(types.InlineKeyboardButton(
                text="⬅ Назад к разделам", 
                callback_data=f"folder_{back_target_id_str}"
            ))
        else:

            logger.warning(f"Папка с ID {folder_id} не найдена в show_question_list. Кнопка 'Назад' ведет в корень.")
            keyboard.add(types.InlineKeyboardButton(
                text="⬅ Назад к категориям", 
                callback_data="folder_root"
            ))

        if message_id_typed:
            try:
                bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=message_id_typed,
                    text=text_to_display,
                    reply_markup=keyboard
                )
            except Exception as e:
                logger.warning(f"Ошибка редактирования в show_question_list (msg_id: {message_id_typed}), отправка нового: {e}")
                bot.send_message(chat_id, text_to_display, reply_markup=keyboard)
        else:
            bot.send_message(chat_id, text_to_display, reply_markup=keyboard)