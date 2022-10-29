"""
TODO

"""
from pathlib import Path

from cleo.helpers import option
from poetry.console.commands.command import Command

from poetry_multiproject_plugin.components.project import (
    cleanup,
    create,
    dist,
    packages,
    prepare,
)
from poetry_multiproject_plugin.components.toml import generate, read

command_name = "collect-project"
command_options = [option("toml", "t", "path to the TOML project file.", flag=False)]


class ProjectCollectCommand(Command):
    name = command_name
    options = command_options

    def handle(self) -> None:
        toml = self.option("toml") or "pyproject.toml"

        self.line(f"Project file <c1>{toml}</c1>")


def _comment():
    pf = Path("../poetry-workspaces/projects/first/pyproject.toml")
    prepare.copy_project(pf)

    packages.copy_packages(pf)

    create.create_new_project_file(pf)

    dist.copy_dist(pf)

    cleanup.remove_project(pf)
