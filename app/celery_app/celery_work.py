from routers.dependency.database.redis import Redis_denpendency
from persistences.redis.connection import Redis_connect

from celery import Celery

redis: Redis_denpendency = Redis_denpendency.from_connect(Redis_connect)

celery = Celery(
    __name__,
    broker=redis.get_redis_url(),
    backend=redis.get_redis_url(),
    include=[
        "app.celery_app.task",
        "app.persistences.redis.cache",
    ],
)


if __name__ == "__main__":
    celery.start()
