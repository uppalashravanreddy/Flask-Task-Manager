"""Run pytest and generate a self-contained dark-themed HTML test report.

Usage:
    python scripts/test_runner.py
    python scripts/test_runner.py --output reports/test-report.html
    python scripts/test_runner.py --tests tests/unit/
    python scripts/test_runner.py --playwright-json reports/playwright-results.json
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
DEFAULT_TESTS = ["tests/unit/", "tests/integration/"]


def _run_pytest(test_paths: list[str]) -> dict:
    JSON_TMP.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        sys.executable, "-m", "pytest", *test_paths,
        "--json-report", f"--json-report-file={JSON_TMP}",
        "-v", "--tb=short", "-q",
    ]
    try:
        subprocess.run(cmd, cwd=ROOT, capture_output=False)
    except FileNotFoundError:
        pass

    if JSON_TMP.exists():
        return json.loads(JSON_TMP.read_text(encoding="utf-8"))

    cmd_fallback = [
        sys.executable, "-m", "pytest", *test_paths,
        "-v", "--tb=short", "--no-header", "-rN",
    ]
    result = subprocess.run(
        cmd_fallback, cwd=ROOT, capture_output=True, text=True,
        encoding="utf-8", errors="replace",
    )
    return {"_raw_stdout": result.stdout, "_raw_stderr": result.stderr,
            "_returncode": result.returncode}


def _load_playwright_results(json_path: Path) -> list[dict]:
    """Load test results from a pytest-json-report playwright output file."""
    if not json_path.exists():
        return []
    try:
        data = json.loads(json_path.read_text(encoding="utf-8"))
        return data.get("tests", [])
    except Exception:
        return []


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


def _render_tests(tests: list[dict], section_label: str = "") -> tuple[str, str]:
    """Return (rows_html, accordion_html) for a list of test result dicts."""
    rows = []
    accordions = []

    if section_label:
        rows.append(
            f'<tr><td colspan="4" style="background:#161b22;color:#8b949e;'
            f'font-weight:600;font-size:11px;text-transform:uppercase;'
            f'letter-spacing:0.05em;padding:6px 10px;">'
            f'{_escape(section_label)}</td></tr>'
        )

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

    return "\n".join(rows), "\n".join(accordions)


def _build_from_json(data: dict, playwright_tests: list[dict], ts: str) -> str:
    summary  = data.get("summary", {})
    total    = summary.get("total", 0)
    passed   = summary.get("passed", 0)
    failed   = summary.get("failed", 0)
    errors   = summary.get("error", 0)
    skipped  = summary.get("skipped", 0)
    duration = round(data.get("duration", 0), 2)

    unit_tests = data.get("tests", [])

    # Merge playwright counts
    pw_passed  = sum(1 for t in playwright_tests if t.get("outcome") == "passed")
    pw_failed  = sum(1 for t in playwright_tests if t.get("outcome") in ("failed", "error"))
    pw_skipped = sum(1 for t in playwright_tests if t.get("outcome") == "skipped")

    grand_total   = total + len(playwright_tests)
    grand_passed  = passed + pw_passed
    grand_failed  = failed + errors + pw_failed
    grand_skipped = skipped + pw_skipped

    unit_rows, unit_accordions = _render_tests(
        unit_tests,
        "Unit + Integration Tests" if playwright_tests else "",
    )
    pw_rows, pw_accordions = _render_tests(playwright_tests, "E2E — Playwright Tests")

    rows_html      = unit_rows + ("\n" + pw_rows if playwright_tests else "")
    accordion_html = unit_accordions + ("\n" + pw_accordions if playwright_tests else "")

    failures_section = ""
    if accordion_html.strip():
        failures_section = f"""
    <div class="section-title">Failure Details</div>
    <div class="accordions">{accordion_html}</div>
    <div class="rerun-hint">
      Re-run failures only: <code>python -m pytest --lf -v</code>
    </div>"""

    # E2E summary bar
    e2e_bar = ""
    if playwright_tests:
        e2e_color = "#3fb950" if pw_failed == 0 else "#f85149"
        e2e_label = "ALL PASSING" if pw_failed == 0 else f"{pw_failed} FAILING"
        e2e_bar = f"""
    <div class="section-title">E2E (Playwright) Summary</div>
    <div class="summary-bar">
      <div class="stat"><span class="stat-val">{len(playwright_tests)}</span><span class="stat-lbl">Total</span></div>
      <div class="stat"><span class="stat-val" style="color:#3fb950;">{pw_passed}</span><span class="stat-lbl">Passed</span></div>
      <div class="stat"><span class="stat-val" style="color:#f85149;">{pw_failed}</span><span class="stat-lbl">Failed</span></div>
      <div class="stat"><span class="stat-val" style="color:#e3b341;">{pw_skipped}</span><span class="stat-lbl">Skipped</span></div>
      <div class="stat"><span class="stat-val" style="color:{e2e_color};">{e2e_label}</span><span class="stat-lbl">Result</span></div>
    </div>"""

    return _wrap_html(
        ts=ts,
        total=grand_total, passed=grand_passed, failed=grand_failed,
        skipped=grand_skipped, duration=duration,
        rows_html=rows_html,
        failures_section=failures_section,
        e2e_summary=e2e_bar,
    )


def _build_from_raw(data: dict, playwright_tests: list[dict], ts: str) -> str:
    stdout = data.get("_raw_stdout", "")
    stderr = data.get("_raw_stderr", "")

    passed = stdout.count(" PASSED")
    failed = stdout.count(" FAILED") + stdout.count(" ERROR")
    raw_html = _escape(stdout + ("\n--- stderr ---\n" + stderr if stderr else ""))
    rows_html = f"""<tr><td colspan="4">
      <pre style="font-size:12px;white-space:pre-wrap;">{raw_html}</pre>
    </td></tr>"""

    if playwright_tests:
        pw_rows, _ = _render_tests(playwright_tests, "E2E — Playwright Tests")
        rows_html += "\n" + pw_rows

    pw_count  = len(playwright_tests)
    pw_passed = sum(1 for t in playwright_tests if t.get("outcome") == "passed")

    return _wrap_html(
        ts=ts,
        total=passed + failed + pw_count,
        passed=passed + pw_passed,
        failed=failed + (pw_count - pw_passed),
        skipped=0, duration=0,
        rows_html=rows_html,
        failures_section="",
        e2e_summary="",
    )


def _wrap_html(
    ts: str, total: int, passed: int, failed: int,
    skipped: int, duration: float,
    rows_html: str, failures_section: str,
    e2e_summary: str = "",
) -> str:
    overall_color = "#3fb950" if failed == 0 else "#f85149"
    overall_label = "ALL PASSING" if failed == 0 else f"{failed} FAILING"

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

    <div class="section-title">Overall Summary</div>
    <div class="summary-bar">
      <div class="stat"><span class="stat-val">{total}</span><span class="stat-lbl">Total</span></div>
      <div class="stat"><span class="stat-val" style="color:#3fb950;">{passed}</span><span class="stat-lbl">Passed</span></div>
      <div class="stat"><span class="stat-val" style="color:#f85149;">{failed}</span><span class="stat-lbl">Failed</span></div>
      <div class="stat"><span class="stat-val" style="color:#e3b341;">{skipped}</span><span class="stat-lbl">Skipped</span></div>
      <div class="stat"><span class="stat-val">{duration}s</span><span class="stat-lbl">Duration</span></div>
      <div class="stat"><span class="stat-val" style="color:{overall_color};">{overall_label}</span><span class="stat-lbl">Result</span></div>
    </div>

    {e2e_summary}

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
    parser.add_argument("--tests", nargs="+", default=DEFAULT_TESTS,
                        help="Test paths to pass to pytest (default: tests/unit/ tests/integration/)")
    parser.add_argument("--playwright-json", default=None,
                        help="Path to playwright pytest-json-report JSON file to merge into report")
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

    # Load playwright results if provided or auto-detect
    pw_json_path = Path(args.playwright_json) if args.playwright_json else ROOT / "reports" / "playwright-results.json"
    playwright_tests = _load_playwright_results(pw_json_path)
    if playwright_tests:
        print(f"Merged {len(playwright_tests)} Playwright test results from {pw_json_path}")

    if "_raw_stdout" in data:
        html = _build_from_raw(data, playwright_tests, ts)
    else:
        html = _build_from_json(data, playwright_tests, ts)

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"Test report written: {out}")

    summary = data.get("summary", {})
    failed  = summary.get("failed", 0) + summary.get("error", 0)
    pw_failed = sum(1 for t in playwright_tests if t.get("outcome") in ("failed", "error"))
    total_failed = failed + pw_failed
    if total_failed:
        print(f"WARNING: {total_failed} test(s) failed — see {out}")
    else:
        print("All tests passed.")


if __name__ == "__main__":
    main()
