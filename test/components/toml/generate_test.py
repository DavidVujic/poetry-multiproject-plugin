from typing import Union

import tomlkit

from poetry_multiproject_plugin.components.toml import generate

pyproject_lib = """\
[tool.poetry]
packages = [
    {include = "hello", from = "../world"},
]
"""

pyproject_cli = """\
[tool.poetry]
packages = [
    {include = "hello", from = "../world"},
]

[tool.poetry.scripts]
my_cli = "my.console.app:run"
"""


def generate_toml(pyproj: str, ns: Union[str, None]) -> tomlkit.TOMLDocument:
    data = tomlkit.loads(pyproj)

    res = generate.generate_valid_dist_project_file(data, ns)

    return tomlkit.loads(res)


def test_generate_project_file_without_any_changes():
    data = generate_toml(pyproject_lib, None)

    assert data["tool"]["poetry"]["packages"] == [{"include": "hello"}]


def test_generate_project_file_with_custom_namespace_for_packages():
    data = generate_toml(pyproject_lib, "xyz")

    assert data["tool"]["poetry"]["packages"] == [{"include": "xyz"}]


def test_generate_project_file_with_custom_namespace_in_script_entry_point():
    data = generate_toml(pyproject_cli, "xyz")

    assert data["tool"]["poetry"]["scripts"] == {"my_cli": "xyz.my.console.app:run"}


def test_generate_project_file_with_unchanged_script_entry_point():
    data = generate_toml(pyproject_cli, "my")

    assert data["tool"]["poetry"]["scripts"] == {"my_cli": "my.console.app:run"}


def test_generate_project_file_with_unchanged_script_entry_point_when_ns_is_in_path():
    data = generate_toml(pyproject_cli, "console")

    assert data["tool"]["poetry"]["scripts"] == {"my_cli": "my.console.app:run"}
