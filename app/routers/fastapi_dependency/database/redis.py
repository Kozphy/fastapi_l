from persistences.redis.connection import Redis_custom
from configuration.api_service_config.config_fastapi import settings
from copy import deepcopy
from aioredis import Redis
import asyncio


async def get_redis() -> Redis:
    nosql_config = deepcopy(settings["nosql"])
    if nosql_config["db"] == "redis":
        del nosql_config["db"]
        redis = await Redis_custom.from_config(**nosql_config).connect_redis()
        return redis
    return None
