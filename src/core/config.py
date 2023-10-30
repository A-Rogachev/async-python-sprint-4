import os

from dotenv import load_dotenv
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings

load_dotenv()

class AppSettings(BaseSettings):
    app_title: str = 'URL Shortener'
    database_dsn: PostgresDsn
    blacklist: list[str] = [
        '127.0.0.1',
    ]

    class Config:
        env_file = '.env'


app_settings = AppSettings()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
