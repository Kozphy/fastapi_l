from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# request validate
class User_base(BaseModel):
    email: EmailStr
    password: str


class User_create(User_base):
    surname: str
    given_name: str
    gender: str
    id_card: str
    phone_number: str
    address1: str
    address2: str
    address3: str
    country: str
    city: str
    region: str
    zip_code: str
    country_code: str
    subscriber_number: str
    description: str


class User_login(User_base):
    pass


class User_response(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True
