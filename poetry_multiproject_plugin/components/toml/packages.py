from pathlib import Path

from tomlkit.toml_document import TOMLDocument


def join_package_paths(package) -> Path:
    from_path = package.get("from", "")
    include_path = package["include"]

    return Path(from_path).joinpath(include_path)


def create_path_data(package) -> dict:
    return {"from": join_package_paths(package), "to": package["include"]}


def packages_to_paths(toml: TOMLDocument) -> list[dict]:
    packages = toml["tool"]["poetry"]["packages"]

    return [create_path_data(package) for package in packages]
