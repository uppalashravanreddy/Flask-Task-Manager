from pathlib import Path

from src.doc_sync import collect_repository_facts, generate_problem_spec
from src.doc_sync.page_creator import build_technical_profile_page
from src.main import run_pipeline


def test_collect_repository_facts_extracts_expected_sections():
    repo_root = Path(__file__).resolve().parents[2]

    facts = collect_repository_facts(repo_root)

    assert facts["project_name"] == "Task Manager Using Flask"
    assert facts["stack"]
    assert "Flask" in facts["stack"]
    assert facts["entry_point"] == "app.py"
    assert facts["database_model"] == "Task"
    assert facts["routes"]
    assert facts["forms"]


def test_generate_problem_spec_writes_markdown_with_not_specified_for_missing_data(tmp_path):
    repo_root = tmp_path
    (repo_root / "README.md").write_text("# Sample App\n", encoding="utf-8")
    (repo_root / "requirements.txt").write_text("flask\n", encoding="utf-8")
    (repo_root / "app.py").write_text("from flask import Flask\napp = Flask(__name__)\n", encoding="utf-8")
    (repo_root / "models.py").write_text("class SampleModel:\n    pass\n", encoding="utf-8")
    (repo_root / "routes.py").write_text("", encoding="utf-8")
    (repo_root / "forms.py").write_text("", encoding="utf-8")

    output_path = repo_root / "docs" / "artifacts" / "FLASK-001" / "problem_spec.md"
    result = generate_problem_spec(repo_root, output_path=output_path)

    assert output_path.exists()
    assert output_path.read_text(encoding="utf-8")
    assert "Not Specified" in result


def test_build_technical_profile_page_formats_facts_into_markdown():
    facts = {
        "project_name": "Task Manager",
        "stack": ["Flask", "Flask-SQLAlchemy"],
        "entry_point": "app.py",
        "database_model": "Task",
        "routes": ["/tasks", "/tasks/<id>"],
        "forms": ["TaskForm"],
        "dependencies": ["flask", "pytest"],
        "version_details": {"flask": "3.1.3"},
    }

    page = build_technical_profile_page(facts)

    assert page.startswith("# Task Manager - Technical Profile (Auto-Generated)")
    assert "## Overview" in page
    assert "## Technical Stack" in page
    assert "## Entry Point" in page
    assert "## Data Model" in page
    assert "## Routes" in page
    assert "## Forms" in page
    assert "## Dependencies" in page
    assert "## Version Details" in page


def test_run_pipeline_writes_technical_profile_report(tmp_path):
    repo_root = tmp_path
    (repo_root / "README.md").write_text("# Sample App\n", encoding="utf-8")
    (repo_root / "requirements.txt").write_text("flask\n", encoding="utf-8")
    (repo_root / "app.py").write_text("from flask import Flask\napp = Flask(__name__)\n", encoding="utf-8")
    (repo_root / "models.py").write_text("class SampleModel:\n    pass\n", encoding="utf-8")
    (repo_root / "routes.py").write_text("", encoding="utf-8")
    (repo_root / "forms.py").write_text("", encoding="utf-8")

    output_path = repo_root / "docs" / "artifacts" / "FLASK-001" / "technical_profile_report.md"
    result = run_pipeline(repo_root, output_path=output_path)

    assert output_path.exists()
    assert output_path.read_text(encoding="utf-8")
    assert "Technical Profile" in result
