from fastapi import (FastAPI, HTTPException,
Depends, Response, status)

from configuration.api_service_config.config_fastapi import settings

from loguru import logger
from routers import post, user, auth


app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

# home
@app.get("/")
async def root():
    print(settings)
    return {"message": "Hello World"}

    