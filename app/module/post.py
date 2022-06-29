from routers.fastapi_dependency.validation.pydantic.post import (
    Post_create,
    Post_update,
    Post_response,
)

from typing import List, Union
from loguru import logger

from persistences.postgresql.modules.posts import posts_table
from persistences.redis.cache import get_cache, set_cache


from aioredis import Redis

from sqlalchemy.engine import CursorResult, Connection
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
import asyncio


def posts_to_database(
    posts: List[Post_create],
    current_user_data: CursorResult,
    sqldb: Connection,
    nosqldb: Union[Redis, None],
    key: str,
    *args,
    **kwargs,
):
    new_posts = []
    for data in posts:
        data = data.dict()
        data["owner_id"] = kwargs["owner_id"]
        new_posts.append(data)

    # logger.debug(f"new_posts is {new_posts}")
    stmt_insert_res_cols = []
    for col in posts_table.c:
        if col not in [posts_table.c.owner_id]:
            stmt_insert_res_cols.append(col)

    stmt_insert_posts = insert(posts_table).returning(*stmt_insert_res_cols)
    all_posts = sqldb.execute(stmt_insert_posts, new_posts).all()
    sqldb.commit()

    # logger.debug(f"all_posts is {all_posts}")
    response = []
    for data in all_posts:
        # data is considered to be nametuple
        response.append(Post_response(**data, owner=current_user_data))

    logger.debug(f"posts_to_database response is {response}")
    ## TODO: fix  Object of type Post_response is not JSON serializable
    asyncio.run(set_cache(response, key, nosqldb))

    logger.debug(f"cache key is {key}")
