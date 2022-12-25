import os
import subprocess
from pathlib import Path

default_args = [
    "--explicit-package-bases",
    "--namespace-packages",
    "--no-error-summary",
    "--no-color-output",
]


def run(dest: str, config_file: str | None) -> list[str]:
    os.environ["MYPYPATH"] = dest

    args = ["--config-file", config_file] if config_file else default_args
    cmd = ["mypy"] + args + [f"{dest}/demo"]

    res = subprocess.run(cmd, capture_output=True, text=True)

    return res.stdout.splitlines()


def check_for_errors(destination: Path, config_file: str | None) -> list[str]:
    lines = run(str(destination), config_file)

    return [line for line in lines if "error:" in line]
