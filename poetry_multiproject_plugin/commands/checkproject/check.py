from pathlib import Path
from typing import List

from cleo.helpers import option
from cleo.io.outputs.output import Verbosity
from poetry.console.commands.build import BuildCommand
from poetry.factory import Factory

from poetry_multiproject_plugin.components.check import check_for_errors
from poetry_multiproject_plugin.components.project import (
    cleanup,
    create,
    packages,
    prepare,
)

command_name = "check-project"


def run_check(destination: Path, config_file: str) -> List[str]:
    rows = check_for_errors(destination, config_file)
    dest = str(destination)

    return [row.replace(dest, "") for row in rows if "error:" in row]


class ProjectCheckCommand(BuildCommand):
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
        path = Path("pyproject.toml").absolute()

        project_path = self.collect_project(path)
        self.prepare_for_build(project_path.absolute())

        self.io.set_verbosity(Verbosity.QUIET)
        super(ProjectCheckCommand, self).handle()

        self.io.set_verbosity(Verbosity.NORMAL)
        mypy_config = self.option("config-file")
        res = run_check(project_path, mypy_config)

        for r in res:
            self.line(r)

        cleanup.remove_project(project_path)
