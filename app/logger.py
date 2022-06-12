from loguru import logger
import sys
from typing import Any, Dict, Optional
# import os
LOGFORMAT = '{time:YYYY-MM-DD HH:mm:ss,SSS} - {name} - {level} - {message}'
# LOGFORMATED = Formatter(LOGFORMAT)

def _set_thirdlib_loggers(verbosity: int = 0, api_verbosity:str = 'info') -> None:
    """
    Set logging level for third party libraries
    :return None
    """
    pass


def setup_logging_pre() -> None:
    """
    Early setup for logging.
    Uses DEBUG loglevel and only the Streamhandler.
    Early messages (before proper logging setup) will therefore only be sent to additional
    logging handlers after the real initialization, because we don't know which
    ones the user desires beforehand.
    """
    logger.remove()
    logger.add(sys.stderr, level='DEBUG')


    
def setup_logging(config: Optional[Dict[str, Any]], mode) -> None:
    """
    Process -v/--verbose, --logfile options
    """
    mode = mode.lower()
    logger.remove()

    logfile = config[mode]["logfile"]
    verbose = config[mode]["verbose"]
    log_level = 'INFO' if verbose < 1 else 'DEBUG'
    logger.add(sys.stderr, level=log_level)

    if logfile:
        logger.add(logfile, level=log_level, format=LOGFORMAT,
         rotation='10MB')

    logger.info(f'{mode} Verbosity set to {verbose}')

