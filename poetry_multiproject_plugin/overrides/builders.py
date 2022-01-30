from pathlib import Path
from typing import Optional

from poetry.core.masonry.builders.builder import BuildIncludeFile


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
        return relative_to_workspace(self)

    if self.source_root is not None:
        return self.path.relative_to(self.source_root)

    return self.path


def overrride(workspace: Optional[Path]):
    """Override the default behaviour to make it workspace aware"""
    BuildIncludeFile.relative_to_project_root = relative_to_project_root
    BuildIncludeFile.relative_to_source_root = relative_to_source_root
    BuildIncludeFile.workspace = property(lambda self: workspace)
