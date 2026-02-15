
# import os
# from sqlalchemy import create_engine
# from sqlalchemy.ext.asyncio import (
#     create_async_engine,
#     async_sessionmaker,
#     AsyncSession,
# )
# from sqlalchemy.orm import declarative_base
# from app.config import DATABASE_URL, DATABASE_URL_SYNC


# Base = declarative_base()

# engine = None
# sync_engine = None
# AsyncSessionLocal = None



# if os.getenv("ENV") != "test":

#     engine = create_async_engine(
#         DATABASE_URL,
#         echo=False,
#         pool_pre_ping=True,
#         connect_args={"statement_cache_size": 0},
#     )

#     AsyncSessionLocal = async_sessionmaker(
#         bind=engine,
#         expire_on_commit=False,
#         autoflush=False,
#         autocommit=False,
#         class_=AsyncSession,
#     )

#     sync_engine = create_engine(
#         DATABASE_URL_SYNC,
#         pool_pre_ping=True,
#     )


# async def create_tables():
#     from app.db.models import file, job, user

#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)





import os
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)
from sqlalchemy.orm import declarative_base
# from app.config import DATABASE_URL, DATABASE_URL_SYNC

import os

DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_URL_SYNC = os.getenv("DATABASE_URL_SYNC")



Base = declarative_base()

# # Always create engines
# engine = create_async_engine(
#     DATABASE_URL,
#     echo=False,
#     pool_pre_ping=True,
#     connect_args={"statement_cache_size": 0},
# )



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
