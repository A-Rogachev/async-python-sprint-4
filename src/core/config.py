import os

from dotenv import load_dotenv
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings

load_dotenv()


class AppSettings(BaseSettings):
    """
    Настройки приложения.
    """
    is_debug: bool
    app_title: str
    logging_echo: bool
    DATABASE_DSN: PostgresDsn
    blacklist: list[str] = [
        '172.0.0.1',
    ]

    class Config:
        env_file = '.env'


app_settings = AppSettings()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
