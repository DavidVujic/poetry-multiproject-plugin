from typing import Dict, List, Set, Union, cast

import tomlkit
from tomlkit.toml_document import TOMLDocument


def extract_top_namespace(include: str) -> str:
    parts = (part for part in include.split("/"))

    return next(parts)


def is_relative(package: Dict[str, str]) -> bool:
    return "from" in package and ".." in package.get("from", "")


def to_include(include: str) -> dict:
    return {"include": include}


def relative_to_local(packages) -> List[Dict[str, str]]:
    relative = [p for p in packages if is_relative(p)]
    includes = {extract_top_namespace(p["include"]) for p in relative}

    return [to_include(i) for i in includes]


def to_valid_dist_packages(
    data: dict, top_ns: Union[str, None]
) -> List[Dict[str, str]]:
    packages = data["tool"]["poetry"]["packages"]

    local = [p for p in packages if not is_relative(p)]

    relative_packages = relative_to_local(packages)

    if top_ns and relative_packages:
        return local + [to_include(top_ns)]

    return local + relative_packages


def parse_ns_from_relative_package_includes(data: dict) -> Set[str]:
    packages = data["tool"]["poetry"]["packages"]
    relative_paths = {p.get("include") for p in packages if is_relative(p)}

    return {str.replace(p, "/", ".") for p in relative_paths}


def to_valid_entry(entry: str, top_ns: str, data: dict) -> str:
    """Constructing an entry, optionally with a custom top namespace

    Appends the custom top namespace when there are relative package includes
    that matches the entry point namespace,
    and when the custom top namespace isn't already added in configuration.
    """
    prefix = f"{top_ns}."
    ns_from_package_includes = parse_ns_from_relative_package_includes(data)

    contains_ns = any((ns in entry) for ns in ns_from_package_includes)
    contains_prefix = prefix in entry

    if contains_ns and not contains_prefix:
        return f"{prefix}{entry}"

    return entry


def generate_valid_dist_project_file(
    data: TOMLDocument, top_ns: Union[str, None]
) -> str:
    """Returns a project file with any relative package includes rearranged,
    according to what is expected by the Poetry tool
    """
    original = tomlkit.dumps(data)
    copy = cast(dict, tomlkit.parse(original))
    dist_packages = to_valid_dist_packages(copy, top_ns)

    copy["tool"]["poetry"]["packages"].clear()

    for package in dist_packages:
        copy["tool"]["poetry"]["packages"].append(package)

    copy["tool"]["poetry"]["packages"].multiline(True)

    scripts = copy["tool"]["poetry"].get("scripts", {})

    if top_ns and scripts:
        rewritten_scripts = {
            k: to_valid_entry(v, top_ns, data) for k, v in scripts.items()
        }

        copy["tool"]["poetry"]["scripts"] = rewritten_scripts

    return tomlkit.dumps(copy)
