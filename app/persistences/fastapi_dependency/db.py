from persistences.sqlalchemy_engine import init_db_engine
from configuration.api_service_config.config_fastapi import settings
from loguru import logger

# Dependency
def get_engine():
    engine = init_db_engine(settings['persistence'])[0]
    return engine

def get_db():
    engine = get_engine()
    try:
        with engine.begin() as conn:
            yield conn
    except Exception as e:
        logger.error(f'{e}')
        raise
    # finally:
    #     conn.close()
