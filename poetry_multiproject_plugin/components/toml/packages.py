from pathlib import Path
from typing import List, cast

from tomlkit.toml_document import TOMLDocument


def join_package_paths(package) -> Path:
    from_path = package.get("from", "")
    include_path = package["include"]

    return Path(from_path).joinpath(include_path)


def contains_wildcard(path: Path) -> bool:
    return "*" in path.as_posix()


def create_path_data(package) -> dict:
    from_path = join_package_paths(package)

    a = {"from": from_path}
    b = {"to": package["include"]} if not contains_wildcard(from_path) else {}

    return {**a, **b}


def packages_to_paths(toml: TOMLDocument) -> List[dict]:
    data = cast(dict, toml)
    packages = data["tool"]["poetry"]["packages"]

    return [create_path_data(package) for package in packages]
