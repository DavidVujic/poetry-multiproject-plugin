from poetry.console.application import Application
from poetry.plugins.application_plugin import ApplicationPlugin

from poetry_multiproject_plugin.commands.buildproject import project


class MultiProjectPlugin(ApplicationPlugin):
    """Poetry Multiproject plugin
    A plugin that adds the "build-project" command.

    The command will make it possible to use relative package includes.
    This feature is very useful for monorepos and using shared code.

    Usage:
    poetry build-project -t path/to/myproject.toml

    Optionally, run the command from the same folder as the actual project specific TOML file:
    poetry build-project
    """

    def activate(self, application: Application):
        application.command_loader.register_factory(
            project.command_name, project.ProjectBuildCommand
        )
