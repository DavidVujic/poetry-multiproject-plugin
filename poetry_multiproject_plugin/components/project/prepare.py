import shutil
from pathlib import Path
from typing import cast

from poetry_multiproject_plugin.components.toml import read


def get_project_name(project_file: Path) -> str:
    content = cast(dict, read.toml(project_file))

    return content["tool"]["poetry"]["name"]


def get_destination(project_file: Path, prefix: str) -> Path:
    grandparent = project_file.parent.parent

    if project_file.parent == grandparent:
        raise ValueError(f"Failed to navigate to the parent of {project_file.parent}")

    project_name = get_project_name(project_file)
    sibling = f".{prefix}_{project_name}"

    return Path(grandparent / sibling)


def copy_project(project_file: Path, destination: Path) -> Path:
    source = project_file.parent.as_posix()

    res = shutil.copytree(
        source,
        destination,
        ignore=shutil.ignore_patterns("*.pyc", "__pycache__", ".venv", ".mypy_cache"),
        dirs_exist_ok=True,
    )

    return Path(res)
