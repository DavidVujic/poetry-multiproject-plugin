"""
TODO

"""
from cleo.helpers import option
from poetry.console.commands.command import Command

command_name = "collect-project"
command_options = [
    option("toml", "t", "path to the TOML project file.", flag=False)
]


class ProjectCollectCommand(Command):
    name = command_name
    options = command_options

    def handle(self) -> None:
        toml = self.option("toml") or "pyproject.toml"

        self.line(f"Project file <c1>{toml}</c1>")
