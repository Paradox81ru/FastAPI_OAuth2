from sqlalchemy import select, func
from sqlalchemy.orm import Session
from OAuth2.db import models
from OAuth2.db.models.user import UserBuilder
from OAuth2.db import crud
from OAuth2 import schemas
from OAuth2.schemas import UserRoles, UerStatus

def test_existence_original_users(db_session: Session):
    """ Проверяет наличие первониачальных пользователей """
    stmt = select(func.count(models.User.id))
    with db_session:
        user_count = db_session.execute(stmt).scalar_one()
        assert user_count == 4
    admin_user = crud.get_user_by_username(db_session, 'Admin')
    assert admin_user.username == 'Admin'
    assert admin_user.role == UserRoles.admin
    assert admin_user.status == UerStatus.ACTIVE

    print(f"Admin user_model: {repr(admin_user)}")
    admin_user_schema = models.User(**admin_user.to_dict())
    print(f"Admin user_schema: {repr(admin_user_schema)}")


    system_user = crud.get_user_by_username(db_session, 'System')
    assert system_user.username == "System"
    assert system_user.role == UserRoles.system
    assert system_user.status == UerStatus.ACTIVE

    paradox_user = crud.get_user_by_username(db_session, 'Paradox')
    assert paradox_user.username == 'Paradox'
    assert paradox_user.role == UserRoles.director
    assert paradox_user.status == UerStatus.ACTIVE

    user = crud.get_user_by_username(db_session, 'User')
    assert user.username == 'User'
    assert user.role == UserRoles.visitor
    assert user.status == UerStatus.ACTIVE

    unknow_user = crud.get_user_by_username(db_session, 'Unknow')
    print(f"unckno user: {unknow_user}")


# def test_check_password(db_session: Session):
#     user = crud.get_user_schema_by_username(db_session, 'Paradox')
#     assert user.check_password('Cucumber_123')


def test_add_user(db_session: Session):
    new_user = UserBuilder('NewUser', 'new_user@mail.ru').set_password("qwerty").build()
    assert new_user.username == 'NewUser'
    assert new_user.email == 'new_user@mail.ru'
    assert new_user.role == UserRoles.visitor
    assert new_user.status == UerStatus.ACTIVE
    crud.add_user(db_session, new_user)

    find_new_user = crud.get_user_by_username(db_session, 'NewUser')
    assert find_new_user.username == 'NewUser'
    assert find_new_user.email == 'new_user@mail.ru'
    assert find_new_user.role == UserRoles.visitor
    assert find_new_user.status == UerStatus.ACTIVE


def test_set_password(db_session: Session):
    password = 'qwerty'
    user_model = UserBuilder("NewUser", "new_user@mail.ru").set_password(password).build()
    user_schema = schemas.UserInDB(**user_model.to_dict())
    assert user_schema.check_password(password)

    password = 'Cucumber_123'
    paradox = crud.get_user_schema_by_username(db_session, 'Paradox')
    assert paradox.check_password(password)
    password = 'cucumber_123'
    assert not paradox.check_password(password)


def test_convert_userdb_to_user(db_session: Session):
    paradox_in_db = crud.get_user_schema_by_username(db_session, 'Paradox')
    paradox = paradox_in_db.to_user()
    assert isinstance(paradox, schemas.User)