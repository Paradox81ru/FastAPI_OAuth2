from OAuth2.db.models.user import User, UserBuilder
from OAuth2.schemas import UserRoles
from OAuth2.db.crud import add_users
from sqlalchemy.orm import Session


def init_users(db: Session):
    """ Добавление пользователей при первой инициализации базы данных """
    user_admin = UserBuilder('Admin', 'paradox81ru@yandex.ru').role(UserRoles.admin).set_password('Cucmber_123').build()
    user_system = UserBuilder('System', 'paradox81ru@gmail.com').role(UserRoles.system).set_password('Cucmber_123').build()
    user_paradox = UserBuilder('Paradox', 'paradox81ru@mail.ru').name("Жорж", "Парадокс") \
                                .role(UserRoles.director).set_password('Cucmber_123').build()
    user_user = UserBuilder("User", 'paradox81ru@hotmail.com').name('Пользователь').set_password('Cucmber_123').build()
    users = (user_admin, user_system, user_paradox, user_user)
    add_users(db, users)