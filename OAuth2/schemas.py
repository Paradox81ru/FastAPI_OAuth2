from pydantic import BaseModel, ConfigDict, SecretStr
from enum import IntEnum
from datetime import datetime
from OAuth2.config import pwd_context

class MyEnum(IntEnum):
    @classmethod
    def get_names(cls):
        return tuple(val.name for val in cls)

    @classmethod
    def get_values(cls):
        return tuple(val.value for val in cls)
    
    @classmethod
    def get_items(cls):
        return {item.name: item.value for item in cls}

class UerStatus(MyEnum):
    """ Перечисление статусов пользователей """
    DELETED = 1
    BLOCKED = 2
    ACTIVE = 3
    

class UserRoles(MyEnum):
    """ Перечисление ролей пользователей """
    system = 1
    super_admin = 2
    admin = 3
    admin_assistant = 4
    director = 5
    director_assistant = 6
    employee = 7
    visitor_vip = 8
    visitor = 9


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
    scopes: list[str] = []


class BaseUser(BaseModel):
    username: str
    role: UserRoles
    status: UerStatus

    model_config = ConfigDict(from_attributes=True)

    def __repr__(self) -> str:
        attrs = tuple(f"{field}={f'\'{value}\'' if isinstance(value, str) else value}" for field, value in self.model_dump().items())
        return f"{self.__class__.__name__}({', '.join(attrs)})"

class AnonymUser(BaseUser):
    username: str = 'Anonym'
    role: UserRoles = UserRoles.visitor
    status: UerStatus = UerStatus.ACTIVE

class User(BaseUser):
    email: str | None
    first_name: str | None = None
    last_name: str | None = None
    date_joined: datetime
    last_login: datetime | None = None


class UserInDB(User):
    password_hash: SecretStr

    def check_password(self, password: str):
        _check =  pwd_context.verify(password, self.password_hash.get_secret_value())
        return pwd_context.verify(password, self.password_hash.get_secret_value())