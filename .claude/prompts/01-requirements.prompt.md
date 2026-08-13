# Phase 1 — Requirements Prompt

## Context
You are acting as an AI pair programmer driving Phase 1 of the Agentic SDLC pipeline for the Flask Task Manager project.

## Input
A JIRA ticket ID (e.g. KAN-27). Fetch the full ticket using the JIRA REST API configured in `.env`.

## Task
1. Display the User Story summary and description from the JIRA ticket.
2. Ask the user 4–6 clarifying questions covering:
   - Field defaults and validation rules
   - UI/UX behaviour (what the user sees)
   - Edge cases (empty state, missing data, concurrent edits)
   - Out-of-scope boundaries
3. Wait for the user to answer all questions.
4. Write `docs/artifacts/<TICKET-ID>/requirements.md` with:
   - Header table (Ticket ID, Phase, Status, Author, Date)
   - User Story (verbatim from JIRA)
   - Functional Requirements table (FR-ID, Requirement, Source, Priority)
   - Non-Functional Requirements table (NFR-ID, Requirement, Metric)
   - Constraints list
   - Acceptance Criteria table (AC-ID, Criteria, Testable?)
   - Out of Scope list
   - Assumptions list
5. Commit: `git add docs/artifacts/<TICKET-ID>/requirements.md && git commit -m "docs(<TICKET-ID>): Phase 1 requirements"`

## Quality gates
- Every FR must be testable.
- Every AC must map to at least one FR.
- No requirements invented beyond what the User Story and user answers support.
