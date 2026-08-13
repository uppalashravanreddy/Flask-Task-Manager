"""Create a single browsable reports surface for the FLASK-001 deliverables.

This helper copies the Markdown SDLC artifacts into a dedicated
`reports/FLASK-001/` directory and generates a small `reports/index.html`
landing page that links to the HTML dashboards and all collected artifacts.
"""
from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOC_ARTIFACTS = ROOT / "docs" / "artifacts" / "FLASK-001"
REPORTS_DIR = ROOT / "reports"
REPORT_FOLDER = REPORTS_DIR / "FLASK-001"
INDEX_FILE = REPORTS_DIR / "index.html"
HTML_REPORTS = ["sdlc-summary.html", "test-report.html"]
PLAYWRIGHT_REPORTS = ["playwright-results.json", "playwright-report.html"]


def _copy_artifacts() -> list[str]:
    REPORT_FOLDER.mkdir(parents=True, exist_ok=True)
    copied: list[str] = []

    for markdown_path in sorted(DOC_ARTIFACTS.glob("*.md")):
        target = REPORT_FOLDER / markdown_path.name
        shutil.copy2(markdown_path, target)
        copied.append(markdown_path.name)

    for html_name in HTML_REPORTS:
        source = REPORTS_DIR / html_name
        if source.exists():
            shutil.copy2(source, REPORT_FOLDER / html_name)

    for report_name in PLAYWRIGHT_REPORTS:
        source = REPORTS_DIR / report_name
        if source.exists():
            shutil.copy2(source, REPORT_FOLDER / report_name)
            copied.append(report_name)

    screenshots_dir = REPORTS_DIR / "playwright-screenshots"
    if screenshots_dir.exists():
        target_dir = REPORT_FOLDER / "playwright-screenshots"
        if target_dir.exists():
            shutil.rmtree(target_dir)
        shutil.copytree(screenshots_dir, target_dir)

    return copied


def _build_index(copied_artifacts: list[str]) -> str:
    links = []
    for file_name in HTML_REPORTS:
        links.append(f'<li><a href="FLASK-001/{file_name}">{file_name}</a></li>')

    for file_name in PLAYWRIGHT_REPORTS:
        if (REPORTS_DIR / file_name).exists():
            links.append(f'<li><a href="FLASK-001/{file_name}">{file_name}</a></li>')

    for file_name in copied_artifacts:
        links.append(
            f'<li><a href="FLASK-001/{file_name}">{file_name}</a></li>'
        )

    screenshots_dir = REPORTS_DIR / "playwright-screenshots"
    if screenshots_dir.exists():
        links.append('<li><a href="FLASK-001/playwright-screenshots/">playwright-screenshots/</a></li>')

    return f"""<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"UTF-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
  <title>FLASK-001 Report Index</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 40px; background: #0d1117; color: #e6edf3; }}
    a {{ color: #58a6ff; text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    .card {{ background: #161b22; border: 1px solid #30363d; padding: 16px; border-radius: 8px; max-width: 900px; }}
    ul {{ line-height: 1.8; }}
  </style>
</head>
<body>
  <div class=\"card\">
    <h1>FLASK-001 Report Index</h1>
    <p>All generated HTML and Markdown artifacts are surfaced from this page.</p>
    <ul>
      {''.join(links)}
    </ul>
  </div>
</body>
</html>
"""


def main() -> None:
    copied = _copy_artifacts()
    INDEX_FILE.write_text(_build_index(copied), encoding="utf-8")
    print(f"Copied {len(copied)} markdown artifacts to {REPORT_FOLDER}")
    print(f"Wrote report index: {INDEX_FILE}")


if __name__ == "__main__":
    main()
