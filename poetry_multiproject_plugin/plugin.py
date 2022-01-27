from poetry.console.application import Application
from poetry.plugins.application_plugin import ApplicationPlugin

from poetry_multiproject_plugin.commands import project_build


class MultiProjectPlugin(ApplicationPlugin):
    """
    A Poetry plugin, adding commands that supports including packages outside of the project root.
    This is achieved by setting the workspace (or commonly the repo) folder as the root folder,
    and being able to specify a project specific TOML file.

    Usage:
    running the command from the workspace root folder
    `poetry build-project --t path/to/myproject.toml`

    Optionally, run the command from the same folder as the actual project specific TOML file:
    `poetry build-project`
    """

    def activate(self, application: Application):
        application.command_loader.register_factory(
            project_build.command_name, project_build.ProjectBuildCommand
        )
