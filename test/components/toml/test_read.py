from pathlib import Path

import tomlkit

from poetry_multiproject_plugin.components.toml import read

pyproject = """\
[tool.poetry]
name = "unit test"
"""

pyproject_with_exclude_pattern = """\
[tool.poetry]
exclude = ["testing.json"]
"""

pyproject_with_complex_exclude_pattern = """\
[tool.poetry]
exclude = [{"path" = "testing.json"}]
"""

pyproject_with_complex_exclude_pattern_containing_format = """\
[tool.poetry]
exclude = [{"path" = "testing.json", "format" = "wheel"}]
"""

pyproject_pep_621 = """\
[tool.poetry]
packages = []

[project]
name = "unit test"
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


def test_get_project_name(monkeypatch):
    monkeypatch.setattr(read, "toml", lambda _: tomlkit.loads(pyproject))

    name = read.project_name(Path.cwd())

    assert name == "unit test"


def test_get_project_name_for_pep_621_project(monkeypatch):
    monkeypatch.setattr(read, "toml", lambda _: tomlkit.loads(pyproject_pep_621))

    name = read.project_name(Path.cwd())

    assert name == "unit test"
