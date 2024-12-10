import os

from dotenv import load_dotenv
from fastapi.templating import Jinja2Templates
from pydantic import SecretStr
from pydantic_settings import BaseSettings


templates = Jinja2Templates(directory="ui/jinja2")


class Settings(BaseSettings):
    auth_test_host: str = "localhost"
    auth_test_port: int = 8000

    auth_server_host: str = "localhost"
    auth_server_port: int = 8001


# @lru_cache
def get_settings():
    """ Возвращает класс настроек """
    env_path = os.path.join(os.getcwd(), 'tests', '.env') if ('IS_TEST' in os.environ and os.environ['IS_TEST'] == 'True') \
                else os.path.join(os.getcwd(),'fastapi_site', '.env')
    load_dotenv(env_path) 
    return Settings()