from poetry.console.application import Application
from poetry.plugins.application_plugin import ApplicationPlugin

from poetry_multiproject_plugin import command


def factory():
    return command.ProjectBuildCommand()


class MultiProjectPlugin(ApplicationPlugin):
    """A Poetry plugin that makes it possible to build projects with custom TOML files.

    Usage:
    poetry build-project --t myproject.toml
    """

    def activate(self, application: Application):
        application.command_loader.register_factory(
            command.ProjectBuildCommand.name, factory
        )
