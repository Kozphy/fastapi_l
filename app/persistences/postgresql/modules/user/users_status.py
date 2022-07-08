from sqlalchemy import Column, Table, MetaData, Boolean, BigInteger, String, Identity
from sqlalchemy.sql.expression import false, true

users_status_meta = MetaData()

users_status_table = Table(
    "users_status",
    users_status_meta,
    Column(
        "id",
        BigInteger,
        Identity(),
        primary_key=True,
        autoincrement=True,
        nullable=False,
    ),
    Column("activate", Boolean, server_default=false(), nullable=False),
    Column("forbidden", Boolean, server_default=false(), nullable=False),
)
