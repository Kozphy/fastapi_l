from persistences.redis.connection import Redis
from configuration.api_service_config.config_fastapi import settings

# def init_pool():
#     nosql = settings["nosql"]
#     if nosql.get("password", None) is not None:
#         pool = ConnectionPool(
#             host=nosql["host"],
#             port=nosql["port"],
#             password=nosql["password"],
#             ssl=nosql["ssl"],
#             ssl_ca_certs=["ssl_ca_certs"],
#             decode_responses=True,
#             health_check_interval=1,
#         )
#         return pool

#     pool = ConnectionPool(
#         host=nosql["host"],
#         port=nosql["port"],
#         ssl=nosql["ssl"],
#         ssl_ca_certs=["ssl_ca_certs"],
#         decode_responses=True,
#         health_check_interval=1,
#     )
#     return pool


def get_redis():
    redis = Redis.from_config(settings["nosql"]).connect_redis()
    return redis
