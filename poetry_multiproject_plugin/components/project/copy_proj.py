import shutil
from pathlib import Path


PREPARE_FOR_DIST = ".prepare_for_dist"


def copy_project(project_file: Path):
    source = project_file.parent.as_posix()
    destination = Path(project_file.parent / PREPARE_FOR_DIST).as_posix()

    shutil.copytree(source, destination)


# pf = Path("../poetry-workspaces/projects/first/pyproject.toml")

# copy_project(pf)
