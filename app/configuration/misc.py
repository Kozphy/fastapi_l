from pathlib import Path
from loguru import logger


def check_folder(folder) -> None:
    ## if log folder not exists create one

    if not Path(folder).exists():
        logger.info(f"Creating {folder}, which not exists")
        Path(folder).mkdir(parents=True)
    return


