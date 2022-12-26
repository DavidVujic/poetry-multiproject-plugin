import shutil
from pathlib import Path


def copy_dist(project_file: Path, copy_path: Path) -> Path:
    source = Path(copy_path / "dist").as_posix()
    destination = Path(project_file.parent / "dist").as_posix()

    res = shutil.copytree(source, destination, dirs_exist_ok=True)

    return Path(res)
