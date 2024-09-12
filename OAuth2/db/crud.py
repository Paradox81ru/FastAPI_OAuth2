from sqlalchemy.orm import Session
from OAuth2.db import models
from OAuth2 import schemas


def add_user(db: Session, user: models.User):
    """ Добавляет пользователя """
    db.add(user)
    db.commit()


def add_users(db: Session, users: list[models.User]):
    """ Добавляет список пользователей """
    db.add_all(users)
    db.commit()


def get_user_by_username(db: Session,  username) -> models.User:
    """ Возвраащет пользовтеля по логину """
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_schema_by_username(db: Session,  username) -> schemas.UserInDB | None:
    """ Возвращает найденного по логину пользователя"""
    # user = get_user_by_username(db, username)
    # return schemas.UserInDB(**user.to_dict()) if user is not None else schemas.AnonymUser()
    user = get_user_by_username(db, username)
    return schemas.UserInDB(**user.to_dict()) if user is not None else None