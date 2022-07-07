from fastapi import FastAPI, HTTPException, Depends, Response, status
from fastapi.middleware.cors import CORSMiddleware

from configuration.api_service_config.config_fastapi import settings

from loguru import logger

from routers import login, post, products, user, vote
from celery_app.task import create_task

# from persistences.redis.key_format import Keys

app = FastAPI()


# @app.on_event("startup")
# async def startup_event():
#     keys = Keys()


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

app.include_router(post.router)
app.include_router(user.router)
app.include_router(login.router)
app.include_router(vote.router)
app.include_router(products.router)

# home
@app.get("/")
async def root():
    print(settings)
    res = create_task.delay(2, 2, 2)
    print(res.get())
    return {"message": "Hello World"}
