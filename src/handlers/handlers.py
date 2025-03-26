from telebot import types

from src.config import Settings


def setup_handlers(bot):
    settings = Settings()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    questions_button = types.KeyboardButton("Ответы на часто задаваемые вопросы")
    special_question_button = types.KeyboardButton("Написать свой вопрос")
    donate_button = types.KeyboardButton("Пожертвовать в фонд")
    markup.add(questions_button)
    markup.add(special_question_button)
    markup.add(donate_button)

    @bot.message_handler(commands=["start"])
    def start_message(message):
        print(message.chat.id)
        bot.send_message(
            message.chat.id,
            text="Привет, {0.first_name} 👋\nВоспользуйся кнопками".format(
                message.from_user
            ),
            reply_markup=markup,
        )

    @bot.message_handler(content_types=["text"])
    def text_messages(message):
        if message.text == "Ответы на часто задаваемые вопросы":
            show_questions_menu(message)
        elif message.text == "Написать свой вопрос":
            bot.send_message(message.chat.id, "Пожалуйста, напишите ваш вопрос.")
        elif message.text == "Пожертвовать в фонд":
            bot.send_message(
                message.chat.id,
                "Спасибо за ваше желание помочь! Пожалуйста, перейдите по следующей ссылке для пожертвования: [ссылка].",
            )
        else:
            bot.send_message(
                settings.RESEND_CHAT_ID,
                f"Вопрос от {message.from_user.first_name} (@{message.from_user.username}): {message.text}",
            )
            bot.send_message(
                message.chat.id, "Ваш вопрос был отправлен. Мы свяжемся с вами позже."
            )

    def show_questions_menu(message):
        keyboard = types.InlineKeyboardMarkup()
        question_one = types.InlineKeyboardButton(
            text="Вопрос 1", callback_data="question_1"
        )
        question_two = types.InlineKeyboardButton(
            text="Вопрос 2", callback_data="question_2"
        )
        question_three = types.InlineKeyboardButton(
            text="Вопрос 3", callback_data="question_3"
        )
        question_four = types.InlineKeyboardButton(
            text="Вопрос 4", callback_data="question_4"
        )
        question_five = types.InlineKeyboardButton(
            text="Вопрос 5", callback_data="question_5"
        )
        question_six = types.InlineKeyboardButton(
            text="Вопрос 6", callback_data="question_6"
        )
        back_button = types.InlineKeyboardButton(
            text="Вернуться назад", callback_data="back_to_main"
        )

        keyboard.add(
            question_one,
            question_two,
            question_three,
            question_four,
            question_five,
            question_six,
            back_button,
        )

        bot.send_message(message.chat.id, "Выберите вопрос:", reply_markup=keyboard)

    @bot.callback_query_handler(func=lambda call: True)
    def callback_query(call):
        if call.data == "question_1":
            markup = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton(
                "Вопрос 1 по теме", callback_data="option1"
            )
            btn2 = types.InlineKeyboardButton(
                "Вопрос 2 по теме", callback_data="option2"
            )
            back = types.InlineKeyboardButton("Назад", callback_data="option3")
            markup.add(btn1, btn2, back)

            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="Вопрос 1:",
                reply_markup=markup,
            )
            bot.answer_callback_query(call.id)
        elif call.data == "question_2":
            markup = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton(
                "Вопрос 1 по теме", callback_data="option1"
            )
            btn2 = types.InlineKeyboardButton(
                "Вопрос 2 по теме", callback_data="option2"
            )
            back = types.InlineKeyboardButton("Назад", callback_data="option3")
            markup.add(btn1, btn2, back)

            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="Вопрос 2:",
                reply_markup=markup,
            )
            bot.answer_callback_query(call.id)
        elif call.data == "question_3":
            markup = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton(
                "Вопрос 1 по теме", callback_data="option1"
            )
            btn2 = types.InlineKeyboardButton(
                "Вопрос 2 по теме", callback_data="option2"
            )
            back = types.InlineKeyboardButton("Назад", callback_data="option3")
            markup.add(btn1, btn2, back)

            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="Вопрос 3:",
                reply_markup=markup,
            )
            bot.answer_callback_query(call.id)
        elif call.data == "question_4":
            markup = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton(
                "Вопрос 1 по теме", callback_data="option1"
            )
            btn2 = types.InlineKeyboardButton(
                "Вопрос 2 по теме", callback_data="option2"
            )
            back = types.InlineKeyboardButton("Назад", callback_data="option3")
            markup.add(btn1, btn2, back)

            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="Вопрос 4:",
                reply_markup=markup,
            )
            bot.answer_callback_query(call.id)
        elif call.data == "question_5":
            markup = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton(
                "Вопрос 1 по теме", callback_data="option1"
            )
            btn2 = types.InlineKeyboardButton(
                "Вопрос 2 по теме", callback_data="option2"
            )
            back = types.InlineKeyboardButton("Назад", callback_data="option3")
            markup.add(btn1, btn2, back)

            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="Вопрос 5:",
                reply_markup=markup,
            )
            bot.answer_callback_query(call.id)
        elif call.data == "question_6":
            markup = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton(
                "Вопрос 1 по теме", callback_data="option1"
            )
            btn2 = types.InlineKeyboardButton(
                "Вопрос 2 по теме", callback_data="option2"
            )
            back = types.InlineKeyboardButton("Назад", callback_data="option3")
            markup.add(btn1, btn2, back)

            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="Вопрос 6:",
                reply_markup=markup,
            )
            bot.answer_callback_query(call.id)
        elif call.data == "option3":
            show_questions_menu(call.message)
            bot.answer_callback_query(call.id)
