from fastapi import APIRouter, FastAPI, HTTPException, Depends, Response, status
from configuration.api_service_config.config_fastapi import settings
from routers.validation.fast_api_pydantic.products import Product

router = APIRouter()


@router.get("/products")
def get_products():
    return Product.all_pks()


@router.post("/products")
def create_products(product: Product):
    return product.save()
