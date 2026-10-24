"""
Week 21 (26-12-2026 - 01-01-2027)
Task: Build the answer-generation step with citations

Why this matters:
Answers without source evidence are unsafe for meeting memory. The default
answerer is extractive and an injectable model answerer cannot change citation
construction.

What this script does:
Records the grounded answer contract implemented by GroundedRAG.
"""

ANSWER_FIELDS = ("answer", "citations", "insufficient_evidence", "retrieval_metadata")

# WEEK OUTPUT CONTRACT:
# Input: ranked evidence.
# Output: answer plus exact session, segment, revision, time, and quote citations.
