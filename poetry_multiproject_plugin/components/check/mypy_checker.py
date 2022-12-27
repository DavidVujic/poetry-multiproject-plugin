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


def run(dest: str, top_ns: str, config_file: Union[str, None]) -> List[str]:
    os.environ["MYPYPATH"] = dest

    args = ["--config-file", config_file] if config_file else default_args
    cmd = ["poetry", "run", "mypy"] + args + [f"{dest}/{top_ns}"]

    res = subprocess.run(cmd, capture_output=True, text=True)

    return res.stdout.splitlines()


def check_for_errors(
    destination: Path, top_ns: str, config_file: Union[str, None]
) -> List[str]:
    lines = run(str(destination), top_ns, config_file)

    return [line for line in lines if "error:" in line]
