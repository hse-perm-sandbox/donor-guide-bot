from src.handlers.keyboards import get_main_menu
from src.services.metric_service import MetricService
from src.config import settings

from .folder_navigation import register_folder_navigation_handlers
from .user_questions import register_user_question_handlers


def setup_handlers(bot):
    markup = get_main_menu()
    register_folder_navigation_handlers(bot)
    register_user_question_handlers(bot)

    @bot.message_handler(commands=["start"])
    def start_message(message):
        bot.send_message(
            message.chat.id,
            text="Привет, {0.first_name} 👋\nВоспользуйся кнопками".format(message.from_user),
            reply_markup=markup,
        )
        MetricService.send_event(str(message.chat.id), "start")

    @bot.message_handler(content_types=["text"])
    def text_messages(message):
        if message.text == "Пожертвовать в фонд":
            bot.send_message(
                message.chat.id,
                f"Спасибо за ваше желание помочь! Пожалуйста, перейдите по следующей ссылке для пожертвования: {settings.DONATION_URL}",
            )
            MetricService.send_event(str(message.chat.id), "пожертвовать-в-фонд")

        else:
            bot.send_message(
                message.chat.id,
                "ℹ️ Пожалуйста, воспользуйтесь кнопками меню.",
                reply_markup=markup,
            )
