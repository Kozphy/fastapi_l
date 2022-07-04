from persistences.redis.connection import Redis_connect
from configuration.api_service_config.config_fastapi import settings
from copy import deepcopy
import redis
from aioredis import Redis as async_redis
from persistences.redis.connection import Redis_connect
from attrs import define


@define
class Redis_denpendency:
    redis_connect: Redis_connect

    @classmethod
    def from_connect(cls, connect: Redis_connect):
        nosql_config = deepcopy(settings["nosql"])
        del nosql_config["db"]
        return cls(redis_connect=connect.from_config(**nosql_config))

    def get_redis(self) -> redis:
        """
        get sync redis
        """
        return self.redis_connect.connect_redis()

    def get_async_redis(self) -> async_redis:
        """
        get async redis
        """
        return self.redis_connect.connect_async_redis()
