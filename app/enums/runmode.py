from enum import Enum

class RunMode(Enum):
    UVICORN='uvicorn'
    API_SERVICE="api_service"
    OTHER="Other"