import re
from pathlib import Path
from typing import Union

from poetry_multiproject_plugin.components.project import copying
from poetry_multiproject_plugin.components.toml import read


def get_destination_folder(project_file: Path, temp_path: Union[str, None]) -> Path:
    if temp_path:
        return Path(temp_path)

    grandparent = project_file.parent.parent

    if project_file.parent == grandparent:
        raise ValueError(f"Failed to navigate to the parent of {project_file.parent}")

    return grandparent


def get_destination(
    project_file: Path, prefix: str, temp_path: Union[str, None]
) -> Path:
    folder = get_destination_folder(project_file, temp_path)

    project_name = read.project_name(project_file)
    sibling = f".{prefix}_{project_name}"

    return Path(folder / sibling)


def copy_project(project_file: Path, destination: Path) -> Path:
    source = project_file.parent

    exclude_patterns = read.get_exclude_patterns(project_file)

    res = copying.copy_tree(source, destination, exclude_patterns)

    return Path(res)


def normalize_top_namespace(namespace: Union[str, None]) -> Union[str, None]:
    return re.sub("[^a-zA-Z_/]", "", namespace.strip("/")) if namespace else None
