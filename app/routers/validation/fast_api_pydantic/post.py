from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict, Union

from .user import User_response

class Post_base(BaseModel):
    title: str
    content: str
    published: bool = True
    owner_id : Union[int, None] = None

## validate request 
class Post_create(Post_base):
    pass


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


