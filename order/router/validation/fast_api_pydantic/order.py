from redis_om import HashModel
from persistences.redis.connection import redis


class Order(HashModel):
    product_id: str
    price: float
    fee: float
    total: float
    quantity: int
    status: str = str  # pending, completed, refunded

    class Meta:
        database = redis
