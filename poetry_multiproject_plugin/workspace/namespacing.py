from pathlib import Path


def extract_namespace(path, workspace):
    grandparent = path.parent.parent

    return grandparent.name if len(grandparent.relative_to(workspace).name) else None


def create_namespaced_path(path, workspace):
    namespace = extract_namespace(path, workspace) or ""
    package_name = path.parent.name
    module_name = path.name

    namespaced_path = "/".join([namespace, package_name, module_name])

    return Path(namespaced_path)
