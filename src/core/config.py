from pydantic import PostgresDsn
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class AppSettings(BaseSettings):
    app_title: str = "NameByDefault"
    # database_dsn: PostgresDsn

    class Config:
        env_file = '.env'


app_settings = AppSettings()
