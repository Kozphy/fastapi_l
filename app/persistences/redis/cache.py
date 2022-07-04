from distutils.log import debug
from persistences.redis.key_format import Keys
from persistences.redis.connection import Redis_connect

from aioredis import Redis
import json
from constants import CACHE_TIME
from loguru import logger
import asyncio

from celery_app.celery_work import celery
from yaml import serialize
from routers.dependency.database.redis import Redis_denpendency

# redis = get_redis


@celery.task(name="cache.get_cache")
async def get_cache(self, keys: str, redis: Redis):
    try:
        data = await redis.get(keys)

        if data:
            return data

        return None
    except Exception as e:
        logger.error(e)
        raise


@celery.task(name="cache.set_cache")
def set_cache(cache_data: list, keys: str):
    try:
        redis = Redis_denpendency.from_connect(Redis_connect)
        result = redis.set(name=keys, value=cache_data, ex=CACHE_TIME)
        return result

    except Exception as e:
        logger.error(e)
        raise
