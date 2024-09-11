from OAuth2.config import get_settings
from OAuth2.db import crud
import os

def test_settings():
    settings = get_settings()
    assert 'IS_TEST' in os.environ and os.environ['IS_TEST'] == 'True'
    assert settings.access_token_expire_minutes == 10
    assert settings.db_connect_str == 'sqlite:///db-test.sqlite3'
