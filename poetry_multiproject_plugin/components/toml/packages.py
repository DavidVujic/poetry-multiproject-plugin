from pathlib import Path

import tomlkit
from tomlkit.toml_document import TOMLDocument


def get_poetry_packages(toml: TOMLDocument):
    return toml["tool"]["poetry"]["packages"]


def packages_to_paths(packages: tomlkit.items.Array) -> list[Path]:
    return [Path(p["from"]).joinpath(p["include"]) for p in packages]
