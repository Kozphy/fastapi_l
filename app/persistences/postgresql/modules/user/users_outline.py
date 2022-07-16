from sqlalchemy import (
    Column,
    ForeignKey,
    Table,
    MetaData,
    BigInteger,
    Identity,
)
from sqlalchemy.types import VARCHAR, TEXT
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text, null

users_table_meta = MetaData()

# TODO: Fix Phone number and id_card must be unique
# TODO: Fix id auto increment need to be correct order when insert failing.
# TODO: accout support multiple type to login
users_table = Table(
    "users",
    users_table_meta,
    Column(
        "id",
        BigInteger,
        Identity(),
        primary_key=True,
        autoincrement=True,
        nullable=False,
    ),
    # Column(
    #     "user_register_id",
    #     ForeignKey("users_register.user_id", onupdate="CASCADE", ondelete="CASCADE"),
    #     nullable=False,
    # ),
    # Column("account", VARCHAR(50), nullable=False, unique=True),
    # Column(
    #     "user_email_id",
    #     ForeignKey("users_email.id", ondelete="CASCADE"),
    #     nullable=False,
    # ),
    # Column(
    #     "user_phone_id",
    #     ForeignKey("users_phone.id", ondelete="CASCADE"),
    #     nullable=False,
    # ),
    Column("password", VARCHAR(100), nullable=False),
    Column("surname", VARCHAR(30), server_default="", nullable=False),
    Column("given_name", VARCHAR(50), server_default="", nullable=False),
    Column("description", TEXT()),
    Column(
        "user_status_id",
        BigInteger,
        ForeignKey("users_status.id", onupdate="CASCADE", ondelete="CASCADE"),
        server_default="0",
        nullable=False,
    ),
    Column(
        "created_at",
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
    ),
    Column(
        "last_update",
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
    ),
    Column("forbidden_at", TIMESTAMP(timezone=True), server_default=null()),
)
