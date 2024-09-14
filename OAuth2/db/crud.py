from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import delete, select, func
from OAuth2.db import models
from OAuth2 import schemas
from uuid import UUID
import sqlalchemy.dialects.sqlite as dialects_sqlite


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


def add_jwt_token(db: Session, jti: UUID, data_expire: datetime, username: str):
    """ Добавляет JWT токен для пользователя """
    user = db.query(models.User).filter(models.User.username == username).one()
    token = models.JWTToken(jti=jti, subject=user, expire=data_expire)
    db.add(token)
    db.commit()


def get_user_jwt_token_count(db_session: Session, username: str):
    """ Возвращает количество токенов у указанного пользователя """
    return db_session.execute(select(func.count(models.JWTToken.jti)).join(models.User).where(models.User.username == username) ).scalar_one()


def get_jwt_token(db: Session, jti: UUID | str):
    """ Возвращает JWT токен по его jti """
    jti = UUID(jti) if isinstance(jti, str) else jti
    return db.query(models.JWTToken).filter(models.JWTToken.jti == jti).one_or_none()


def has_jwt_token(db: Session, jti: UUID | str) -> bool:
    """ Проверяет, существует ли указанный JWT токен """
    jti = UUID(jti) if isinstance(jti, str) else jti
    result = db.query(models.JWTToken).filter(models.JWTToken.jti == jti).one_or_none()
    return result is not None

def remove_jwt_token(db: Session, jti: UUID | str):
    """ Удалеят JWT токен по его UUID """
    jti = UUID(jti) if isinstance(jti, str) else jti
    # db.execute(delete(models.JWTToken).where(models.JWTToken.jti == jti))
    db.query(models.JWTToken).where(models.JWTToken.jti == jti).delete(synchronize_session='fetch')
    db.commit()


def remove_user_jwt_tokens(db: Session, username: str):
    """ Удаляет все токены для указанного пользователя """
    user: models.User = db.query(models.User).filter(models.User.username == username).one()
    user.jwt_tokens.clear()
    db.commit()


def remove_expire_token(db: Session):
    """ Удаляет все истёкшие токены """
    # db.execute(delete(models.JWTToken).where(models.JWTToken.expire < datetime.now()))
    # db.query(models.JWTToken).where(models.JWTToken.expire < datetime.now()).delete(synchronize_session='fetch')

    expire_tokens = db.query(models.JWTToken).filter(models.JWTToken.expire < datetime.now())
    for token in expire_tokens:
        db.delete(token)
    db.commit()
