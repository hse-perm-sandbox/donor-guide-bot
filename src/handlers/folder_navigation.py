from telebot import types
from src.database.database import get_session
from src.database.repositories.folder import FolderRepository
from src.database.repositories.question import QuestionRepository

def register_folder_navigation_handlers(bot):
    session = next(get_session())
    folder_repo = FolderRepository(session)
    question_repo = QuestionRepository(session)

    @bot.message_handler(func=lambda msg: msg.text == "Ответы на часто задаваемые вопросы")
    def show_root_folders(message):
        show_folder_level(chat_id=message.chat.id, parent_id=None)

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
                bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    text="🔍 В этой категории пока нет вопросов.",
                )

    @bot.callback_query_handler(func=lambda call: call.data.startswith("question_"))
    def question_callback_handler(call):
        question_id = int(call.data.split("_")[1])
        question = question_repo.get_by_id(question_id)

        if not question:
            bot.answer_callback_query(call.id, "Вопрос не найден.")
            return

        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(
            text="⬅ Назад", callback_data=f"backtofolder_{question.folder_id}"
        ))

        text = f"❓ <b>{question.question}</b>\n\n{question.answer_text or 'Ответ пока не добавлен.'}"
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=text,
            parse_mode="HTML",
            reply_markup=keyboard
        )

    @bot.callback_query_handler(func=lambda call: call.data.startswith("backtofolder_"))
    def back_to_folder(call):
        folder_id = int(call.data.split("_")[1])
        questions = question_repo.get_by_folder(folder_id)
        show_question_list(call.message.chat.id, questions, call.message.message_id, folder_id)

    def show_folder_level(chat_id: int, parent_id: int | None, message_id: int | None = None):
        folders = folder_repo.get_by_parent(parent_id)
        keyboard = types.InlineKeyboardMarkup()

        for folder in folders:
            keyboard.add(types.InlineKeyboardButton(
                text=folder.folder_name,
                callback_data=f"folder_{folder.id}"
            ))

        if parent_id is not None:
            current = folder_repo.get_by_id(parent_id)
            back_target = current.parent_id
            keyboard.add(types.InlineKeyboardButton(
                text="⬅ Назад", callback_data=f"folder_{back_target if back_target is not None else 'root'}"
            ))

        text = "📂 Выберите раздел:"
        if message_id:
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=text,
                reply_markup=keyboard
            )
        else:
            bot.send_message(chat_id, text, reply_markup=keyboard)

    def show_question_list(chat_id: int, questions: list, message_id: int, folder_id: int):
        keyboard = types.InlineKeyboardMarkup()

        for q in questions:
            keyboard.add(types.InlineKeyboardButton(
                text=q.question[:50],
                callback_data=f"question_{q.id}"
            ))


        folder = folder_repo.get_by_id(folder_id)
        back_target = folder.parent_id

        keyboard.add(types.InlineKeyboardButton(
            text="⬅ Назад",
            callback_data=f"folder_{back_target if back_target is not None else 'root'}"
        ))

        bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="📖 Выберите вопрос:",
            reply_markup=keyboard
        )
