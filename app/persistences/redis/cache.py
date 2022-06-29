from persistences.redis.key_format import Keys
from aioredis import Redis
import json
from constants import CACHE_TIME
from loguru import logger


async def get_cache(keys: str, redis: Redis):
    try:
        data = await redis.get(keys)

        if data:
            return data

        return None
    except Exception as e:
        logger.error(e)
        raise


async def set_cache(data, keys: str, redis: Redis):
    try:
        result = await redis.set(name=keys, value=json.dumps(data), ex=CACHE_TIME)
        return result
    except Exception as e:
        logger.error(e)
        raise
