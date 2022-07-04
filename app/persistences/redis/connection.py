from attrs import define, field
from persistences.base import Base
from loguru import logger
import redis
import aioredis
from aioredis import Redis as async_redis
from typing import Union


@define
class Redis_connect:
    common_config: Base
    db_num: int
    ssl: str
    ssl_ca_certs: str
    decode_responses: bool
    health_check_interval: int
    url: Union[str, None]

    @classmethod
    def from_config(cls, **kwargs):
        base_attris = [
            attr
            for attr in dir(Base)
            if not attr.startswith("_") and attr not in ["from_config"]
        ]
        base = Base.from_config(base_attris, **kwargs)
        kwargs = {k: v for k, v in kwargs.items() if k not in base_attris}
        redis = cls(
            common_config=base,
            decode_responses=True,
            url=None,
            **kwargs,
        )
        if redis.url is None:
            redis.init_redis_url()
        return redis

    def init_redis_url(self) -> None:
        """
        redis:// creates a TCP socket connection.
        See more at: https://www.iana.org/assignments/uri-schemes/prov/redis
        rediss:// creates a SSL wrapped TCP socket connection.
        See more at: https://www.iana.org/assignments/uri-schemes/prov/rediss

        For example:
        redis://[[username]:[password]]@localhost:6379/0
        rediss://[[username]:[password]]@localhost:6379/0
        unix://[[username]:[password]]@/path/to/socket.sock?db=0
        """
        common = self.common_config
        support_url_schemas = {
            "redis": "redis://",
            "rediss": "rediss://",
            "unix": "unix://",
        }

        base_url_list = [
            support_url_schemas[common.url_schema],
            common.username,
            ":",
            common.password,
            "@",
            common.host,
        ]

        if base_url_list[1] == "None" and base_url_list[3] == "None":
            for i in [":", "@"]:
                base_url_list.remove(i)

        base_url = "".join(filter(lambda el: el != "None", base_url_list))

        if common.url_schema == "unix":
            url = f"{base_url}?db={self.db_num}"
            self.url = url
            return

        url = f"{base_url}:{common.port}/{self.db_num}"
        self.url = url
        return

    def get_redis_url(self) -> str:
        return self.url

    async def connect_async_redis(self) -> async_redis:
        logger.info("connect to async redis")
        logger.debug(f"Connecting to redis url is {self.url}")
        redis = await aioredis.from_url(self.url)
        return redis

    def connect_redis(
        self,
    ) -> redis:
        logger.info("connect to sync redis")
        # pool = redis.ConnectionPool(
        #     host=self.common_config.host,
        #     port=self.common_config.port,
        #     db=self.db_num,
        # )
        r = redis.Redis.from_url(self.url)
        return r
