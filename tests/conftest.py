import pytest
from fastapi.testclient import TestClient
from app.main import create_app

@pytest.fixture(scope="session")
def client():
    app = create_app()
    return TestClient(app)
