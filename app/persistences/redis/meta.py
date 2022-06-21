from redis_om import get_redis_connection
from configuration.api_service_config.config_fastapi import settings

nosql = settings["nosql"]

redis = get_redis_connection(
    host=nosql["host"],
    port=nosql["port"],
    password=nosql["password"],
    decode_responses=True,
)
