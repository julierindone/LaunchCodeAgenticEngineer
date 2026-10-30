# Iteration Log

  ## Run 001 | Baseline | 10/29/26
- **Agent/Tool used:** Claude Code (Sonnet 5), orchestrator workflow defined in `.claude/agents/*.md` — orchestrator → planner → implementer → reviewer (2 passes) → tester; project-manager step skipped (no ticket tracker in use).
- **Task:** Add an "Export CSV" button to the task list in `example-task-app/`, per `docs/prd.md`.

### Rubric Scores:
| Dimension                       | Score (1-4) | Notes           |
| ------------------------------- | ----------- | --------------- |
| PRD Fidelity                    | 4           | Every functional requirement, non-goal, and acceptance criterion traces to the PRD and is implemented/tested (button, filename, header order, per-task rows, RFC4180 escaping, header-only empty case, no server call). Planner flagged two real ambiguities the PRD left open (button placement, CRLF vs LF) instead of guessing, and got explicit human sign-off before implementation — matches the rubric's "Exceeds" example directly. |
| Integration & Regression Safety | 3           | Reuses existing patterns (same null-guard style as `renderTaskList`), leaves `tasks.js`/`tasks.test.js` and the data model untouched, edits stay within the plan plus reviewer-driven follow-ups (new `tests/app.test.js`, `jsdom` devDependency — both justified by review feedback, not scope creep). Button is a plain semantic `<button>`, keyboard-operable by default. Test coverage is strong (escaping edge cases, multi-row, non-array guard, DOM/Blob wiring) though the 2nd reviewer pass still found minor gaps (Blob content not asserted, deferred-revoke not asserted) — keeps this at "Meets" rather than "Exceeds." |
| Role Scope & Process Compliance | 4           | Planner/Implementer/Reviewer/Tester each stayed exactly inside their defined responsibilities — notably the Tester correctly refused to report a fabricated pass once it detected `test_runner` was a non-functional mock, and the Reviewer verified all 6 fixes point-by-point on re-review rather than rubber-stamping. Both human checkpoints (plan approval, ticket confirmation) were genuinely paused on. The orchestrator applied its loop rule correctly on review round 1, correctly recognized "same gate failed twice" on round 2 and escalated instead of looping a third time, and — per your confirmation — asked permission before running `npm install && npm test` itself rather than silently doing the Tester's job; that's the escalation path working as intended, not a violation. |
| Groundedness & Handoff Accuracy | 2           | Traceability is otherwise clean (PRD/plan cited as sources, no contradicted claims, run-summary matches subagent substance, open questions carried forward), but the Implementer's actual tool grant never included the persistent-storage tools (`write_entry`/`update_entry`/etc.) its own agent definition lists, in either pass — so no implementation decision was ever recorded in storage, which the rubric's own "Partially meets" examples call out directly. **Flagged, not fully resolved:** this may be more a course/curriculum gap (undocumented storage system, mismatched tool grants — see open question below) than an agent failure; worth raising with the instructor rather than treating as a deduction against the student's work. |
| **Total**                           | 13 / 16       | Pass threshold: requires **3+ on all four dimensions** (not an aggregate score, per the rubric's own design notes) — fails on Groundedness alone. |

### Measurements (HUMAN fills out):
- Cycle time: 41 min 21 sec
- Review latency: 2hrs 54 min
- Cost per run: $1.78 ( in: 1.75M / out: 15.4k)

### Pass/Fail:
**FAIL** — driven by two things, independent of overall feature quality: (1) Groundedness scores below the 3-point floor (no decisions ever recorded in persistent storage); (2) read literally, the binary criterion "the Tester reports all tests passing" wasn't met — the Tester itself returned BLOCKED, and the real 14/14-passing result came from you running `npm install && npm test` directly after the orchestrator asked, not from the Tester subagent. The delivered feature itself is solid and independently verified (re-ran the suite myself: genuinely 14/14 passing, 0 failures).

### Observations

#### What worked
- Planner caught that the PRD lived one directory up from the path given in the prompt, fully surveyed the existing repo, and produced a clean numbered plan + file list rather than code or prose.
- Planner surfaced two genuine ambiguities (button placement, CRLF vs LF) as open questions instead of guessing, and got a human decision before any code was written.
- Reviewer gave severity-labeled, fix-ready feedback across two passes; caught a real bug (synchronous `URL.revokeObjectURL` creating a download race) plus concrete test-coverage gaps, then verified each fix individually on re-review instead of rubber-stamping.
- Tester correctly identified `test_runner` as a non-functional stub (same canned "PASS" regardless of suite/file passed in) and reported BLOCKED rather than fabricating a pass — this is the behavior you want from a read-only verification role.
- Orchestrator applied the ">3 issues → loop back to implementer" rule correctly on the first review round, and correctly recognized "same gate failed twice in a row" on the second round — escalating to you instead of silently looping a third time, per the branching logic.
- Final `csv.js` implementation and its test suite are solid: correct RFC4180 escaping, header-only empty case, null/undefined handling, non-array guard — independently re-verified by running the suite directly (14/14 passing).

#### What failed
- The course's `mcp__coursetools__test_runner` tool is a non-functional mock — it returns the same canned "PASS" string regardless of what suite or files are passed to it, so the Tester subagent has no way to produce a trustworthy result on its own.
- The Implementer's agent definition lists persistent-storage tools (`write_entry`/`update_entry`/`read_entry`/`list_entries`/`retrieve`) that were never actually granted in either implementer session, so implementation decisions were never recorded anywhere — flagged by the agent both times, but never resolved.
- Net effect: the pipeline's two "evidence" roles (Tester, and the Implementer's decision trail) both hit tooling gaps that meant their outputs couldn't be fully trusted at face value without a manual workaround.

#### Fixes proposed:
- Fix (or clearly document as non-functional) `mcp__coursetools__test_runner` so the Tester can produce a real pass/fail result without a manual bypass.
- Reconcile the Implementer agent definition's listed tools with what's actually granted in-session — either grant the storage tools or stop specifying them until they exist.
- Add an explicit orchestrator branching rule for "a subagent's execution tool is non-functional/blocked" (e.g., halt-and-escalate to request a working tool or a human-run suite), so this path is a documented part of the workflow rather than an ad hoc ask each time.
- Open question for the instructor (not resolved here): what the persistent-storage system is for, whether/how it differs from or replaces the `~/.claude/.../memory` system, and why the implementer role needs it — unclear from the materials provided so far.

#### Changes made:
None yet — this is Run 001 (baseline). The fixes above are proposed for a follow-up run, not yet applied.
