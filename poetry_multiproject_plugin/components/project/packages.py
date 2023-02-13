import shutil
from pathlib import Path
from typing import Union

from poetry_multiproject_plugin.components.toml import read
from poetry_multiproject_plugin.components.toml.packages import packages_to_paths


def copy_packages(
    project_file: Path, destination: Path, top_ns: Union[str, None] = None
) -> None:
    content = read.toml(project_file)
    package_paths = packages_to_paths(content)

    for p in package_paths:
        p_from = p["from"]
        p_to = p["to"]
        source = Path(project_file.parent / p_from)

        is_relative_path = str(p_from).startswith("..")

        to = f"{top_ns}/{p_to}" if top_ns and is_relative_path else p_to

        to = Path(destination / to)

        shutil.copytree(
            source,
            to,
            ignore=shutil.ignore_patterns("__pycache__", ".mypy_cache"),
            dirs_exist_ok=True,
        )
