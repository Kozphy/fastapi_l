from datetime import datetime
from attrs import define
from typing import Any


def serialize_dates(v):
    return v.isoformat() if isinstance(v, datetime) else v


@define
class Node:
    dataval: Any
