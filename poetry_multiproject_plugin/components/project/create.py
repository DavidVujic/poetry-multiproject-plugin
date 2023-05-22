from pathlib import Path
from typing import Union

from poetry_multiproject_plugin.components.toml import generate, read


def create_new_project_file(
    project_file: Path, destination: Path, top_ns: Union[str, None] = None
) -> Path:
    original = read.toml(project_file)
    generated = generate.generate_valid_dist_project_file(original, top_ns)

    destination = Path(destination / project_file.name)

    with open(destination.as_posix(), "w", encoding="utf-8", newline="") as f:
        f.write(generated)

    return destination
