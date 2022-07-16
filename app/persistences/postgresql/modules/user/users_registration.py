from sqlalchemy import (
    Column,
    ForeignKey,
    Table,
    MetaData,
    BigInteger,
    Identity,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.types import VARCHAR
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from persistences.postgresql.modules.user.users_outline import (
    users_table_meta,
)
from enums.register import Register

register_enum = ENUM(Register, name="register_enum", metadata=users_table_meta)

users_register_table = Table(
    "users_register",
    users_table_meta,
    Column(
        "id",
        BigInteger,
        Identity(),
        primary_key=True,
        autoincrement=True,
        nullable=False,
    ),
    Column(
        "user_id",
        ForeignKey("users.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    ),
    Column(
        "registration",
        VARCHAR(255),
        nullable=False,
    ),
    Column("registration_type", register_enum, nullable=False),
    Column(
        "create_at",
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
    UniqueConstraint("user_id", "registration_type"),
)
