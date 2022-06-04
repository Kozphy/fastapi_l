from fastapi import (HTTPException,
Depends, Response, status, APIRouter)

from typing import List

from persistences.fastapi_dependency.db import get_db
from persistences.postgresql.modules.posts import Post_table

from sqlalchemy import text, select, literal_column, insert, delete, update
from sqlalchemy.engine import Transaction

from routers.validation.fast_api_pydantic.post import Post_create, Post_update, Post_response
from routers.validation.auth import oauth2

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/" ,response_model=List[Post_response])
def get_posts(current_user: int= Depends(oauth2.get_current_user), db: Transaction = Depends(get_db)):
    # posts = db.execute(text("""SELECT * FROM posts""")).all()

    stmt = (
        select(
            Post_table
        )
    )

    posts = []
    p = db.execute(stmt)
    posts_content = p.all()
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
    # print(posts) 
    return posts


    

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Post_response)
def create_posts(post: Post_create, current_user: int= Depends(oauth2.get_current_user), db: Transaction = Depends(get_db)):
    # stmt_1 = text("""INSERT INTO posts (title, content, published) VALUES (
    #     :title, :content, :published) returning * """
    # )
    # p = db.execute(stmt_1, [{'title': post.title, 'content': post.content, 'published': post.published}]).all()
    print(current_user)

    stmt_2 = insert(Post_table).values(title=post.title, content=post.content,
     published=post.published).returning(
         Post_table,
     )

    new_post = post.dict()
    stmt_3 = insert(Post_table).values(**new_post).returning(Post_table)

    p = db.execute(stmt_3)

    all_posts = p.all()
    # print(all_posts)

    return all_posts[0]


@router.get("/{id}", response_model=Post_response)
def get_post(id: int, response: Response, db: Transaction = Depends(get_db)):
    # stmt_1 = text("""SELECT * from posts WHERE id = :s""")
    # p = db.execute(stmt_1, (str(id),)).fetchone()
    # print(p)

    stmt_2 = select(Post_table).where(Post_table.c.id == id)
    p = db.execute(stmt_2).first()
    # print(p)

    post_title = ['id', 'title', 'content', 'published', 'create_at']
    result = {}
    for i, title in enumerate(post_title):
        result.update({title:p[i]})
        
    if not p:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} not found")
    
    return result


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, current_user: int= Depends(oauth2.get_current_user), db: Transaction = Depends(get_db)):
 
    
    stmt = select(Post_table).where(Post_table.c.id == id)
    p = db.execute(stmt).first()
    # print(p)

    if p == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    del_stmt = delete(Post_table).where(Post_table.c.id == id)
    db.execute(del_stmt)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
   

@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=Post_response )
def update_post(id: int, post: Post_update, current_user: int= Depends(oauth2.get_current_user), db: Transaction = Depends(get_db)):

    stmt = select(Post_table).where(Post_table.c.id == id)
    p = db.execute(stmt).first()
    if p == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    update_stmt = update(Post_table).where(Post_table.c.id == id).\
    values(title=post.title, content=post.content, published=post.published).\
    returning(Post_table)

    update_data=db.execute(update_stmt).first()
    # print(update_data)


    return update_data