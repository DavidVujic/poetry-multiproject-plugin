from pathlib import Path
from typing import Optional

from poetry.factory import Factory


class MultiProjectFactory(Factory):
    """
    Overriding the builtin Poetry poetry.factory.Factory.locate function,
    to be able to set a custom filename when invoking a command from this plugin.
    """

    def __init__(self, filename):
        self.filename = filename
        super().__init__()

    def locate(self, cwd: Optional[Path] = None) -> Path:
        cwd = Path(cwd or Path.cwd())
        candidates = [cwd]
        candidates.extend(cwd.parents)

        for path in candidates:
            poetry_file = path / self.filename

            if poetry_file.exists():
                return poetry_file

        else:
            raise RuntimeError(
                f"Could not find {self.filename} file in {cwd} or its parents"
            )
