import ast
import pathlib
from typing import List


def create_namespace_path(top_ns: str, current: str) -> str:
    return f"{top_ns}.{current}"


def mutate_import(node: ast.Import, namespaces: List[str], top_ns: str) -> bool:
    did_mutate = False

    for alias in node.names:
        if alias.name in namespaces:
            alias.name = create_namespace_path(top_ns, alias.name)
            did_mutate = True

    return did_mutate


def mutate_import_from(
    node: ast.ImportFrom, namespaces: List[str], top_ns: str
) -> bool:
    did_mutate = False

    if not node.module or node.level != 0:
        return did_mutate

    for namespace in namespaces:
        if node.module == namespace or node.module.startswith(f"{namespace}."):
            node.module = create_namespace_path(top_ns, node.module)
            did_mutate = True

    return did_mutate


def mutate_imports(node: ast.AST, namespaces: List[str], top_ns: str) -> bool:
    if isinstance(node, ast.Import):
        return mutate_import(node, namespaces, top_ns)

    if isinstance(node, ast.ImportFrom):
        return mutate_import_from(node, namespaces, top_ns)

    return False


def rewrite_module(path: pathlib.Path, namespaces: List[str], top_ns: str) -> bool:
    file_path = path.as_posix()

    with open(file_path, "r") as f:
        tree = ast.parse(f.read(), path.name)

    res = {mutate_imports(node, namespaces, top_ns) for node in ast.walk(tree)}

    if True in res:
        rewritten_source_code = ast.unparse(tree)  # type: ignore[attr-defined]

        with open(file_path, "w") as f:
            f.write(rewritten_source_code)

        return True

    return False
