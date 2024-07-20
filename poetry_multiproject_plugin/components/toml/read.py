from pathlib import Path
from typing import List, Set, Union

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


def parse_exclude_path(data: dict) -> Union[str, None]:
    if data.get("format"):
        return None

    return data.get("path")


def parse_exclude_pattern(data: Union[str, dict]) -> Union[str, None]:
    if isinstance(data, dict):
        return parse_exclude_path(data)

    return data


def parse_exclude_patterns(data: dict) -> Set[str]:
    config: list = data["tool"]["poetry"].get("exclude", [])

    res = {parse_exclude_pattern(c) for c in config}

    return {r for r in res if r}


def get_exclude_patterns(path: Path) -> Set[str]:
    data: dict = toml(path)

    return parse_exclude_patterns(data)
