from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.db import engine, create_tables
from app.db.models import File, Job, User
from app.api.routes import auth
from dotenv import load_dotenv
load_dotenv()

from app.api.routes import upload, download, convert
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


app.include_router(auth.router)

app.include_router(upload.router)
app.include_router(convert.router)
app.include_router(download.router)
@app.get("/health")
async def health():
    return {"hello": "hi"}




