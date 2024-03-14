from pathlib import Path

import tomlkit

from poetry_multiproject_plugin.components.toml import packages

pyproject = """\
[tool.poetry]
packages = [
    {include = "hello", from = "../world"},
    {include = "hello/**/*.py", from = "../world"},
    {include = "hello/**/*.py"},
    {include = "*", from = "src"},
    {include = "*", from = "../../src"},
]
"""


def test_packages_to_paths():
    expected = [
        {"from": Path("../world/hello"), "to": "hello"},
        {"from": Path("../world/hello/**/*.py")},
        {"from": Path("hello/**/*.py")},
        {"from": Path("src/*")},
        {"from": Path("../../src/*")},
    ]

    data = tomlkit.loads(pyproject)

    res = packages.packages_to_paths(data)

    assert res == expected
