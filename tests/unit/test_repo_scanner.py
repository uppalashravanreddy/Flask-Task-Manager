from pathlib import Path

from src.doc_sync.repo_scanner import DEFAULT_SCAN_FILES, get_scan_targets, read_repository_files


def test_read_repository_files_reads_existing_files(tmp_path):
    repo_root = tmp_path
    (repo_root / "README.md").write_text("# Sample App\n", encoding="utf-8")
    (repo_root / "requirements.txt").write_text("flask\n", encoding="utf-8")
    (repo_root / "app.py").write_text("print('hello')\n", encoding="utf-8")

    contents = read_repository_files(repo_root)

    assert contents["README.md"] == "# Sample App\n"
    assert contents["requirements.txt"] == "flask\n"
    assert contents["app.py"] == "print('hello')\n"


def test_read_repository_files_returns_empty_strings_for_missing_files(tmp_path):
    repo_root = tmp_path

    contents = read_repository_files(repo_root)

    assert set(contents) == set(DEFAULT_SCAN_FILES)
    assert all(contents[file_name] == "" for file_name in DEFAULT_SCAN_FILES)


def test_get_scan_targets_returns_expected_files():
    targets = get_scan_targets()

    assert targets == DEFAULT_SCAN_FILES
    assert "README.md" in targets
    assert "requirements.txt" in targets
