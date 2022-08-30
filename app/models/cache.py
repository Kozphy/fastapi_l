from loguru import logger
from persistences.redis.cache import get_cache, set_cache
import json
from aioredis import Redis
from celery_app.pickling import save
import asyncio


def data_to_redis_cache(cache_data, key):
    logger.debug("data to redis cache")

    try:
        result = set_cache.apply_async(
            args=[
                json.dumps(cache_data),
                key,
            ]
        )
        return result.state
    except set_cache.OperationalError as e:
        logger.error(e)
        raise


def get_data_from_redis_cache(key):
    try:
        result = get_cache.apply_async(
            args=[key],
        )
        return result.get()

    except get_cache.OperationalError as e:
        logger.error(e)
        raise
