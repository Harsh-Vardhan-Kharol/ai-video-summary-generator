"""
Week 24 (16-01-2027 - 22-01-2027)
Task: Define the RAG-frontend API contract with Dev

Why this matters:
The frontend must remain independent of graph and vector storage choices.
The versioned query response is the stable seam between Harsh and Dev.

What this script does:
Documents the implemented `/v1/query` and records response shapes.
"""

`POST /v1/query` accepts `question`, optional `session_ids`, and `top_k`; it
returns `answer`, `citations[]`, `insufficient_evidence`, and
`retrieval_metadata`. Citations include session, segment, revision, time range,
and quote.

# WEEK OUTPUT CONTRACT:
# Input: frontend query JSON.
# Output: versioned cited answer JSON; no direct database access.
