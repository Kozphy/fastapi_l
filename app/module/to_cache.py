from loguru import logger
from persistences.redis.cache import get_cache, set_cache
import json
from aioredis import Redis
from celery_app.pickling import save
import asyncio
import pickle
import cloudpickle


def data_to_redis_cache(cache_data, key):
    logger.debug("data to redis cache")

    try:
        # logger.debug(type(nosqldb))
        # db = cloudpickle.dumps(nosqldb)
        result = set_cache.apply_async(
            (
                json.dumps(cache_data),
                key,
            )
        )

        return result
    except Exception as e:
        logger.error(e)
        raise

    # task = asyncio.create_task()
