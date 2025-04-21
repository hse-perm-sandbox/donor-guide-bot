from telebot import types

from src.database.database import get_session
from src.database.repositories.folder import FolderRepository
from .user_questions import register_user_question_handlers
from src.handlers.keyboards import get_inline_keyboard_for_folder, get_main_menu


def setup_handlers(bot):
    markup = get_main_menu()
    register_user_question_handlers(bot)

    @bot.message_handler(commands=["start"])
    def start_message(message):
        bot.send_message(
            message.chat.id,
            text="Привет, {0.first_name} 👋\nВоспользуйся кнопками".format(message.from_user),
            reply_markup=markup,
        )

    @bot.message_handler(content_types=["text"])
    def text_messages(message):

        if message.text == "Ответы на часто задаваемые вопросы":
            folder_repo = FolderRepository(next(get_session()))
            root_folder = folder_repo.get_root_folder_with_content()
            keyboard = get_inline_keyboard_for_folder(root_folder)
            # Проверяем, пришло ли сообщение или callback
            if isinstance(message, types.Message):
                # Если это сообщение (первый вызов)
                bot.send_message(message.chat.id, "Главное меню:", reply_markup=keyboard)
            else:
                # Если это callback (нажатие кнопки "Назад")
                bot.edit_message_text(
                    chat_id=message.message.chat.id,
                    message_id=message.message.message_id,
                    text="Главное меню:",
                    reply_markup=keyboard,
                )

        elif message.text == "Пожертвовать в фонд":
            bot.send_message(
                message.chat.id,
                "Спасибо за ваше желание помочь! Пожалуйста, перейдите по следующей ссылке для пожертвования: [ссылка].",
            )

        else:
            bot.send_message(
                message.chat.id,
                "ℹ️ Пожалуйста, воспользуйтесь кнопками меню.",
                reply_markup=markup,
            )

    def show_questions_menu(message_or_call):
        keyboard = types.InlineKeyboardMarkup()

        question_one = types.InlineKeyboardButton(
            text="🧬 Донорство костного мозга", callback_data="question_1"
        )

        question_two = types.InlineKeyboardButton(
            text="🩸 Донорство крови", callback_data="question_2"
        )

        question_three = types.InlineKeyboardButton(
            text="📞 Контакты фонда", callback_data="question_3"
        )

        keyboard.row(question_one)
        keyboard.row(question_two)
        keyboard.row(question_three)

        # Проверяем, пришло ли сообщение или callback
        if isinstance(message_or_call, types.Message):
            # Если это сообщение (первый вызов)
            bot.send_message(message_or_call.chat.id, "Главное меню:", reply_markup=keyboard)
        else:
            # Если это callback (нажатие кнопки "Назад")
            bot.edit_message_text(
                chat_id=message_or_call.message.chat.id,
                message_id=message_or_call.message.message_id,
                text="Главное меню:",
                reply_markup=keyboard,
            )

    @bot.callback_query_handler(func=lambda call: True)
    def callback_query(call):

        if call.data == "question_1":
            markup = types.InlineKeyboardMarkup()

            btn1 = types.InlineKeyboardButton(
                "Что нужно знать", callback_data="bone_marrow_option_1"
            )

            btn2 = types.InlineKeyboardButton(
                "Как стать донором", callback_data="bone_marrow_option_2"
            )

            btn3 = types.InlineKeyboardButton(
                "Как проходит донация", callback_data="bone_marrow_option_3"
            )

            btn4 = types.InlineKeyboardButton(
                "Часто задаваемые вопросы", callback_data="bone_marrow_option_4"
            )

            back = types.InlineKeyboardButton("Назад", callback_data="bone_marrow_option_5")

            markup.add(btn1)
            markup.add(btn2)
            markup.add(btn3)
            markup.add(btn4)
            markup.add(back)

            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="🧬 Донорство костного мозга:",
                reply_markup=markup,
            )
            bot.answer_callback_query(call.id)

        elif call.data == "bone_marrow_option_1":
            markup = types.InlineKeyboardMarkup()
            back = types.InlineKeyboardButton("Назад", callback_data="question_1")

            btn_1 = types.InlineKeyboardButton(
                "Что такое костный мозг?", callback_data="what_should_you_know_option_1"
            )

            btn_2 = types.InlineKeyboardButton(
                "Что такое трансплантация костного мозга?",
                callback_data="what_should_you_know_option_2",
            )

            btn_3 = types.InlineKeyboardButton(
                "Что такое национальный регистр потенциальных доноров?",
                callback_data="what_should_you_know_option_3",
            )

            btn_4 = types.InlineKeyboardButton(
                "Почему важно пополнять российский регистр?",
                callback_data="what_should_you_know_option_4",
            )

            markup.add(btn_1)
            markup.add(btn_2)
            markup.add(btn_3)
            markup.add(btn_4)
            markup.add(back)

            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="Что нужно знать:",
                reply_markup=markup,
            )
            bot.answer_callback_query(call.id)

        elif call.data == "bone_marrow_option_2":
            markup = types.InlineKeyboardMarkup()
            back = types.InlineKeyboardButton("Назад", callback_data="question_1")

            btn_1 = types.InlineKeyboardButton(
                "Кто может стать донором костного мозга?",
                callback_data="how_to_become_a_donor_option_1",
            )

            btn_2 = types.InlineKeyboardButton(
                "Как попасть в федеральный регистр?", callback_data="how_to_become_a_donor_option_2"
            )

            btn_3 = types.InlineKeyboardButton(
                "Как ищут донора костного мозга?", callback_data="how_to_become_a_donor_option_3"
            )

            markup.add(btn_1)
            markup.add(btn_2)
            markup.add(btn_3)
            markup.add(back)

            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="Как стать донором:",
                reply_markup=markup,
            )
            bot.answer_callback_query(call.id)

        elif call.data == "bone_marrow_option_3":
            markup = types.InlineKeyboardMarkup()
            back = types.InlineKeyboardButton("Назад", callback_data="question_1")

            btn_1 = types.InlineKeyboardButton(
                "Как происходит забор костного мозга у донора?",
                callback_data="how_does_donation_work_option_1",
            )

            btn_2 = types.InlineKeyboardButton(
                "Нужно ли готовиться к сдаче костного мозга?",
                callback_data="how_does_donation_work_option_2",
            )

            markup.add(btn_1)
            markup.add(btn_2)
            markup.add(back)

            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="Как проходит донация:",
                reply_markup=markup,
            )
            bot.answer_callback_query(call.id)

        elif call.data == "bone_marrow_option_4":
            markup = types.InlineKeyboardMarkup()
            back = types.InlineKeyboardButton("Назад", callback_data="question_1")

            btn_1 = types.InlineKeyboardButton(
                "Как происходит забор костного мозга у донора?", callback_data="FAQ_option_1"
            )

            markup.add(btn_1)
            markup.add(back)

            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="Часто задаваемые вопросы:",
                reply_markup=markup,
            )
            bot.answer_callback_query(call.id)

        elif call.data == "bone_marrow_option_5":
            show_questions_menu(call)
            bot.answer_callback_query(call.id)

        elif call.data == "question_2":
            markup = types.InlineKeyboardMarkup()

            btn1 = types.InlineKeyboardButton("Как подготовиться", callback_data="blood_option_1")

            btn2 = types.InlineKeyboardButton("После донации", callback_data="blood_option_2")

            btn3 = types.InlineKeyboardButton("Противопоказания", callback_data="blood_option_3")

            btn4 = types.InlineKeyboardButton(
                "Часто задаваемые вопросы", callback_data="blood_option_4"
            )

            btn5 = types.InlineKeyboardButton("Как это помогает", callback_data="blood_option_5")

            btn6 = types.InlineKeyboardButton(
                "Узнать, нужны ли доноры", callback_data="blood_option_6"
            )

            back = types.InlineKeyboardButton("Назад", callback_data="blood_option_7")

            markup.add(btn1)
            markup.add(btn2)
            markup.add(btn3)
            markup.add(btn4)
            markup.add(btn5)
            markup.add(btn6)
            markup.add(back)

            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="🩸 Донорство крови:",
                reply_markup=markup,
            )
            bot.answer_callback_query(call.id)

        elif call.data == "blood_option_1":
            markup = types.InlineKeyboardMarkup()
            back = types.InlineKeyboardButton("Назад", callback_data="question_2")

            btn_1 = types.InlineKeyboardButton(
                "Как подготовиться к сдаче крови?", callback_data="get_ready_option_1"
            )

            btn_2 = types.InlineKeyboardButton(
                "Рекомендации донорам крови", callback_data="get_ready_option_2"
            )

            btn_3 = types.InlineKeyboardButton(
                "Что можно есть перед сдачей крови?", callback_data="get_ready_option_3"
            )

            btn_4 = types.InlineKeyboardButton(
                "Почему при донорстве важен вес?", callback_data="get_ready_option_4"
            )

            markup.add(btn_1)
            markup.add(btn_2)
            markup.add(btn_3)
            markup.add(btn_4)
            markup.add(back)

            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="Как подготовиться:",
                reply_markup=markup,
            )
            bot.answer_callback_query(call.id)

        elif call.data == "blood_option_2":
            markup = types.InlineKeyboardMarkup()
            back = types.InlineKeyboardButton("Назад", callback_data="question_2")

            btn_1 = types.InlineKeyboardButton(
                "Как подготовиться к сдаче крови?", callback_data="after_option_1"
            )

            btn_2 = types.InlineKeyboardButton(
                "Рекомендации донорам крови", callback_data="after_option_2"
            )

            markup.add(btn_1)
            markup.add(btn_2)
            markup.add(back)

            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="После донации:",
                reply_markup=markup,
            )
            bot.answer_callback_query(call.id)

        elif call.data == "blood_option_3":
            markup = types.InlineKeyboardMarkup()
            back = types.InlineKeyboardButton("Назад", callback_data="question_2")

            btn_1 = types.InlineKeyboardButton(
                "Показания к донорству крови и компонентов",
                callback_data="contraindications_option_1",
            )

            btn_2 = types.InlineKeyboardButton(
                "Постоянные медицинские противопоказания",
                callback_data="contraindications_option_2",
            )

            btn_3 = types.InlineKeyboardButton(
                "Временные медицинские противопоказания", callback_data="contraindications_option_3"
            )

            markup.add(btn_1)
            markup.add(btn_2)
            markup.add(btn_3)
            markup.add(back)

            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="Противопоказания:",
                reply_markup=markup,
            )
            bot.answer_callback_query(call.id)

        elif call.data == "blood_option_4":
            markup = types.InlineKeyboardMarkup()
            back = types.InlineKeyboardButton("Назад", callback_data="question_2")

            btn_1 = types.InlineKeyboardButton(
                "Что делать, если боишься вида крови?", callback_data="FAQ_option_1"
            )

            btn_2 = types.InlineKeyboardButton(
                "Повышает ли донорство риск развития рака?", callback_data="FAQ_option_2"
            )

            btn_3 = types.InlineKeyboardButton(
                "Можно ли быть донором с татуировкой?", callback_data="FAQ_option_3"
            )

            btn_4 = types.InlineKeyboardButton(
                "Что такое гемоглобин и как его повысить?", callback_data="FAQ_option_3"
            )

            markup.add(btn_1)
            markup.add(btn_2)
            markup.add(btn_3)
            markup.add(btn_4)
            markup.add(back)

            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="Часто задаваемые вопросы:",
                reply_markup=markup,
            )
            bot.answer_callback_query(call.id)

        elif call.data == "blood_option_5":
            markup = types.InlineKeyboardMarkup()
            back = types.InlineKeyboardButton("Назад", callback_data="question_2")

            btn_1 = types.InlineKeyboardButton(
                "Как донорская кровь помогает реципиенту?", callback_data="how_it_helps_option_1"
            )

            markup.add(btn_1)
            markup.add(back)

            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="Как это помогает:",
                reply_markup=markup,
            )
            bot.answer_callback_query(call.id)

        elif call.data == "blood_option_6":
            markup = types.InlineKeyboardMarkup()
            back = types.InlineKeyboardButton("Назад", callback_data="question_2")

            btn_1 = types.InlineKeyboardButton(
                "Как узнать, нужны ли сейчас доноры крови?",
                callback_data="how_do_you_know_option_1",
            )

            markup.add(btn_1)
            markup.add(back)

            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="Узнать, нужны ли доноры:",
                reply_markup=markup,
            )

        elif call.data == "blood_option_7":
            show_questions_menu(call)
            bot.answer_callback_query(call.id)

        elif call.data == "question_3":

            markup = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton(
                "Где сдавать кровь в Петербурге ", callback_data="contacts_option_1"
            )

            btn2 = types.InlineKeyboardButton(
                "Список отделений переливания крови", callback_data="contacts_option_2"
            )

            btn3 = types.InlineKeyboardButton(
                "Контакты и телефон фонда", callback_data="contacts_option_3"
            )

            back = types.InlineKeyboardButton("Назад", callback_data="contacts_option_4")

            markup.add(btn1)
            markup.add(btn2)
            markup.add(btn3)
            markup.add(back)

            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="📞 Контакты фонда:",
                reply_markup=markup,
            )
            bot.answer_callback_query(call.id)

        elif call.data == "contacts_option_1":
            markup = types.InlineKeyboardMarkup()
            back = types.InlineKeyboardButton("Назад", callback_data="question_3")
            markup.add(back)

            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="🏥 Вот где можно сдавать кровь в Петербурге:\n\n"
                "1. ///////////////////\n"
                "2. ///////////////////\n"
                "3. ///////////////////////\n"
                "4. /////////////////////////",
                reply_markup=markup,
            )
            bot.answer_callback_query(call.id)

        elif call.data == "contacts_option_2":
            markup = types.InlineKeyboardMarkup()
            back = types.InlineKeyboardButton("Назад", callback_data="question_3")
            markup.add(back)

            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="🏥� Список отделений переливания крови:\n\n"
                "1. ////////////\n"
                "2. /////////////\n"
                "3. /////////////////////\n\n",
                reply_markup=markup,
            )
            bot.answer_callback_query(call.id)

        elif call.data == "contacts_option_3":
            markup = types.InlineKeyboardMarkup()
            back = types.InlineKeyboardButton("Назад", callback_data="question_3")
            markup.add(back)

            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="📞 Контактная информация фонда:\n\n"
                "Телефон: //////////////\n"
                "Email: ///////////////\n"
                "Адрес: //////////////////\n"
                "Сайт: ///////////////////",
                reply_markup=markup,
            )
            bot.answer_callback_query(call.id)

        elif call.data == "contacts_option_4":
            show_questions_menu(call)
            bot.answer_callback_query(call.id)
