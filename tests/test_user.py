from sqlalchemy import select, func
from sqlalchemy.orm import Session
from OAuth2.db import models
from OAuth2.db.models.user import UserBuilder
from OAuth2.db import crud
from OAuth2 import schemas
from OAuth2.schemas import UserRoles, UerStatus
from OAuth2.config import get_settings

settings = get_settings()

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
    admin_user_schema = schemas.UserInDB(**admin_user.to_dict())
    print(f"Admin user_schema: {repr(admin_user_schema)}")
    assert not admin_user_schema.check_password("qwerty")
    assert admin_user_schema.check_password(settings.init_admin_password.get_secret_value())

    system_user = crud.get_user_by_username(db_session, 'System')
    assert system_user.username == "System"
    assert system_user.role == UserRoles.system
    assert system_user.status == UerStatus.ACTIVE
    system_user_schema = schemas.UserInDB(**system_user.to_dict())
    assert not system_user_schema.check_password("qwerty")
    assert system_user_schema.check_password(settings.init_system_password.get_secret_value())

    director_user = crud.get_user_by_username(db_session, 'Paradox')
    assert director_user.username == 'Paradox'
    assert director_user.role == UserRoles.director
    assert director_user.status == UerStatus.ACTIVE
    director_user_schema = schemas.UserInDB(**director_user.to_dict())
    assert not director_user_schema.check_password("qwerty")
    assert director_user_schema.check_password(settings.init_director_password.get_secret_value())

    user = crud.get_user_by_username(db_session, 'User')
    assert user.username == 'User'
    assert user.role == UserRoles.visitor
    assert user.status == UerStatus.ACTIVE
    user_schema = schemas.UserInDB(**user.to_dict())
    assert not user_schema.check_password("qwerty")
    assert user_schema.check_password(settings.init_user_password.get_secret_value())

    unknow_user = crud.get_user_by_username(db_session, 'Unknow')
    print(f"Uncknow user: {unknow_user}")


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