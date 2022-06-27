from gettext import translation
from fastapi import (
    APIRouter,
    FastAPI,
    HTTPException,
    Depends,
    Response,
    status,
    BackgroundTasks,
)
from routers.fastapi_dependency.validation.pydantic.products import Product
from routers.fastapi_dependency.database.redis import get_redis
from aioredis import Redis
from typing import Type, Union
from persistences.redis.key_format import Keys, make_keys

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/")
async def get_products(redis: Redis = Depends(get_redis)):
    print(await redis.keys())
    # return [format(pk) for pk in Product.all_pks()]


def format(pk: str):
    product = Product.get(pk)

    return {
        "id": product.pk,
        "name": product.name,
        "price": product.price,
        "quantity": product.quantity,
    }


async def product_to_redis(key: Keys, mapping_data, redis):
    async with redis.pipeline(transaction=True) as pipe:
        res = (
            await pipe.hset(name=key.product_key("123"), mapping=mapping_data)
            .hgetall(key.product_key("123"))
            .execute()
        )
    print(key.product_key("123"))
    print(res)


@router.post("/")
async def create_products(
    product: Product,
    background_tasks: BackgroundTasks,
    keys: Keys = Depends(make_keys),
    redis: Redis = Depends(get_redis),
):
    background_tasks.add_task(product_to_redis, keys, product.dict(), redis)
    # result = pipe.hgetall(0)
    # print(result.execute())

    # return result


@router.get("/{pk}")
def get(pk: str):
    return Product.get(pk)


@router.delete("/{pk}")
def delete(pk: str):
    return Product.delete(pk)
