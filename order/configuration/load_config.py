from yaml import load, dump
try:
    from yaml import CLoader as Loader, CSafeLoader as CSLoader, CDumper as Dumper
except:
    from yaml import Loader, Dumper

# from pathlib import Path
from loguru import logger
from typing import Any, Dict, Optional
# from .misc import check_folder

class Load_config():
    ## TODO: compare wtih cli option
    # def determine_config_destination(self, args=None):
    #     logger.debug('determine where is config file')

    #     self.process_api_service_config()

        # use default
        # config_dir_name = DEFAULT_CONFIG_DIR_NAME
        # config_name = DEFAULT_CONFIG_NAME

        
        # if args['user_data_dir'] != DEFAULT_USERDATA_DIR:
        #     # user_data_dir use args
        #     user_dir = f"{BOT_DIR}/{args['user_data_dir']}"
        #     check_folder(f"{user_dir}/{config_dir_name}")

        # if args['config'] != CONFIG:
        #     # config use args
        #     config_name = args['config']

        # destination = f"{DEFAULT_CONFIG_API_SERVICE}"
        # return destination

    def determine_api_service_config(self, args=None):
        logger.debug('determine where is config file')
        from constants import (DEFAULT_CONFIG_API_SERVICE)
        return DEFAULT_CONFIG_API_SERVICE

    def load_yaml_setting(self, destination) -> Dict[str, Any]:
        
        logger.debug('parse yaml file')
        try:
            with open(destination, 'r') as f:
                yaml = CSLoader(stream=f).get_data()
            return yaml
        except FileNotFoundError as e:
            logger.error(e)
            raise Exception(f"file {destination} not found")



