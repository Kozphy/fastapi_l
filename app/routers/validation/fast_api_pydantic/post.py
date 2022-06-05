from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict

from .user import User_response

class Post_base(BaseModel):
    title: str
    content: str
    published: bool = True

## validate request 
class Post_create(BaseModel):
    data: List[Dict[Post_base]]


class Post_update(Post_base):
    published: bool

## validate response
class Post_response(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    create_at: datetime
    owner: User_response

    class Config:
        orm_mode = True


