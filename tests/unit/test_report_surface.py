from pathlib import Path
import subprocess
import sys


def test_sync_reports_creates_single_accessible_surface(tmp_path):
    repo_root = Path(__file__).resolve().parents[2]
    reports_dir = repo_root / "reports"

    subprocess.run(
        [sys.executable, "scripts/sync_reports.py"],
        cwd=repo_root,
        check=True,
    )

    index = reports_dir / "index.html"
    flasks_dir = reports_dir / "FLASK-001"

    assert index.exists()
    assert index.stat().st_size > 0
    assert flasks_dir.exists()
    assert any(flasks_dir.glob("*.md"))
