from pathlib import Path

import tomlkit
from tomlkit.toml_document import TOMLDocument


def packages_to_paths(toml: TOMLDocument) -> list[dict]:
    packages = toml["tool"]["poetry"]["packages"]

    return [
        {"from": Path(p["from"]).joinpath(p["include"]), "to": p["include"]}
        for p in packages
    ]
