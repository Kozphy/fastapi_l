import uvicorn
import click
from pathlib import Path


# exit()
@click.group()
def cli():
    pass

@cli.command()
@click.option('--reload', type=bool, default=True)
def active(reload):
    uvicorn.run('main:app', reload=reload)