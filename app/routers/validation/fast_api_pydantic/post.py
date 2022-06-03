from pydantic import BaseModel
from datetime import datetime

class Post_base(BaseModel):
    title: str
    content: str
    published: bool = True

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

    class Config:
        orm_mode = True


