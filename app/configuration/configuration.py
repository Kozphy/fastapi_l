from loguru import logger
from pathlib import Path
from typing import Any, Dict, Optional
from configuration.process_options import Process_options
from configuration.load_config import Load_config
from enums.runmode import RunMode

from attrs import define

@define
class Configuration:
    """
    Class to read and init configuration
    Reuse this class for the app, every script that required configuration
    """
    process: Process_options

    @classmethod
    def from_options(cls, args: Optional[Dict[str, Any]]=None):
        return cls(
            process = Process_options.from_args(args),
        )

    def get_config(self) -> Dict[str, Any]:
        """
        Return the config. Use this method to get the bot config
        :return: Dict: configuration
        """
        logger.debug("Checking configured whether exist")
        if self.process.configured is None:
            self.load_config()

        return self.process.configured
    
        
    def load_config(self) -> Dict[str, Any]:
        """
        Extract information from sys.argv and load the all services configuration
        """    
            
        load = Load_config()
        # load api service config
        api_service_destination = load.determine_api_service_config(self.process._args)
        self.process._yaml = load.load_yaml_setting(api_service_destination)
        self._merge_args_yaml() 

    def _merge_args_yaml(self):
        """
        The command permission is args > .env > config
        While cmd permission bigger than another one, override smaller one.
        """

        logger.debug('merge config and yaml')
        self.process.configured = {}
        if (self.process._args['mode'] == RunMode.API_SERVICE or 
         self.process._args['mode'] == RunMode.UVICORN):
            self.process._process_api_service_config()
        # self.process._process_logging_options()
        # self.process._process_common()
        # self.process._process_persistece_options()
        

        
