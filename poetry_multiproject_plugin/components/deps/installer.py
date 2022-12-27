import os
import subprocess
from pathlib import Path


def run_install_command():
    subprocess.run(["poetry", "install", "--only", "main", "--quiet"])


def navigate_to(path: Path):
    os.chdir(str(path))


def install_deps(destination: Path):
    current_dir = Path.cwd()

    navigate_to(destination)
    run_install_command()

    navigate_to(current_dir)
