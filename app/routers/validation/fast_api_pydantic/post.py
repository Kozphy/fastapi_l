from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict, Union

from .user import User_response

class Post_base(BaseModel):
    id: int
    title: str
    content: str
    create_at: datetime
    published: bool = True
    owner_id : Union[int, None] = None

## validate request 
class Post_create(Post_base):
    pass


class Post_update(Post_base):
    published: bool

## validate response
class Post_response(Post_base):
    vote: int
    owner: User_response

    class Config:
        orm_mode = True


