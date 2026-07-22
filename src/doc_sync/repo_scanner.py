"""Repository scanning utilities for the documentation sync pipeline.

This module loads the repository files required to build the technical
profile page and returns a normalized structure of repository facts.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List


DEFAULT_SCAN_FILES: List[str] = [
    "README.md",
    "requirements.txt",
    "app.py",
    "models.py",
    "routes.py",
    "forms.py",
]


def read_repository_files(repo_root: str | Path) -> Dict[str, str]:
    """Read the configured repository files and return their contents.

    Missing files or invalid repository paths are represented by an empty
    string so Strict Fact Mode can explicitly mark them as "Not Specified"
    later.
    """
    root = Path(repo_root)
    contents: Dict[str, str] = {file_name: "" for file_name in DEFAULT_SCAN_FILES}

    if not root.exists() or not root.is_dir():
        return contents

    for file_name in DEFAULT_SCAN_FILES:
        file_path = root / file_name
        try:
            contents[file_name] = file_path.read_text(encoding="utf-8")
        except (FileNotFoundError, IsADirectoryError, PermissionError, OSError):
            contents[file_name] = ""

    return contents


def get_scan_targets() -> List[str]:
    """Return the repository files that will be scanned."""
    return list(DEFAULT_SCAN_FILES)
