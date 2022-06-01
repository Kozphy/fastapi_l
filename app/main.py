from fastapi import (FastAPI, HTTPException,
Depends, Response, status)
from pydantic import BaseModel
from typing import Optional
from random import randrange

from sqlalchemy import text, select, literal_column, insert
from sqlalchemy.engine import Transaction
from persistences.fastapi_dependency.db import get_db
from persistences.postgresql.modules.posts import Post_table
from configuration.api_service_config.config_fastapi import settings
from loguru import logger

app = FastAPI()



class Post(BaseModel):
    title: str
    content: str
    published: bool = True

my_posts = [
    {
        "title": "title of post 1",
        "content": "content of post 1",
        "id": 1
     },
     {
         "title": "favorite foods",
         "content": "pizza, pasta, burger",
         "id": 2,
     }
]

@app.get("/")
async def root():
    print(settings)
    return {"message": "Hello World"}

@app.get("/posts" )
def get_posts(db: Transaction = Depends(get_db)):
    # posts = db.execute(text("""SELECT * FROM posts""")).all()

    stmt = (
        select(
            Post_table
        )
    )

    posts = []
    posts_content = db.execute(stmt).all()
    for post in posts_content:
        posts.append(
            {
                'id': post[0],
                'title': post[1],
                'content': post[2],
                'published': post[3],
                'create_at': post[4],
            }
        )
        
    return {"data": posts}


    

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post, db: Transaction = Depends(get_db)):
    stmt = insert(Post_table).values(title=post.title, content=post.content,
     published=post.published).returning(
         Post_table.c.title,
         Post_table.c.content,
         Post_table.c.published,
     )
    # TODO: fix returning maximum recursive issue
    db.execute(stmt)
    # for p in new_posts:
    #     print(p)



    # return {"data": new_posts}
    # post_dict = post.dict()
    # post_dict['id'] = randrange(0, 100000)
    # my_posts.append(post_dict)
    # return {"data": post_dict}

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

# @app.get("/posts/latest")
# def get_latest_post():
#     post = my_posts[len(my_posts)-1]
#     return {"detail": post}

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} not found")
    print(post)
    return {"data": f"{post}"}

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # deleting post
    # find the index in the aarray that has required ID 
    # my_posts.pop(i)
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
   

@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int, post: Post):
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {'data': post_dict}

# @app.get("/sqlalchemy")
# def test_posts(db: Transaction = Depends(get_db)):
#     stmt = select(text("'id'"), Post_table.c.id)
#     print(stmt)
#     result = []
#     for row in db.execute(stmt):
#         result.append(row)
#     print(result)
    # return {"data", result} 