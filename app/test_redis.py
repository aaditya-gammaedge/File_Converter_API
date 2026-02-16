import asyncio
import os

import redis.asyncio as redis
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL")


async def test():
    try:
        r = redis.from_url(REDIS_URL, decode_responses=True)

        response = await r.ping()
        print("Ping response:", response)

        await r.set("test_key", "hello_redis", ex=30)

        value = await r.get("test_key")
        print("Value from Redis:", value)

        print("Redis connection working!")

    except Exception as e:
        print(" Redis connection failed:", e)


asyncio.run(test())
