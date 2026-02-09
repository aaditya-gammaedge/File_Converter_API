from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.db import engine, create_tables
from app.db.models import File, Job, User
from app.api.routes import auth

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

app = FastAPI(lifespan=lifespan)


app.include_router(auth.router)

@app.get("/health")
async def health():
    return {"hello": "hi"}
