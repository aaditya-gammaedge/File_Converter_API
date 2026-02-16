from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.db import engine, create_tables
from app.db.models import File, Job, User
from app.api.routes import auth
from dotenv import load_dotenv


from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.utils.cleanup import cleanup_expired_files


load_dotenv()

from app.api.routes import upload, download, convert,health
@asynccontextmanager
async def lifespan(app: FastAPI):
    
    try:
        await create_tables()
        print("Database connected & tables created")
    except Exception as e:
        print("Database Startup Failed:", e)

    yield


    await engine.dispose()
    print("Database connection closed from supabase")

app = FastAPI(lifespan=lifespan, title="File_ConverterAPI")


@app.get("/")
def root():
    return {"message": "File Converter API is running!"}

app.include_router(auth.router)

app.include_router(upload.router)
app.include_router(convert.router)
app.include_router(download.router)
app.include_router(health.router)



from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()
@scheduler.scheduled_job("interval", hours=1)
async def scheduled_cleanup():
    await cleanup_expired_files()

@asynccontextmanager
async def lifespan(app):
    scheduler.start()
    yield
    scheduler.shutdown()




# from dotenv import load_dotenv
# load_dotenv()

# import os
# from fastapi import FastAPI
# from contextlib import asynccontextmanager

# from app.db.db import engine
# from app.api.routes import auth, upload, download, convert, health
# from apscheduler.schedulers.asyncio import AsyncIOScheduler
# from app.utils.cleanup import cleanup_expired_files


# scheduler = AsyncIOScheduler()


# @asynccontextmanager
# async def lifespan(app: FastAPI):

#     print("App startup")

#     # 🚨 DO NOT start scheduler during tests
#     if os.getenv("ENV") != "test":
#         scheduler.start()

#     yield

#     if os.getenv("ENV") != "test":
#         scheduler.shutdown()

#     await engine.dispose()
#     print("Database connection closed")


# app = FastAPI(lifespan=lifespan, title="File_ConverterAPI")

# # Routers
# app.include_router(auth.router)
# app.include_router(upload.router)
# app.include_router(convert.router)
# app.include_router(download.router)
# app.include_router(health.router)


# @scheduler.scheduled_job("interval", hours=1)
# async def scheduled_cleanup():
#     await cleanup_expired_files()
