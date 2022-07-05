from distutils.log import debug
from persistences.redis.key_format import Keys
from persistences.redis.connection import Redis_connect

from aioredis import Redis
import json
from constants import CACHE_TIME

# from loguru import logger
from celery.utils.log import get_task_logger
import asyncio
import redis as redis_sync

from celery_app.celery_work import celery
from yaml import serialize
from routers.dependency.database.redis import Redis_denpendency

redis: redis_sync = Redis_denpendency.from_connect(Redis_connect).get_redis()
logger = get_task_logger(__name__)


@celery.task(name="cache.get_cache")
def get_cache(keys: str):
    try:
        data = redis.get(keys)

        if data:
            return data

        return None
    except Exception as e:
        logger.error(e)
        raise


@celery.task(name="cache.set_cache")
def set_cache(cache_data: list, keys: str):
    try:
        result = redis.set(name=keys, value=cache_data, ex=CACHE_TIME)
        return result

    except Exception as e:
        logger.error(e)
        raise
