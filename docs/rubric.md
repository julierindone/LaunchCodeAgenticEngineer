# 1. Quality Rubric
## 1.1 Dimensions

### 1.1.1 Build Result Accuracy
Measures whether the agent correctly identified the final outcome of the Docker build. A high score requires the stated result, success or failure, to match the actual exit status of the build command.
### 1.1.2 Warning and Error Coverage
Measures how completely the agent captured warnings and errors from the build output. A high score requires all messages at warning level or above to appear in the summary, with no material omissions. 
### 1.1.3 Recommendation Consistency
Measures whether the agent’s final recommendation follows logically from the build result and the summary it produced. A high score requires the recommendation to be both directionally correct and supported by the evidence the agent cited.

---
## Alternatives Considered
A binary pass/fail checklist. Ruled out because it can't distinguish a near-miss from a complete failure, and can't capture partial credit.

---
## Scoring Guide
### 1.1.1 Build Result Accuracy
1. **Does not meet:** Reports the wrong build outcome, or does not report an outcome at all.   
		**Ex:** Agent output: "I ran the build process." The build actually failed with two errors, but no outcome — success or failure — is ever stated.

2. **Partially meets:** Reports the outcome ambiguously or with missing context—e.g., says "the build had issues" without stating pass or fail.   
		**Ex:** Agent output: "The build had some issues during the process." The build failed, but "issues" never clarifies whether it ultimately succeeded or failed.

3. **Meets:** Correctly identifies whether the Docker image built successfully or failed.   
		**Ex:** Agent output: "The Docker image failed to build."

4. **Exceeds:** Correctly identifies the outcome and includes supporting evidence, such as the exit code or the final line of build output.  
		**Ex:** Agent output: "The Docker image failed to build. Exit code: 1. Final build output line: 'ERROR: failed to solve: process "/bin/sh -c npm install" did not complete successfully.'"

### 1.1.2 Warning and Error Coverage
1.	**Does not meet:** The summary omits one or more errors that appeared in the build output. A reviewer reading only the summary would have an incomplete or misleading picture of what went wrong.  
		**Ex:** Agent output reads: “The build encountered some issues and did not complete successfully.” The build log contained three distinct errors. None are named in the summary.

2.	**Partially meets:** The summary captures all errors but omits one or more warnings. The picture is not misleading, but it is incomplete.  
		**Ex:** Agent output reads: “The build failed with the following errors: missing base image tag, undefined build argument NODE_ENV. No warnings were reported.” The build log contained those two errors plus a deprecation warning for a legacy COPY syntax. The warning is absent from the summary.

3.	**Meets:** The summary captures all errors and all warnings present in the build output. Nothing material is missing.   
		**Ex:** Agent output reads: “The build failed with two errors (missing base image tag, undefined build argument NODE_ENV) and one warning (deprecated COPY syntax on line 12).” All items from the build log are present.

4.	**Exceeds:** The summary captures all errors and warnings, groups or prioritizes them, so the most important issues are immediately visible without requiring the reviewer to read the full log.   
		**Ex:** Agent output reads: “The build failed. Two errors must be resolved before the image can build: a missing base image tag (blocking) and an undefined build argument NODE_ENV (blocking). One non-blocking warning is present: deprecated COPY syntax on line 12, which will become an error in Docker 26.” Errors and warnings are separated, labeled by severity, and the warning includes forward-looking context.


### 1.1.3 Recommendation Consistency
1. **Does not meet:** The recommendation contradicts the build result; e.g., recommends proceeding after a failed build —or- no recommendation is given.  
		**Ex:** Agent output: "The build failed with two errors. Recommendation: proceed to the next step." (The recommendation directly contradicts the failed build result.)

2. **Partially meets:** The recommendation is directionally correct but is not supported by the evidence in the summary, or is too vague to act on.  
		**Ex:** Agent output: "The build failed. Recommendation: fix the issues before proceeding." (Directionally correct, but doesn't reference which specific errors need fixing — too vague to act on.)

3. **Meets:** The recommendation is consistent with the build result and follows logically from the summary produced.  
		**Ex:** Agent output: "The build failed due to a missing base image tag. Recommendation: do not proceed until the Dockerfile is corrected." (Logically follows from the stated build result.)

4. **Exceeds:** The recommendation is consistent, well-supported, and includes specific next steps that follow directly from the errors or warnings identified.  
		**Ex:** Agent output: "The build failed due to a missing base image tag in line 1 of the Dockerfile. Recommendation: add a valid tag (e.g., `node:24-slim`) to the FROM instruction, then rerun the build to confirm the fix before proceeding." (Consistent, well-supported, and gives a concrete next step tied directly to the identified error.)

## Pass Threshold
A run passes if it scores:
1. 4 on Recommendation Consistency
2. 3 or higher for the other 2 dimensions.

**Reasoning:** We need a correct pass/fail recommendation, and we need a list of all errors and warnings present, but it doesn't matter if the list is organized (4 on *Warning and Error Coverage* ), and the 4 on *Build Result Accuracy* is well covered by level 4 on *Recommendation Consistency*. The recommendation for debugging the problem would be a huge timesaver for the developer, so *Recommendation Consistency* requires a 4.

## Notes on Threshold Design
* Considered a dimension floor requiring 3+ across all three dimensions. Ruled out because a run scoring 3 on Recommendation Consistency only requires the recommendation to be logically consistent — it doesn't require concrete next steps. Given that the actionable fix is the most time-saving part of the output for a developer, a 3 wasn't a high enough bar for that specific dimension.
* Considered requiring a 4 on all three dimensions. Ruled out as overly strict.
