from models.m_user import check_account_exist
from pydantic import BaseModel, EmailStr, validator, ValidationError, root_validator

# from fastapi import HTTPException, status
from datetime import datetime
from typing import Optional, Union, Literal


# request validate
class User_base(BaseModel):
    email: Union[EmailStr, Literal[""], None] = None
    phone: Optional[str] = None
    username: Optional[str] = None
    password: str

    @validator("phone")
    def phone_must_start_with_plus(cls, v):
        if v is not None and v != "" and not v.startswith("+"):
            raise ValueError("phone must be E.164 format.")
        return v


class User_create(User_base):
    surname: str
    given_name: str
    description: str
    password_check: str

    @root_validator(pre=True)
    def check_account_exist(cls, values):
        email, phone, username = (
            values.get("email", None),
            values.get("phone", None),
            values.get("username", None),
        )

        if not (email or phone or username):
            raise ValueError(
                "please input one of email, phone and username value as your account."
            )

        return values

    @validator("password_check", pre=True)
    def password_match(cls, v, values, **kwargs):
        if "password" in values and v != values["password"]:
            raise ValueError("password and password_check must be match.")
        return v


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


class User_create_response(BaseModel):
    registration: Union[str, EmailStr]
    created_at: datetime

    class Config:
        orm_mode = True


# TODO: one of email phone and username value must exist
# Optional email
class User_response(BaseModel):
    email: Union[EmailStr, Literal[""], None] = None
    phone: Optional[int] = None
    username: Optional[str] = None
    created_at: datetime

    class Config:
        orm_mode = True
