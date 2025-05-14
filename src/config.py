from pydantic_settings import BaseSettings, SettingsConfigDict

CONN_STR_TEMPLATE = "postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"


class Settings(BaseSettings):
    """Класс конфигурируемые параметры приложения. Параметры могут быть переопределены
    в файле .env в корне проекта или через переменные окружения."""

    LOG_LEVEL: str = "WARNING"
    TELEGRAM_TOKEN: str = "default_token"
    RESEND_CHAT_ID: int = 0
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5433
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "postgres"

    @property
    def DATABASE_URL(self) -> str:
        return CONN_STR_TEMPLATE.format(
            user=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            dbname=self.POSTGRES_DB,
        )

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=True
    )


settings = Settings()
