import shutil
from pathlib import Path
from typing import Union

from poetry_multiproject_plugin.components.toml import read
from poetry_multiproject_plugin.components.toml.packages import packages_to_paths


def copy_packages(project_file: Path, destination: Path, top_ns: Union[str, None] = None):
    content = read.toml(project_file)
    package_paths = packages_to_paths(content)

    for p in package_paths:
        source = Path(project_file.parent / p["from"])

        top_ns_path = f"{top_ns}/" if top_ns else ""
        to = Path(destination / top_ns_path / p["to"])

        shutil.copytree(
            source,
            to,
            ignore=shutil.ignore_patterns("__pycache__", ".mypy_cache"),
            dirs_exist_ok=True,
        )
