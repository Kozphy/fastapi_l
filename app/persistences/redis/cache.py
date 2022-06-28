from persistences.redis.key_format import Keys
from aioredis import Redis
import json
from constants import CACHE_TIME


async def get_cache(keys: Keys, redis: Redis):
    data = await redis.get(keys)

    if data:
        return data

    return None


async def set_cache(data, keys: Keys, redis: Redis):
    await redis.set(name=keys.cache_key(), value=json.dumps(data), ex=CACHE_TIME)
