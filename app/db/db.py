from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import DATABASE_URL ,DATABASE_URL_SYNC



engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
        connect_args={
        "statement_cache_size": 0  
    })


AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
    class_=AsyncSession
)


SYNC_DATABASE_URL = DATABASE_URL_SYNC.replace(
    "postgresql+asyncpg",
    "postgresql"
)

sync_engine = create_engine(
    DATABASE_URL_SYNC,
    pool_pre_ping=True,
)

Base = declarative_base()


async def create_tables():
    from app.db.models import file, job, user

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)



