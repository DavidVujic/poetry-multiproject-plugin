import shutil
from pathlib import Path

from poetry_multiproject_plugin.components.project import prepare
from poetry_multiproject_plugin.components.toml import read
from poetry_multiproject_plugin.components.toml.packages import packages_to_paths


def copy_packages(project_file: Path):
    content = read.toml(project_file)
    package_paths = packages_to_paths(content)

    destination = prepare.get_destination(project_file)

    for p in package_paths:
        source = Path(project_file.parent / p["from"])
        to = Path(destination / p["to"])

        shutil.copytree(
            source,
            to,
            ignore=shutil.ignore_patterns("__pycache__", ".mypy_cache"),
            dirs_exist_ok=True,
        )
