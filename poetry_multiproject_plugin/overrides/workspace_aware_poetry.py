from pathlib import Path

from poetry.core.poetry import Poetry
from poetry.factory import Factory
from poetry_multiproject_plugin.workspace import workspaces


def create(poetry: Poetry, toml: str) -> Poetry:
    path = Path(toml).absolute()

    return Factory().create_poetry(path.parent)
