from pathlib import Path

workspace_file = ".workspace"
default_toml = "pyproject.toml"


def find_upwards(cwd: Path, name: str) -> Path | None:
    if cwd == Path(cwd.root):
        return None

    fullpath = cwd / name

    return fullpath if fullpath.exists() else find_upwards(cwd.parent, name)


def find_upwards_dir(cwd: Path, name: str) -> Path | None:
    fullpath = find_upwards(cwd, name)

    return fullpath.parent if fullpath else None


def find_repo_root(cwd: Path) -> Path | None:
    return find_upwards_dir(cwd, ".git")


def find_workspace_root(cwd: Path) -> Path | None:
    return (
        find_upwards_dir(cwd, workspace_file)
        or find_upwards_dir(cwd, default_toml)
        or find_repo_root(cwd)
    )
