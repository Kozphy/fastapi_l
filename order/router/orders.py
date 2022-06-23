from fastapi import APIRouter, FastAPI, HTTPException, Depends, Response, status
from order.router.validation.fast_api_pydantic.order import Order
from starlette.requests import Request
import requests

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/")
async def create_order(request: Request):  # id, quantity
    body = await request.json()

    req = requests.get("http://0.0.0.0:8080/products/%s" % body["id"])

    return req.json()
