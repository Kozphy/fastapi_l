from redis_om import HashModel
from persistences.redis.meta import redis


class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database = redis
