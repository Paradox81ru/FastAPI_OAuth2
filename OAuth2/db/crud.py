from sqlalchemy.orm import Session
from OAuth2.db.models import User as UserModel


def add_user(db: Session, user: UserModel):
    """ Добавляет пользователя """
    with db:
        db.add(user)
        db.commit()

def add_users(db: Session, users: list[UserModel]):
    """ Добавляет список пользователей """
    with db:
        db.add_all(users)
        db.commit()