from redis import ConnectionPool
from persistences.redis.connection import connect_redis
from configuration.api_service_config.config_fastapi import settings


def init_pool():
    nosql = settings["nosql"]
    if nosql.get("password", None) is not None:
        pool = ConnectionPool(
            host=nosql["host"],
            port=nosql["port"],
            password=nosql["password"],
            decode_responses=True,
        )
        return pool

    pool = ConnectionPool(
        host=nosql["host"],
        port=nosql["port"],
        decode_responses=True,
    )
    return pool


def get_redis():
    pool = init_pool()
    redis = connect_redis(pool)
    return redis
