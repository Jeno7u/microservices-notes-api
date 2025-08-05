import asyncio

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from .config import TEST_DB_URL
from auth.app.models.base import Base as auth_base
from notes.app.models.base import Base as notes_base


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
    

@pytest.fixture
async def auth_engine():
    engine = create_async_engine(TEST_DB_URL, echo=True)

    async with engine.begin() as conn:
        await conn.execute(text("CREATE SCHEMA IF NOT EXISTS auth"))
        await conn.run_sync(auth_base.metadata.drop_all)
        await conn.run_sync(auth_base.metadata.create_all)

    yield engine
    await engine.dispose()


@pytest.fixture
async def notes_engine():
    engine = create_async_engine(TEST_DB_URL, echo=True)

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
def test_user_data():
    return {
        "login": "testuser",
        "name": "Test",
        "surname": "User",
        "email": "test@example.com",
        "password": "testpassword123"
    }