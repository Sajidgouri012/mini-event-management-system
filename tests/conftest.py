"""
Pytest configuration and fixtures for the Event Management System tests.
"""

import pytest
import pytest_asyncio
import asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.main import app
from app.database.db_connection import get_session
from app.models import Base

# ✅ SQLite test DB URL (or switch to Postgres test DB here)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope="session")
async def test_engine():
    engine = create_async_engine(TEST_DATABASE_URL, echo=True, future=True)
    yield engine
    await engine.dispose()

@pytest_asyncio.fixture(scope="session")
async def async_session_maker_fixture(test_engine):
    async_session_maker = async_sessionmaker(
        test_engine, class_=AsyncSession, expire_on_commit=False
    )
    yield async_session_maker

@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_database(test_engine):
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

@pytest_asyncio.fixture
async def override_get_session(async_session_maker_fixture):
    async def _override():
        async with async_session_maker_fixture() as session:
            yield session
    return _override

@pytest_asyncio.fixture
async def client(override_get_session):
    app.dependency_overrides[get_session] = override_get_session
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver/api/v1") as ac:
        yield ac
    app.dependency_overrides.clear()
