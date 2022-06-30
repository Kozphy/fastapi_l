from loguru import logger
from persistences.redis.cache import get_cache, set_cache
import asyncio


def data_to_redis_cache(cache_data, key, nosqldb):
    logger.debug("data to redis cache")
    try:
        result = asyncio.run(set_cache(cache_data, key, nosqldb))
        print(result)
        return result
    except Exception as e:
        logger.debug(e)
        raise

    # task = asyncio.create_task()
