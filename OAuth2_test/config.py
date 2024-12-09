import os

from dotenv import load_dotenv
from fastapi.templating import Jinja2Templates
from pydantic import SecretStr
from pydantic_settings import BaseSettings


templates = Jinja2Templates(directory="ui/jinja2")


class Settings(BaseSettings):
    auth_server: str = 'http://127.0.0.1:8001'


# @lru_cache
def get_settings():
    """ Возвращает класс настроек """
    env_path = os.path.join(os.getcwd(), 'tests', '.env') if ('IS_TEST' in os.environ and os.environ['IS_TEST'] == 'True') \
                else os.path.join(os.getcwd(),'fastapi_site', '.env')
    load_dotenv(env_path) 
    return Settings()