from persistences.redis.connection import Redis_custom
from configuration.api_service_config.config_fastapi import settings
from copy import deepcopy
from aioredis import Redis


def redis_init() -> Redis_custom:
    nosql_config = deepcopy(settings["nosql"])
    del nosql_config["db"]
    redis: Redis_custom = Redis_custom.from_config(**nosql_config)
    return redis


async def get_redis() -> Redis:
    redis: Redis_custom = redis_init()
    return await redis.connect_redis()
