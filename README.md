
# build app
```bash
pip install -e .
```

# before active serivce modifying backup_config.yaml in configuration/backup_config.yaml to config.yaml


# command
```bash
usage: api_services

Options:
--logfile       TEXT
-v, --verbose   INTEGER
--config        TEXT
--reload        bool

# Common options for all
--help
```

# command for Alembic database migration 
```bash
usage: alembic_cmds

positional arguments:
current 
downgrade
revision
upgrade

# Common options for all
--help

# Options for alembic_cmds:
--logfile TEXT
-v, --verbose INTEGER
--config TEXT

# Common Options current for current, downgrade
--revision TEXT
--sql BOOLEAN
--tag BOOLEAN

# Options for upgrade
--force BOOLEAN

# Options for revision
-m, --message TEXT
--autogenerate BOOLEAN
```
