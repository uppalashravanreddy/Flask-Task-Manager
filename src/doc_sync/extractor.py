"""Extract structured documentation facts from repository files.

This module parses configuration files and Python source code using Strict
Fact Mode. If required information cannot be found in the repository, it
returns the exact value "Not Specified" instead of making assumptions.
"""

from __future__ import annotations

import ast
import re
from pathlib import Path
from typing import Any, Dict, List, Optional


def _normalize_text(value: Optional[str]) -> str:
    """Return a normalized non-empty string or the strict fallback."""
    if value is None:
        return "Not Specified"
    text = value.strip()
    return text if text else "Not Specified"


class RepositoryExtractor:
    """Extract repository facts for documentation generation."""

    def __init__(self) -> None:
        """Initialize the extractor with strict-mode defaults."""
        self.strict_fact_mode = True

    def extract(self, repo_files: Dict[str, str]) -> Dict[str, Any]:
        """Extract technical facts from repository file contents."""
        requirements_text = repo_files.get("requirements.txt", "")
        readme_text = repo_files.get("README.md", "")
        routes_text = repo_files.get("routes.py", "")
        models_text = repo_files.get("models.py", "")
        app_text = repo_files.get("app.py", "")
        forms_text = repo_files.get("forms.py", "")

        extracted: Dict[str, Any] = {
            "project_name": self._extract_project_name(readme_text),
            "stack": self._extract_stack(requirements_text),
            "entry_point": self._extract_entry_point(app_text),
            "database_model": self._extract_database_model(models_text),
            "routes": self._extract_routes(routes_text),
            "forms": self._extract_forms(forms_text),
            "dependencies": self._extract_dependencies(requirements_text),
            "version_details": self._extract_versions(requirements_text),
        }

        return extracted

    def _extract_project_name(self, readme_text: str) -> str:
        """Extract the project title from the README heading."""
        match = re.search(r"^#\s+(.+)$", readme_text, re.MULTILINE)
        return _normalize_text(match.group(1) if match else None)

    def _extract_stack(self, requirements_text: str) -> List[str]:
        """Extract recognized stack dependencies from requirements content."""
        if not requirements_text.strip():
            return ["Not Specified"]

        packages = [line.strip() for line in requirements_text.splitlines() if line.strip()]
        normalized: List[str] = []
        for package in packages:
            package_name = re.split(r"[<>=!~\s\[]", package, 1)[0].strip().lower()
            if package_name in {"flask", "flask_sqlalchemy", "flask_wtf", "wtforms", "sqlalchemy"}:
                normalized.append(package_name)

        if not normalized:
            return ["Not Specified"]
        return normalized

    def _extract_entry_point(self, app_text: str) -> str:
        """Extract the application entry point from app.py."""
        if not app_text.strip():
            return "Not Specified"
        return "app.py"

    def _extract_database_model(self, models_text: str) -> str:
        """Extract the primary database model class from models.py."""
        if not models_text.strip():
            return "Not Specified"

        try:
            tree = ast.parse(models_text)
        except SyntaxError:
            return "Not Specified"

        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                return node.name

        return "Not Specified"

    def _extract_routes(self, routes_text: str) -> List[str]:
        """Extract route paths from route decorators in routes.py."""
        if not routes_text.strip():
            return ["Not Specified"]

        matches = re.findall(r"@app\.route\(['\"]([^'\"]+)['\"]", routes_text)
        if not matches:
            return ["Not Specified"]
        return matches

    def _extract_forms(self, forms_text: str) -> List[str]:
        """Extract forms defined in forms.py."""
        if not forms_text.strip():
            return ["Not Specified"]

        try:
            tree = ast.parse(forms_text)
        except SyntaxError:
            return ["Not Specified"]

        form_names: List[str] = []
        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                form_names.append(node.name)

        if not form_names:
            return ["Not Specified"]
        return form_names

    def _extract_dependencies(self, requirements_text: str) -> List[str]:
        """Extract dependency names from requirements.txt."""
        if not requirements_text.strip():
            return ["Not Specified"]

        dependencies = [
            re.split(r"[<>=!~\s\[]", line.strip(), 1)[0].strip()
            for line in requirements_text.splitlines()
            if line.strip()
        ]
        filtered = [dep for dep in dependencies if dep]

        if not filtered:
            return ["Not Specified"]
        return filtered

    def _extract_versions(self, requirements_text: str) -> Dict[str, str]:
        """Extract package versions from requirements.txt when present."""
        if not requirements_text.strip():
            return {"Not Specified": "Not Specified"}

        versions: Dict[str, str] = {}
        for line in requirements_text.splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            match = re.match(r"^([A-Za-z0-9_.-]+)\s*(.*)$", stripped)
            if match:
                package_name = match.group(1)
                version_part = match.group(2).strip()
                if version_part:
                    versions[package_name] = version_part
                else:
                    versions[package_name] = "Not Specified"

        if not versions:
            return {"Not Specified": "Not Specified"}
        return versions
