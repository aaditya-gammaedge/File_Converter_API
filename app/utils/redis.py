# import redis
# from app.config import (
#     UPSTASH_REDIS_HOST,
#     UPSTASH_REDIS_PORT,
#     UPSTASH_REDIS_PASSWORD
# )

# redis_client = redis.Redis(
#     host=UPSTASH_REDIS_HOST,
#     port=int(UPSTASH_REDIS_PORT),
#     password=UPSTASH_REDIS_PASSWORD,
#     ssl=True,
#     decode_responses=True,
# )


import redis

from app.config import (UPSTASH_REDIS_HOST, UPSTASH_REDIS_PASSWORD,
                        UPSTASH_REDIS_PORT)

redis_client = None

# checkingg
if UPSTASH_REDIS_HOST and UPSTASH_REDIS_PORT:
    redis_client = redis.Redis(
        host=UPSTASH_REDIS_HOST,
        port=int(UPSTASH_REDIS_PORT),
        password=UPSTASH_REDIS_PASSWORD,
        ssl=True,
        decode_responses=True,
    )
