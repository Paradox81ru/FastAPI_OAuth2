import os
os.environ['IS_TEST'] = 'True'

from OAuth2.db.db_connection import session as db_session
import alembic.config
import alembic.environment

import alembic
import pytest


@pytest.fixture(autouse=True, scope='session')
def setup():
    # Перед началом теста тестовая база удаляется,
    if os.path.exists('db-test.sqlite3'):
        os.remove('db-test.sqlite3')

    alembic_cfg = alembic.config.Config('alembic.ini')
    # и с помощью alembic инициируется новая тестовая база.
    alembic.command.upgrade(alembic_cfg, 'head')
    yield
   
@pytest.fixture()
def session():
    yield db_session
    db_session.close()