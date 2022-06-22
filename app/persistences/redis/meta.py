from redis_om import get_redis_connection
from configuration.api_service_config.config_fastapi import settings

nosql = settings["nosql"]

if nosql.get("password", None) is not None:
    redis = get_redis_connection(
        host=nosql["host"],
        port=nosql["port"],
        password=nosql["password"],
        decode_responses=True,
    )
else:
    redis = get_redis_connection(
        host=nosql["host"],
        port=nosql["port"],
        decode_responses=True,
    )
