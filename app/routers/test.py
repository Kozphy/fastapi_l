from fastapi import (FastAPI, HTTPException,
Depends, Response, status, APIRouter)

router = APIRouter(
    prefix="/test",
    tags=['Test'],
)

@router.get("/")
def test():
    print('hello test')