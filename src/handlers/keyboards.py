from telebot import types
from src.schemas.folder import FolderWithContentDto


def get_main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    questions_button = types.KeyboardButton("Ответы на часто задаваемые вопросы")
    special_question_button = types.KeyboardButton("Написать свой вопрос")
    donate_button = types.KeyboardButton("Пожертвовать в фонд")
    markup.add(questions_button)
    markup.add(special_question_button)
    markup.add(donate_button)
    return markup


def get_inline_keyboard_for_folder(folder: FolderWithContentDto) -> types.InlineKeyboardMarkup:
    """Создает inline-клавиатуру для содержимого каталога"""
    markup = types.InlineKeyboardMarkup()
    for subfolder in folder.subfolders:
        markup.add(
            types.InlineKeyboardButton(
                text=f"📁 {subfolder.folder_name}", callback_data=f"folder_{subfolder.id}"
            )
        )

    for question in folder.questions:
        markup.add(
            types.InlineKeyboardButton(
                text=f"❓ {question.question[:20]}...", callback_data=f"question_{question.id}"
            )
        )

    markup.add(
        types.InlineKeyboardButton(
            text="⬅️ Назад",
            callback_data=(
                f"folder_{folder.id}" if folder.id else "Ответы на часто задаваемые вопросы"
            ),
        )
    )

    return markup
