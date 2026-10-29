# 1. Quality Rubric — `example-task-app` feature pipeline

Applies to one run of the orchestrated pipeline in `.claude/agents/`: **orchestrator → planner → implementer → reviewer → tester → project-manager**. It's written for any small feature added to `example-task-app/` that's governed by a single PRD. Examples include a new export, a filter or sort control, a new task field, or input validation.

Nothing in the criteria depends on a particular feature. Wherever the rubric says "the PRD," it means whatever PRD governs the run being graded. The examples are drawn from several different hypothetical features so that no single feature's details leak into the criteria.

Out of scope: `email-summarize` (not part of the feature pipeline) and `docs-reviewer.md` (currently empty). `code-reviewer` is held to the same standard as `reviewer` when someone uses it on its own.

## 1.0 Before Grading

The grader needs four inputs:

1. **The governing PRD.** List its requirements, acceptance criteria, and non-goals before reading any output. That list is the checklist for PRD Fidelity.
2. **The planner's plan and file list.** This sets the authorized scope for Integration & Regression Safety and for the implementer's boundary.
3. **Every subagent's result document**, plus the stored decision entries. These are the evidence for Role Scope and Groundedness.
4. **`docs/run-summary.md`** and the project-manager's ticket-update result.

If the PRD has no section for non-goals, treat "existing behavior remains unchanged" as an implied non-goal.

## 1.1 Dimensions

### 1.1.1 PRD Fidelity
Measures whether the delivered feature implements every requirement and acceptance criterion in the governing PRD, and respects every non-goal. A high score requires each requirement to trace to a specific PRD line and be backed by code or a test, including the edge cases the PRD names (empty states, invalid input, special characters, boundary values). Delivering the headline behavior alone isn't enough.

### 1.1.2 Integration & Regression Safety
Measures whether the change fits the existing app instead of working around it:
- It reuses existing data sources, functions, and patterns rather than adding parallel ones.
- It leaves existing behavior and the data model unchanged unless the PRD explicitly allows it.
- It changes only the files in the approved plan and adds no unplanned dependencies or config.
- Its tests target the new behavior's real risks, not just the happy path.

When the feature adds UI, this dimension also covers basic accessibility: semantic, keyboard-operable controls that match the app's existing markup patterns.

### 1.1.3 Role Scope & Process Compliance
Measures whether each role stayed inside the tools and responsibilities its agent definition gives it:
- the planner doesn't write code
- the implementer doesn't run tests or delete storage entries, and writes only the files in the plan
- the reviewer is read-only and labels findings Critical / Warning / Suggestion
- the tester doesn't fix failures
- the project-manager only touches the ticket
- the orchestrator never does a subagent's work

It also checks two other things. First, both human-in-the-loop checkpoints were genuinely paused on: **plan approval** before any code is written, and **ticket confirmation** before the project-manager runs. Second, the orchestrator applied its branching rules (loop, skip, halt-and-escalate) when their conditions arose.

### 1.1.4 Groundedness & Handoff Accuracy
Measures whether claims made during the run trace to their sources:
- Retrieved facts are attributed to their `source_document`, and low-confidence keyword hits are verified before use.
- Implementation decisions are recorded in storage (`write_entry` / `update_entry`, not duplicated).
- Open questions are carried forward between roles rather than dropped.
- `docs/run-summary.md` reports exactly what the reviewer and tester returned.

The project-manager treats the run summary as its source of truth when it changes a shared ticket, so any inaccuracy in the summary ends up on that ticket.

---
## Alternatives Considered

**Keeping "Accessibility" as its own dimension, as in the sample rubric.** Ruled out for a general rubric because many features in this pipeline have little or no UI (a data export, a validation rule, a sort helper). A standalone accessibility score would be empty or trivial for those runs. Accessibility is instead a conditional criterion inside Integration & Regression Safety: it applies in full whenever the feature adds or changes UI. If a run is mostly UI work (a modal, a drag-and-drop list), graders can note the accessibility findings separately in their comments.

**Folding Groundedness into Role Scope & Process Compliance.** Ruled out because the two fail independently. Every role can stay inside its tool grants while the implementer cites a document for something it doesn't say, or the orchestrator writes "all tests passing" when the tester reported a blocker. This pipeline also has retrieval with attribution rules and persistent decision storage, which need their own criterion.

**A separate "Test Coverage" dimension.** Ruled out because "Tester reports all tests passing" is already a binary gate. Whether the tests *target the right risks* is scored under Integration & Regression Safety.

**Scoring the human checkpoints as their own dimension.** Ruled out because pausing is binary: either the orchestrator waited or it didn't. Both checkpoints are a floor condition inside Role Scope & Process Compliance and are also binary acceptance criteria below.

**Writing a separate rubric per feature.** Ruled out because the pipeline's roles, checkpoints, and handoff rules are the same for every feature; only the PRD changes. Keeping the criteria generic and pulling the requirements from the PRD at grading time (section 1.0) means scores stay comparable across features.

---

## Scoring Guide

### 1.1.1 PRD Fidelity
1. **Does not meet:** A requirement or acceptance criterion is missing or contradicted, a non-goal is violated, or the run summary claims a requirement is met when no code backs it.
   **Example:** A PRD for a "filter by status" control says filtering happens client-side and lists "no backend changes" as a non-goal. The implementation adds a server query parameter instead.
2. **Partially meets:** The main flow works, but at least one edge case or secondary requirement the PRD names is handled wrong or not at all.
   **Example:** A new "priority" field displays and saves correctly. But the PRD says tasks without a priority show "None," and they render as blank instead.
3. **Meets:** Every requirement and acceptance criterion in the PRD is implemented and traceable to its PRD line, and no non-goal is crossed.
   **Example:** An export feature produces the required file name, columns in the specified order, correctly escaped values, and the specified output for an empty list. The plan maps each of these to its PRD requirement number.
4. **Exceeds:** As "Meets," plus the run identifies a requirement interaction or ambiguity the PRD doesn't spell out, and either resolves it in line with the PRD's intent or raises it as an open question instead of guessing.
   **Example:** The planner notes that a new sort control and an existing filter could interact (does sorting apply before or after filtering?). The PRD is silent, so the planner raises it as an open question, and the human's answer is recorded before implementation starts.

### 1.1.2 Integration & Regression Safety
1. **Does not meet:** The change alters existing behavior or the data model without the PRD's permission, adds a parallel data source, or breaks an existing test.
   **Example:** To add a "due soon" badge, the implementer renames an existing task field. An existing test that asserts the field list now fails.
2. **Partially meets:** Existing behavior is intact, but the integration is fragile or goes beyond scope. Typical signs:
   - logic or data duplicated instead of reused
   - an unplanned dependency or config change
   - a non-semantic interactive element (e.g., a clickable `<div>`) when UI is involved
   - tests that cover only the happy path

   **Example:** A validation feature adds a third-party validation library to `package.json` (not in the plan) for one regex check. Its only test submits a valid value.
3. **Meets:** The change reuses existing functions and data, leaves unrelated behavior and the data model untouched, edits only planned files, and adds tests for the PRD's edge cases. Any new UI uses semantic, keyboard-operable elements consistent with the existing markup. Existing tests pass unchanged.
   **Example:** A sort feature adds a pure `sortTasks(tasks, key)` function with unit tests for ties and missing values. The existing render path calls it, and no existing test is modified.
4. **Exceeds:** As "Meets," plus the implementation anticipates an integration, robustness, or accessibility issue the PRD didn't mention and handles it the way the app already handles similar concerns.
   **Example:** The implementer keeps new logic DOM-free so it can be tested with the existing `node --test` setup, and records a decision explaining the split. Or, when a UI control re-renders the list, focus is returned to the control rather than lost.

### 1.1.3 Role Scope & Process Compliance
1. **Does not meet:** A role acts outside its tool grants or responsibilities in a way that affects the outcome, or the orchestrator skips a human checkpoint.
   **Example:** The tester loosens an assertion so a failing test passes. Or the orchestrator invokes the implementer before the human approves the plan. Or the project-manager updates the ticket without human confirmation.
2. **Partially meets:** Each role stays inside its boundary, but a handoff loses information, or a branching rule is applied loosely.
   **Example:** The reviewer returns five issues and the orchestrator moves on to the tester anyway, ignoring the "more than three issues" loop rule.
3. **Meets:** Every role works within its definition:
   - the planner produces a numbered plan and file list
   - the implementer reads the plan from storage and writes only the listed files
   - the reviewer returns labeled findings with fix examples and makes no edits
   - the tester reports pass, fail, or blocker without changing anything
   - the project-manager uses only `task_tracker`

   Both human checkpoints are genuinely paused on, and any branching rule whose condition arises is applied.

   **Example:** The orchestrator shows the plan and waits for approval, delegates each phase, writes only handoff briefs and `docs/run-summary.md`, and asks for confirmation before invoking the project-manager.
4. **Exceeds:** As "Meets," plus a branching rule actually fires during the run, is applied correctly, and the orchestrator states which rule triggered it and why.
   **Example:** The tester reports one failure. The orchestrator cites the "any failing test" loop rule, sends the failure output to the implementer, and re-runs the tester. When that phase fails a second time, it halts and escalates to the human with a short summary.

### 1.1.4 Groundedness & Handoff Accuracy
1. **Does not meet:** A claim contradicts its source, or the run summary or ticket misstates what a subagent reported.
   **Example:** The tester reports that the suite couldn't run (environment blocker), but the run summary says "all tests passing," and the ticket is marked `Done`.
2. **Partially meets:** The outcomes are reported correctly, but some claims, decisions, or open questions aren't traceable. Typical signs:
   - a retrieved fact used without naming its `source_document`
   - a keyword-only retrieval hit relied on without verification
   - significant decisions never recorded in storage
   - a planner's open question that never reaches the implementer

   **Example:** The implementer picks a date format "per the standards doc" but doesn't name the document and records no `decision` entry. A later reader can't confirm the choice.
3. **Meets:**
   - Every retrieved claim names its `source_document`.
   - Low-confidence hits are verified or flagged, and empty retrievals are noted explicitly.
   - Each significant decision is stored once and revised with `update_entry` if it changes.
   - Open questions are carried forward or answered.
   - The run summary's review and test sections match the substance of the subagents' result documents.

   **Example:** The implementer's result lists the `entry_id` of each decision, each citing its source. The run summary reports the reviewer's counts by severity and the tester's pass/fail exactly as returned.
4. **Exceeds:** As "Meets," plus the run catches and resolves a conflict between sources (two reference documents, or a document and the PRD) rather than silently picking one.
   **Example:** Two reference documents disagree on how a field should be formatted. The implementer flags the conflict, follows the PRD-aligned source, records the reasoning in a decision entry, and the run summary lists it under "Open follow-ups."

## Pass Threshold
A run passes only if **both** of these hold:

1. It scores **3 or higher on all four dimensions**.
2. It meets every binary acceptance criterion:
   - the feature behaves as the governing PRD describes
   - the Reviewer reports no unresolved Critical issues
   - the Tester reports all tests passing (a blocker isn't a pass)
   - the plan-approval checkpoint was honored
   - the ticket-confirmation checkpoint was honored

**Reasoning:** Each dimension guards a different way a run can look finished while still leaving work for the human. A spec-accurate feature can still break existing behavior. A clean integration can come from a run that skipped plan approval. A fully compliant run can still write a summary that misreports the test result onto a shared ticket. Because every run in this pipeline ends in an outward-facing action (the ticket update), Role Scope and Groundedness can't be traded off against a well-built feature.

## Notes on Threshold Design
Considered an aggregate minimum (e.g., 12/16) instead of a per-dimension floor. Ruled out because it would let a run pass with a 1 on Groundedness, such as a summary claiming tests passed when they didn't, as long as the other three dimensions scored 4. That's exactly the failure that would put a false `Done` on the ticket.

`eval/rubric.json` defines `overall_pass_threshold: 12` across four dimensions with a per-dimension threshold of 3. That's equivalent to the floor used here, so the two rubrics agree. If this rubric is ported into `eval/rubric.json`, keep the per-dimension `pass_threshold: 3` and treat the overall threshold as informational only.
