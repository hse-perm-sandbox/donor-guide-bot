import logging

import telebot

from src.config import settings
from src.handlers.handlers import setup_handlers
from src.logging_config import setup_logging


def start():
    """Cоздание экземпляра бота, настройка обработчиков и запуск бота."""

    setup_logging()
    logger = logging.getLogger(__name__)

    bot = telebot.TeleBot(settings.TELEGRAM_TOKEN)
    setup_handlers(bot)
    logger.info(f"Бот запущен")

    bot.polling(none_stop=True, interval=0)


if __name__ == "__main__":
    start()
