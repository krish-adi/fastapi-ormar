import asyncio
from typing import Generator

from fastapi.testclient import TestClient
import pytest
import sqlalchemy

from .main import app
from .database import database, metadata, TEST_DB_URL


@pytest.fixture(autouse=True, scope="session")
def create_test_database():
    engine = sqlalchemy.create_engine(TEST_DB_URL)
    metadata.drop_all(engine)
    metadata.create_all(engine)
    yield
    # metadata.drop_all(engine)


# Force the pytest-asyncio loop to be the main one
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop


# method to run ormar model operations
@pytest.fixture(scope="session")
@pytest.mark.asyncio
async def db():
    async def wrapper(func):
        async with database:
            async with database.transaction(force_rollback=False):
                return await func
    return wrapper


@pytest.fixture(scope="session")
def client() -> Generator:
    yield TestClient(app)
