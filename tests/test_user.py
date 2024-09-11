from sqlalchemy import select, func
from sqlalchemy.orm import Session
from OAuth2.db.models import User
from OAuth2.db.models.user import UserBuilder
from OAuth2.db import crud
from OAuth2.schemas import UserRoles, UerStatus

def test_existence_original_users(session: Session):
    """ Проверяет наличие первониачальных пользователей """
    stmt = select(func.count(User.id))
    with session:
        user_count = session.execute(stmt).scalar_one()
        assert user_count == 4
    admin_user = crud.get_user_by_username(session, 'Admin')
    assert admin_user.username == 'Admin'
    assert admin_user.role == UserRoles.admin
    assert admin_user.status == UerStatus.ACTIVE

    system_user = crud.get_user_by_username(session, 'System')
    assert system_user.username == "System"
    assert system_user.role == UserRoles.system
    assert system_user.status == UerStatus.ACTIVE

    paradox_user = crud.get_user_by_username(session, 'Paradox')
    assert paradox_user.username == 'Paradox'
    assert paradox_user.role == UserRoles.director
    assert paradox_user.status == UerStatus.ACTIVE

    user = crud.get_user_by_username(session, 'User')
    assert user.username == 'User'
    assert user.role == UserRoles.visitor
    assert user.status == UerStatus.ACTIVE


def test_add_user(session: Session):
    new_user = UserBuilder('NewUser', 'new_user@mail.ru').set_password("qwerty").build()
    assert new_user.username == 'NewUser'
    assert new_user.email == 'new_user@mail.ru'
    assert new_user.role == UserRoles.visitor
    assert new_user.status == UerStatus.ACTIVE
    crud.add_user(session, new_user)

    find_new_user = crud.get_user_by_username(session, 'NewUser')
    assert find_new_user.username == 'NewUser'
    assert find_new_user.email == 'new_user@mail.ru'
    assert find_new_user.role == UserRoles.visitor
    assert find_new_user.status == UerStatus.ACTIVE