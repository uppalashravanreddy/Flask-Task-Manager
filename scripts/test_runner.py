"""Run pytest and generate a self-contained dark-themed HTML test report.

Usage:
    python scripts/test_runner.py
    python scripts/test_runner.py --output reports/test-report.html
    python scripts/test_runner.py --tests tests/unit/
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).parent.parent
DEFAULT_OUTPUT = ROOT / "reports" / "test-report.html"
JSON_TMP = ROOT / "reports" / ".pytest-results.json"


def _run_pytest(test_path: str) -> dict:
    JSON_TMP.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        sys.executable, "-m", "pytest", test_path,
        f"--json-report", f"--json-report-file={JSON_TMP}",
        "-v", "--tb=short", "-q",
    ]
    try:
        subprocess.run(cmd, cwd=ROOT, capture_output=False)
    except FileNotFoundError:
        pass

    if JSON_TMP.exists():
        return json.loads(JSON_TMP.read_text(encoding="utf-8"))

    cmd_fallback = [
        sys.executable, "-m", "pytest", test_path, "-v", "--tb=short",
        "--no-header", "-rN",
    ]
    result = subprocess.run(
        cmd_fallback, cwd=ROOT, capture_output=True, text=True,
        encoding="utf-8", errors="replace",
    )
    return {"_raw_stdout": result.stdout, "_raw_stderr": result.stderr,
            "_returncode": result.returncode}


def _status_badge(outcome: str) -> str:
    styles = {
        "passed":  ("color:#3fb950;background:#1a3027;", "PASSED"),
        "failed":  ("color:#f85149;background:#3d1a1a;", "FAILED"),
        "error":   ("color:#f85149;background:#3d1a1a;", "ERROR"),
        "skipped": ("color:#e3b341;background:#2e2200;", "SKIPPED"),
        "xfailed": ("color:#8b949e;background:#21262d;", "XFAILED"),
        "xpassed": ("color:#3fb950;background:#1a3027;", "XPASSED"),
    }
    style, label = styles.get(outcome, ("color:#8b949e;background:#21262d;", outcome.upper()))
    return f'<span class="badge" style="{style}">{label}</span>'


def _escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
    )


def _build_from_json(data: dict, ts: str) -> str:
    summary = data.get("summary", {})
    total    = summary.get("total", 0)
    passed   = summary.get("passed", 0)
    failed   = summary.get("failed", 0)
    errors   = summary.get("error", 0)
    skipped  = summary.get("skipped", 0)
    duration = round(data.get("duration", 0), 2)

    tests = data.get("tests", [])
    rows = []
    accordions = []

    for t in tests:
        nodeid   = t.get("nodeid", "")
        outcome  = t.get("outcome", "unknown")
        dur      = round(t.get("duration", 0), 3)
        parts    = nodeid.split("::", 1)
        filepath = parts[0]
        testname = parts[1] if len(parts) > 1 else nodeid

        rows.append(
            f"<tr><td><code>{_escape(filepath)}</code></td>"
            f"<td>{_escape(testname)}</td>"
            f"<td>{_status_badge(outcome)}</td>"
            f"<td>{dur}s</td></tr>"
        )

        if outcome in ("failed", "error"):
            call_info = t.get("call", {}) or {}
            longrepr  = call_info.get("longrepr") or ""
            crash     = call_info.get("crash", {}) or {}
            crash_msg = crash.get("message", "")
            tb_html   = _escape(longrepr) if longrepr else _escape(crash_msg)
            accordions.append(f"""
          <details class="failure-item">
            <summary>
              <span class="failure-name">{_escape(testname)}</span>
              <span class="failure-file">{_escape(filepath)}</span>
              {_status_badge(outcome)}
            </summary>
            <pre class="traceback">{tb_html}</pre>
          </details>""")

    rows_html = "\n".join(rows)
    accordion_html = "\n".join(accordions)
    failures_section = ""
    if accordions:
        failures_section = f"""
    <div class="section-title">Failure Details</div>
    <div class="accordions">{accordion_html}</div>
    <div class="rerun-hint">
      Re-run failures only:
      <code>python -m pytest --lf -v</code>
    </div>"""

    return _wrap_html(
        ts=ts,
        total=total, passed=passed, failed=failed,
        errors=errors, skipped=skipped, duration=duration,
        rows_html=rows_html,
        failures_section=failures_section,
    )


def _build_from_raw(data: dict, ts: str) -> str:
    stdout = data.get("_raw_stdout", "")
    stderr = data.get("_raw_stderr", "")
    rc     = data.get("_returncode", -1)

    passed = stdout.count(" PASSED")
    failed = stdout.count(" FAILED") + stdout.count(" ERROR")
    raw_html = _escape(stdout + ("\n--- stderr ---\n" + stderr if stderr else ""))
    rows_html = f"""<tr><td colspan="4">
      <pre style="font-size:12px;white-space:pre-wrap;">{raw_html}</pre>
    </td></tr>"""

    return _wrap_html(
        ts=ts,
        total=passed + failed, passed=passed, failed=failed,
        errors=0, skipped=0, duration=0,
        rows_html=rows_html,
        failures_section="",
    )


def _wrap_html(
    ts: str, total: int, passed: int, failed: int,
    errors: int, skipped: int, duration: float,
    rows_html: str, failures_section: str,
) -> str:
    overall_color = "#3fb950" if failed == 0 and errors == 0 else "#f85149"
    overall_label = "ALL PASSING" if failed == 0 and errors == 0 else f"{failed + errors} FAILING"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Test Report — FLASK-001</title>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ background: #0d1117; color: #e6edf3; font-family: -apple-system, BlinkMacSystemFont,
      "Segoe UI", Helvetica, Arial, sans-serif; font-size: 14px; line-height: 1.5; }}
    a {{ color: #388bfd; text-decoration: none; }}
    code {{ font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
      font-size: 12px; background: #161b22; padding: 2px 6px; border-radius: 4px; }}
    .container {{ max-width: 1100px; margin: 0 auto; padding: 24px 16px; }}
    .header {{ border-bottom: 1px solid #30363d; padding-bottom: 16px; margin-bottom: 24px; }}
    .header h1 {{ font-size: 24px; font-weight: 600; color: #f0f6fc; }}
    .header .sub {{ color: #8b949e; font-size: 13px; margin-top: 4px; }}
    .section-title {{ font-size: 16px; font-weight: 600; color: #f0f6fc; margin: 32px 0 12px; }}
    .summary-bar {{ display: flex; gap: 16px; flex-wrap: wrap; padding: 12px 16px;
      background: #161b22; border: 1px solid #30363d; border-radius: 8px; margin-bottom: 8px; }}
    .stat {{ display: flex; flex-direction: column; align-items: center; }}
    .stat-val {{ font-size: 22px; font-weight: 700; }}
    .stat-lbl {{ font-size: 11px; color: #8b949e; text-transform: uppercase; letter-spacing: 0.05em; }}
    .badge {{ font-size: 11px; font-weight: 600; padding: 2px 8px; border-radius: 12px;
      letter-spacing: 0.04em; }}
    table {{ width: 100%; border-collapse: collapse; font-size: 13px; margin-top: 12px; }}
    thead tr {{ border-bottom: 1px solid #30363d; }}
    th {{ color: #8b949e; font-weight: 600; text-align: left; padding: 8px 10px;
      font-size: 12px; text-transform: uppercase; letter-spacing: 0.04em; }}
    tbody tr {{ border-bottom: 1px solid #21262d; }}
    tbody tr:hover {{ background: #161b22; }}
    td {{ padding: 8px 10px; color: #e6edf3; vertical-align: top; }}
    .accordions {{ margin-top: 8px; }}
    .failure-item {{ border: 1px solid #f85149; border-radius: 6px; margin-bottom: 10px;
      background: #161b22; overflow: hidden; }}
    .failure-item > summary {{ cursor: pointer; padding: 10px 14px; display: flex;
      align-items: center; gap: 10px; list-style: none; user-select: none; }}
    .failure-item > summary::-webkit-details-marker {{ display: none; }}
    .failure-item[open] > summary {{ background: #21262d; border-bottom: 1px solid #30363d; }}
    .failure-name {{ font-weight: 600; color: #f0f6fc; flex: 1; font-size: 13px; }}
    .failure-file {{ font-size: 11px; color: #8b949e; }}
    .traceback {{ font-size: 12px; padding: 12px 14px; background: #0d1117;
      white-space: pre-wrap; word-break: break-word; color: #e6edf3;
      font-family: "SFMono-Regular", Consolas, monospace; }}
    .rerun-hint {{ margin-top: 12px; font-size: 13px; color: #8b949e; }}
    .rerun-hint code {{ font-size: 12px; }}
    .footer {{ color: #484f58; font-size: 12px; margin-top: 40px; padding-top: 16px;
      border-top: 1px solid #21262d; text-align: center; }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>Test Report</h1>
      <div class="sub">FLASK-001 &mdash; Automated Documentation Sync &nbsp;|&nbsp; {ts}</div>
    </div>

    <div class="section-title">Summary</div>
    <div class="summary-bar">
      <div class="stat"><span class="stat-val">{total}</span><span class="stat-lbl">Total</span></div>
      <div class="stat"><span class="stat-val" style="color:#3fb950;">{passed}</span><span class="stat-lbl">Passed</span></div>
      <div class="stat"><span class="stat-val" style="color:#f85149;">{failed}</span><span class="stat-lbl">Failed</span></div>
      <div class="stat"><span class="stat-val" style="color:#f85149;">{errors}</span><span class="stat-lbl">Errors</span></div>
      <div class="stat"><span class="stat-val" style="color:#e3b341;">{skipped}</span><span class="stat-lbl">Skipped</span></div>
      <div class="stat"><span class="stat-val">{duration}s</span><span class="stat-lbl">Duration</span></div>
      <div class="stat"><span class="stat-val" style="color:{overall_color};">{overall_label}</span><span class="stat-lbl">Result</span></div>
    </div>

    <div class="section-title">Test Results</div>
    <table>
      <thead><tr><th>File</th><th>Test</th><th>Status</th><th>Duration</th></tr></thead>
      <tbody>{rows_html}</tbody>
    </table>

    {failures_section}

    <div class="footer">
      Flask Task Manager &mdash; Agentic SDLC Pipeline &nbsp;&bull;&nbsp;
      <a href="sdlc-summary.html">Pipeline Dashboard</a>
    </div>
  </div>
</body>
</html>"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT),
                        help="Output HTML path")
    parser.add_argument("--tests", default="tests/",
                        help="Test path to pass to pytest (default: tests/)")
    args = parser.parse_args()

    try:
        import pytest_json_report  # noqa: F401
    except ImportError:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "pytest-json-report", "-q"],
            check=False,
        )

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    data = _run_pytest(args.tests)

    if "_raw_stdout" in data:
        html = _build_from_raw(data, ts)
    else:
        html = _build_from_json(data, ts)

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"Test report written: {out}")

    summary = data.get("summary", {})
    failed  = summary.get("failed", 0) + summary.get("error", 0)
    if failed:
        print(f"WARNING: {failed} test(s) failed — see {out}")
    else:
        print(f"All tests passed.")


if __name__ == "__main__":
    main()
