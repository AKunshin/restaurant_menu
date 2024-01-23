from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Режим работы приложения
    MODE: Literal["DEV", "TEST", "PROD"]

    # Данные для подключения к рабочей БД
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_NAME: str
    DB_PASS: str

    @property
    def database_url(self):
        """Получение DSN рабочей БД"""
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # Данные для подключения к тестовой БД
    TEST_DB_HOST: str = "localhost"
    TEST_DB_PORT: int = 5432
    TEST_DB_USER: str = "rest_user"
    TEST_DB_NAME: str = "test_restaurant_db"
    TEST_DB_PASS: str = "pass"

    @property
    def test_database_url(self):
        """Получение DSN тестовой БД"""
        return f"postgresql+asyncpg://{self.TEST_DB_USER}:{self.TEST_DB_PASS}@{self.TEST_DB_HOST}:{self.TEST_DB_PORT}/{self.TEST_DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
