# Architecture — FLASK-001: Automated Documentation Sync

| Field | Value |
|---|---|
| Ticket ID | FLASK-001 |
| Phase | 2 — Architecture |
| Status | Complete |
| Author | SDLC Pipeline (architecture agent) |
| Date | 2026-07-30 |

## 1. Architecture Overview

The FLASK-001 feature implements a three-stage sequential pipeline that automates the generation of technical documentation from a Flask application repository. The pipeline reads a fixed set of canonical source files, extracts structured facts about the project into a normalized schema, and renders those facts into a versioned Markdown technical profile intended for publication to Confluence. Each stage is encapsulated in its own module within the `src/doc_sync/` package, enabling independent testing and future extension without altering the overall pipeline contract.

## 2. Component Diagram

```
CLI Entry Point
src/main.py
  --repo <path>
  --output <path>
       |
       v
+----------------+       +----------------+       +--------------------+
|   Scanner      | ----> |   Extractor    | ----> |   Page Creator     |
| repo_scanner.py|       | extractor.py   |       | page_creator.py    |
+----------------+       +----------------+       +--------------------+
       |                        |                          |
  Reads 6 canonical       Parses raw file           Renders structured
  repo files from         content into              facts into versioned
  filesystem              structured facts          Markdown document
  (app.py, models.py,     Returns "Not              written to --output
   routes.py, forms.py,   Specified" for            path
   requirements.txt,      absent fields
   tests/)
                                 |
                    collect_repository_facts()
                    generate_problem_spec()
                    (exported via __init__.py)
```

## 3. Component Responsibilities

| Component | File | Responsibility |
|---|---|---|
| Repo Scanner | `src/doc_sync/repo_scanner.py` | Reads the 6 canonical repository files from the path supplied by the CLI; returns raw file content as a dictionary keyed by logical file name; raises on missing required files |
| Extractor | `src/doc_sync/extractor.py` | Accepts raw file content dictionary; applies regex and structural parsing to derive structured facts (routes, models, dependencies, secret management strategy, test count); returns "Not Specified" for any field that cannot be determined |
| Page Creator | `src/doc_sync/page_creator.py` | Accepts the structured facts dictionary; formats content into a Markdown technical profile document with versioning metadata; writes the final artifact to the configured output path |
| Package Init | `src/doc_sync/__init__.py` | Exposes the public API of the `doc_sync` package; exports `collect_repository_facts` (wraps Scanner + Extractor) and `generate_problem_spec` (wraps Page Creator) for use by the CLI entry point and external callers |
| CLI Entry Point | `src/main.py` | Parses `--repo` and `--output` CLI flags; orchestrates the full pipeline by calling `run_pipeline()`; provides human-readable console output and non-zero exit codes on failure |
| Test Suite | `tests/` | Validates all pipeline stages at unit, integration, and E2E levels; unit tests cover each module in isolation, integration tests cover the full pipeline with a fixture repository, and E2E tests cover the live Flask application via Playwright |

## 4. Data Flow

1. **CLI Trigger** — Developer executes `python src/main.py --repo <repo_path> --output <output_path>`; the argument parser validates both flags and invokes `run_pipeline()`.
2. **Scan Phase** — `repo_scanner.py` traverses the repository at `<repo_path>` and reads the 6 canonical files (`app.py`, `models.py`, `routes.py`, `forms.py`, `requirements.txt`, and the `tests/` directory listing); raw content is assembled into a string-keyed dictionary.
3. **Extract Phase** — `extractor.py` receives the raw content dictionary; regex patterns and line-level parsing extract structured facts including route definitions, model fields, declared dependencies, secret key sourcing strategy, and test file names; any unresolvable field is set to the sentinel string `"Not Specified"`.
4. **Fact Aggregation** — `collect_repository_facts()` (exported from `__init__.py`) merges the scan and extract outputs into a single normalized facts dictionary that is the canonical intermediate representation of the repository state.
5. **Spec Generation** — `generate_problem_spec()` (exported from `__init__.py`) passes the facts dictionary to `page_creator.py`; the page creator prepends a run timestamp and incremental version identifier to support the "each run creates a new versioned page" requirement (AC-6).
6. **Markdown Render** — `page_creator.py` interpolates facts into a Markdown template, formatting routes, models, and dependency lists as structured tables and code blocks; missing facts appear as `"Not Specified"` in the rendered output (AC-3).
7. **Artifact Output** — The completed Markdown document is written to `<output_path>`; `src/main.py` prints a success message including the resolved output path and exits with code 0; the artifact is ready for manual or automated upload to the Confluence Documentation space (AC-4, AC-5).

## 5. Technology Choices

| Area | Choice | Rationale |
|---|---|---|
| Implementation language | Python 3 | Consistent with the Flask application under documentation; no additional runtime required on developer machines already running the app |
| File reading and path handling | `pathlib.Path` + built-in `open()` | `pathlib` provides cross-platform path manipulation with an idiomatic API; avoids third-party dependency for a straightforward filesystem read task |
| Content extraction | `re` (standard library regex) | Sufficient for the deterministic patterns present in Flask route decorators, SQLAlchemy model field definitions, and `requirements.txt` dependency lines; no external parsing library needed |
| Output format | Markdown (`.md`) | Human-readable without tooling; directly renderable by Confluence's Markdown macro and most wiki engines; version-controllable as plain text; decouples the sync script from Confluence API availability |
| Application database | SQLite via Flask-SQLAlchemy | Appropriate for a single-developer task manager; zero-configuration, file-backed, and fully supported by SQLAlchemy's ORM abstraction |
| Secret management | Environment variable via `os.environ` | Removes hardcoded `SECRET_KEY` from source control; compatible with `.env` files loaded by python-dotenv and with container/CI environment injection patterns |

## 6. Security Design

**SECRET_KEY Management** — The Flask `SECRET_KEY` was previously hardcoded in `app.py` and has been remediated to read exclusively from `os.environ['SECRET_KEY']`. The application will raise a `KeyError` at startup rather than silently operate with a weak or known key if the variable is absent, making misconfiguration visible immediately. Deployment environments must supply this value via a `.env` file (excluded from version control via `.gitignore`) or through a secrets manager injected at runtime.

**No PII in Generated Output** — The doc sync pipeline reads only structural source files (`app.py`, `models.py`, `routes.py`, `forms.py`, `requirements.txt`, and test directory listings). None of these files contain user data, database content, or credentials. The extractor is scoped to code-level facts; it does not read SQLite database files, log files, or environment files, ensuring no personally identifiable information or runtime secrets can appear in the generated Markdown artifact.

**File Write Boundaries** — The page creator writes exclusively to the path supplied via the `--output` CLI flag. There is no dynamic path construction from repository content, preventing a maliciously crafted repository from redirecting output to arbitrary filesystem locations. The calling developer is responsible for ensuring the output path is within an appropriate workspace directory before executing the script.

## 7. Test Architecture

| Layer | Directory | Count | Purpose |
|---|---|---|---|
| Unit | `tests/unit/` | 9 tests across 3 files | Validates individual module behaviour in isolation using mocked filesystem and fixture data; covers `doc_sync` package (4 tests in `test_doc_sync.py`), extractor logic (2 tests in `test_extractor.py`), and repo scanner logic (3 tests in `test_repo_scanner.py`) |
| Integration | `tests/integration/` | 1 test in `test_pipeline.py` | Executes the full Scanner → Extractor → Page Creator pipeline against a controlled fixture repository on the real filesystem; asserts that the output Markdown document is produced and contains expected structured content |
| End-to-End | `tests/e2e/` | 10 tests in `test_app_ui.py` | Drives the live Flask application through a real browser using Playwright; covers the home page render, task addition via `/add`, task editing via `/edit/<id>`, task deletion via `/delete=/<id>`, and navigation flows; validates the application's user-facing behaviour independently of the documentation pipeline |

## 8. Architecture Decision Records

### ADR-001: Three-stage pipeline over monolithic script

**Status:** Accepted

**Context:** The initial implementation could have been written as a single script that reads files, parses them, and writes output in sequence. As the scope expanded to include multiple canonical files, a structured intermediate representation, and the "Not Specified" sentinel requirement, a monolithic approach would have made individual stages difficult to unit-test in isolation and would have coupled I/O concerns with parsing logic.

**Decision:** Decompose the pipeline into three discrete modules — `repo_scanner.py` (I/O), `extractor.py` (parsing and normalization), and `page_creator.py` (rendering) — each with a single responsibility and a well-defined interface. The `__init__.py` composes them into two public functions that the CLI entry point consumes.

**Consequences:** Each stage can be unit-tested independently with mocked inputs, reducing test surface complexity. The extractor can be extended to parse additional file types without modifying the scanner or page creator. The page creator can be retargeted to a different output format (e.g., HTML or reStructuredText) without affecting upstream stages. The trade-off is slightly more file overhead compared to a single script, which is acceptable given the test and maintainability benefits.

---

### ADR-002: Markdown output over direct Confluence API

**Status:** Accepted

**Context:** AC-5 requires that generated content target the Confluence Documentation space and AC-6 requires each run to create a new versioned page. The most direct implementation would use the Confluence REST API to create pages programmatically. However, this would introduce an authenticated network dependency into the local developer script, require API token management, and couple the pipeline to a specific Confluence instance URL and space key.

**Decision:** Generate a versioned Markdown document to a local output path. The developer (or a future CI step) is responsible for uploading the artifact to Confluence using the platform's Markdown import capability or a separate automation layer. Version identifiers are embedded in the document header at generation time to satisfy AC-6 without requiring stateful knowledge of previously created Confluence pages.

**Consequences:** The sync script runs entirely offline and requires no external credentials, making it safe to execute in sandboxed or air-gapped environments and trivial to test. The decoupling means Confluence publication is a manual or separately automated step rather than an automatic side effect of running the script, which is an acceptable operational trade-off for the current scope. If direct API publication becomes a requirement in a future ticket, a fourth pipeline stage (`confluence_publisher.py`) can be added without altering the existing three stages.
