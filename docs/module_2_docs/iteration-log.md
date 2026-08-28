# Iteration Log

## Run 001 | 8/28/26 | Baseline
- **Agent/Tool used:** Claude
- **Task:** When asked to summarize email or send email summaries to Slack, cecks new Gmail messages and post a summary to the #general Slack channel.

### Rubric Scores:
**I'm not doing this - the wrong rubric was in the repo, and I've spent way too much time troubleshooting in this lesson to be waste any more writing one for this.**

| Dimension | Score (1-4) | Notes           |
| --------- | ----------- | --------------- |
|           |             |                 |
|           |             |                 |
|           |             |                 |
| Total     | {X / Y}     | Pass threshold: |

### Measurements:
**There was no status bar, and none of these things were displayed, I guess because Claude was used as a background process.**
- Cycle time:
		Start: 2026-08-28T22:14:22
		Actually finished: 15:53
- Review latency: {X min}
- Cost per run: ${X.XX} ({token input} in / {token output} out)

### Pass/Fail: Being that this wasted 1.5 hours of my life to send 10 emails to Slack, I would call that a fail.

### Observations

#### What worked
Once I troubleshooted the heck out of it, it did what i asked.
#### What failed
1. The command. It took (my desktop) Claude and I at least 10 attempts before we came up with the right syntax and the right combinations of flags and values before it would work. This is what (finally) did:
   `claude -p --agent email-summarize --allowedTools="mcp__gmail__search_emails,mcp__gmail__read_email,mcp__slack__slack_list_channels,mcp__slack__slack_post_message" "Fetch 10 newest unread Gmail messages, summarize each one, post the result to #general, and confirm success."`
2. Too many emails. Had to alter prompt for newest 10 only.

#### Changes made:
None - baseline