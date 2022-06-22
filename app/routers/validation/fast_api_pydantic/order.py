from redis_om import HashModel
from persistences.redis.meta import redis


class Order(HashModel):
    product_id: str
    price: float
    fee: float
    total: float
    quantity: int
    status: str = str

    class Meta:
        database = redis
