from redis import asyncio as aioredis
from redis import ConnectionPool


def connect_redis(pool: ConnectionPool):
    redis = aioredis.Redis(pool)
    return redis
