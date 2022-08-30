from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, Union, Literal

# request validate
class User_base(BaseModel):
    email: Union[EmailStr, Literal[""]]
    phone: Optional[str]
    username: Optional[str]
    password: str


class User_create(User_base):
    surname: str
    given_name: str
    description: str
    password_check: str


class User_address(BaseModel):
    city: str
    region: str
    address1: str
    address2: str
    address3: str
    country: str
    zip_code: str


class User_id_card(BaseModel):
    gender: str
    id_card: str


class User_phone(BaseModel):
    country_code: str
    subscriber_number: str


class User_login(User_base):
    pass


# TODO: one of email phone and username value must exist
class User_response(BaseModel):
    id: int
    email: Union[EmailStr, Literal[""]]
    phone: Optional[int]
    username: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True
