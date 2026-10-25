"""
Week 28 (13-02-2027 - 19-02-2027)
Task: Log accuracy issues found

Why this matters:
Known limitations need to be visible rather than hidden behind an aggregate
confidence number. This list directs post-evaluation fixes and explains the
remaining human-review boundary to evaluators.

What this script does:
Records accuracy limitations discovered from deterministic fixture evaluation.
"""

# Accuracy issue log

| ID | Issue | Impact | Current handling |
| --- | --- | --- | --- |
| NLP-01 | Lexical support can flag a correct paraphrase for review. | Medium false-review rate. | `review_required`; no graph persistence until accepted. |
| NLP-02 | LLM output quality is unverified without configured provider credentials. | High release evidence gap. | Fixture tests remain deterministic; live evaluation is blocked. |
| NLP-03 | Relative dates such as Friday cannot become an ISO date without meeting timezone/date. | Medium scheduling ambiguity. | Preserve `due_date_text`; leave `due_at` null. |
| NLP-04 | A speaker label is not a person identity. | High cross-session identity risk. | Never assign an owner from `SPEAKER_nn`; retain unassigned/uncertain state. |
| NLP-05 | Current frontend hard-codes AI content and backend has no summary API. | High live-display integration gap. | Contract documented; Dev endpoint/UI binding required. |
