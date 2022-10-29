import shutil
from pathlib import Path

from poetry_multiproject_plugin.components.project import prepare


def copy_dist(project_file: Path) -> Path:
    copy_path = prepare.get_destination(project_file)

    source = Path(copy_path / "dist").as_posix()
    destination = Path(project_file.parent / "dist").as_posix()

    res = shutil.copytree(source, destination, dirs_exist_ok=True)

    return Path(res)
