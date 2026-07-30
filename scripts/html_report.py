"""Generate a self-contained dark-themed SDLC pipeline summary HTML report.

Usage:
    python scripts/html_report.py
    python scripts/html_report.py --output reports/sdlc-summary.html
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).parent.parent
STATE_FILE = ROOT / ".sdlc" / "state.json"
DEFAULT_OUTPUT = ROOT / "reports" / "sdlc-summary.html"

STATUS_COLORS = {
    "pending":     ("#8b949e", "#21262d"),
    "in_progress": ("#388bfd", "#1c2c4a"),
    "completed":   ("#3fb950", "#1a3027"),
    "failed":      ("#f85149", "#3d1a1a"),
    "skipped":     ("#8b949e", "#21262d"),
}

STATUS_LABELS = {
    "pending":     "PENDING",
    "in_progress": "IN PROGRESS",
    "completed":   "COMPLETED",
    "failed":      "FAILED",
    "skipped":     "SKIPPED",
}

PHASE_ARCHIVE_DIRS = {
    "1": "01-requirements",
    "2": "02-architecture",
    "3": "03-design-review",
    "4": "04-impl-planning",
    "5": "05-implementation",
    "6": "06-code-review",
    "7": "07-verification",
    "8": "08-pr",
}


def _load_state() -> dict:
    if not STATE_FILE.exists():
        return {}
    return json.loads(STATE_FILE.read_text(encoding="utf-8"))


def _file_info(rel_path: str | None) -> tuple[bool, str]:
    if not rel_path:
        return False, "N/A"
    p = ROOT / rel_path
    if p.exists():
        size = p.stat().st_size
        return True, f"{size:,} bytes"
    return False, "not created"


def _badge(status: str) -> str:
    color, bg = STATUS_COLORS.get(status, ("#8b949e", "#21262d"))
    label = STATUS_LABELS.get(status, status.upper())
    return (
        f'<span class="badge" style="color:{color};background:{bg};">'
        f'{label}</span>'
    )


def _phase_cards(state: dict) -> str:
    phases = state.get("phases", {})
    cards = []
    for num_str in sorted(phases.keys(), key=int):
        phase = phases[num_str]
        status = phase["status"]
        color, bg = STATUS_COLORS.get(status, ("#8b949e", "#21262d"))
        exists, size = _file_info(phase.get("output_file"))
        output_label = phase.get("output_file") or "—"
        output_class = "artifact-ok" if exists else "artifact-missing"
        retry = phase.get("retry_count", 0)
        last_error = phase.get("last_error") or ""
        archive_dir = PHASE_ARCHIVE_DIRS.get(num_str, "")
        archive_path = f".sdlc/phase-outputs/{archive_dir}/"
        archive_exists = (ROOT / archive_path).exists() and any(
            (ROOT / archive_path).iterdir()
        ) if (ROOT / archive_path).exists() else False
        archive_label = archive_path if archive_exists else "—"

        started = phase.get("started_at") or "—"
        completed = phase.get("completed_at") or "—"

        error_row = ""
        if last_error:
            error_row = f'<div class="phase-error">Error: {last_error}</div>'

        cards.append(f"""
        <div class="phase-card" style="border-color:{color};">
          <div class="phase-header" style="background:{bg};">
            <span class="phase-num">Phase {num_str}</span>
            {_badge(status)}
          </div>
          <div class="phase-body">
            <div class="phase-name">{phase["name"]}</div>
            <div class="phase-meta">Agent: <code>@{phase["agent"]}</code></div>
            <div class="phase-meta">Output: <span class="{output_class}">{output_label}</span></div>
            <div class="phase-meta">Size: {size}</div>
            <div class="phase-meta">Archive: <code>{archive_label}</code></div>
            <div class="phase-meta">Retries: {retry}</div>
            <div class="phase-meta">Started: {started}</div>
            <div class="phase-meta">Completed: {completed}</div>
            {error_row}
          </div>
        </div>""")
    return "\n".join(cards)


def _artifacts_table(state: dict) -> str:
    phases = state.get("phases", {})
    rows = []
    for num_str in sorted(phases.keys(), key=int):
        phase = phases[num_str]
        out = phase.get("output_file")
        exists, size = _file_info(out)
        icon = '<span style="color:#3fb950;">EXISTS</span>' if exists else '<span style="color:#f85149;">MISSING</span>'
        rows.append(
            f"<tr><td>Phase {num_str}</td><td>{phase['name']}</td>"
            f"<td><code>{out or '—'}</code></td>"
            f"<td>{icon}</td><td>{size}</td></tr>"
        )
    return "\n".join(rows)


def _progress_bar(state: dict) -> str:
    phases = state.get("phases", {})
    total = len(phases)
    done = sum(1 for p in phases.values() if p["status"] == "completed")
    failed = sum(1 for p in phases.values() if p["status"] == "failed")
    pct = int((done / total) * 100) if total else 0
    return f"""
    <div class="progress-label">{done} / {total} phases complete &nbsp;|&nbsp; {failed} failed</div>
    <div class="progress-bar">
      <div class="progress-fill" style="width:{pct}%;"></div>
    </div>"""


def generate_html(state: dict) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    project = state.get("project", "FLASK-001")
    feature = state.get("feature", "Automated Documentation Sync")
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>SDLC Pipeline — {project}</title>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ background: #0d1117; color: #e6edf3; font-family: -apple-system, BlinkMacSystemFont,
      "Segoe UI", Helvetica, Arial, sans-serif; font-size: 14px; line-height: 1.5; }}
    a {{ color: #388bfd; text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    code {{ font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
      font-size: 12px; background: #161b22; padding: 2px 6px; border-radius: 4px; }}
    .container {{ max-width: 1200px; margin: 0 auto; padding: 24px 16px; }}
    .header {{ border-bottom: 1px solid #30363d; padding-bottom: 16px; margin-bottom: 24px; }}
    .header h1 {{ font-size: 24px; font-weight: 600; color: #f0f6fc; }}
    .header .sub {{ color: #8b949e; font-size: 13px; margin-top: 4px; }}
    .section-title {{ font-size: 16px; font-weight: 600; color: #f0f6fc; margin: 32px 0 12px; }}
    .progress-label {{ color: #8b949e; font-size: 13px; margin-bottom: 6px; }}
    .progress-bar {{ height: 8px; background: #21262d; border-radius: 4px; overflow: hidden;
      border: 1px solid #30363d; }}
    .progress-fill {{ height: 100%; background: #238636; border-radius: 4px;
      transition: width 0.4s ease; }}
    .cards-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
      gap: 16px; margin-top: 16px; }}
    .phase-card {{ border: 1px solid #30363d; border-radius: 8px; overflow: hidden;
      background: #161b22; }}
    .phase-header {{ display: flex; align-items: center; justify-content: space-between;
      padding: 10px 14px; gap: 8px; }}
    .phase-num {{ font-size: 12px; font-weight: 600; color: #8b949e; text-transform: uppercase;
      letter-spacing: 0.04em; }}
    .badge {{ font-size: 11px; font-weight: 600; padding: 2px 8px; border-radius: 12px;
      letter-spacing: 0.04em; }}
    .phase-body {{ padding: 12px 14px; }}
    .phase-name {{ font-size: 14px; font-weight: 600; color: #f0f6fc; margin-bottom: 8px; }}
    .phase-meta {{ font-size: 12px; color: #8b949e; margin-top: 3px; }}
    .artifact-ok {{ color: #3fb950; }}
    .artifact-missing {{ color: #f85149; }}
    .phase-error {{ font-size: 11px; color: #f85149; margin-top: 6px; word-break: break-word;
      background: #3d1a1a; padding: 4px 6px; border-radius: 4px; }}
    table {{ width: 100%; border-collapse: collapse; font-size: 13px; margin-top: 12px; }}
    thead tr {{ border-bottom: 1px solid #30363d; }}
    th {{ color: #8b949e; font-weight: 600; text-align: left; padding: 8px 10px;
      font-size: 12px; text-transform: uppercase; letter-spacing: 0.04em; }}
    tbody tr {{ border-bottom: 1px solid #21262d; }}
    tbody tr:hover {{ background: #161b22; }}
    td {{ padding: 8px 10px; color: #e6edf3; vertical-align: top; }}
    .footer {{ color: #484f58; font-size: 12px; margin-top: 40px; padding-top: 16px;
      border-top: 1px solid #21262d; text-align: center; }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>SDLC Pipeline Dashboard</h1>
      <div class="sub">{project} &mdash; {feature} &nbsp;|&nbsp; Generated: {ts}</div>
    </div>

    <div class="section-title">Pipeline Progress</div>
    {_progress_bar(state)}

    <div class="section-title">Phase Status</div>
    <div class="cards-grid">
      {_phase_cards(state)}
    </div>

    <div class="section-title">Artifacts</div>
    <table>
      <thead><tr><th>Phase</th><th>Name</th><th>Output File</th><th>Status</th><th>Size</th></tr></thead>
      <tbody>{_artifacts_table(state)}</tbody>
    </table>

    <div class="footer">
      Flask Task Manager &mdash; Agentic SDLC Pipeline &nbsp;&bull;&nbsp;
      <a href="test-report.html">Test Report</a>
    </div>
  </div>
</body>
</html>"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT),
                        help="Output HTML path (default: reports/sdlc-summary.html)")
    args = parser.parse_args()

    state = _load_state()
    html = generate_html(state)
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"Report written: {out}")


if __name__ == "__main__":
    main()
