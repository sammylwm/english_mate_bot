import os
from pathlib import Path
from typing import ClassVar

from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL

env_path = Path(__file__).parent / ".env"


class ConfigBase(BaseSettings):
    model_config = SettingsConfigDict(env_file=str(env_path), env_file_encoding="utf-8", extra="ignore")


class AppConfig(BaseModel):
    root_path: str = "/english_mate"
    title: str = "App"
    host: str = "0.0.0.0"  # noqa: S104
    port: int = 8000
    reload: bool = True


class ApiV1Prefix(BaseModel):
    prefix: str = "/v2"
    auth: str = "/auth"


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()

    @property
    def token_url(self) -> str:
        parts = (self.prefix, self.v1.prefix, self.v1.auth, "/login")
        path = "".join(parts)
        return path.removeprefix("/")


class DatabaseConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="POSTGRES_")
    host: ClassVar[str] = "db" if os.getenv("APP_ENV", "dev") == "prod" else "localhost"
    db: str = ""
    user: str = ""
    password: SecretStr = SecretStr("")

    @property
    def async_url(self) -> str:
        return URL.create(
            drivername="postgresql+asyncpg",
            database=self.db,
            host=self.host,
            username=self.user,
            password=self.password.get_secret_value(),
        ).render_as_string(hide_password=False)


class Settings(BaseSettings):
    app: AppConfig = AppConfig()
    api: ApiPrefix = ApiPrefix()
    db: DatabaseConfig = DatabaseConfig()


settings = Settings()
