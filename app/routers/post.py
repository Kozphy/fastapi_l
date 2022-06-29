from fastapi import HTTPException, Depends, Response, status, APIRouter, BackgroundTasks

from typing import List, Dict, Optional, Union
from loguru import logger
import asyncio

from persistences.postgresql.modules.posts import posts_table
from persistences.postgresql.modules.votes import votes_table
from persistences.redis.cache import get_cache, set_cache
from persistences.redis.key_format import Keys, make_keys
from module.post import posts_to_database

from aioredis import Redis

from sqlalchemy import (
    text,
    select,
    literal_column,
    insert,
    delete,
    update,
    Table,
    MetaData,
    and_,
    or_,
    func,
)
from sqlalchemy.engine import CursorResult, Connection

from routers.fastapi_dependency.database.sqlalchemy_db import get_db
from routers.fastapi_dependency.validation.pydantic.post import (
    Post_create,
    Post_update,
    Post_response,
)
from routers.fastapi_dependency.validation.auth import oauth2
from routers.fastapi_dependency.database.redis import get_redis


router = APIRouter(prefix="/posts", tags=["Posts"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=List[Post_response],
    response_model_exclude_unset=True,
)
def create_posts(
    posts: List[Post_create],
    background_tasks: BackgroundTasks,
    current_user_data: CursorResult = Depends(oauth2.get_current_user),
    db: Connection = Depends(get_db),
    redis: Redis = Depends(get_redis),
    keys: Keys = Depends(make_keys),
):
    logger.debug(f"create posts")
    logger.debug(current_user_data)
    owner_id = current_user_data[0]

    cache_key = keys.cache_key(owner_id)
    posts_to_database(posts, current_user_data, db, redis, cache_key, owner_id=owner_id)
    # background_tasks.add_task(
    #     posts_to_database, posts, current_user_data, db, redis, keys
    # )
    ## TODO: thinking how to get_cache after set_cache have completed
    response = asyncio.run(get_cache(cache_key, redis))

    logger.debug(f"create_posts response is {response}")

    return response


@router.get("/", response_model=List[Post_response])
def get_posts(
    current_user_data: CursorResult = Depends(oauth2.get_current_user),
    db: Connection = Depends(get_db),
    limit: int = 10,
    skip: int = 0,
    precisely_search: Optional[str] = "",
    ambiguous_search: Optional[str] = None,
    redis: Redis = Depends(get_redis),
):
    logger.debug("get posts")
    logger.debug(current_user_data)
    current_user_id = current_user_data[0]
    logger.debug(current_user_id)

    # if both of following are True trigger ambiguously_search to search all posts content
    if precisely_search == "" and ambiguous_search is None:
        ambiguous_search = ""

    # TODO: split prrecisly_search and ambiguous_search into two separate queries
    # stmt_select_all = (
    #     select(
    #         posts_table
    #     ).limit(limit).offset(skip).where(
    #         posts_table.c.owner_id == current_user_id,
    #             or_(
    #                 posts_table.c.title == precisely_search,
    #                 posts_table.c.title.like(f'%{ambiguous_search}%')
    #             )
    #     )
    # )

    posts = []

    stmt_join = (
        select(posts_table, func.count(votes_table.c.post_id).label("vote"))
        .outerjoin(votes_table, onclause=votes_table.c.post_id == posts_table.c.id)
        .group_by(posts_table.c.id)
        .limit(limit)
        .offset(skip)
        .where(
            posts_table.c.owner_id == current_user_id,
            or_(
                posts_table.c.title == precisely_search,
                posts_table.c.title.like(f"%{ambiguous_search}%"),
            ),
        )
    )

    data_join = db.execute(stmt_join).all()
    # print(data_join)
    for post in data_join:
        posts.append({**post, "owner": current_user_data})

    # data = db.execute(stmt_select_all).all()
    # for post in data:
    #     # data is considered to be nametuple
    #     posts.append(Post_response(**post, owner=current_user_data))

    return posts


@router.get("/{id}", response_model=Post_response)
def get_post(
    id: int,
    current_user_data: CursorResult = Depends(oauth2.get_current_user),
    db: Connection = Depends(get_db),
):
    logger.debug(f"get one post")
    # stmt_1 = text("""SELECT * from posts WHERE id = :s""")
    # p = db.execute(stmt_1, (str(id),)).fetchone()
    current_user_id = current_user_data[0]

    # stmt_select_one = select(posts_table).where(
    #     posts_table.c.owner_id == current_user_id,
    #     posts_table.c.id == id
    #     )

    stmt_select_join_one = (
        select(posts_table, func.count(votes_table.c.post_id).label("vote"))
        .outerjoin(votes_table, onclause=votes_table.c.post_id == posts_table.c.id)
        .group_by(posts_table.c.id)
        .where(posts_table.c.id == id)
    )

    data = db.execute(stmt_select_join_one).first()

    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} not found",
        )

    logger.debug(f"data is {data}")
    response = Post_response(**data, owner=current_user_data)

    return response


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    current_user_data: CursorResult = Depends(oauth2.get_current_user),
    db: Connection = Depends(get_db),
):
    logger.debug(f"delete post")

    stmt = select(posts_table).where(posts_table.c.id == id)
    data = db.execute(stmt).first()
    current_user_id = current_user_data[0]
    # print(p)

    if data == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist",
        )

    if data.owner_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not authorized to delete action",
        )

    del_stmt = delete(posts_table).where(posts_table.c.id == id)
    db.execute(del_stmt)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=Post_response)
def update_post(
    id: int,
    post: Post_update,
    current_user_data: CursorResult = Depends(oauth2.get_current_user),
    db: Connection = Depends(get_db),
):
    logger.debug(f"update post")

    stmt = select(posts_table).where(posts_table.c.id == id)
    data = db.execute(stmt).first()
    if data == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist",
        )

    current_user_id = current_user_data[0]

    if data.owner_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not authorized to update action",
        )

    update_stmt = (
        update(posts_table)
        .where(posts_table.c.id == id)
        .values(title=post.title, content=post.content, published=post.published)
        .returning(posts_table)
    )

    update_data = db.execute(update_stmt).first()
    response = Post_response(**update_data, owner=current_user_data)
    # print(update_data)

    return response
