from fastapi import (HTTPException,
Depends, Response, status, APIRouter)

from typing import List, Dict
from loguru import logger

from persistences.fastapi_dependency.db import get_db
from persistences.postgresql.modules.posts import Post_table
from persistences.postgresql.modules.users import User_table


from sqlalchemy import (text, select, literal_column, insert, delete, update,
Table, MetaData)
from sqlalchemy.engine import CursorResult, Connection

from routers.validation.fast_api_pydantic.post import Post_create, Post_update, Post_response
from routers.validation.fast_api_pydantic.user import User_response
from routers.validation.auth import oauth2

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=List[Post_response])
def create_posts(posts: List[Post_create], current_user_data: CursorResult= Depends(oauth2.get_current_user), db: Connection = Depends(get_db)):
    logger.debug(f"create posts")

    owner_id = current_user_data[0]
    new_posts = []
    for data in posts:
        data.owner_id = owner_id
        new_posts.append(data.dict())
    
    logger.debug(f"new_posts is {new_posts}")
    stmt_insert_posts = insert(Post_table).returning(Post_table)
    all_posts = db.execute(stmt_insert_posts, new_posts).all()
    logger.debug(f"all_posts is {all_posts}")

    response = []
    for data in all_posts:
        # data is considered to be nametuple
        response.append(Post_response(**data, owner=current_user_data))


    return response

@router.get("/" ,response_model=List[Post_response])
def get_posts(current_user_data: CursorResult= Depends(oauth2.get_current_user), db: Connection = Depends(get_db), 
    limit: int = 10):
    logger.debug('get posts')
    logger.debug(f'limit is {limit}')
    # posts = db.execute(text("""SELECT * FROM posts""")).all()
    # print(f'current_user {current_user}')
    current_user_id = current_user_data[0]

    stmt_select_all = (
        select(
            Post_table
        ).where(Post_table.c.owner_id == current_user_id)
    )

    posts = []
    data = db.execute(stmt_select_all).fetchmany(limit)
    for post in data:
        # data is considered to be nametuple
        posts.append(Post_response(**post, owner=current_user_data))

    return posts



@router.get("/{id}", response_model=Post_response)
def get_post(id: int, current_user_data: CursorResult= Depends(oauth2.get_current_user), db: Connection = Depends(get_db)):
    logger.debug(f'get one post')
    # stmt_1 = text("""SELECT * from posts WHERE id = :s""")
    # p = db.execute(stmt_1, (str(id),)).fetchone()
    current_user_id = current_user_data[0]

    stmt_select_one = select(Post_table).where(
        Post_table.c.owner_id == current_user_id,
        Post_table.c.id == id
        )
    data = db.execute(stmt_select_one).first()

    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} not found")

    logger.debug(f'data is {data}')
    response = Post_response(**data, owner=current_user_data)
    
    return response


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, current_user_data: CursorResult= Depends(oauth2.get_current_user), db: Connection = Depends(get_db)):
    logger.debug(f'delete post')
    
    stmt = select(Post_table).where(Post_table.c.id == id)
    data = db.execute(stmt).first()
    current_user_id = current_user_data[0]
    # print(p)

    if data == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    if data.owner_id != current_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to delete action")

    del_stmt = delete(Post_table).where(Post_table.c.id == id)
    db.execute(del_stmt)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
   

@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=Post_response )
def update_post(id: int, post: Post_update, current_user_data: CursorResult= Depends(oauth2.get_current_user), db: Connection = Depends(get_db)):
    logger.debug(f'update post')

    stmt = select(Post_table).where(Post_table.c.id == id)
    data = db.execute(stmt).first()
    if data == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

    current_user_id = current_user_data[0]

    if data.owner_id != current_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to update action")
    
    update_stmt = update(Post_table).where(Post_table.c.id == id).\
    values(title=post.title, content=post.content, published=post.published).\
    returning(Post_table)


    update_data=db.execute(update_stmt).first()
    response = Post_response(**update_data, owner=current_user_data)
    # print(update_data)


    return response