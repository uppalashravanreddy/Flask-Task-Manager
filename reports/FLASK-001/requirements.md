# Requirements — FLASK-001: Automated Documentation Sync

| Field | Value |
|---|---|
| Ticket ID | FLASK-001 |
| Phase | 1 — Requirements |
| Status | Complete |
| Author | SDLC Pipeline (requirements agent) |
| Date | 2026-07-30 |

## 1. User Story

As a developer working on the Flask Task Manager project, I want to run a local CLI script that automatically scans the repository, extracts structured facts about the codebase, and publishes a versioned technical profile page to the Confluence Documentation space, so that project documentation stays accurate and current without requiring manual authoring effort after each change.

## 2. Functional Requirements

| ID | Requirement | Source | Priority |
|---|---|---|---|
| FR-1 | The system shall provide a CLI entry point (`src/main.py`) accepting `--repo` and `--output` flags that a developer can invoke locally to trigger the full documentation sync pipeline. | problem_spec.md | Must Have |
| FR-2 | The system shall scan a defined set of canonical repository files (`app.py`, `models.py`, `routes.py`, `forms.py`, `requirements.txt`, and one additional config file) and make their contents available for fact extraction. | problem_spec.md | Must Have |
| FR-3 | The system shall extract structured facts from scanned files via `extractor.py`; any field for which information cannot be determined shall be represented as the literal string `"Not Specified"` rather than null, empty, or raising an error. | problem_spec.md | Must Have |
| FR-4 | The system shall produce a Markdown-formatted technical profile document via `page_creator.py`, suitable for publication to a Confluence Documentation space, with each pipeline run creating a new, distinctly versioned page rather than overwriting existing content. | problem_spec.md | Must Have |
| FR-5 | The system shall maintain a test suite comprising unit tests for `doc_sync` modules, `extractor`, and `repo_scanner`; at least one integration test covering the full pipeline; and end-to-end Playwright tests covering the Flask application UI (home, add, edit, delete, navigation). New logic introduced by this feature must include corresponding unit tests. | Derived — test coverage requirement | Should Have |

## 3. Non-Functional Requirements

| ID | Requirement | Metric |
|---|---|---|
| NFR-1 | Performance — the full sync pipeline (scan, extract, generate) shall complete within an acceptable local execution time without external blocking. | Pipeline execution completes in under 30 seconds on a standard developer workstation against the defined canonical file set. |
| NFR-2 | Reliability — missing or incomplete repository data shall not cause pipeline failure; graceful degradation using `"Not Specified"` placeholders shall allow the output document to always be produced. | 100% of pipeline runs against a partial or empty file set produce a valid Markdown output file with no unhandled exceptions. |
| NFR-3 | Maintainability — the doc-sync feature shall be implemented as a modular package (`src/doc_sync/`) with clearly separated responsibilities: scanning, extraction, and page creation. Public API surface shall be exposed through `__init__.py` via `collect_repository_facts` and `generate_problem_spec`. | Each of the three internal modules has a single well-defined responsibility; no cross-module circular imports; public API limited to the two exported functions. |
| NFR-4 | Security — the Flask application's `SECRET_KEY` shall never be stored in source control; it must be read exclusively from the OS environment at runtime via `os.environ`. | Static analysis and code review confirm no hardcoded secret values in `app.py` or any committed file; CI pipeline fails if a secret pattern is detected in the diff. |

## 4. Constraints

- Python 3.11 or higher is required for all runtime and test execution environments.
- The Flask framework (>=3.0.0) is the mandated web framework; no alternative frameworks are permitted within this project.
- SQLite is the designated database for local application state via Flask-SQLAlchemy (>=3.0.0); no external database server is required or supported in scope.
- No Confluence API credentials, tokens, or secrets of any kind may be stored in source control, environment files committed to the repository, or any artifact produced by the pipeline.

## 5. Acceptance Criteria

| ID | Criteria | Testable? |
|---|---|---|
| AC-1 | A developer can execute `python src/main.py --repo <path> --output <path>` on a local machine and the script starts the sync pipeline without error. | Yes |
| AC-2 | The pipeline scans all specified canonical repository files and includes content from each file in the extraction step. | Yes |
| AC-3 | For any repository file field or metadata item that cannot be determined from the scanned content, the output document contains the literal text `"Not Specified"` in place of that value. | Yes |
| AC-4 | The pipeline produces a Markdown technical profile document at the path specified by `--output` that is well-formed, non-empty, and contains structured sections derived from the scanned repository. | Yes |
| AC-5 | The generated Markdown document is formatted and structured such that it can be published directly to a Confluence Documentation space without manual reformatting. | Yes |
| AC-6 | Each execution of the pipeline creates a new versioned page or output file; re-running the script does not overwrite or mutate the artifact produced by a prior run. | Yes |

## 6. Out of Scope

- Automatic push or publish of the generated Markdown document to Confluence via API; the current scope ends at local file generation.
- Authentication or credential management for any Confluence instance.
- Scanning of files outside the defined set of six canonical repository files.
- Modification of the Flask Task Manager application's runtime behaviour, database schema, or existing routes (the `/delete=/<id>` URL quirk is a known issue and is explicitly excluded from this ticket).
- Continuous or scheduled synchronisation; the pipeline is triggered manually on demand only.
- Support for repository formats or version control systems other than the local file system layout described in the repository structure.
- Parsing or documentation of Python dependencies beyond those listed in `requirements.txt`.

## 7. Assumptions

- The developer running the pipeline has Python 3.11+ installed and the project dependencies from `requirements.txt` available in the active virtual environment.
- The six canonical repository files (`app.py`, `models.py`, `routes.py`, `forms.py`, `requirements.txt`, and the `src/doc_sync/__init__.py` package file) are present and readable at the path supplied via `--repo`.
- The `SECRET_KEY` environment variable is set in the developer's local environment before running the Flask application; the documentation pipeline itself does not require this variable.
- Confluence page versioning semantics (new page per run vs. version increment on an existing page) will be determined by the team at the time of Confluence integration and are not binding on the local file-generation behaviour delivered in this ticket.
- The `"Not Specified"` sentinel value is acceptable to downstream consumers (human reviewers, Confluence pages) and will not cause parsing errors in any tooling that processes the output document.
- Existing unit, integration, and E2E tests are assumed to be passing on the main branch prior to development of this feature; this ticket does not require remediation of pre-existing test failures outside the doc-sync scope.
