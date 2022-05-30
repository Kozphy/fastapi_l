from loguru import logger
from .misc import check_file_parent_folder
from logger import setup_logging
from typing import Any, Dict, Optional
from enums.runmode import RunMode
from pathlib import PurePath
import pprint

from attrs import define

@define
class Process_options:
    configured: Dict[str, Any]
    _args: Optional[Dict[str, Any]]
    _yaml: Optional[Dict[str, Any]]

    @classmethod
    def from_args(cls, args: Optional[Dict[str, Any]]):
        return cls(
            configured=None,
            args=args,
            yaml=None,
        )
        
    # logging
    # def _process_logging_options(self):
    #     """
    #     change logger level
    #     """
    #     logger.debug('process logging options')

    # common 
    # def _process_common(self):
    #     logger.debug("process common options")
    #     common = self._yaml['common']

    #     self.configured.update({'common': common})

    # persistence 
    # def _process_persistece_options(self):
    #     logger.debug("process persistence options") 

    # api services
    ##TODO: compare with cmds option
    def _process_api_service_config(self):
        api_service_config = self._yaml['api_service']
        self.configured['api_service'] = {}
        for config in api_service_config:
            if config not in ['persistence', 'logfile']:
                self.configured['api_service'].update({config:api_service_config[config]})

        self._process_api_services_log_options()
        self._process_api_services_persistence_options()


    def _process_api_services_log_options(self) -> None:
        logger.debug("process api services log options")
        from constants import DEFAULT_API_SERVICE_LOG, API_SERVICE_LOG_VERBOSE

        api_service_log_config = {
            'logfile': DEFAULT_API_SERVICE_LOG,
            'verbose': API_SERVICE_LOG_VERBOSE,
        }

        # yaml
        yaml_api_service = self._yaml['api_service']
        if yaml_api_service['logfile'] is not None:
            api_service_log_config['logfile'] = yaml_api_service['logfile']

        # args
        if self._args['logfile'] is not None:
            api_service_log_config['logfile'] = self._args['logfile']

        self.configured['api_service'].update(api_service_log_config)

        api_service_config = self.configured['api_service']

        logger.debug(f"api service logfile in {api_service_config['logfile']}")
        check_file_parent_folder(api_service_config['logfile'])

        # setting logfiles
        setup_logging(self.configured, self._args['mode'].name)




    def _process_api_services_persistence_options(self):
        logger.debug("process api services persistence options")
        yaml_api_service = self._yaml['api_service']

        api_service_persistence = {
            **yaml_api_service['persistence'],
        }

        self.configured['api_service'].update({"persistence":api_service_persistence})