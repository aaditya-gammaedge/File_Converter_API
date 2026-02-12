import functools
from fastapi import HTTPException
from app.utils.redis import redis_client


RATE_LIMIT = 10
WINDOW = 60


def rate_limit(limit: int = RATE_LIMIT, window: int = WINDOW):

    def decorator(func):

        @functools.wraps(func)
        async def wrapper(*args, **kwargs):            
            current_user = kwargs.get("current_user")

            if not current_user:
                raise HTTPException(
                    status_code=401,
                    detail="Authentication required"
                )
            user_id = str(current_user.id)
            redis_key = f"rate_limit:{user_id}"

            current = redis_client.get(redis_key)



            if current and int(current) >= limit:
                raise HTTPException(
                    status_code=429,
                    detail="Rate limit exceeded"
                )

            redis_client.incr(redis_key)

            if not current:
                redis_client.expire(redis_key, window)

            return await func(*args, **kwargs)

        return wrapper

    return decorator
