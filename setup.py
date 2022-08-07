from importlib.metadata import entry_points
from xml.etree.ElementInclude import include
from setuptools import find_packages
from skbuild import setup

setup(
    packages=find_packages(
        where="app",
        include={"*"},
    )
    pakcage_dir={"": "app"},
    include_package_data=True,
    entry_points={
        "console_scripts":[
            "api_servies = cmds.api_servies:cli",
            "alembic_cmds = cmds.alembic_cmds:cli",
        ]
    }
)
