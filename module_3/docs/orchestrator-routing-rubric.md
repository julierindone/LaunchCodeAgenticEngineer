# Quality Rubric — Orchestrator Routing & Handoff Integrity

Applies to one run of the orchestrated pipeline in `.claude/agents/`: **orchestrator → planner → implementer → reviewer → tester → project-manager**. It's written for any small feature added to `example-task-app/` that's governed by a single PRD. Examples include a new export, a filter or sort control, a new task field, or input validation.

Nothing in the criteria depends on a particular feature. Wherever the rubric refers to "the PRD" or "the plan," it means whatever PRD or plan governs the run being graded. The examples are drawn from several different hypothetical features so that no single feature's details leak into the criteria.

Out of scope: `email-summarize` (not part of the feature pipeline) and `docs-reviewer.md` (currently empty). `code-reviewer` is held to the same standard as `reviewer` when someone uses it on its own.

This rubric is deliberately narrower than [the feature-quality rubric](feature-pipeline-rubric.md): it does not score whether the delivered feature matches the PRD. It scores whether the orchestration itself — routing, handoffs, tool scope, and information isolation between roles — held up. A run can deliver a correct feature while still failing every dimension here, and the reverse. Grade both rubrics independently against the same run; neither substitutes for the other.

## 1.0 Before Grading

The grader needs four inputs:

1. **The orchestrator's full invocation trace** — which subagent was called, in what order, with what input attached. This is the evidence for Routing Misfire.
2. **Every subagent's raw result document**, exactly as it left that role, before the orchestrator or next role touched it. This is the evidence for Output Format Mismatch and Context Bleed Attempt.
3. **Each role's tool-call log** alongside its agent definition's tool grant list (`.claude/agents/*.md` frontmatter). This is the evidence for Over-Broad Tool Grant.
4. **Each role's handoff brief** — the specific document the orchestrator attached when invoking it. This is the ground truth against which Context Bleed Attempt is checked: anything a role states that isn't traceable to this document is a candidate leak.

Grade all four dimensions from the trace and the handoff documents, not from whether the final feature works — that is out of scope for this rubric.

## 1.1 Dimensions

### 1.1.1 Routing Misfire
Measures whether the Orchestrator invoked each subagent in the correct order, handed it the correct input, and skipped only what the branching logic says to skip.

**Recognition cue:** a subagent runs at the wrong time, or starts from the wrong material.

### 1.1.2 Output Format Mismatch
Measures whether a subagent's output was structured so the Orchestrator or the next subagent in line could reliably read and act on it.

**Recognition cue:** the consumer of a handoff misinterprets the result, has to guess at missing structure, or stalls.

### 1.1.3 Over-Broad Tool Grant
Measures whether a subagent's tool calls were necessary for its specific task — a signal of whether its tool grant is scoped correctly, independent of whether the call itself succeeded.

**Recognition cue:** a tool call that doesn't serve the role's one job, even though the tool is on that role's grant list.

### 1.1.4 Context Bleed Attempt
Measures whether a subagent referenced information it was never handed — something that leaked outside the handoff document.

**Recognition cue:** a subagent "knows" a detail that isn't in its brief. In the in-process pattern, the handoff document is the only legitimate channel between roles, so any such detail is a leak to investigate.

---

## Scoring Guide

### 1.1.1 Routing Misfire
1. **Does not meet:** A subagent ran out of order, was handed the wrong input, or was invoked/skipped in violation of the branching logic.
   **Example:** The Orchestrator passed the raw feature request to the Implementer instead of the Planner's plan, so the Implementer designed its own approach and ignored the plan entirely.
2. **Partially meets:** Order and input are substantially correct, but a branching rule (loop, skip, halt-and-escalate) was applied loosely, or a handoff was incomplete — e.g., the Implementer received the plan but not the accompanying file list.
3. **Meets:** Every subagent ran at the correct point in the standard sequence (or down a correctly-taken skip/loop/halt branch), and received exactly the input its role definition specifies, with nothing substituted or missing.
4. **Exceeds:** As "Meets," plus a branching condition actually arose during the run (a three-plus-issue review, a failing test, a repeated gate failure), and the Orchestrator named which rule triggered and why before acting on it.

### 1.1.2 Output Format Mismatch
1. **Does not meet:** A subagent's output format caused the Orchestrator or the next subagent to misread or stall on the result.
   **Example:** The Planner returned its plan as a flowing paragraph rather than a numbered list with an explicit file list, so the Implementer couldn't cleanly extract which files to change.
2. **Partially meets:** The format is mostly usable, but the consumer must infer or dig out part of the needed structure — e.g., a file list is present but buried in prose rather than called out explicitly.
3. **Meets:** Every handoff document is in the structured form its consumer needs — a numbered plan with an explicit file list, severity-labeled review findings, a pass/fail/blocker test report, etc. — and can be parsed without interpretation or follow-up.
4. **Exceeds:** As "Meets," plus the format anticipates the next role's actual use of it beyond the minimum — e.g., the Reviewer's findings arrive pre-sorted by severity with fix examples the Implementer can act on directly.

### 1.1.3 Over-Broad Tool Grant
1. **Does not meet:** A subagent used a tool on its grant list in a way that didn't serve its specific task, meaningfully expanding its scope or context beyond the job at hand.
   **Example:** The Reviewer used `codebase_search` to roam unrelated parts of the project when reading the few modified files would have sufficed, bloating its context.
2. **Partially meets:** A tool call occurred that wasn't strictly necessary, but its cost or scope impact was negligible — e.g., one redundant `file_read` of a file already in context.
3. **Meets:** Every tool call a subagent made directly served its one job; no role reached for a tool beyond what its specific task required, even though the tool was available to it.
4. **Exceeds:** As "Meets," plus the run's tool usage (or its absence) surfaces a concrete, specific recommendation for narrowing that role's grant, and the Orchestrator or grader can point to exactly which grant line is wider than the role ever needs.

### 1.1.4 Context Bleed Attempt
1. **Does not meet:** A subagent referenced or relied on information that was never in its handoff document.
   **Example:** The Tester referred to a design trade-off the Planner had considered, even though the Tester's handoff contained only the modified files.
2. **Partially meets:** Phrasing is ambiguous enough that it's unclear whether the subagent relied on outside knowledge or coincidentally produced similar wording — worth flagging in grader notes, but not a confirmed leak.
3. **Meets:** Every claim or reference a subagent makes traces cleanly to its own handoff document; no role shows awareness of another role's input, intermediate reasoning, or prior results.
4. **Exceeds:** As "Meets," plus the grader can positively confirm the isolation — e.g., each role's result cites only material present in its own brief, and a deliberate check (comparing the brief against the result line by line) finds nothing extraneous.

## Pass Threshold

A run passes only if it scores **3 or higher on all four dimensions.**

**Reasoning:** Each dimension catches a different way the orchestration can look like it worked while actually having broken the process that's supposed to guarantee a trustworthy result. A run can route every subagent correctly (no Routing Misfire) while still leaking context between roles that are meant to be isolated. A run can keep every role's output perfectly legible to its consumer while a role quietly grabs a tool well outside its one job. Because this rubric is about the integrity of the pipeline mechanism — not the feature it produced — none of these four can be traded off against the others; a 4 on three dimensions does not excuse a 1 on the fourth.

## Notes on Threshold Design

Considered an aggregate minimum (e.g., 12/16) instead of a per-dimension floor, matching the pattern in `eval/rubric.json`. Ruled out for the same reason as that rubric: it would let a run pass with a 1 on Context Bleed Attempt — a confirmed cross-role leak — as long as routing, formatting, and tool scope all scored 4. A leaked detail between roles that are supposed to be isolated is exactly the kind of silent failure a per-dimension floor exists to catch, so each dimension keeps its own `pass_threshold: 3`, consistent with `eval/rubric.json`'s existing convention.

If this rubric is ported into `eval/rubric.json`, add these four dimensions (routing_misfire, output_format_mismatch, over_broad_tool_grant, context_bleed_attempt) alongside or in place of the existing ones, each with `pass_threshold: 3`, and set `overall_pass_threshold` to match whichever set of dimensions is in use.
