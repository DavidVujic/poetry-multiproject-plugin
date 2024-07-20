import shutil
from pathlib import Path
from typing import Set

defaults_to_ignore = {
    "*.pyc",
    "__pycache__",
    ".venv",
    ".mypy_cache",
    "node_modules",
    ".git",
}


def copy_tree(source: Path, destination: Path, exclude_patterns: Set[str]) -> str:
    to_ignore = defaults_to_ignore.union(exclude_patterns)

    return shutil.copytree(
        source.as_posix(),
        destination.as_posix(),
        ignore=shutil.ignore_patterns(*to_ignore),
        dirs_exist_ok=True,
    )
