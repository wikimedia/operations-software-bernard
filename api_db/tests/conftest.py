# Test fixture for our tests
import pytest
from fastapi.testclient import TestClient

from app.main import app

#TODO add fixture for DB connection mock

@pytest.fixture(scope="module")
def test_app():
    client = TestClient(app)
    yield client
