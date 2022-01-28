from pathlib import Path

from poetry.core.poetry import Poetry
from poetry.factory import Factory
from poetry_multiproject_plugin.repo import repo


def create_modified_poetry(poetry: Poetry, toml: str) -> Poetry:
    cwd = Path.cwd()
    path = Path(toml).absolute()

    modified = Factory().create_poetry(path.parent)

    modified.file.parent = repo.find_workspace_root(cwd) or modified.file.parent

    return modified
