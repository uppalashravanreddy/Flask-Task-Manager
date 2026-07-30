"""Post-write phase hook — called by Claude Code after any Write tool call.

If the written file is a recognised SDLC phase output, this hook:
  1. Copies the file to .sdlc/phase-outputs/<phase>/ with a timestamp header
  2. Regenerates the HTML SDLC summary report
  3. Prints a confirmation message

Phase output map:
  docs/artifacts/FLASK-001/requirements.md      → 01-requirements/
  docs/artifacts/FLASK-001/architecture.md       → 02-architecture/
  docs/artifacts/FLASK-001/design-review.md      → 03-design-review/
  docs/artifacts/FLASK-001/impl-plan.md          → 04-impl-planning/
  docs/artifacts/FLASK-001/review_report.md      → 06-code-review/
  docs/artifacts/FLASK-001/verification_report.md → 07-verification/
  .sdlc/pr-description.md                        → 08-pr/
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent

PHASE_OUTPUT_MAP: dict[str, str] = {
    "docs/artifacts/FLASK-001/requirements.md":       "01-requirements",
    "docs/artifacts/FLASK-001/architecture.md":        "02-architecture",
    "docs/artifacts/FLASK-001/design-review.md":       "03-design-review",
    "docs/artifacts/FLASK-001/impl-plan.md":           "04-impl-planning",
    "docs/artifacts/FLASK-001/review_report.md":       "06-code-review",
    "docs/artifacts/FLASK-001/verification_report.md": "07-verification",
    ".sdlc/pr-description.md":                         "08-pr",
}


def _normalise(path: str) -> str:
    try:
        p = Path(path)
        for parent in [p, *p.parents]:
            if (parent / ".git").exists():
                return str(p.relative_to(parent)).replace("\\", "/")
    except Exception:
        pass
    return path.replace("\\", "/")


def _timestamp_prefix(phase_key: str) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return f"<!-- Archived: {ts} | Phase: {phase_key} | Source: SDLC pipeline -->\n"


def _copy_to_archive(source: Path, phase_key: str) -> Path:
    archive_dir = ROOT / ".sdlc" / "phase-outputs" / phase_key
    archive_dir.mkdir(parents=True, exist_ok=True)
    dest = archive_dir / source.name
    content = source.read_text(encoding="utf-8")
    prefix = _timestamp_prefix(phase_key)
    dest.write_text(prefix + content, encoding="utf-8")
    return dest


def _regenerate_html() -> None:
    html_script = ROOT / "scripts" / "html_report.py"
    if html_script.exists():
        subprocess.run(
            [sys.executable, str(html_script)],
            capture_output=True,
            cwd=str(ROOT),
        )


def main() -> None:
    raw = sys.stdin.read()
    if not raw.strip():
        sys.exit(0)

    try:
        data = json.loads(raw)
        file_path = data.get("tool_input", {}).get("file_path", "")
    except (json.JSONDecodeError, AttributeError):
        sys.exit(0)

    normalised = _normalise(file_path)

    if normalised not in PHASE_OUTPUT_MAP:
        sys.exit(0)

    phase_key = PHASE_OUTPUT_MAP[normalised]
    source = ROOT / normalised

    if not source.exists():
        sys.exit(0)

    try:
        archived = _copy_to_archive(source, phase_key)
        print(f"[SDLC] Archived phase output: {archived.relative_to(ROOT)}", flush=True)
        _regenerate_html()
        print(f"[SDLC] HTML report updated: reports/sdlc-summary.html", flush=True)
    except Exception as e:
        print(f"[SDLC WARNING] post_write_phase failed: {e}", file=sys.stderr)

    sys.exit(0)


if __name__ == "__main__":
    main()
