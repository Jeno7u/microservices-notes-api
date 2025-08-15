import os
import httpx
import asyncio
from pathlib import Path

import pytest
from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from auth.app.models.base import Base as auth_base
from auth.app.models import User
from notes.app.models.base import Base as notes_base


test_env = Path(__file__).parent.parent / ".env"
print(test_env)
load_dotenv(test_env)

TEST_DB_USER = os.getenv("TEST_DB_USER")
TEST_DB_PASSWORD = os.getenv("TEST_DB_PASSWORD")
TEST_DB_HOST = os.getenv("TEST_DB_HOST")
TEST_DB_PORT = os.getenv("TEST_DB_PORT")
TEST_DB_NAME = os.getenv("TEST_DB_NAME")

TEST_DB_URL = f"postgresql+asyncpg://{TEST_DB_USER}:{TEST_DB_PASSWORD}@{TEST_DB_HOST}:{TEST_DB_PORT}/{TEST_DB_NAME}"
print(TEST_DB_URL)
ECHO = bool(os.getenv("ECHO_TEST_DB"))


async def registrate_user(test_user_data, app):
    """Function for registrating user"""
    register_data = test_user_data.copy()
    register_data.pop("is_admin")

    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/auth/register/", json=register_data)
        
    return response


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
    

@pytest.fixture
async def auth_engine():
    engine = create_async_engine(TEST_DB_URL, echo=ECHO)

    async with engine.begin() as conn:
        await conn.execute(text("CREATE SCHEMA IF NOT EXISTS auth"))
        await conn.run_sync(auth_base.metadata.drop_all)
        await conn.run_sync(auth_base.metadata.create_all)

    yield engine
    await engine.dispose()


@pytest.fixture
async def notes_engine():
    engine = create_async_engine(TEST_DB_URL, echo=ECHO)

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
def create_notes_db(notes_session):
    async def override_get_db():
        yield notes_session
    
    from notes.app.main import app
    from notes.app.core.db import get_db

    app.dependency_overrides[get_db] = override_get_db

    yield

    app.dependency_overrides.clear()


@pytest.fixture
def test_user_data1():
    user_data =  {
        "login": "bormir123",
        "name": "Boris",
        "surname": "Mironov",
        "email": "test1@example.com",
        "password": "test1password123",
        "is_admin": False
    }
    return user_data


@pytest.fixture
def test_user_data2():
    user_data =  {
        "login": "almay123",
        "name": "Alfred",
        "surname": "Mayers",
        "email": "test2@example.com",
        "password": "test2password123",
        "is_admin": True
    }
    return user_data


@pytest.fixture
def test_note_data1():
    notes_data =  {
        "name": "TODO list",
        "text": "I should do my homework today and take out garbage"
    }
    return notes_data


@pytest.fixture
def test_note_data2():
    notes_data =  {
        "name": "Things that I like",
        "text": "I love playing minecraft and terraria. Also I'm in love with ice cream."
    }
    return notes_data


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