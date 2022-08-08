from setuptools import find_packages
from skbuild import setup

setup(
    packages=find_packages(
        where="app",
        include={"*"},
    ),
    package_dir={"": "app"},
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "api_servies = cmds.api_servies:cli",
            "alembic_cmds = cmds.alembic_cmds:cli",
        ]
    },
)
