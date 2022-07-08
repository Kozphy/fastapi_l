import click
from loguru import logger
from logger import setup_logging_pre

from configuration.configuration import Configuration
from enums.runmode import RunMode
from persistences.alembic_migrations import (
    migration_autogenerate,
    migration_current,
    migration_downgrade,
    migration_upgrade,
)
from persistences.sqlalchemy_engine import init_db_engine


@click.group()
@click.pass_context
@click.option("--logfile", type=str, default=None)
@click.option("-v", "--verbose", type=int, default=1)
@click.option("--config", type=str, default=None)
def cli(ctx, logfile, verbose, config):
    setup_logging_pre()
    ctx.ensure_object(dict)

    args = {
        "mode": RunMode.API_SERVICE,
        "logfile": logfile,
        "verbose": verbose,
        "config": config,
    }

    configured = Configuration.from_options(args).get_config()["api_service"][
        "persistence"
    ]

    engine, url, db_name = init_db_engine(configured, echo=True, future=True)

    context = {"engine": engine, "url": url, "db_name": db_name}
    logger.debug(f"configured is {context}")

    ctx.obj.update(context)


@cli.command()
@click.pass_context
def current(ctx):
    logger.info("show migration version")
    migration_current(**ctx.obj)


@cli.command()
@click.pass_context
@click.option("-m", "--message", type=str, default="test")
def autogenerate(ctx, message):
    migration_autogenerate(**ctx.obj, message=message)


@cli.command()
@click.pass_context
@click.option("--revision", type=str, default="head")
@click.option("--sql", type=bool, default=False)
@click.option("--tag", type=bool, default=None)
def upgrade(ctx, revision, sql, tag):
    migration_upgrade(**ctx.obj, revision=revision, sql=sql, tag=tag)


@cli.command()
@click.pass_context
@click.option("--revision", type=str, default="base")
@click.option("--sql", type=bool, default=False)
@click.option("--tag", type=bool, default=None)
def downgrade(ctx, revision, sql, tag):
    migration_downgrade(**ctx.obj, revision=revision, sql=sql, tag=tag)
