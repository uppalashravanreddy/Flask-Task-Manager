"""Public entry points for the documentation sync pipeline."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from .extractor import RepositoryExtractor
from .page_creator import build_technical_profile_page
from .repo_scanner import read_repository_files


def collect_repository_facts(repo_root: str | Path) -> Dict[str, Any]:
    """Collect repository facts for technical profile generation."""
    repo_files = read_repository_files(repo_root)
    extractor = RepositoryExtractor()
    facts = extractor.extract(repo_files)
    stack = facts.get("stack", [])
    if isinstance(stack, list):
        normalized_stack = []
        for item in stack:
            if isinstance(item, str):
                lowered = item.lower()
                mapping = {
                    "flask": "Flask",
                    "flask_sqlalchemy": "Flask-SQLAlchemy",
                    "flask_wtf": "Flask-WTF",
                    "wtforms": "WTForms",
                    "sqlalchemy": "SQLAlchemy",
                }
                normalized_stack.append(mapping.get(lowered, lowered))
        facts["stack"] = normalized_stack
    return facts


def generate_problem_spec(repo_root: str | Path, output_path: str | Path | None = None) -> str:
    """Generate a markdown problem-spec artifact from repository evidence."""
    facts = collect_repository_facts(repo_root)
    output = Path(output_path or Path(repo_root) / "docs" / "artifacts" / "FLASK-001" / "problem_spec.md")
    output.parent.mkdir(parents=True, exist_ok=True)

    content = [
        "# Problem Specification — FLASK-001",
        "",
        "## Repository Evidence",
        f"- Project Name: {facts.get('project_name', 'Not Specified')}",
        f"- Entry Point: {facts.get('entry_point', 'Not Specified')}",
        f"- Database Model: {facts.get('database_model', 'Not Specified')}",
        "",
        "## Notes",
        "- Missing information is explicitly marked as Not Specified.",
    ]

    output.write_text("\n".join(content) + "\n", encoding="utf-8")
    return output.read_text(encoding="utf-8")


__all__ = [
    "RepositoryExtractor",
    "build_technical_profile_page",
    "collect_repository_facts",
    "generate_problem_spec",
]
