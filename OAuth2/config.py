from pydantic_settings import BaseSettings
from functools import lru_cache
from dotenv import load_dotenv
from pydantic import SecretStr

load_dotenv()

class Settings(BaseSettings):
    secret_key: SecretStr = "15d29aad37ecf71a6094bf2552232839a9df526f968d3c49e6885883892dca01"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    db_connect_str: str = 'sqlite:///db.sqlite3'


@lru_cache
def get_settings():
    return Settings()