from fastapi import (HTTPException,
Depends, Response, status, APIRouter)

from sqlalchemy.engine import Transaction
from sqlalchemy import text, select, literal_column, insert, delete, update

from persistences.postgresql.modules.users import User_table
from persistences import utils
from persistences.fastapi_dependency.db import get_db

from routers.validation.fast_api_pydantic.user import User_create, User_response

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=User_response)
def create_users(user: User_create, db: Transaction = Depends(get_db)):

    stmt_check = select(User_table).where(User_table.c.email == user.email)
    check_email = db.execute(stmt_check).first()
    if check_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{user.email} email already exists")

    # hash the password - user.password
    hash_password = utils.hash(user.password)
    user.password = hash_password

    new_user = user.dict()
    # print(new_user)
    stmt = insert(User_table).values(**new_user).returning(User_table)

    result = db.execute(stmt).first()
    user_title = ['id', 'email', 'password', 'created_at']
    # print(result)
    res = {}
    for i, title in enumerate(user_title):
        res.update({title:result[i]})
    
    return res 

@router.get("/{id}", response_model=User_response)
def get_user(id: int, db: Transaction = Depends(get_db)):

    stmt = select(User_table).where(User_table.c.id == id)

    user = db.execute(stmt).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} does not exist")

    return user