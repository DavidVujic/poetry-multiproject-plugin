import shutil
from pathlib import Path


PREPARE_FOR_DIST = ".prepare_for_dist"


def get_destination(project_file: Path) -> Path:
    return Path(project_file.parent / PREPARE_FOR_DIST)


def copy_project(project_file: Path) -> None:
    source = project_file.parent.as_posix()
    destination = get_destination(project_file).as_posix()

    shutil.copytree(source, destination)
