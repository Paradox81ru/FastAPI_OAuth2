import os
os.environ['IS_TEST'] = 'True'

from main import app
from fastapi.testclient import TestClient

import pytest


@pytest.fixture()
def client():
    return TestClient(app)