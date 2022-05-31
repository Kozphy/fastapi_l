from pydantic import BaseSettings
from configuration.configuration import Configuration
from typing import Dict, Any 
from enums.runmode import RunMode

class Settings(BaseSettings):
    api_service_config: Dict[str, Any]

    @classmethod
    def from_config(cls):
        api_service_config = Configuration.from_options({'mode': RunMode.API_SERVICE}).get_config()
        return cls(
            api_service_config=api_service_config
        )
        