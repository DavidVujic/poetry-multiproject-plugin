import os
import subprocess
from pathlib import Path


def ensure_reusable_venv():
    subprocess.run(["poetry", "config", "--local", "virtualenvs.in-project", "false"])
    subprocess.run(["poetry", "config", "--local", "virtualenvs.path", "--unset"])


def run_install_command():
    subprocess.run(["poetry", "install", "--only", "main", "--quiet"])


def navigate_to(path: Path):
    os.chdir(str(path))


def install_deps(destination: Path):
    current_dir = Path.cwd()

    navigate_to(destination)
    ensure_reusable_venv()
    run_install_command()

    navigate_to(current_dir)
