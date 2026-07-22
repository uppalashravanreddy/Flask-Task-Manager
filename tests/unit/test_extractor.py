from src.doc_sync.extractor import RepositoryExtractor


def test_extract_returns_expected_metadata_for_repository_files():
    repo_files = {
        "README.md": "# Sample App\n",
        "requirements.txt": "flask==3.1.3\nflask_sqlalchemy\n",
        "app.py": "from flask import Flask\napp = Flask(__name__)\n",
        "models.py": "class Task:\n    pass\n",
        "routes.py": "@app.route('/tasks')\ndef list_tasks():\n    return ''\n",
        "forms.py": "class TaskForm:\n    pass\n",
    }

    extractor = RepositoryExtractor()
    facts = extractor.extract(repo_files)

    assert facts["project_name"] == "Sample App"
    assert facts["stack"] == ["flask", "flask_sqlalchemy"]
    assert facts["entry_point"] == "app.py"
    assert facts["database_model"] == "Task"
    assert facts["routes"] == ["/tasks"]
    assert facts["forms"] == ["TaskForm"]


def test_extract_uses_not_specified_when_values_are_missing():
    extractor = RepositoryExtractor()
    facts = extractor.extract({})

    assert facts["project_name"] == "Not Specified"
    assert facts["stack"] == ["Not Specified"]
    assert facts["entry_point"] == "Not Specified"
    assert facts["database_model"] == "Not Specified"
    assert facts["routes"] == ["Not Specified"]
    assert facts["forms"] == ["Not Specified"]
    assert facts["dependencies"] == ["Not Specified"]
