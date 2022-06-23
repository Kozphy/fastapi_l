from fastapi import FastAPI, HTTPException, Depends, Response, status
from fastapi.middleware.cors import CORSMiddleware
from app.configuration.api_service_config.config_fastapi import settings

from loguru import logger
from routers import post, products, user, auth, vote

from order.router import orders


app = FastAPI()

origins = [
    "https://www.google.com",
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(orders.router)

# home
@app.get("/")
async def root():
    return {"message": "welcome order service"}
