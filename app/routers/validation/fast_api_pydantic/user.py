from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# request validate
class User_create(BaseModel):
    email: EmailStr
    password: str

class User_login(User_create):
    pass
    

class User_response(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

# JWT
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str]