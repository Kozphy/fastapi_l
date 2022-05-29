# TODO: change to match api env
from loguru import logger
from pathlib import Path
from typing import Any, Dict, Optional
from configuration.process_options import Process_options
from configuration.load_config import Load_config

from attrs import define

@define
class Configuration:
    """
    Class to read and init bot configuration
    Reuse this class for the bot, every script that required configuration
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
        :return: Dict: Bot config
        """
        logger.debug("Checking configured whether exist")
        if len(self.process.configured) == 0:
            self.load_config()

        return self.process.configured
    
        
    def load_config(self) -> Dict[str, Any]:

        """
        Extract information from sys.argv and load the bot configuration
        :return: Configuration dictionary
        """    
            
        # Load all configs
        load = Load_config()

        destination = load.determine_destination(self.process._args)
        self.process._yaml = load.load_yaml_setting(destination)
        self._merge_args_yaml() 

    def _merge_args_yaml(self):
        """
        The command permission is args > .env > config
        While cmd permission biggger than another one, override smaller one.
        """

        logger.debug('merge config and yaml')

        # exit()
        self.process._process_logging_options()
        self.process._process_common()
        self.process._process_persistece_options()
        

        
