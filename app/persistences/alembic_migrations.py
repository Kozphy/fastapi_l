# alembic
from loguru import logger
from constants import ALEMBIC_CONFIG_FILE
from alembic.config import Config
from alembic import command, script
from alembic.runtime import migration

from persistences.sqlalchemy_engine import init_db_engine
# from sqlalchemy import engine
from sqlalchemy_utils.functions import create_database, database_exists

cfg = Config(ALEMBIC_CONFIG_FILE)

def migration_upgrade(configured, revision, sql, tag):
    engine, url, db_name = init_db_engine(configured, echo=True, future=True)

    with engine.begin() as connection:
        cfg.attributes['connection'] = connection
        if database_exists(url) == False:
            logger.info(f'{db_name} database not exists, create it')
            create_database(url)
            command.upgrade(cfg, revision, sql, tag)
    
        # check revision whether is head
        if check_current_head(cfg, engine) == False:
            logger.info(f'upgrade {db_name} database schema')
            command.upgrade(cfg, revision, sql, tag)
    
    # command.history(alem_config, verbose=True)

def migration_downgrade(configured, revision, sql, tag):
    engine, _, db_name = init_db_engine(configured, echo=True, future=True)

    with engine.begin() as connection:
        cfg.attributes['connection'] = connection
        logger.info(f'downgrade {db_name} database schema')
        command.downgrade(cfg, revision, sql, tag)

def migration_autogenerate(configured, message, **kwargs):
    engine, _, db_name = init_db_engine(configured, echo=True, future=True)
    with engine.begin() as connection:
        cfg.attributes['connection'] = connection
        logger.info(f'autogenerate {db_name} database schema')
        command.revision(cfg, autogenerate=True, message=message, **kwargs)



# def migration_show_history(configured, rev_range='base:current', verbose='True'):
#     alem_config, _ = setting_alembic_cfg(configured)
#     command.history(alem_config, verbose=verbose)

# def migration_revision(configured, message='', autogenerate='True'):
#     alem_config, _ = setting_alembic_cfg(configured)
#     command.revision(alem_config, message=message, autogenerate=autogenerate)

def check_current_head(alembic_cfg, connectable):
    # type: (Config, engine.Engine) -> bool
    directory = script.ScriptDirectory.from_config(alembic_cfg)
    with connectable.begin() as connection:
        context = migration.MigrationContext.configure(connection)
        return set(context.get_current_heads()) == set(directory.get_heads())