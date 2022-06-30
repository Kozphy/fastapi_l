from datetime import datetime


def serialize_dates(v):
    return v.isoformat() if isinstance(v, datetime) else v
