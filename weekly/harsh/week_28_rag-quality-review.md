"""
Week 28 (13-02-2027 - 19-02-2027)
Task: Review RAG answer quality across test cases

Why this matters:
The thesis evaluation must distinguish retrieval support from language fluency.
The baseline can be reviewed offline and replaced by provider evaluation later.

What this script does:
Defines the manual review categories used for answer quality.
"""

Review categories: factual support, coverage, citation correctness, revision
currency, scope filtering, and insufficient-evidence behavior.

# WEEK OUTPUT CONTRACT:
# Input: test questions, answer, citations, and reference transcript.
# Output: evidence-backed quality notes and prioritized defects.
