from telebot import types

def get_main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    questions_button = types.KeyboardButton("Ответы на часто задаваемые вопросы")
    special_question_button = types.KeyboardButton("Написать свой вопрос")
    donate_button = types.KeyboardButton("Пожертвовать в фонд")
    markup.add(questions_button)
    markup.add(special_question_button)
    markup.add(donate_button)
    return markup
