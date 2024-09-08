from pydantic import BaseModel
from enum import IntEnum

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


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disable: bool | None = None


class UserInDB(User):
    hashed_password : str