from sqlalchemy import Column, Table, MetaData, Boolean, BigInteger, String, Identity
from sqlalchemy.sql.expression import false, true

account_status_meta = MetaData()

account_status_table = Table(
    "account_status",
    account_status_meta,
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
