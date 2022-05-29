# TODO: change to match api env
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CSafeLoader as CSLoader, CDumper as Dumper
except:
    from yaml import Loader, Dumper

from pathlib import Path
from loguru import logger
from typing import Any, Dict, Optional
from exceptions import OperationalException
from .misc import check_folder

class Load_config():
    def determine_destination(self, args):
        logger.debug('determine where is user_data_dir')
        from constants import (CONFIG, BOT_DIR, DEFAULT_USERDATA_DIR, 
        DEFAULT_CONFIG_NAME, DEFAULT_CONFIG_DIR_NAME)
        # use default
        user_dir = DEFAULT_USERDATA_DIR 
        config_dir_name = DEFAULT_CONFIG_DIR_NAME
        config_name = DEFAULT_CONFIG_NAME

        
        if args['user_data_dir'] != DEFAULT_USERDATA_DIR:
            # user_data_dir use args
            user_dir = f"{BOT_DIR}/{args['user_data_dir']}"
            check_folder(f"{user_dir}/{config_dir_name}")

        if args['config'] != CONFIG:
            # config use args
            config_name = args['config']

        destination = f"{user_dir}/{config_dir_name}/{config_name}"
        return destination


    def load_yaml_setting(self, destination) -> Dict[str, Any]:
        
        logger.debug('parse yaml file')
        try:
            with open(destination, 'r') as f:
                yaml = CSLoader(stream=f).get_data()
            return yaml
        except FileNotFoundError as e:
            logger.error(e)
            raise OperationalException(f"file {destination} not found")



