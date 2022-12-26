import shutil
from pathlib import Path


def remove_project(project_path: Path):
    shutil.rmtree(project_path)
