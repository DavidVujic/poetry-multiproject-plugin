from pathlib import Path
from typing import List

from tomlkit.toml_document import TOMLDocument
from tomlkit.toml_file import TOMLFile

from poetry_multiproject_plugin.components.toml.packages import join_package_paths


def toml(path: Path) -> TOMLDocument:
    p = path.as_posix()

    toml_file = TOMLFile(p)

    return toml_file.read()


def package_paths(path: Path) -> List[Path]:
    data: dict = toml(path)
    packages = data["tool"]["poetry"]["packages"]

    return [join_package_paths(p) for p in packages]


def project_name(path: Path) -> str:
    data: dict = toml(path)

    return data["tool"]["poetry"]["name"]
