import logging
from telebot import types

from src.config import settings
from src.database.database import get_session
from src.database.repositories.user import UserRepository
from src.database.repositories.user_question import UserQuestionRepository
from src.schemas.user import UserBase
from src.schemas.user_question import UserQuestionBase


def setup_handlers(bot):
    logger = logging.getLogger(__name__)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    questions_button = types.KeyboardButton("Ответы на часто задаваемые вопросы")
    special_question_button = types.KeyboardButton("Написать свой вопрос")
    donate_button = types.KeyboardButton("Пожертвовать в фонд")
    markup.add(questions_button)
    markup.add(special_question_button)
    markup.add(donate_button)

    user_data = {}

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
            show_questions_menu(message)

        elif message.text == "Написать свой вопрос":

            msg = bot.send_message(
                message.chat.id, "📝 Пожалуйста, напишите ваш вопрос. (Отправьте одним сообщением)"
            )

            bot.register_next_step_handler(msg, process_question_text)
            user_data[message.chat.id] = {"state": "awaiting_question"}

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

    def process_question_text(message):
        user_data[message.chat.id]["question"] = message.text
        msg = bot.send_message(message.chat.id, "📧 Теперь укажите ваш email для обратной связи:")
        bot.register_next_step_handler(msg, process_email)

    def process_email(message):
        if "@" not in message.text or "." not in message.text:
            msg = bot.send_message(
                message.chat.id, "❌ Это не похоже на email. Пожалуйста, введите корректный адрес:"
            )
            bot.register_next_step_handler(msg, process_email)
            return

        user_data[message.chat.id]["email"] = message.text

        repo = UserRepository(next(get_session()))
        user = repo.create_or_update(
            UserBase.model_construct(
                telegram_chat_id=message.chat.id,
                telegram_username=bot.get_chat(message.chat.id).username,
                email=message.text,
            )
        )

        sent = True
        try:
            send_question_to_fund(message.chat.id)
        except Exception as error:
            logger.error(error)
            sent = False
        repo = UserQuestionRepository(next(get_session()))
        repo.create(
            UserQuestionBase.model_construct(
                question_text=user_data[message.chat.id]["question"],
                sent=sent,
                user_id=user.id,
            )
        )

        bot.send_message(
            message.chat.id,
            "✅ Ваш вопрос и контакты отправлены в фонд. Спасибо!",
            reply_markup=markup,
        )

    def send_question_to_fund(chat_id):
        data = user_data.get(chat_id, {})
        question = data.get("question", "Не указан")
        email = data.get("email", "Не указан")
        user = bot.get_chat(chat_id)

        bot.send_message(
            settings.RESEND_CHAT_ID,
            f"❓ Новый вопрос от пользователя:\n"
            f"Имя: {user.first_name}\n"
            f"Username: @{user.username}\n"
            f"Email: {email}\n\n"
            f"Вопрос: {question}",
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
