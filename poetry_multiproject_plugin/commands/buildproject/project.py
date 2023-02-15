from pathlib import Path
from typing import List, Union

from cleo.helpers import option
from cleo.io.inputs.option import Option
from poetry.console.commands.build import BuildCommand
from poetry.factory import Factory

from poetry_multiproject_plugin.components import parsing
from poetry_multiproject_plugin.components.project import (
    cleanup,
    create,
    dist,
    packages,
    prepare,
)

command_name = "build-project"


def create_command_options() -> List[Option]:
    parent = BuildCommand.options or []

    current = [
        option(
            long_name="with-top-namespace",
            description="To arrange relative includes, and to modify import statements.",
            flag=False,
        )
    ]

    return parent + current


class ProjectBuildCommand(BuildCommand):
    name = command_name

    options = create_command_options()

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

    def rewrite_modules(self, project_path: Path, top_ns: str) -> None:
        folder = project_path / top_ns

        if not folder.exists():
            return

        self.line(f"Using normalized top namespace: {top_ns}")
        namespaces = [item.name for item in folder.iterdir() if item.is_dir()]

        modules = folder.glob("**/*.py")

        for module in modules:
            was_rewritten = parsing.rewrite_module(module, namespaces, top_ns)
            if was_rewritten:
                self.line(
                    f"Updated <c1>{module.parent.name}/{module.name}</c1> with new top namespace for local imports."
                )

    def prepare_for_build(self, path: Path):
        project_poetry = Factory().create_poetry(path)

        self.set_poetry(project_poetry)

    def handle(self):
        path = self.poetry.file.path.absolute()

        self.line(f"Using <c1>{path}</c1>")

        top_ns = prepare.normalize_top_namespace(self.option("with-top-namespace"))
        project_path = self.collect_project(path, top_ns)

        if top_ns:
            self.rewrite_modules(project_path, top_ns)

        self.prepare_for_build(project_path.absolute())

        super(ProjectBuildCommand, self).handle()

        dist.copy_dist(path, project_path)
        self.line("Copied <c1>dist</c1> folder.")

        cleanup.remove_project(project_path)
        self.line("Removed temporary folder.")
        self.line("<c1>Done!</c1>")
