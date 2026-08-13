"""
Generate a combined HTML index report for a SDLC pipeline test run.

Usage:
    python scripts/generate_html_report.py --ticket FLASK-002

Reads:
    reports/<TICKET-ID>/unit-report.html
    reports/<TICKET-ID>/integration-report.html
    reports/<TICKET-ID>/e2e-report.html

Writes:
    reports/<TICKET-ID>/index.html
"""
import argparse
import re
import sys
from datetime import datetime
from pathlib import Path


def _extract_counts(html_path: Path) -> dict:
    """Parse pytest-html summary line into pass/fail/skip/error counts."""
    if not html_path.exists():
        return {"total": 0, "passed": 0, "failed": 0, "errors": 0, "skipped": 0,
                "status": "missing"}

    text = html_path.read_text(encoding="utf-8", errors="replace")

    # pytest-html ≥4: "N passed, M failed, K error, J skipped" in data-* or summary span
    # Try multiple patterns for version compatibility
    passed  = int(re.search(r'(\d+)\s+passed',  text).group(1)) if re.search(r'\d+\s+passed',  text) else 0
    failed  = int(re.search(r'(\d+)\s+failed',  text).group(1)) if re.search(r'\d+\s+failed',  text) else 0
    errors  = int(re.search(r'(\d+)\s+error',   text).group(1)) if re.search(r'\d+\s+error',   text) else 0
    skipped = int(re.search(r'(\d+)\s+skipped', text).group(1)) if re.search(r'\d+\s+skipped', text) else 0
    total   = passed + failed + errors + skipped

    status = "PASS" if (failed == 0 and errors == 0 and total > 0) else (
             "FAIL" if (failed > 0 or errors > 0) else "NO TESTS")

    return {"total": total, "passed": passed, "failed": failed,
            "errors": errors, "skipped": skipped, "status": status}


def generate(ticket_id: str) -> Path:
    base = Path("reports") / ticket_id
    base.mkdir(parents=True, exist_ok=True)

    unit_path = base / "unit-report.html"
    int_path  = base / "integration-report.html"
    e2e_path  = base / "e2e-report.html"

    unit = _extract_counts(unit_path)
    intg = _extract_counts(int_path)
    e2e  = _extract_counts(e2e_path)

    overall_total   = unit["total"]   + intg["total"]   + e2e["total"]
    overall_passed  = unit["passed"]  + intg["passed"]  + e2e["passed"]
    overall_failed  = unit["failed"]  + intg["failed"]  + e2e["failed"]
    overall_errors  = unit["errors"]  + intg["errors"]  + e2e["errors"]
    overall_skipped = unit["skipped"] + intg["skipped"] + e2e["skipped"]
    overall_status  = "PASS" if (overall_failed == 0 and overall_errors == 0 and overall_total > 0) else "FAIL"

    status_colour = "#28a745" if overall_status == "PASS" else "#dc3545"

    def row(label: str, d: dict, report_file: str) -> str:
        colour = "#28a745" if d["status"] == "PASS" else (
                 "#dc3545" if d["status"] in ("FAIL", "missing") else "#6c757d")
        link = f'<a href="{report_file}" target="_blank">{report_file}</a>' if d["status"] != "missing" else "<em>not generated</em>"
        return (f"<tr><td>{label}</td><td>{d['total']}</td>"
                f"<td style='color:{colour}'><b>{d['passed']}</b></td>"
                f"<td style='color:{'#dc3545' if d['failed'] else 'inherit'}'>{d['failed']}</td>"
                f"<td>{d['errors']}</td><td>{d['skipped']}</td>"
                f"<td><span style='color:{colour};font-weight:bold'>{d['status']}</span></td>"
                f"<td>{link}</td></tr>")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Test Report — {ticket_id}</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
           margin: 40px; background: #f8f9fa; color: #212529; }}
    h1   {{ color: #343a40; }}
    .badge {{ display:inline-block; padding: 8px 20px; border-radius: 4px;
              font-size: 1.3em; font-weight: bold; color: white;
              background: {status_colour}; margin-bottom: 24px; }}
    table {{ border-collapse: collapse; width: 100%; background: white;
             box-shadow: 0 1px 3px rgba(0,0,0,.12); border-radius: 6px;
             overflow: hidden; }}
    th    {{ background: #343a40; color: white; padding: 12px 16px; text-align: left; }}
    td    {{ padding: 10px 16px; border-bottom: 1px solid #dee2e6; }}
    tr:last-child td {{ border-bottom: none; }}
    .footer {{ margin-top: 24px; color: #6c757d; font-size: 0.85em; }}
  </style>
</head>
<body>
  <h1>Test Report — {ticket_id}</h1>
  <div class="badge">{overall_status}</div>

  <table>
    <thead>
      <tr>
        <th>Test Type</th><th>Total</th><th>Passed</th><th>Failed</th>
        <th>Errors</th><th>Skipped</th><th>Status</th><th>Report</th>
      </tr>
    </thead>
    <tbody>
      {row("Unit",        unit, "unit-report.html")}
      {row("Integration", intg, "integration-report.html")}
      {row("E2E",         e2e,  "e2e-report.html")}
      <tr style="background:#f1f3f5;font-weight:bold">
        <td>TOTAL</td>
        <td>{overall_total}</td>
        <td style="color:#28a745">{overall_passed}</td>
        <td style="color:{'#dc3545' if overall_failed else 'inherit'}">{overall_failed}</td>
        <td>{overall_errors}</td>
        <td>{overall_skipped}</td>
        <td colspan="2">
          <span style="color:{status_colour};font-weight:bold">{overall_status}</span>
        </td>
      </tr>
    </tbody>
  </table>

  <div class="footer">
    Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')} |
    SDLC Pipeline — Flask Task Manager | Ticket: {ticket_id}
  </div>
</body>
</html>"""

    out = base / "index.html"
    out.write_text(html, encoding="utf-8")
    print(f"Report written: {out}")
    print(f"Overall: {overall_status} — {overall_passed}/{overall_total} passed")
    return out


def main():
    parser = argparse.ArgumentParser(description="Generate combined HTML test report")
    parser.add_argument("--ticket", required=True, help="JIRA ticket ID (e.g. FLASK-002)")
    args = parser.parse_args()
    out = generate(args.ticket)
    sys.exit(0 if "PASS" in out.read_text() else 1)


if __name__ == "__main__":
    main()
