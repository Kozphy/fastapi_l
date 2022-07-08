import uvicorn
import click
from logger import setup_logging_pre
from pathlib import Path
from configuration.configuration import Configuration

from enums.runmode import RunMode
from pprint import pprint


@click.group()
@click.pass_context
@click.option("--logfile", type=str, default=None)
@click.option("-v", "--verbose", type=int, default=0)
@click.option("--config", type=str, default=None)
def cli(ctx, logfile, verbose, config):
    setup_logging_pre()
    ctx.ensure_object(dict)
    args = {
        "mode": RunMode.UVICORN,
        "logfile": logfile,
        "verbose": verbose,
        "config": config,
    }
    ctx.obj.update(args)


@cli.command()
@click.pass_context
@click.option("--reload", type=bool, default=False)
def active(ctx, reload):
    c = Configuration.from_options(ctx.obj).get_config()["uvicorn"]

    setting = {
        "host": c["host"],
        "port": int(c["port"]),
        "log_level": c["log_level"],
        "workers": c["workers"],
    }

    uvicorn.run("main:app", reload=reload, **setting)
