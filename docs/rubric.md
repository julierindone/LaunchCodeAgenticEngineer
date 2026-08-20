# 1. Quality Rubric

## 1.1 Dimensions

### 1.1.1 Build Result Accuracy
Measures whether the agent correctly identified the final outcome of the Docker build. A high score requires the stated result, success or failure, to match the actual exit status of the build command.

### 1.1.2 Warning and Error Coverage
Measures how completely the agent captured warnings and errors from the build output. A high score requires all messages at warning level or above to appear in the summary, with no material omissions. 

### 1.1.3 Recommendation Consistency
Measures whether the agent’s final recommendation follows logically from the build result and the summary it produced. A high score requires the recommendation to be both directionally correct and supported by the evidence the agent cited.

## 1.2 Alternatives Considered
* A binary pass/fail checklist. Ruled out because it can't distinguish a near-miss from a complete failure, and can't capture partial credit.