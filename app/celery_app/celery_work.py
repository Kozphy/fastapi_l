from routers.fastapi_dependency.database.redis import redis_init

from celery import Celery

redis = redis_init()

celery = Celery(
    __name__,
    broker=redis.get_redis_url(),
    backend=redis.get_redis_url(),
    include=["app.task"],
)


if __name__ == "__main__":
    celery.start()
