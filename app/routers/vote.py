from fastapi import HTTPException, Depends, Response, status, APIRouter
from loguru import logger


from persistences.postgresql.modules.votes import votes_table
from persistences.postgresql.modules.posts import posts_table

from sqlalchemy.engine import Connection, CursorResult
from sqlalchemy import select, insert, delete

from routers.dependency.database.sqlalchemy_db import get_db
from routers.dependency.pydantic.vote import Vote
from routers.dependency.security import oauth2

router = APIRouter(prefix="/vote", tags=["Vote"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(
    vote: Vote,
    current_user_data: CursorResult = Depends(oauth2.get_current_user),
    db: Connection = Depends(get_db),
):
    current_user_id = current_user_data[0]

    find_vote_stmt = select(votes_table).where(
        votes_table.c.user_id == current_user_id, votes_table.c.post_id == vote.post_id
    )
    found_vote = db.execute(find_vote_stmt).first()

    if vote.dir == 1:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"You {current_user_id} already voted on post {vote.post_id}",
            )

        # check vote.post_id data whether exists in post table
        check_post_stmt = select(posts_table).where(posts_table.c.id == vote.post_id)
        check_post = db.execute(check_post_stmt).first()
        if not check_post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post {vote.post_id} does not exist",
            )

        # insert vote data
        stmt_insert_vote = insert(votes_table)

        insert_vote_data = {"user_id": current_user_id, **vote.dict()}

        logger.debug(f"insert_vote_data is {insert_vote_data}")

        db.execute(stmt_insert_vote, insert_vote_data)
        return {"message": "successfully vote"}

    if not found_vote:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vote {vote.post_id} does not exist",
        )

    del_vote_stmt = delete(votes_table).where(
        votes_table.c.user_id == current_user_id, votes_table.c.post_id == vote.post_id
    )

    db.execute(del_vote_stmt)

    return {"message": "successfully delete vote"}
