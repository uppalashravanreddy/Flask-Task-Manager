from pathlib import Path

from src.main import run_pipeline


def test_pipeline_writes_markdown_report(tmp_path):
    repo_root = tmp_path
    (repo_root / "README.md").write_text("# Sample App\n", encoding="utf-8")
    (repo_root / "requirements.txt").write_text("flask\n", encoding="utf-8")
    (repo_root / "app.py").write_text("from flask import Flask\napp = Flask(__name__)\n", encoding="utf-8")
    (repo_root / "models.py").write_text("class Task:\n    pass\n", encoding="utf-8")
    (repo_root / "routes.py").write_text("@app.route('/tasks')\ndef list_tasks():\n    return ''\n", encoding="utf-8")
    (repo_root / "forms.py").write_text("class TaskForm:\n    pass\n", encoding="utf-8")

    output_path = repo_root / "docs" / "artifacts" / "FLASK-001" / "technical_profile_report.md"
    report = run_pipeline(repo_root, output_path=output_path)

    assert output_path.exists()
    assert output_path.read_text(encoding="utf-8")
    assert "Technical Profile" in report
    assert "Sample App" in report
