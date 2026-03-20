import os

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class ConfigBase(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


class BotConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="BOT_")
    TOKEN: SecretStr = SecretStr("")


class DatabaseConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="POSTGRES_")
    host = "db" if os.getenv("APP_ENV", "dev") == "prod" else "localhost"
    DB: str = ""
    USER: str = ""
    PASSWORD: SecretStr = SecretStr("")
    DB_URL: str = ""

    def __init__(self, **data):
        super().__init__(**data)
        self.DB_URL = f"postgresql+asyncpg://{self.USER}:{self.PASSWORD.get_secret_value()}@{self.host}:5432/{self.DB}"


class Settings(BaseSettings):
    bot: BotConfig = BotConfig()
    db: DatabaseConfig = DatabaseConfig()


settings = Settings()
