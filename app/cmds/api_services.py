import uvicorn
import click
from logger import setup_logging_pre
from pathlib import Path
from configuration.configuration import Configuration
from persistences.alembic_migrations import (migration_autogenerate, migration_downgrade,
migration_upgrade)
from enums.runmode import RunMode
from pprint import pprint


@click.group()
@click.pass_context
@click.option('--logfile', type=str, default=None)
@click.option('-v','--verbose', type=int, default=0)
@click.option('--config', type=str, default=None)
def cli(ctx, logfile, verbose, config):
    setup_logging_pre()
    ctx.ensure_object(dict)
    args = {
        'mode': RunMode.UVICORN,
        'logfile': logfile,
        'verbose': verbose,
        'config': config,
    }
    ctx.obj.update(args)



@cli.command()
@click.pass_context
@click.option('--reload', type=bool, default=True)
def active(ctx, reload):
    c = Configuration.from_options(ctx.obj).get_config()['uvicorn']

    setting = {
        'host': c['host'],
        'port': int(c['port']),
        'log_level': c['log_level'],
    }


    uvicorn.run('main:app', reload=reload, **setting)

@cli.command()
@click.option('-m', '--message', type=str, default='test')
def alembic_autogenerate(message):
    args = {
        'mode': RunMode.API_SERVICE,
    }
    c = Configuration.from_options(args).get_config()['api_service']['persistence']

    migration_autogenerate(c, message)
    

@cli.command()
@click.option('--revision', type=str, default='head')
@click.option('--sql', type=bool, default=False)
@click.option('--tag', type=bool, default=None)
def alembic_upgrade(revision, sql, tag):
    args = {
        'mode': RunMode.API_SERVICE,
    }
    c = Configuration.from_options(args).get_config()['api_service']['persistence']

    migration_upgrade(c, revision, sql, tag)

@cli.command()
@click.option('--revision', type=str, default='base')
@click.option('--sql', type=bool, default=False)
@click.option('--tag', type=bool, default=None)
def alembic_downgrade(revision, sql, tag):
    args = {
        'mode': RunMode.API_SERVICE,
    }
    c = Configuration.from_options(args).get_config()['api_service']['persistence']

    migration_downgrade(c, revision, sql, tag)