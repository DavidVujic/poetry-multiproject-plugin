from pathlib import Path

from cleo.helpers import option
from poetry.console.commands.build import BuildCommand
from poetry_multiproject_plugin.overrides import builders, workspace_aware_poetry
from poetry_multiproject_plugin.workspace import workspaces

command_name = "build-project"
command_options = BuildCommand.options + [
    option("toml", "t", "custom TOML file.", flag=False)
]


class ProjectBuildCommand(BuildCommand):
    name = command_name
    options = command_options

    def handle(self) -> None:
        toml = self.option("toml") or workspaces.default_toml

        workspace = workspaces.find_workspace_root(Path.cwd())
        modified = workspace_aware_poetry.create(self.poetry, toml)

        self.set_poetry(modified)

        self.line(
            f"Project file <c1>{modified.file.resolve()}</c1>"
            f"\nWorkspace <c1>{modified.file.parent}</c1>"
        )

        builders.overrride(workspace)

        super(ProjectBuildCommand, self).handle()
