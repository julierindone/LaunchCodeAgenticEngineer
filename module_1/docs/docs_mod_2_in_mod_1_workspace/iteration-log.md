# Iteration Log

## Run 001 | 9/05/26 | Baseline
- **Agent/Tool used:** Claude
- **Task:** Edit a technical blog post through several rounds of revision.
- **Prompt:**
 
	```md
	I need your help editing a technical blog post through several rounds of revision.
	We will work through this in stages, and I need you to apply a consistent style guide throughout. Here is the style guide -- memorize it, because every edit you make must follow these rules:
	STYLE GUIDE (apply to all edits):
	- Never use passive voice. Always rewrite passive constructions as active voice.
	- Sentences must be 25 words or fewer. Split any longer sentence into two.
	- Never use the word "utilize" -- replace it with "use"
	- Never use the word "leverage" -- replace it with "use" or "build on"
	- Technical terms must be bolded on first use in each section
	- Every section must end with a one-sentence summary starting with "In short:"
	- Oxford comma required in all lists
	Here is the blog post. Please read it carefully but do not edit anything yet -- just confirm you have read it and understood the style guide.
	---
	BLOG POST: Getting Started with API Integration
	Introduction APIs are utilized by developers to connect different software systems together. When you leverage an API, you are essentially sending a request to a remote server and waiting for a response to be returned to you. This response can then be processed by your application in whatever way is needed.

	Authentication Most APIs require authentication, which is handled through API keys or tokens. These credentials are sent with each request, and they are validated by the server before a response is given. If invalid credentials are provided, a 401 error will be returned.
	Making Requests HTTP requests are made using methods like GET, POST, PUT, and DELETE. A GET request is used when data needs to be retrieved, while POST is utilized when new data needs to be created on the server. The response that is returned will include a status code, headers, and usually a body containing JSON data that can then be parsed.

	Error Handling Errors in API integrations are often caused by network issues, invalid input, or rate limiting applied by the provider. It is recommended that retry logic be implemented with exponential backoff for transient errors. Permanent errors, such as 404 or 400 responses, should be surfaced to the user rather than retried.
	```

### Rubric Scores:
| Dimension                                         | Score (1-4) | Notes                                            |
| ------------------------------------------------- | ----------- | ------------------------------------------------ |
| Rule Accuracy — correct rule version per section? | 4           | End post followed all rules.                     |
| Task Adherence — tracked which rules changed?     | 4           | Acknowledged, Tracked, and recapped all changes. |
| Coherence — internally consistent final post?     | 4           | Consistent throughout                            |
| Total                                             | 12 / 12     | Pass threshold:                                  |

### Measurements:
- Cycle time: 24 min 40 sec
- Review latency: 38 min
- Cost per run: $0.22 ( 728.8k in / 25.2k out)

### Pass/Fail: Pass

### Observations

#### Questions from Text:
- Which rules were misapplied and in which messages? **None.**
•	Whether errors were omission (forgot a rule existed) or commission (applied an old rule post-change): **Neither.**
•	A one-sentence description of the most significant drift observed **N/A**

#### What worked
The whole thing worked perfectly. It seems like the text was expecting the activity to use up more of the ctx; after completing it and creating a markdown file with the final version, it was still only at 7%, so I'm thinking that's why.  

#### What failed
None

#### Fixes proposed:
None

---
---

## Run 002 | 9/07/26
- **Agent/Tool used:** Claude
- **Task:** Edit a technical blog post through several rounds of revision.
- **Prompt:** see Run 001
 
### Rubric Scores:
| Dimension                                         | Score (1-4) | Notes                                            |
| ------------------------------------------------- | ----------- | ------------------------------------------------ |
| Rule Accuracy — correct rule version per section? | 4           | End post followed all rules.                     |
| Task Adherence — tracked which rules changed?     | 4           | Acknowledged, Tracked, and recapped all changes. |
| Coherence — internally consistent final post?     | 4           | Consistent throughout                            |
| Total                                             | 12 / 12     | Pass threshold:                                  |

### Measurements:
- Cycle time: 21 min 24 sec
- Review latency: 17 min
- Cost per run: $0.50 ( 642.6k in / 18.3k out)

### Pass/Fail: Pass

### Observations

#### Questions from Text:
Same answers as above:
- Which rules were misapplied and in which messages? **None.**
•	Whether errors were omission (forgot a rule existed) or commission (applied an old rule post-change): **Neither.**
•	A one-sentence description of the most significant drift observed **N/A**

#### What worked
Same as run 001
The whole thing still worked perfectly. Something I noticed is the difference in tone between the runs - run 001 was straight-to-the-point, while run 002 kept a more casual tone.

#### What failed
None

#### Fixes proposed:
None

## Run 003 | 9/08/26
- **Agent/Tool used:** Claude
- **Task:** Edit a technical blog post through several rounds of revision.
- **Prompt:** see Run 001
 
### Rubric Scores:
| Dimension                                         | Score (1-4) | Notes                                            |
| ------------------------------------------------- | ----------- | ------------------------------------------------ |
| Rule Accuracy — correct rule version per section? | 4           | Correct current ruleset throughout process.      |
| Task Adherence — tracked which rules changed?     | 4           | Acknowledged, Tracked, and recapped all changes. |
| Coherence — internally consistent final post?     | 4           | Consistent throughout                            |
| Total                                             | 12 / 12     | Pass threshold:                                  |

### Measurements:
- Cycle time: 38:35
- Review latency: 17 min
- Cost per run: $0.17 ( 193.3K in / 4.4k out)

### Pass/Fail: Pass

### Observations

#### Questions from Text:
Same answers as above:
- Which rules were misapplied and in which messages? **None.**
•	Whether errors were omission (forgot a rule existed) or commission (applied an old rule post-change): **Neither.**
•	A one-sentence description of the most significant drift observed **N/A**

#### What worked
Same as run 001 & 002
The whole thing still worked perfectly. The final pass rethought the bolding and bolded a few more terms.

#### What failed
None

#### Fixes proposed:
None

---
---

## Run 004 | 9/09/26
- **Agent/Tool used:** Claude
- **Task:** Edit a technical blog post through several rounds of revision.
- **Prompt:** see Run 001

### Rubric Scores:
| Dimension                                         | Score (1-4) | Notes                                                                    |
| ------------------------------------------------- | ----------- | ------------------------------------------------------------------------ |
| Rule Accuracy — correct rule version per section? | 4           | Slight fluctuation with bolding; phase 2 corrected phase 1 inaccuracies. |
| Task Adherence — tracked which rules changed?     | 4           | Acknowledged, Tracked, and recapped all changes.                         |
| Coherence — internally consistent final post?     | 4           | Final post adhered to all styling.                                       |
| Total                                             | 12 / 12     | Pass threshold:    9                                                     |

### Measurements:
- Cycle time: 25:18
- Review latency: 21min
- Cost per run: $0.49 ( 286.5k in 23.1k out)

### Pass/Fail: Pass

### Observations

#### Questions from Text:
Same answers as above:
- Which rules were misapplied and in which messages? **None.**
•	Whether errors were omission (forgot a rule existed) or commission (applied an old rule post-change): **Neither.**
•	A one-sentence description of the most significant drift observed **N/A**

#### What worked
Output followed all rules. perfectly. The final pass rethought the bolding and bolded a few more terms.

#### What failed
None

#### Fixes proposed:
None

#### Questions from text:
1. Did phase two orient correctly from the handoff alone?  Yes
2. Any handoff gaps that caused problems? No
3. How did phase two compare to the original baseline? Same amount of accuracy.
4. Was the boundary visible in output quality, positively or negatively? No.
