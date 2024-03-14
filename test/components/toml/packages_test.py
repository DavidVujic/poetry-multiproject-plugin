import tomlkit

from poetry_multiproject_plugin.components.toml import packages

pyproject = """\
[tool.poetry]
packages = [
    {include = "hello", from = "../world"},
    {include = "hello/**/*.py", from = "../world"},
    {include = "hello/**/*.py"},
    {include = "*", from = "src"},
]
"""

def test_packages_to_paths():
    data = tomlkit.loads(pyproject)

    res = packages.packages_to_paths(data)
