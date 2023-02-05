from pathlib import Path
from typing import Union

from poetry.console.commands.build import BuildCommand
from poetry.factory import Factory

from poetry_multiproject_plugin.components.project import (
    cleanup,
    create,
    dist,
    packages,
    prepare,
)
from poetry_multiproject_plugin.components.toml import read

command_name = "build-project"


class ProjectBuildCommand(BuildCommand):
    name = command_name

    def collect_project(self, path: Path, top_ns: Union[str, None]) -> Path:
        destination = prepare.get_destination(path, "prepare")

        prepare.copy_project(path, destination)
        packages.copy_packages(path, destination, top_ns)
        self.line(
            f"Copied project & packages into temporary folder <c1>{destination}</c1>"
        )

        generated = create.create_new_project_file(path, destination, top_ns)
        self.line(f"Generated <c1>{generated}</c1>")

        return destination

    def prepare_for_build(self, path: Path):
        project_poetry = Factory().create_poetry(path)

        self.set_poetry(project_poetry)

    def handle(self):
        path = self.poetry.file.path.absolute()

        self.line(f"Using <c1>{path}</c1>")

        project_name = read.normalized_project_name(path)

        self.line(f"Normalized project name is {project_name}")

        project_path = self.collect_project(path, project_name)
        self.prepare_for_build(project_path.absolute())

        super(ProjectBuildCommand, self).handle()

        dist.copy_dist(path, project_path)
        self.line("Copied <c1>dist</c1> folder.")

        cleanup.remove_project(project_path)
        self.line("Removed temporary folder.")
        self.line("<c1>Done!</c1>")
