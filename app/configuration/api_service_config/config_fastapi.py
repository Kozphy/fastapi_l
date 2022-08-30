from pydantic import BaseSettings
from configuration.configuration import Configuration
from typing import Dict, Any
from enums.runmode import RunMode

from functools import lru_cache

# TODO: fix deployment to heroku env setting error
class Settings(BaseSettings):
    api_service_config: Dict[str, Any]

    @classmethod
    def from_config(cls):
        api_service_config = Configuration.from_options(
            {"mode": RunMode.API_SERVICE}
        ).get_config()
        return cls(api_service_config=api_service_config)


@lru_cache()
def get_settings():
    return Settings.from_config().api_service_config["api_service"]


settings: Dict[str, Any] = get_settings()
