import tomlkit

from poetry_multiproject_plugin.components.toml import read

pyproject = """\
[tool.poetry]
packages = [
    {include = "hello", from = "../world"},
]
"""

pyproject_with_exclude_pattern = """\
[tool.poetry]
packages = [
    {include = "hello", from = "../world"},
]

exclude = ["testing.json"]
"""

pyproject_with_complex_exclude_pattern = """\
[tool.poetry]
packages = [
    {include = "hello", from = "../world"},
]

exclude = [{"path" = "testing.json"}]
"""

pyproject_with_complex_exclude_pattern_containing_format = """\
[tool.poetry]
packages = [
    {include = "hello", from = "../world"},
]

exclude = [{"path" = "testing.json", "format" = "wheel"}]
"""


def test_read_exclude_pattern_should_return_empty_result():
    data = tomlkit.loads(pyproject)

    res = read.parse_exclude_patterns(data)

    assert res == set()


def test_read_exclude_pattern_should_return_patterns_to_exclude():
    data = tomlkit.loads(pyproject_with_exclude_pattern)

    res = read.parse_exclude_patterns(data)

    assert res == {"testing.json"}


def test_read_complex_exclude_pattern_should_return_patterns_to_exclude():
    data = tomlkit.loads(pyproject_with_complex_exclude_pattern_containing_format)

    res = read.parse_exclude_patterns(data)

    assert res == set()


def test_read_complex_exclude_pattern_with_format_should_return_empty_result():
    data = tomlkit.loads(pyproject_with_complex_exclude_pattern)

    res = read.parse_exclude_patterns(data)

    assert res == {"testing.json"}
