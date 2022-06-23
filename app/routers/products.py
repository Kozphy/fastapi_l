from fastapi import APIRouter, FastAPI, HTTPException, Depends, Response, status
from routers.fastapi_dependency.validation.pydantic.products import Product
from routers.fastapi_dependency.database.redis import get_redis

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/")
def get_products():
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
def create_products(product: Product):
    return product.save()


@router.get("/{pk}")
def get(pk: str):
    return Product.get(pk)


@router.delete("/{pk}")
def delete(pk: str):
    return Product.delete(pk)
