from fastapi import APIRouter, FastAPI, HTTPException, Depends, Response, status
from configuration.api_service_config.config_fastapi import settings
from routers.validation.fast_api_pydantic.products import Product

router = APIRouter()


@router.get("/products")
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


@router.post("/products")
def create_products(product: Product):
    return product.save()


@router.get("/product/{pk}")
def get(pk: str):
    return Product.get(pk)


@router.delete("/product/{pk}")
def delete(pk: str):
    return Product.delete(pk)
