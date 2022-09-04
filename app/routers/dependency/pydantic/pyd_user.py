from pydantic import BaseModel, EmailStr, validator, ValidationError, root_validator
import phonenumbers
from phonenumbers import geocoder, NumberParseException, PhoneNumber

from enums.country_code import CountryCodeId

from datetime import datetime
from typing import Optional, Union, Literal
from loguru import logger


# request validate
class User_base(BaseModel):
    email: Union[EmailStr, Literal[""], None] = None
    phone: Optional[str] = None
    username: Optional[str] = None
    password: str

    @validator("phone")
    def check_phone(cls, phone_v):
        if phone_v is None or phone_v == "":
            return phone_v

        ## phone must start with plus
        if not phone_v.startswith("+"):
            raise ValueError("phone must be E.164 format.")

        ## check phone country code
        try:
            ph_parse: PhoneNumber = phonenumbers.parse(phone_v)
            ## TODO: fix phone number area code is not start at 09 in taiwan
            ## check right digits
            if not phonenumbers.is_possible_number(ph_parse):
                raise ValueError("Phone number not possible.")

            ## check It's in an assigned exchange
            if not phonenumbers.is_valid_number(ph_parse):
                raise ValueError("Phone number not valid.")

            # Note: geocoder.description_for_number must be used after
            # phone have passed is_possbile_number and is_valid_number validation process.
            # otherwise region will return empty if user input phone is invalid number.
            region: str = geocoder.description_for_number(ph_parse, "en")
            if not hasattr(CountryCodeId, region):
                raise ValueError(
                    f"Currently, CountryCode: +{ph_parse.country_code}  not support in app"
                )

        except NumberParseException as e:
            if e.error_type == NumberParseException.INVALID_COUNTRY_CODE:
                raise ValueError(
                    "The country code supplied did not belong to a supported country or non-geographical entity."
                )
            else:
                logger.error(e)
                raise ValueError(e)

        return phone_v


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
