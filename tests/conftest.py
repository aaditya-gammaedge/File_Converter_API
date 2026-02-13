
import asyncio
import pytest

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
)
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.db import Base
from app.api.routes.auth import get_db 



DATABASE_URL = "sqlite+aiosqlite:///./test.db"


engine = create_async_engine(
    DATABASE_URL,
    future=True,
    echo=False,
)

TestingSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)



@pytest.fixture(scope="session")
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)




@pytest.fixture
async def db_session(setup_database):
    async with TestingSessionLocal() as session:
        yield session

from httpx import AsyncClient
from httpx import ASGITransport


@pytest.fixture
async def client(db_session):

    async def override_get_db():
        yield db_session

    from app.main import app
    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as ac:
        yield ac

    app.dependency_overrides.clear()
