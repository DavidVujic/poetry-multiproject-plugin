from pathlib import Path

from poetry_multiproject_plugin.components.project import prepare
from poetry_multiproject_plugin.components.toml import generate, read


def create_new_project_file(project_file: Path) -> Path:
    original = read.toml(project_file)
    generated = generate.generate_valid_dist_project_file(original)

    destination = Path(prepare.get_destination(project_file) / project_file.name)

    with open(destination.as_posix(), "w") as f:
        f.write(generated)

    return destination
