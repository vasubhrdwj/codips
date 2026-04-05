import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.db.session import Base, engine


@pytest.fixture(autouse=True)
def reset_db():
    """Re-create tables before each test and drop them after."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c
