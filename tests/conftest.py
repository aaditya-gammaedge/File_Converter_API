
# import asyncio
# import pytest_asyncio

# from httpx import AsyncClient
# from sqlalchemy.ext.asyncio import (
#     create_async_engine,
#     AsyncSession,
# )
# from sqlalchemy.orm import sessionmaker
# from httpx import AsyncClient
# from httpx import ASGITransport


# from app.main import app
# from app.db.db import Base
# from app.api.routes.auth import get_db 



# DATABASE_URL1 = "sqlite+aiosqlite:///./test.db"


# engine = create_async_engine(
#     DATABASE_URL1,
#     future=True,
#     echo=False,
# )

# TestingSessionLocal = sessionmaker(
#     bind=engine,
#     class_=AsyncSession,
#     expire_on_commit=False,
# )



# @pytest_asyncio.fixture(scope="session",autouse=True)
# async def setup_database():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#     yield
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)




# @pytest_asyncio.fixture   
# async def db_session(setup_database):
#     async with TestingSessionLocal() as session:
#         yield session


# @pytest_asyncio.fixture(autouse=True)
# async def client(db_session):

#     async def override_get_db():
#         yield db_session

    
#     app.dependency_overrides[get_db] = override_get_db

#     transport = ASGITransport(app=app)

#     async with AsyncClient(
#         transport=transport,
#         base_url="http://test",
#     ) as ac:
#         yield ac

#     app.dependency_overrides.clear()


import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.main import app
from app.db.db import Base
from app.api.auth.dependencies import get_db  


DATABASE_URL1 = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(
    DATABASE_URL1,
    future=True,
    echo=False,
)

TestingSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def db_session(setup_database):
    async with TestingSessionLocal() as session:
        yield session


@pytest_asyncio.fixture
async def client(db_session):

    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as ac:
        yield ac

    app.dependency_overrides.clear()
