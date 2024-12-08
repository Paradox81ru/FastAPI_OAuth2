import os

from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from pwdlib import PasswordHash
from pydantic import SecretStr
from pydantic_settings import BaseSettings

from Auth.base import AbstractPwdContext

oauth2_scheme = OAuth2PasswordBearer(
    auto_error=False,
    tokenUrl='/api/oauth/token',
    scopes={"me": "Read information about the current user.", "items": "Read items."}
)

class MyPwdContext(AbstractPwdContext):
    def __init__(self, pwd_context):
        self._pwd_context = pwd_context

    def hash(self, password) -> str:
        return self._pwd_context.hash(password)

    def verify(self, password, _hash) -> bool:
        return self._pwd_context.verify(password, _hash)


class Settings(BaseSettings):
    secret_key: SecretStr = "15d29aad37ecf71a6094bf2552232839a9df526f968d3c49e6885883892dca01"
    access_token_expire_minutes: int = 5
    refresh_token_expire_minutes: int = 30
    db_connect_str: str = 'sqlite:///db.sqlite3'

    init_admin_password: SecretStr = "Cucumber_123"
    init_system_password: SecretStr = "Cucumber_123"
    init_director_password: SecretStr = "Cucumber_123"
    init_user_password: SecretStr = "Cucumber_123"


def get_pwd_context():
    """ Возвращает класс работы с паролем """
    # pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
    # Почему то библиотека passlib не хочет работать, возможно проблема, давнее отсутствие поддержки данной библиотеки.
    pwd_context = PasswordHash.recommended()
    # По этой причине пока что используется более современная библиотека pwdlib.
    my_pwd_context = MyPwdContext(pwd_context)
    return my_pwd_context

# @lru_cache
def get_settings():
    """ Возвращает класс настроек """
    env_path = os.path.join(os.getcwd(), 'tests', '.env') if ('IS_TEST' in os.environ and os.environ['IS_TEST'] == 'True') \
                else os.path.join(os.getcwd(),'Auth', '.env')
    load_dotenv(env_path) 
    return Settings()