from cleo.helpers import option
from poetry.console.commands.build import BuildCommand
from poetry_multiproject_plugin.overrides import poetry_override
from poetry_multiproject_plugin.repo import repo

command_name = "build-project"
command_options = BuildCommand.options + [
    option("toml", "t", "custom TOML file.", flag=False)
]


class ProjectBuildCommand(BuildCommand):
    name = command_name
    options = command_options

    def handle(self) -> None:
        toml = self.option("toml") or repo.default_toml
        modified = poetry_override.create_modified_poetry(self.poetry, toml)

        self.set_poetry(modified)

        self.line(
            f"Project file <c1>{modified.file.resolve()}</c1>"
            f"\nWorkspace <c1>{modified.file.parent}</c1>"
        )

        super(ProjectBuildCommand, self).handle()
