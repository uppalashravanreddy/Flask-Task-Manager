"""Create Markdown documentation pages from extracted repository facts.

This module formats repository facts into a Confluence-style technical profile
page using Strict Fact Mode. Missing fields fall back to the exact value
"Not Specified" rather than being omitted or guessed.
"""

from __future__ import annotations

from typing import Any, Dict, Iterable, List


def _coerce_text(value: Any) -> str:
    """Return a string value or the strict fallback when the value is missing."""
    if value is None:
        return "Not Specified"
    if isinstance(value, str):
        return value.strip() or "Not Specified"
    if isinstance(value, (list, tuple)):
        return ", ".join(str(item) for item in value) if value else "Not Specified"
    if isinstance(value, dict):
        return ", ".join(f"{k}: {v}" for k, v in value.items()) if value else "Not Specified"
    return str(value)


def _format_list(items: Iterable[Any]) -> str:
    """Format a list of values into a Markdown bullet list."""
    values = list(items)
    if not values:
        return "- Not Specified"

    bullet_lines = [f"- {value}" for value in values]
    return "\n".join(bullet_lines)


def build_technical_profile_page(facts: Dict[str, Any]) -> str:
    """Format extracted repository facts into a professional Markdown page."""
    app_name = _coerce_text(facts.get("project_name", "Not Specified"))
    stack = facts.get("stack") or ["Not Specified"]
    entry_point = _coerce_text(facts.get("entry_point", "Not Specified"))
    database_model = _coerce_text(facts.get("database_model", "Not Specified"))
    routes = facts.get("routes") or ["Not Specified"]
    forms = facts.get("forms") or ["Not Specified"]
    dependencies = facts.get("dependencies") or ["Not Specified"]
    version_details = facts.get("version_details") or {"Not Specified": "Not Specified"}

    lines: List[str] = [
        f"# {app_name} - Technical Profile (Auto-Generated)",
        "",
        "## Overview",
        f"- Application Name: {app_name}",
        f"- Summary: Technical profile generated from repository evidence for {app_name}.",
        "",
        "## Technical Stack",
        _format_list(stack),
        "",
        "## Entry Point",
        f"- Primary Entry Point: {entry_point}",
        "",
        "## Data Model",
        f"- Primary Data Model: {database_model}",
        "",
        "## Routes",
        _format_list(routes),
        "",
        "## Forms",
        _format_list(forms),
        "",
        "## Dependencies",
        _format_list(dependencies),
        "",
        "## Version Details",
        _format_list([f"{name}: {value}" for name, value in version_details.items()]),
        "",
        "## Notes",
        "- Missing sections or attributes are reported as Not Specified.",
    ]

    return "\n".join(lines) + "\n"
