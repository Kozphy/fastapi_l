from fastapi import (FastAPI, HTTPException,
Depends, Response, status)
from fastapi.middleware.cors import CORSMiddleware

from configuration.api_service_config.config_fastapi import settings

from loguru import logger
from routers import post, user, auth, vote


app = FastAPI()

origins = [
    "https://www.google.com",
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
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
app.include_router(auth.router)
app.include_router(vote.router)


# home
@app.get("/")
async def root():
    # print(settings)
    return {"message": "Hello World"}

    