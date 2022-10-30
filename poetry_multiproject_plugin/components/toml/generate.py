import tomlkit
from tomlkit.toml_document import TOMLDocument


def extract_top_namespace(include: str) -> str:
    parts = (part for part in include.split("/"))

    return next(parts)


def is_relative(package: dict[str, str]) -> bool:
    return "from" in package and ".." in package.get("from", "")


def relative_to_local(packages) -> list[dict[str, str]]:
    relative = [p for p in packages if is_relative(p)]
    includes = {extract_top_namespace(p["include"]) for p in relative}

    return [{"include": i} for i in includes]


def to_valid_dist_packages(data: TOMLDocument) -> list[dict[str, str]]:
    packages = data["tool"]["poetry"]["packages"]

    local = [p for p in packages if not is_relative(p)]
    modified = relative_to_local(packages)

    return local + modified


def generate_valid_dist_project_file(data: TOMLDocument) -> str:
    """Returns a project file with any relative package includes rearranged,
    according to what is expected by the Poetry tool
    """
    original = tomlkit.dumps(data)
    copy = tomlkit.parse(original)
    dist_packages = to_valid_dist_packages(copy)

    copy["tool"]["poetry"]["packages"].clear()

    for package in dist_packages:
        copy["tool"]["poetry"]["packages"].append(package)

    copy["tool"]["poetry"]["packages"].multiline(True)

    return tomlkit.dumps(copy)
