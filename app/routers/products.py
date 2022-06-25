from gettext import translation
from fastapi import APIRouter, FastAPI, HTTPException, Depends, Response, status
from routers.fastapi_dependency.validation.pydantic.products import Product
from routers.fastapi_dependency.database.redis import get_redis
from aioredis import Redis
from typing import Type, Union

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


@router.post("/")
async def create_products(product: Product, redis: Redis = Depends(get_redis)):
    async with redis.pipeline(transaction=True) as pipe:
        res = await pipe.hset(name=0, mapping=product.dict()).hgetall(0).execute()
    print(res)
    # result = pipe.hgetall(0)
    # print(result.execute())

    # return result


@router.get("/{pk}")
def get(pk: str):
    return Product.get(pk)


@router.delete("/{pk}")
def delete(pk: str):
    return Product.delete(pk)
