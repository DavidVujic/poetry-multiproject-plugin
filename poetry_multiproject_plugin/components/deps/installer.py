import os
import subprocess
from pathlib import Path


def ensure_reusable_venv():
    subprocess.run(["poetry", "config", "--local", "virtualenvs.in-project", "false"])
    subprocess.run(["poetry", "config", "--local", "virtualenvs.path", "--unset"])


def run_install_command(is_verbose):
    quiet = [] if is_verbose else ["--quiet"]
    subprocess.run(["poetry", "install", "--only", "main", "--no-root"] + quiet)


def navigate_to(path: Path):
    os.chdir(str(path))


def install_deps(destination: Path, is_verbose: bool):
    current_dir = Path.cwd()

    navigate_to(destination)
    ensure_reusable_venv()
    run_install_command(is_verbose)

    navigate_to(current_dir)
