from redis import asyncio as aioredis
from attrs import define, field

from typing import Union, Dict


@define
class Redis:
    redis_config = Dict[str, Union[bool, int]]
    url_schema: str
    username: str
    password: str
    host: str
    port: str
    db_num: int
    ssl: str
    ssl_ca_certs: str
    decode_responses: bool
    health_check_interval: int

    @classmethod
    def from_config(cls, **kwargs):
        print(kwargs)
        return cls()

    def init_redis_url(self):
        if self.url_schema == "redis":
            """
            redis:// creates a TCP socket connection.
            See more at: https://www.iana.org/assignments/uri-schemes/prov/redis
            """
            url = ""

    def connect_redis(self):
        url = self.init_redis_url()
        redis = aioredis.from_url(url)
        return redis
