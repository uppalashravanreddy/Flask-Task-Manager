"""SDLC Pipeline Reporter — Flask Task Manager.

Generates a Markdown summary report of the full 8-phase SDLC pipeline,
including phase status, output file existence, and timing metrics.

Usage:
    python scripts/reporter.py
    python scripts/reporter.py --output .sdlc/sdlc-report.md
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).parent.parent
STATE_FILE = ROOT / ".sdlc" / "state.json"
DEFAULT_OUTPUT = ROOT / ".sdlc" / "sdlc-report.md"

STATUS_ICON = {
    "pending":     "○ Pending",
    "in_progress": "► In Progress",
    "completed":   "✓ Completed",
    "failed":      "✗ Failed",
    "skipped":     "— Skipped",
}

REVIEW_AREAS = [
    ("Correctness",       "docs/artifacts/FLASK-001/requirements.md"),
    ("Security",          ".github/skills/analyze-codebase.md"),
    ("Error Handling",    "src/doc_sync/repo_scanner.py"),
    ("Test Coverage",     "tests/unit/test_doc_sync.py"),
    ("Code Clarity",      "src/doc_sync/extractor.py"),
    ("DRY Principle",     "src/doc_sync/page_creator.py"),
    ("Dependency Safety", "requirements.txt"),
]


def _load_state() -> dict:
    if not STATE_FILE.exists():
        raise FileNotFoundError(f"State file not found: {STATE_FILE}")
    return json.loads(STATE_FILE.read_text(encoding="utf-8"))


def _file_status(relative_path: str | None) -> str:
    if not relative_path:
        return "N/A"
    path = ROOT / relative_path
    if path.exists():
        size = path.stat().st_size
        return f"✓ exists ({size:,} bytes)"
    return "✗ not found"


def _duration(started: str | None, completed: str | None) -> str:
    if not started or not completed:
        return "—"
    try:
        s = datetime.fromisoformat(started)
        c = datetime.fromisoformat(completed)
        delta = c - s
        minutes = int(delta.total_seconds() // 60)
        seconds = int(delta.total_seconds() % 60)
        return f"{minutes}m {seconds}s"
    except Exception:
        return "—"


def _count_tests() -> tuple[int, int]:
    unit_dir = ROOT / "tests" / "unit"
    int_dir = ROOT / "tests" / "integration"
    unit_count = sum(1 for f in unit_dir.glob("test_*.py")) if unit_dir.exists() else 0
    int_count = sum(1 for f in int_dir.glob("test_*.py")) if int_dir.exists() else 0
    return unit_count, int_count


def generate_report(state: dict, output_path: Path | None = None) -> Path:
    if output_path is None:
        output_path = DEFAULT_OUTPUT

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    phases = state["phases"]
    completed_phases = sum(1 for p in phases.values() if p["status"] == "completed")
    failed_phases = sum(1 for p in phases.values() if p["status"] == "failed")
    unit_tests, int_tests = _count_tests()

    lines: list[str] = []

    lines += [
        "# SDLC Pipeline Report — FLASK-001",
        "",
        "| Field | Value |",
        "|---|---|",
        f"| Project | {state['project']} |",
        f"| Feature | {state['feature']} |",
        f"| Repository | {state.get('repository', 'Flask-Task-Manager')} |",
        f"| Report Generated | {now} |",
        f"| Pipeline Started | {state.get('started_at') or '—'} |",
        f"| Last Updated | {state.get('last_updated') or '—'} |",
        "",
        "---",
        "",
        "## Pipeline Progress",
        "",
        f"**{completed_phases}/8 phases completed**"
        + (f" | {failed_phases} failed" if failed_phases else ""),
        "",
        "| Phase | Name | Status | Output File | Duration |",
        "|---|---|---|---|---|",
    ]

    for num in range(1, 9):
        key = str(num)
        phase = phases[key]
        status = STATUS_ICON.get(phase["status"], phase["status"])
        output = _file_status(phase.get("output_file"))
        duration = _duration(phase.get("started_at"), phase.get("completed_at"))
        lines.append(f"| {num} | {phase['name']} | {status} | {output} | {duration} |")

    lines += [
        "",
        "---",
        "",
        "## Phase Details",
        "",
    ]

    for num in range(1, 9):
        key = str(num)
        phase = phases[key]
        lines += [
            f"### Phase {num}: {phase['name']}",
            "",
            f"- **Status:** {phase['status']}",
            f"- **Agent:** `@{phase['agent']}`",
            f"- **Prompt:** `{phase.get('prompt', '—')}`",
            f"- **Output:** {_file_status(phase.get('output_file'))}",
            f"- **Started:** {phase.get('started_at') or '—'}",
            f"- **Completed:** {phase.get('completed_at') or '—'}",
        ]
        if phase.get("failure_reason"):
            lines.append(f"- **Failure Reason:** {phase['failure_reason']}")
        lines.append("")

    lines += [
        "---",
        "",
        "## Implementation Tasks",
        "",
    ]

    tasks = state.get("tasks", {})
    if tasks:
        lines += [
            "| Task ID | Completed | Completed At |",
            "|---|---|---|",
        ]
        for tid, task in sorted(tasks.items()):
            done = "✓" if task.get("completed") else "○"
            at = task.get("completed_at", "—")
            lines.append(f"| {tid} | {done} | {at} |")
    else:
        lines.append("No implementation tasks recorded yet.")

    lines += [
        "",
        "---",
        "",
        "## Code & Test Assets",
        "",
        "| Asset | Location | Present |",
        "|---|---|---|",
    ]

    assets = [
        ("Repository Scanner",    "src/doc_sync/repo_scanner.py"),
        ("Fact Extractor",        "src/doc_sync/extractor.py"),
        ("Page Creator",          "src/doc_sync/page_creator.py"),
        ("CLI Entry Point",       "src/main.py"),
        ("Orchestrator",          "scripts/orchestrator.py"),
        ("State Manager",         "scripts/state_manager.py"),
        ("Reporter",              "scripts/reporter.py"),
        ("Unit Tests",            "tests/unit/"),
        ("Integration Tests",     "tests/integration/"),
        ("Copilot Instructions",  ".github/copilot-instructions.md"),
        ("SDLC State File",       ".sdlc/state.json"),
    ]
    for name, path in assets:
        full = ROOT / path
        present = "✓" if full.exists() else "✗"
        lines.append(f"| {name} | `{path}` | {present} |")

    lines += [
        "",
        f"- Unit test files: {unit_tests}",
        f"- Integration test files: {int_tests}",
        "",
        "---",
        "",
        "## Agents & Prompts Registry",
        "",
        "| Phase | Agent File | Prompt File |",
        "|---|---|---|",
    ]

    for num in range(1, 9):
        key = str(num)
        phase = phases[key]
        agent_file = f".github/agents/{num:02d}-{phase['agent']}.md"
        prompt_file = phase.get("prompt", "—")
        lines.append(f"| {num} — {phase['name']} | `{agent_file}` | `{prompt_file}` |")

    lines += [
        "",
        "---",
        "",
        "## Code Review Dimensions",
        "",
        "| Area | Source File | Present |",
        "|---|---|---|",
    ]
    for area, path in REVIEW_AREAS:
        present = "✓" if (ROOT / path).exists() else "✗"
        lines.append(f"| {area} | `{path}` | {present} |")

    lines += [
        "",
        "---",
        "",
        "*Generated by `scripts/reporter.py` — Flask Task Manager Agentic SDLC Pipeline*",
        "",
    ]

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT,
                        help=f"Output path (default: {DEFAULT_OUTPUT})")
    args = parser.parse_args()

    state = _load_state()
    report_path = generate_report(state, args.output)
    print(f"SDLC report written to: {report_path}")


if __name__ == "__main__":
    main()
