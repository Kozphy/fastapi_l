from pathlib import Path

ROOT_SERVICE_NAME = "app"
ROOT_DIR = Path.cwd() / ROOT_SERVICE_NAME

# config
ROOT_CONFIG_DIR_NAME = "configuration"
DEFAULT_ROOT_CONFIG_DIR = Path(ROOT_DIR, ROOT_CONFIG_DIR_NAME)
## service config
ROOT_CONFIG_API_SERVICE_DIR_NAME = "api_service_config"
CONFIG_NAME = "config.yaml"
DEFAULT_ROOT_CONFIG_API_SERVICE_DIR = Path(
    DEFAULT_ROOT_CONFIG_DIR, ROOT_CONFIG_API_SERVICE_DIR_NAME
)
DEFAULT_CONFIG_API_SERVICE = Path(DEFAULT_ROOT_CONFIG_API_SERVICE_DIR, CONFIG_NAME)

# log
ROOT_LOG_DIR_NAME = "log"
ROOT_LOG_NAME = "app.txt"
DEFAULT_ROOT_LOG_DIR = Path(ROOT_DIR, ROOT_LOG_DIR_NAME)
DEFAULT_ROOT_LOG = Path(DEFAULT_ROOT_LOG_DIR, ROOT_LOG_NAME)

## service log
ROOT_API_SERVICE_LOG_DIR_NAME = "api_service_log"
API_SERVICE_LOG_NAME = "api_service_log.txt"
API_SERVICE_LOG_VERBOSE = 0
DEFAULT_API_SERIVCE_LOG_DIR = Path(DEFAULT_ROOT_LOG_DIR, ROOT_API_SERVICE_LOG_DIR_NAME)
DEFAULT_API_SERVICE_LOG = Path(DEFAULT_API_SERIVCE_LOG_DIR, API_SERVICE_LOG_NAME)

# alembic
ALEMBIC_INI_NAME = "alembic.ini"
ALEMBIC_CONFIG_FILE = f"{ROOT_DIR}/{ALEMBIC_INI_NAME}"

# database
ROOT_PERSISTENCE_DIR_NAME = "persistences"
# DEFAULT_DB_USER = 'root'
# DEFAULT_DB_HOST = 'localhost'
# DEFAULT_DB_DIR_NAME = 'db'
# DEFAULT_DB_NAME = 'test'
# DEFAULT_DB_PORT = 8080

# redis
DEFAULT_KEY_PREFIX = "fastapi-demo"
CACHE_TIME = 120

# robot test framework
ROOT_TEST_DIR_NAME = "robot_test"
ROOT_TEST_DIR = Path(ROOT_DIR, ROOT_TEST_DIR_NAME)
SUT_NAME = "sut"
SUT_PATH = Path(ROOT_TEST_DIR, SUT_NAME)
