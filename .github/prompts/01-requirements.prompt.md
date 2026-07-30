---
mode: agent
description: Phase 1 — Generate requirements.md by clarifying the FLASK-001 user story with the developer
tools:
  - read_file
  - write_file
  - run_in_terminal
---

You are acting as the `requirements` agent for SDLC Phase 1.

Read the user story from #file:docs/artifacts/FLASK-001/problem_spec.md.

Then ask the developer the following clarifying questions and wait for answers before writing any document:

1. Should the pipeline support any output format other than Markdown (e.g., HTML, Confluence wiki markup)?
2. Should "Not Specified" fields be omitted from the output or included with the placeholder text?
3. Is there a maximum file size limit for the generated technical profile document?
4. Should the script accept command-line arguments (e.g., `--repo-path`, `--output-path`) or use hardcoded defaults?
5. Are there any additional repository files beyond the six listed that should be scanned in future iterations?

After receiving answers, generate `docs/artifacts/FLASK-001/requirements.md` that captures:
- The original user story verbatim
- A clarifications log with your questions and the developer's answers
- Functional requirements (FR-01 through FR-0N) with acceptance criteria and priority
- Non-functional requirements (NFR-01 through NFR-0N) with measurable metrics
- Explicit out-of-scope items
- Assumptions and dependencies
- A sign-off checklist

When done, run: `python scripts/state_manager.py complete 1`
