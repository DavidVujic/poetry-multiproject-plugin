from pathlib import Path
from typing import Optional

from poetry.core.masonry.builders.builder import BuildIncludeFile
from poetry_multiproject_plugin.workspace import namespacing


def relative_to_workspace(target) -> Path:
    if target.workspace is not None:
        return target.path.relative_to(target.workspace)

    return target.path


def relative_to_project_root(self) -> Path:
    if self.workspace:
        return relative_to_workspace(self)

    return self.path.relative_to(self.project_root)


def relative_to_source_root(self) -> Path:
    if self.workspace:
        return namespacing.create_namespaced_path(self.path, self.workspace)

    if self.source_root is not None:
        return self.path.relative_to(self.source_root)

    return self.path


def overrride(workspace: Optional[Path]):
    """Override the default behaviour to make it workspace aware"""
    BuildIncludeFile.relative_to_project_root = relative_to_project_root
    BuildIncludeFile.relative_to_source_root = relative_to_source_root
    BuildIncludeFile.workspace = property(lambda self: workspace)
