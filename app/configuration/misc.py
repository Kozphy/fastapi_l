from pathlib import Path, PurePath
from loguru import logger


def check_file_parent_folder(file_path) -> None:
    if not isinstance(file_path, (str, Path)):
        raise Exception(f'{file_path} is not {Path} or {str} object')
    
    parent_folder = Path(file_path).parent
    if isinstance(file_path, str):
        logger.debug(f'{file_path} parent folder is {parent_folder}')

    if not parent_folder.exists():
        raise Exception(f'{parent_folder} folder is not exists')



def create_parent_folder(file_path) -> None:
    parent_folder = file_path.parent

    if not Path(parent_folder).exists():
        logger.info(f"Creating {parent_folder} folder, if {parent_folder} not exists")
        Path(parent_folder).mkdir(parents=True)
    return