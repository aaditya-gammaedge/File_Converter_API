
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

# import os
# os.environ["ENV"] = "test"
# import pytest_asyncio
# from httpx import AsyncClient, ASGITransport
# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
# from app.main import app
# from app.db.db import Base
# from app.api.auth.dependencies import get_db  
# # from app.api.auth.dependencies import get_db


# DATABASE_URL1 = "sqlite+aiosqlite:///./test.db"

# engine = create_async_engine(
#     DATABASE_URL1,
#     future=True,
#     echo=False,
# )

# TestingSessionLocal = async_sessionmaker(
#     bind=engine,
#     expire_on_commit=False,
# )


# @pytest_asyncio.fixture(scope="session", autouse=True)
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


# @pytest_asyncio.fixture
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



import os
os.environ["ENV"] = "test"

import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.main import app
from app.db.db import Base
from app.api.auth.dependencies import get_db
import app.db.db as db_module


# DATABASE_URL1 = "sqlite+aiosqlite:///:memory:"
# DATABASE_URL1 = "sqlite+aiosqlite:///./test.db"
DATABASE_URL1 = "sqlite+aiosqlite://"



engine = create_async_engine(
    DATABASE_URL1,
    future=True,
    echo=False,
)

# engine = create_async_engine(
#     DATABASE_URL1,
#     connect_args={"check_same_thread": False},
# )

TestingSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)



# @pytest_asyncio.fixture(scope="session")
# def event_loop():
#     import asyncio
#     loop = asyncio.new_event_loop()
#     yield loop
#     loop.close()

@pytest_asyncio.fixture(autouse=True)
async def override_database():

    #  Replace production sessionmaker with test one
    db_module.AsyncSessionLocal = TestingSessionLocal

    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    # Drop tables after test
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture(scope="function", autouse=True)
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


