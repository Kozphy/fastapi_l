import uvicorn
import click
from logger import setup_logging_pre
from pathlib import Path
from configuration.configuration import Configuration
from enums.runmode import RunMode
# from constants import (DEFAULT_API_SERVICE_LOG,
# DEFAULT_CONFIG_SERVICE)
from pprint import pprint


@click.group()
@click.pass_context
@click.option('--logfile', type=str, default=None)
@click.option('-v','--verbosity', type=int, default=0)
@click.option('--config', type=str, default=None)
def cli(ctx, logfile, verbosity, config):
    setup_logging_pre()
    ctx.ensure_object(dict)
    args = {
        'mode': RunMode.API_SERVICE,
        'logfile': logfile,
        'verbosity': verbosity,
        'config': config,
    }
    ctx.obj.update(args)


@cli.command()
@click.pass_context
@click.option('--reload', type=bool, default=True)
def active(ctx, reload):
    c = Configuration.from_options(ctx.obj).get_config()
    c = c['api_service']
    # pprint(c)
    # exit() 
    

    
    uvicorn.run('main:app', reload=reload, host=c['host'],
     port=c['port'], log_level=c['log_level'])