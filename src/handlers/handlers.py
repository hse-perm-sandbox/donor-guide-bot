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

        bot.send_message(message.chat.id, "Главное меню:", reply_markup=keyboard)

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

            markup.add(btn1)
            markup.add(btn2)
            markup.add(back)

            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="🧬 Донорство костного мозга:",
                reply_markup=markup,
            )
            bot.answer_callback_query(call.id)

        elif call.data == "option3":
            show_questions_menu(call.message)
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

            markup.add(btn1)
            markup.add(btn2)
            markup.add(back)

            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="🩸 Донорство крови:",
                reply_markup=markup,
            )
            bot.answer_callback_query(call.id)
        
        elif call.data == "option3":
            show_questions_menu(call.message)
            bot.answer_callback_query(call.id)





        elif call.data == "question_3":

            markup = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton(
                "Где сдавать кровь в Петербурге ", callback_data="option_1"
            )

            btn2 = types.InlineKeyboardButton(
                "Список отделений переливания крови", callback_data="option_2"
            )

            btn3 = types.InlineKeyboardButton(
                "Контакты и телефон фонда", callback_data="option_3"
            )

            back = types.InlineKeyboardButton("Назад", callback_data="option_4")

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




        elif call.data == "option_1":
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

        elif call.data == "option_2":
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

        elif call.data == "option_3":
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

        elif call.data == "option_4":
            show_questions_menu(call.message)
            bot.answer_callback_query(call.id)
