# alembic
from loguru import logger
from constants import ALEMBIC_CONFIG_FILE
from alembic.config import Config
from alembic import command, script
from alembic.runtime import migration

from persistences.sqlalchemy_engine import init_db_engine
# from sqlalchemy import engine
from sqlalchemy_utils.functions import create_database, database_exists
# from main import api_service_config

cfg = Config(ALEMBIC_CONFIG_FILE)

# def setting_alembic_cfg(configured):
#     logger.debug("Setting alembic context env")
#     db_para = {}
#     for (key, value) in configured['persistence'].items():
#         if key not in ['ORM', 'path']:
#             db_para.update({key: value})


#     url = init_db_url(**db_para)
#     alembic_cfg = Config(ALEMBIC_CONFIG_FILE)
#     alembic_cfg.set_main_option("script_location", "./src/alembic_scripts")
#     alembic_cfg.set_main_option("sqlalchemy.url", url)
#     logger.debug(f"db url is {url}")
#     return alembic_cfg, url, configured['persistence']['db_name']



def migration_upgrade(configured, revision='head', sql=None, tag=None):
    # TODO: fix Can't load plugin: sqlalchemy.dialects:postgresql.psycopg issue
    engine, url, db_name = init_db_engine(configured, echo=True, future=True)
    exit()
    with engine.begin() as connection:
        cfg.attributes['connection'] = connection
        command.upgrade(cfg, revision, sql=sql, tag=tag)
    # if database_exists(url) == False:
    #     logger.debug(f'{db_name} database not exists, create it')
    #     create_database(url)
    #     command.upgrade(alem_config, revision, sql, tag)
    # # check revirsion whether is head
    # if check_current_head(alem_config, engine.create_engine(url)) == False:
    #     logger.debug(f'upgrade {db_name} database schema')
    #     command.upgrade(alem_config, revision, sql, tag)
    
    # command.history(alem_config, verbose=True)

# TODO: implement alembic downgrade in cmd with bot config
# def migration_downgrade(configured, revision='base'):
#     alem_config, _, db_name = setting_alembic_cfg(configured)
#     logger.debug(f'downgrade {db_name} database schema')
#     command.downgrade(alem_config, revision)
    
# def migration_show_history(configured, rev_range='base:current', verbose='True'):
#     alem_config, _ = setting_alembic_cfg(configured)
#     command.history(alem_config, verbose=verbose)

# def migration_revision(configured, message='', autogenerate='True'):
#     alem_config, _ = setting_alembic_cfg(configured)
#     command.revision(alem_config, message=message, autogenerate=autogenerate)

# def check_current_head(alembic_cfg, connectable):
#     # type: (Config, engine.Engine) -> bool
#     directory = script.ScriptDirectory.from_config(alembic_cfg)
#     with connectable.begin() as connection:
#         context = migration.MigrationContext.configure(connection)
#         return set(context.get_current_heads()) == set(directory.get_heads())