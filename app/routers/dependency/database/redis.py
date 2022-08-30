from persistences.redis.connection import Redis_connect
from configuration.api_service_config.config_fastapi import settings
from copy import deepcopy
import redis as sync_redis
from aioredis import Redis as async_redis
from attrs import define
from typing import Dict, Any


@define
class Redis_denpendency:
    """create redis connection

    Returns:
        Redis_denpendency
    """

    redis_connect: Redis_connect
    config: Dict[str, Any]

    @classmethod
    def from_connect(cls, connect: Redis_connect, config: Dict[str, Any] = settings):
        nosql_config = deepcopy(settings["nosql"])
        del nosql_config["db"]
        redis_connect = connect.from_config(**nosql_config)
        return cls(redis_connect=redis_connect, config=nosql_config)

    def get_redis_url(self) -> str:
        return self.redis_connect.url

    def get_redis(self) -> sync_redis:
        """
        get sync redis
        """
        return self.redis_connect.connect_redis()

    def get_async_redis(self) -> async_redis:
        """
        get async redis
        """
        return self.redis_connect.connect_async_redis()
