from sqlalchemy import select, func
from sqlalchemy.orm import Session
from OAuth2.db.models import User
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