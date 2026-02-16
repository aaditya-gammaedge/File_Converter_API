import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.orm import declarative_base

# from app.config import DATABASE_URL, DATABASE_URL_SYNC


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_URL_SYNC = os.getenv("DATABASE_URL_SYNC")


Base = declarative_base()


if DATABASE_URL.startswith("sqlite"):
    engine = create_async_engine(
        DATABASE_URL,
        echo=False,
        pool_pre_ping=True,
    )
else:
    engine = create_async_engine(
        DATABASE_URL,
        echo=False,
        pool_pre_ping=True,
        connect_args={"statement_cache_size": 0},
    )


AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
    class_=AsyncSession,
)

sync_engine = create_engine(
    DATABASE_URL_SYNC,
    pool_pre_ping=True,
)


async def create_tables():
    from app.db.models import file, job, user

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
