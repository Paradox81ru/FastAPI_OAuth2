from datetime import datetime
from OAuth2.db.models import Base
from sqlalchemy import String, SMALLINT
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm import selectinload, joinedload, contains_eager
from OAuth2.config import pwd_context
from OAuth2.schemas import UserRoles, UerStatus
from OAuth2.db.db_types import MyDateTime
# from OAuth2.db.models import JWTToken


class User(Base):
    """ Пользователь """
    __tablename__ = 'accounts_user'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(60), nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    first_name: Mapped[str | None] = mapped_column(String(60), default="")
    last_name: Mapped[str | None] = mapped_column(String(60), default="")
    email: Mapped[str] = mapped_column(String(254))
    status: Mapped[UerStatus] = mapped_column(SMALLINT)
    role: Mapped[UserRoles] = mapped_column(SMALLINT)
    date_joined: Mapped[datetime] = mapped_column(MyDateTime, default=datetime.now)
    last_login: Mapped[datetime | None] = mapped_column(MyDateTime)
    jwt_tokens: Mapped[list['JWTToken']] = relationship(back_populates='subject')


    def set_password(self, password: str):
        self.password_hash = pwd_context.hash(password)

    def check_password(self, password: str):
        return pwd_context.verify(self.password_hash, password)
    
    def __repr__(self):
        return f"User(id={self.id}, username={self.username}, first_name={self.first_name}, last_name={self.last_name}," \
               f"email={self.email}, status={self.status}, role={self.role}, date_joined={self.date_joined}," \
               f"last_logind={self.last_login})"


class UserBuilder:
    """ Класс создатель пользователя """
    def __init__(self, username: str, email: str) -> None:
        self._user = User(username=username, email=email)
    
    def name(self, first_name='', last_name=''):
        self._user.first_name = first_name
        self._user.last_name = last_name
        return self
    
    def role(self, role: UserRoles):
        self._user.role = role
        return self
    
    def set_password(self, password):
        self._user.set_password(password)
        return self
    
    def build(self):
        if self._user.password_hash is None:
            raise AttributeError("The password field is not set")
        if self._user.role is None:
            self.role(UserRoles.visitor)
        self._user.status = UerStatus.ACTIVE
        return self._user