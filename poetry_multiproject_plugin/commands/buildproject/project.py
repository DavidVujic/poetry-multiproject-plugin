from pathlib import Path

from cleo.helpers import option
from poetry.console.commands.build import BuildCommand
from poetry.factory import Factory

from poetry_multiproject_plugin.components.project import (
    cleanup,
    create,
    dist,
    packages,
    prepare,
)

command_name = "build-project"
command_options = [option("toml", "t", "path to the TOML project file.", flag=False)]


class ProjectBuildCommand(BuildCommand):
    name = command_name
    options = command_options

    def collect_project(self, path: Path) -> Path:
        destination = prepare.get_destination(path)

        prepare.copy_project(path)
        packages.copy_packages(path)
        self.line(f"Copied project & packages into temporary folder <c1>{destination}</c1>")

        generated = create.create_new_project_file(path)
        self.line(f"Generated <c1>{generated}</c1>")

        return destination

    def prepare_for_build(self, path: Path):
        project_poetry = Factory().create_poetry(path.absolute())

        self.set_poetry(project_poetry)

    def handle(self):
        toml = self.option("toml") or "pyproject.toml"
        path = Path(toml)

        self.line(f"Using <c1>{path}</c1>")

        project_path = self.collect_project(path)
        self.prepare_for_build(project_path)

        super(ProjectBuildCommand, self).handle()

        dist.copy_dist(path)
        self.line("Copied <c1>dist</c1> folder.")

        cleanup.remove_project(path)
        self.line("Removed temporary folder.")
        self.line("<c1>Done!</c1>")
