from routers.fastapi_dependency.validation.pydantic.post import (
    Post_create,
    Post_update,
    Post_response,
)

from typing import List, Union, Any
from loguru import logger

from persistences.postgresql.modules.posts import posts_table


from aioredis import Redis

from sqlalchemy.engine import Connection
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

from module.misc import serialize_dates


def posts_to_database(
    posts: List[Post_create],
    current_user_data: dict,
    sqldb: Connection,
    *args,
    **kwargs,
):
    logger.debug("posts to database")
    new_posts = []
    for data in posts:
        data = data.dict()
        data["owner_id"] = kwargs["owner_id"]
        new_posts.append(data)

    logger.debug(f"new_posts is {new_posts}")
    stmt_insert_res_cols = []
    for col in posts_table.c:
        if col not in [posts_table.c.owner_id]:
            stmt_insert_res_cols.append(col)

    stmt_insert_posts = insert(posts_table).returning(*stmt_insert_res_cols)
    all_posts = sqldb.execute(stmt_insert_posts, new_posts).all()

    all_posts: list[dict[str, Any]] = [data._asdict() for data in all_posts]

    logger.debug(f"all_posts is {all_posts}")

    cache_data = []
    current_user_data = {k: serialize_dates(v) for k, v in current_user_data.items()}
    for data in all_posts:
        data.update({k: serialize_dates(v) for k, v in data.items()})
        # data is considered to be nametuple
        cache_data.append({**data, "owner": current_user_data})

    return cache_data
