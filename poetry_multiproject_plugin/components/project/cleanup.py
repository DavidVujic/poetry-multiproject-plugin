import shutil
from pathlib import Path

from poetry_multiproject_plugin.components.project import prepare


def remove_project(project_file: Path):
    copy_path = prepare.get_destination(project_file)

    shutil.rmtree(copy_path)
