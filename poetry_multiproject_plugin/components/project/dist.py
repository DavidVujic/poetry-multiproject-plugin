import shutil
from pathlib import Path

from poetry_multiproject_plugin.components.project import prepare


def copy_dist(project_file: Path) -> Path:
    copy_path = prepare.get_destination(project_file)

    source = Path(copy_path / "dist").as_posix()
    destination = project_file.parent.as_posix()

    res = shutil.copytree(source, destination)

    return Path(res)
