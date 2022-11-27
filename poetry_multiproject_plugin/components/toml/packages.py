from pathlib import Path
from typing import List, cast

from tomlkit.toml_document import TOMLDocument


def join_package_paths(package) -> Path:
    from_path = package.get("from", "")
    include_path = package["include"]

    return Path(from_path).joinpath(include_path)


def create_path_data(package) -> dict:
    return {"from": join_package_paths(package), "to": package["include"]}


def packages_to_paths(toml: TOMLDocument) -> List[dict]:
    data = cast(dict, toml)
    packages = data["tool"]["poetry"]["packages"]

    return [create_path_data(package) for package in packages]
