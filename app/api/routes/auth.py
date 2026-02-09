from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.db import AsyncSessionLocal
from app.db.models.user import User
from app.db.schemas.user_schema import UserCreate, UserLogin, UserRead
from app.api.auth.jwt import hash_password, verify_password
from app.api.auth.jwt import create_access_token


router = APIRouter(prefix="/auth", tags=["auth"])


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


@router.post("/register", response_model=UserRead)
async def register_user(
    payload: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(User).where(User.email == payload.email)
    )
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    user = User(
        email=payload.email,
        hashed_password=hash_password(payload.password)
    )
    # hashed_password = hash_password(payload.password)
    # new_user = User(email=user.email, hashed_password=hashed_password)

    db.add(user)
    await db.commit()
    await db.refresh(user)
    
    return user
    print("login")


@router.post("/login")
async def login_user(
    payload: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(User).where(User.email == payload.email)
    )
    user = result.scalar_one_or_none()

    if not user or not verify_password(
        payload.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    token = create_access_token(user.id)

    return {
        "access_token": token,
        "token_type": "bearer"
    }
