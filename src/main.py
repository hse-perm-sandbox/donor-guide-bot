import telebot

from src.config import Settings
from src.handlers.handlers import setup_handlers


def start():
    """Cоздание экземпляра бота, настройка обработчиков и запуск бота."""

    settings = Settings()
    bot = telebot.TeleBot(settings.TELEGRAM_TOKEN)
    setup_handlers(bot)
    bot.polling(none_stop=True, interval=0)


if __name__ == "__main__":
    start()
