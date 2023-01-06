import os
import subprocess
from pathlib import Path
from typing import List, Union

default_args = [
    "--explicit-package-bases",
    "--namespace-packages",
    "--no-error-summary",
    "--no-color-output",
]


def install(is_verbose: bool):
    args = [] if is_verbose else ["--quiet"]
    cmd = ["poetry", "add", "mypy"] + args
    subprocess.run(cmd)


def run(dest: Path, top_ns: str, config_file: Union[str, None]) -> List[str]:
    args = ["--config-file", config_file] if config_file else default_args
    cmd = ["poetry", "run", "mypy"] + args + [f"{dest}/{top_ns}"]

    res = subprocess.run(cmd, capture_output=True, text=True)

    return res.stdout.splitlines()


def navigate_to(path: Path):
    os.chdir(str(path))


def check_for_errors(
    destination: Path, top_ns: str, is_verbose: bool, config_file: Union[str, None]
) -> List[str]:
    current_dir = Path.cwd()

    navigate_to(destination)

    install(is_verbose)
    lines = run(destination, top_ns, config_file)

    navigate_to(current_dir)

    return [line for line in lines if "error:" in line]
