# HANDOFF DOCUMENT

## Overall Task

The user is editing a technical blog post titled "Getting Started with API Integration" through multiple rounds of revision, one section at a time. Every edit — past and future — must conform to a fixed style guide provided at the start of the session. The goal is to fully revise all four sections (Introduction, Authentication, Making Requests, Error Handling) so the entire post follows the style guide consistently.

## Phase One Summary

Two of four sections have been edited and applied against the style guide: **Introduction** and **Authentication**. Both were rewritten to eliminate passive voice, remove "utilize"/"leverage," cap sentence length at 25 words, bold technical terms on first use within the section, and end with an "In short:" summary sentence. The user approved both sections without requesting changes. **Making Requests** and **Error Handling** have not yet been touched and remain in their original form.

## Current State of All Artifacts

**Introduction (revised, current):**

> Developers use **APIs** to connect different software systems together. When you use an API, you send a **request** to a remote server and wait for a **response**. Your application then processes that response however it needs.
>
> In short: developers use APIs to send requests to remote servers and process the responses they get back.

**Authentication (revised, current):**

> Most APIs require authentication, and developers handle it through **API keys** or **tokens**. Your application sends these **credentials** with each request, and the server validates them before it returns a response. If you provide invalid credentials, the server returns a **401 error**.
>
> In short: APIs authenticate requests using API keys or tokens, and invalid credentials trigger a 401 error.

**Making Requests (original, NOT yet edited):**

> Making Requests HTTP requests are made using methods like GET, POST, PUT, and DELETE. A GET request is used when data needs to be retrieved, while POST is utilized when new data needs to be created on the server. The response that is returned will include a status code, headers, and usually a body containing JSON data that can then be parsed.

**Error Handling (original, NOT yet edited):**

> Error Handling Errors in API integrations are often caused by network issues, invalid input, or rate limiting applied by the provider. It is recommended that retry logic be implemented with exponential backoff for transient errors. Permanent errors, such as 404 or 400 responses, should be surfaced to the user rather than retried.

## Rules and Constraints in Effect

```
STYLE GUIDE (apply to all edits):
- Never use passive voice. Always rewrite passive constructions as active voice.
- Sentences must be 25 words or fewer. Split any longer sentence into two.
- Never use the word "utilize" -- replace it with "use"
- Never use the word "leverage" -- replace it with "use" or "build on"
- Technical terms must be bolded on first use in each section
- Every section must end with a one-sentence summary starting with "In short:"
- Oxford comma required in all lists
```

Working interpretation established during phase one (not stated verbatim by the user, but applied consistently and unchallenged across both edited sections):

- "Bolded on first use in each section" means bolding resets per section — a term already bolded in an earlier section gets bolded again the first time it reappears in a new section.
- The Oxford comma rule only triggers for lists of three or more items; two-item "or"/"and" pairs (e.g., "API keys or tokens") are left without a comma.
- Each section's structural edit only affects prose within that section; the "In short:" sentence is appended as a new final sentence, not a rewrite of an existing one.

## Phase Two Instructions

1. Edit the **Making Requests** section, applying the full style guide (as done for Introduction and Authentication): eliminate passive voice, remove "utilize"/"leverage" if present, cap sentences at 25 words, bold technical terms on first use within this section, add Oxford commas to any list of three or more items, and end with an "In short:" summary sentence. Note this section already contains "utilized" ("POST is utilized") which must be replaced, and an Oxford-comma-compliant list ("GET, POST, PUT, and DELETE") that should be preserved as-is.
2. Present the revised Making Requests section to the user and wait for approval or correction before moving on, matching the turn-by-turn pattern used in phase one.
3. Edit the **Error Handling** section using the same process and constraints.
4. Present the revised Error Handling section to the user and wait for approval or correction.
5. Once all four sections are approved, offer to assemble and display the complete, fully revised blog post in one piece so the user can review it end-to-end.

## Acceptance Criteria for Phase Two

No separate acceptance criteria were specified beyond the style guide itself. The style guide, copied verbatim above, is the full and only specification for what constitutes a correct edit. Each section is correct when it satisfies all seven bullet points of that style guide.

## Known Constraints and Gotchas

- The user is proceeding section-by-section and expects each section edited only when explicitly instructed ("Now edit only the X section") — do not get ahead and edit multiple sections in one turn.
- The original post's section headers run directly into body text with no line break (e.g., "Introduction APIs are utilized..."); phase one silently reformatted headers onto their own line as part of presenting each edit, and the user raised no objection — continue this formatting convention.
- The user has not yet indicated whether bullet-point "Changes made" explanations after each section (as given in phase one responses) should continue — phase one included them each time without pushback, so continuing that pattern is reasonable, but this was never explicitly requested as a permanent requirement.
- Watch for "utilize" appearing again in Making Requests ("POST is utilized") — must be replaced with "use," consistent with the Introduction fix.
