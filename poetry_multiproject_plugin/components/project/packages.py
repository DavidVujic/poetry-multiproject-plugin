from pathlib import Path
from typing import Union

from poetry_multiproject_plugin.components.toml import read
from poetry_multiproject_plugin.components.toml.packages import packages_to_paths
from poetry_multiproject_plugin.components.project import copying


def is_relative_path(path: str) -> bool:
    return str(path).startswith("..")


def copy_packages(
    project_file: Path, destination: Path, top_ns: Union[str, None] = None
) -> None:
    content = read.toml(project_file)
    package_paths = packages_to_paths(content)
    exclude_patterns = read.parse_exclude_patterns(content)

    relative_package_paths = [p for p in package_paths if is_relative_path(p["from"])]

    for p in relative_package_paths:
        p_from = p["from"]
        p_to = p["to"]
        source = Path(project_file.parent / p_from)

        to = f"{top_ns}/{p_to}" if top_ns else p_to

        to_path = Path(destination / to)

        copying.copy_tree(source, to_path, exclude_patterns)
