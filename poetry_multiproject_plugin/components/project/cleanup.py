import shutil
import os
from pathlib import Path


def remove_project(project_path: Path):
    shutil.rmtree(project_path)


def remove_file(project_path: Path, file_name: str):
    try:
        os.remove(project_path / file_name)
    except FileNotFoundError:
        pass
