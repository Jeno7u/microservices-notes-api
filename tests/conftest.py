import os
import asyncio
from pathlib import Path

import pytest
from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from auth.app.models.base import Base as auth_base
from auth.app.models import User
from notes.app.models.base import Base as notes_base


test_env = Path(__file__).parent / ".env"
load_dotenv(test_env)

TEST_DB_URL = os.getenv("ASYNC_DATABASE_URL")


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
    

@pytest.fixture
async def auth_engine():
    engine = create_async_engine(TEST_DB_URL, echo=False)

    async with engine.begin() as conn:
        await conn.execute(text("CREATE SCHEMA IF NOT EXISTS auth"))
        await conn.run_sync(auth_base.metadata.drop_all)
        await conn.run_sync(auth_base.metadata.create_all)

    yield engine
    await engine.dispose()


@pytest.fixture
async def notes_engine():
    engine = create_async_engine(TEST_DB_URL, echo=False)

    async with engine.begin() as conn:
        await conn.execute(text("CREATE SCHEMA IF NOT EXISTS notes"))
        await conn.run_sync(notes_base.metadata.drop_all)
        await conn.run_sync(notes_base.metadata.create_all)

    yield engine
    await engine.dispose()


@pytest.fixture
async def auth_session(auth_engine):
    async with AsyncSession(auth_engine) as session:
        yield session
        await session.rollback()

    await auth_engine.dispose()


@pytest.fixture
async def notes_session(notes_engine):
    async with AsyncSession(notes_engine) as session:
        yield session
        await session.rollback()

    await notes_engine.dispose()

@pytest.fixture
def create_auth_db(auth_session):
    async def override_get_db():
        yield auth_session
    
    from auth.app.main import app
    from auth.app.core.db import get_db

    app.dependency_overrides[get_db] = override_get_db

    yield

    app.dependency_overrides.clear()


@pytest.fixture
def test_user_data1():
    user_data =  {
        "login": "testuser1",
        "name": "Test1",
        "surname": "User1",
        "email": "test1@example.com",
        "password": "test1password123",
        "is_admin": False
    }
    return user_data


@pytest.fixture
def test_user_data2():
    user_data =  {
        "login": "testuser2",
        "name": "Test2",
        "surname": "User2",
        "email": "test2@example.com",
        "password": "test2password123",
        "is_admin": True
    }
    return user_data


@pytest.fixture
def test_user1(test_user_data1):
    user = User(
        login=test_user_data1["login"],
        name=test_user_data1["name"],
        surname=test_user_data1["surname"],
        email=test_user_data1["email"],
        password=test_user_data1["password"],
        is_admin=test_user_data1["is_admin"]
    )
    return user


@pytest.fixture
def test_user2(test_user_data2):
    user = User(
        login=test_user_data2["login"],
        name=test_user_data2["name"],
        surname=test_user_data2["surname"],
        email=test_user_data2["email"],
        password=test_user_data2["password"],
        is_admin=test_user_data2["is_admin"]
    )
    return user