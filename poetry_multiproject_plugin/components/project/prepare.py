import shutil
from pathlib import Path

from poetry_multiproject_plugin.components.toml import read

PREPARE_FOR_DIST = ".prepare_for_dist"


def get_project_name(project_file: Path) -> str:
    content = read.toml(project_file)

    return content["tool"]["poetry"]["name"]


def get_destination(project_file: Path) -> Path:
    grandparent = project_file.parent.parent

    if project_file.parent == grandparent:
        raise ValueError(f"Failed to navigate to the parent of {project_file.parent}")

    project_name = get_project_name(project_file)
    sibling = f"{PREPARE_FOR_DIST}_{project_name}"

    return Path(grandparent / sibling)


def copy_project(project_file: Path) -> Path:
    source = project_file.parent.as_posix()
    destination = get_destination(project_file).as_posix()

    res = shutil.copytree(source, destination)

    return Path(res)
