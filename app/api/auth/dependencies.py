from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID



from app.api.auth.jwt import decode_access_token
from app.db.db import AsyncSessionLocal
from app.db.models import User


bearer_scheme = HTTPBearer(auto_error=True)


async def get_db():
    if AsyncSessionLocal is None:
        raise RuntimeError("Database session not initialized")

    async with AsyncSessionLocal() as session:
        yield session




async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    token = credentials.credentials  

    user_id: UUID | None = decode_access_token(token)

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )


    user = await db.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )



    return user





