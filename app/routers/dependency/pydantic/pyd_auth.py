from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# JWT
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str]