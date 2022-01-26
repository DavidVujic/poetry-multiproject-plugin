from pathlib import Path

from poetry.core.poetry import Poetry
from poetry_multiproject_plugin.overrides import factory_override
from poetry_multiproject_plugin.repo import repo


def create_modified_poetry(poetry: Poetry, toml: str) -> Poetry:
    cwd = Path.cwd()
    path = Path(toml).absolute()

    factory = factory_override.MultiProjectFactory(path.name)
    modified = factory.create_poetry(path.parent)

    modified.file.parent = repo.find_workspace_root(cwd) or modified.file.parent

    return modified
