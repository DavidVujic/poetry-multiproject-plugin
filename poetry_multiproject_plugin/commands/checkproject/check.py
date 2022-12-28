import itertools
from pathlib import Path
from typing import List

from cleo.helpers import option
from cleo.io.outputs.output import Verbosity
from poetry.console.commands.command import Command
from poetry.factory import Factory

from poetry_multiproject_plugin.components.check import check_for_errors
from poetry_multiproject_plugin.components.deps import install_deps
from poetry_multiproject_plugin.components.project import (
    cleanup,
    create,
    packages,
    prepare,
)
from poetry_multiproject_plugin.components.toml import read

command_name = "check-project"


def run_check(destination: Path, pyproj: str, config_file: str) -> List[str]:
    paths = read.package_paths(destination / pyproj)

    rows = [check_for_errors(destination, str(path), config_file) for path in paths]
    flattened = itertools.chain.from_iterable(rows)

    dest = str(destination)

    return [row.replace(dest, "") for row in flattened]


class ProjectCheckCommand(Command):
    name = command_name

    options = [
        option(
            long_name="config-file",
            description="Path to mypy config file. Use it to override the defaults.",
            flag=False,
        )
    ]

    def collect_project(self, path: Path) -> Path:
        destination = prepare.get_destination(path, "check")

        prepare.copy_project(path, destination)
        packages.copy_packages(path, destination)

        create.create_new_project_file(path, destination)

        return destination

    def prepare_for_build(self, path: Path):
        project_poetry = Factory().create_poetry(path)

        self.set_poetry(project_poetry)

    def handle(self):
        pyproj = "pyproject.toml"
        path = Path(pyproj).absolute()

        project_path = self.collect_project(path)
        self.prepare_for_build(project_path.absolute())

        self.io.set_verbosity(Verbosity.QUIET)

        cleanup.remove_file(project_path, "poetry.lock")
        cleanup.remove_file(project_path, "poetry.toml")

        install_deps(project_path)

        mypy_config = self.option("config-file")
        res = run_check(project_path, pyproj, mypy_config)

        self.io.set_verbosity(Verbosity.NORMAL)
        for r in res:
            self.line(r)

        cleanup.remove_project(project_path)
