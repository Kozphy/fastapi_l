from pathlib import Path
from loguru import logger


def check_file_parent_folder(file_path) -> None:
    ## if log folder not exists create one
    parent_folder = file_path.parent

    if not Path(parent_folder).exists():
        logger.info(f"Creating {parent_folder} folder, if not exists")
        Path(parent_folder).mkdir(parents=True)
    return


