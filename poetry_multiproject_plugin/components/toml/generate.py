import tomlkit
from tomlkit.toml_document import TOMLDocument


def to_valid_dist_package(package: dict[str, str]) -> dict[str, str]:
    if ".." not in package.get("from", ""):
        return package

    return {"include": package["include"]}


def to_valid_dist_packages(data: TOMLDocument) -> list[dict[str, str]]:
    packages = data["tool"]["poetry"]["packages"]

    return [to_valid_dist_package(p) for p in packages]


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
