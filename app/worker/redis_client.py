import redis

from app.config import (UPSTASH_REDIS_HOST, UPSTASH_REDIS_PASSWORD,
                        UPSTASH_REDIS_PORT)

redis_client = redis.Redis(
    host=UPSTASH_REDIS_HOST,
    port=int(UPSTASH_REDIS_PORT),
    password=UPSTASH_REDIS_PASSWORD,
    ssl=True,
    decode_responses=True,
)


def get_next_job():
    job = redis_client.blpop("convert_queue", timeout=0)
    if job:
        return job[1]
    return None
