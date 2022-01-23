from cleo.helpers import option
from poetry.console.commands.build import BuildCommand
from poetry.core.masonry.builder import Builder

from poetry_multiproject_plugin import factory_override


class ProjectBuildCommand(BuildCommand):
    """
    A custom build command with support for using a custom TOML file.

    Usage:
    poetry build-project --t myproject.toml
    """

    name = "build-project"

    options = [
        option("toml", "t", "project TOML file.", flag=False),
        option("format", "f", "Limit the format to either sdist or wheel.", flag=False),
    ]

    def handle(self) -> None:
        path = self.poetry.file.path.parent

        filename = self.option("toml") or "pyproject.toml"
        fmt = self.option("format") or "all"

        factory = factory_override.MultiProjectFactory(filename)
        poet = factory.create_poetry(path)

        self.line(
            f"Building <c1>{poet.package.pretty_name}</c1>"
            f" (<c2>{poet.package.version}</c2>)"
            f" from <c1>{poet.file.name}</c1>"
        )

        builder = Builder(poet)
        builder.build(fmt, executable=self.env.python)
