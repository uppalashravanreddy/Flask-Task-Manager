"""Command-line entry point for the documentation sync pipeline.

This script orchestrates repository scanning, fact extraction, and page
creation to produce a technical profile report in Markdown format.
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path
from typing import Optional

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.doc_sync.page_creator import build_technical_profile_page
from src.doc_sync.repo_scanner import read_repository_files
from src.doc_sync.extractor import RepositoryExtractor


LOGGER = logging.getLogger("doc_sync.main")


def _configure_logging() -> None:
    """Configure a simple logger for pipeline execution."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )


def run_pipeline(repo_root: str | Path | None = None, output_path: str | Path | None = None) -> str:
    """Run the documentation sync pipeline end to end."""
    _configure_logging()
    root = Path(repo_root or ".").resolve()
    output = Path(output_path or root / "docs" / "artifacts" / "FLASK-001" / "technical_profile_report.md")
    output.parent.mkdir(parents=True, exist_ok=True)

    try:
        LOGGER.info("Scanning repository at %s", root)
        repo_files = read_repository_files(root)

        LOGGER.info("Extracting repository facts")
        extractor = RepositoryExtractor()
        facts = extractor.extract(repo_files)

        LOGGER.info("Building technical profile page")
        report_content = build_technical_profile_page(facts)

        output.write_text(report_content, encoding="utf-8")
        LOGGER.info("Report written to %s", output)
        return report_content
    except Exception as exc:  # pragma: no cover - defensive error handling
        LOGGER.exception("Pipeline failed for %s: %s", root, exc)
        fallback_content = (
            "# Error - Technical Profile (Auto-Generated)\n\n"
            "- Pipeline execution failed.\n"
            f"- Error: {exc}\n"
        )
        output.write_text(fallback_content, encoding="utf-8")
        return fallback_content


def main(argv: Optional[list[str]] = None) -> int:
    """CLI entry point for the documentation sync pipeline."""
    parser = argparse.ArgumentParser(description="Generate a technical profile report from a repository")
    parser.add_argument("repo_dir", nargs="?", default=".", help="Path to the repository to scan")
    parser.add_argument("--repo-path", "--repo", dest="repo_path", default=None, help="Path to the repository to scan")
    parser.add_argument("--output-path", "--output", dest="output_path", default=None, help="Path to the generated technical profile report")
    args = parser.parse_args(argv)

    repo_dir = args.repo_path or args.repo_dir
    output_path = args.output_path

    try:
        run_pipeline(repo_dir, output_path=output_path)
    except Exception as exc:  # pragma: no cover - defensive error handling
        LOGGER.exception("CLI execution failed: %s", exc)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
