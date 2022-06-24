from fastapi import APIRouter, FastAPI, HTTPException, Depends, Response, status
from routers.fastapi_dependency.validation.pydantic.products import Product
from routers.fastapi_dependency.database.redis import get_redis

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/")
def get_products(redis: get_redis = Depends()):
    return [format(pk) for pk in Product.all_pks()]


def format(pk: str):
    product = Product.get(pk)

    return {
        "id": product.pk,
        "name": product.name,
        "price": product.price,
        "quantity": product.quantity,
    }


@router.post("/")
def create_products(product: Product, redis: get_redis = Depends()):
    pipe = redis.pipeline()
    print(product.dict())

    pipe.hset(name=0, mapping=product.dict())
    result = pipe.hgetall(0)
    print(result)

    # return result


@router.get("/{pk}")
def get(pk: str):
    return Product.get(pk)


@router.delete("/{pk}")
def delete(pk: str):
    return Product.delete(pk)
