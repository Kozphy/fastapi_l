from sqlalchemy import Column, Table, MetaData, Boolean, BigInteger, String, Identity
from sqlalchemy.sql.schema import ForeignKey

from persistences.postgresql.modules.user.users_in_formosa import users_in_formosa_table
from persistences.postgresql.modules.posts import posts_table

votes_meta = MetaData()

votes_table = Table(
    "votes",
    votes_meta,
    Column(
        "user_id",
        BigInteger,
        ForeignKey(users_in_formosa_table.c.id, ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    ),
    Column(
        "post_id",
        BigInteger,
        ForeignKey(posts_table.c.id, ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    ),
)
