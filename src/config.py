from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Класс конфигурируемые параметры приложения. Параметры могут быть переопределены
    в файле .env в корне проекта или через переменные окружения."""

    LOG_LEVEL: str = "WARNING"
    TELEGRAM_TOKEN: str = "7761012427:AAG2LJi0yNKxj3AEs0WLmwpQRU0SzVsxcM0"
    RESEND_CHAT_ID: int = "1259813535"

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=True
    )
