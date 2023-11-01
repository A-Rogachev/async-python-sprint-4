import os

from dotenv import load_dotenv
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings

load_dotenv()


class AppSettings(BaseSettings):
    app_title: str
    postgres_db: str
    postgres_user: str
    postgres_password: str
    database_dsn: PostgresDsn
    blacklist: list[str] = [
        '172.0.0.1',
    ]

    class Config:
        env_file = '.env'


app_settings = AppSettings()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
