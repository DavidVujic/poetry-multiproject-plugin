from pathlib import Path

from tomlkit.toml_document import TOMLDocument
from tomlkit.toml_file import TOMLFile


def toml(path: Path) -> TOMLDocument:
    p = path.as_posix()

    toml_file = TOMLFile(p)

    return toml_file.read()
