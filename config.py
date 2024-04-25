from pydantic_settings import BaseSettings
from typing import ClassVar

DATABASE_URL = "sqlite:///database.db?check_same_thread=False"
TITLE_PROJECT = "Teamder"
API_PREFIX = "/api"


class Settings(BaseSettings):
    title: ClassVar[str] = TITLE_PROJECT
    db_url: ClassVar[str] = DATABASE_URL
    api_pref: ClassVar[str] = API_PREFIX


settings = Settings()
