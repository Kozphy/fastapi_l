from fastapi import (HTTPException,
Depends, Response, status, APIRouter)

from typing import List
from loguru import logger

from persistences.fastapi_dependency.db import get_db
from persistences.postgresql.modules.posts import Post_table
from persistences.postgresql.modules.users import User_table


from sqlalchemy import (text, select, literal_column, insert, delete, update,
Table, MetaData)
from sqlalchemy.engine import Transaction

from routers.validation.fast_api_pydantic.post import Post_create, Post_update, Post_response
from routers.validation.auth import oauth2

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)



@router.get("/" ,response_model=List[Post_response])
def get_posts(current_user_data: int= Depends(oauth2.get_current_user), db: Transaction = Depends(get_db)):
    # posts = db.execute(text("""SELECT * FROM posts""")).all()
    # print(f'current_user {current_user}')
    print(current_user_data)
    current_user_id = current_user_data[0]

    stmt = (
        select(
            Post_table
        ).where(Post_table.c.owner_id == current_user_id)
    )

    posts = []
    data = db.execute(stmt).all()
    # print(all_post)
    for post in data:
        posts.append(Post_response(**post, owner=current_user_data))

    return posts


    

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Post_response)
def create_posts(posts: Post_create, current_user_data: int= Depends(oauth2.get_current_user), db: Transaction = Depends(get_db)):
    logger.debug(f"create posts {posts}")



    # TODO: insert multiple posts at once
    owner_id = current_user_data[0]

    new_post = posts.dict()
    logger.debug(f"new_post is {new_post}")
    new_post.update({"owner_id": owner_id})

    stmt_3 = insert(Post_table).values(**new_post).returning(Post_table)

    data = db.execute(stmt_3)

    all_posts = data.all()
    print(all_posts)
    

    return all_posts[0]


@router.get("/{id}", response_model=Post_response)
def get_post(id: int, response: Response, db: Transaction = Depends(get_db)):
    logger.debug(f'get one post')
    # stmt_1 = text("""SELECT * from posts WHERE id = :s""")
    # p = db.execute(stmt_1, (str(id),)).fetchone()

    stmt_2 = select(Post_table).where(Post_table.c.id == id)
    data = db.execute(stmt_2).first()

    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} not found")


    result = Post_response(**data)
        
    
    return result


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, current_user: int= Depends(oauth2.get_current_user), db: Transaction = Depends(get_db)):
    logger.debug(f'delete post')
    
    stmt = select(Post_table).where(Post_table.c.id == id)
    data = db.execute(stmt).first()
    # print(p)

    if data == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    if data.owner_id != current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to delete action")

    del_stmt = delete(Post_table).where(Post_table.c.id == id)
    db.execute(del_stmt)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
   

@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=Post_response )
def update_post(id: int, post: Post_update, current_user: int= Depends(oauth2.get_current_user), db: Transaction = Depends(get_db)):

    stmt = select(Post_table).where(Post_table.c.id == id)
    data = db.execute(stmt).first()
    if data == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    if data.owner_id != current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to update action")
    
    update_stmt = update(Post_table).where(Post_table.c.id == id).\
    values(title=post.title, content=post.content, published=post.published).\
    returning(Post_table)

    update_data=db.execute(update_stmt).first()
    # print(update_data)


    return update_data