from cleo.helpers import option
from poetry.console.commands.build import BuildCommand
from poetry.core.masonry.builder import Builder
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
        fmt = self.option("format") or "all"

        modified = poetry_override.create_modified_poetry(self.poetry, toml)

        self.line(
            f"Building <c1>{modified.package.pretty_name}</c1>"
            f" (<c2>{modified.package.version}</c2>)."
            f"\nUsing <c1>{modified.file.resolve()}.</c1>"
            f"\nThe workspace folder is set to <c1>{modified.file.parent}</c1>."
        )

        builder = Builder(modified)
        builder.build(fmt, executable=self.env.python)
