# Test fixture for our tests
import os

import pytest


@pytest.fixture(scope="module")
def test_app():
    os.environ["ENV"] = "test"
    from starlette.testclient import TestClient
    from app import main

    with TestClient(main.APP) as test_client:
        yield test_client
