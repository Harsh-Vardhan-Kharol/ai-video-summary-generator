"""
Week 20 (19-12-2026 - 25-12-2026)
Task: Build the RAG query API endpoint

Why this matters:
The frontend needs a single safe query boundary instead of direct graph or
database access. It must make insufficient evidence explicit.

What this script does:
Records the POST /v1/query endpoint supplied by backend/app/main.py.
"""

The endpoint accepts a question, optional session scope, and bounded `top_k`.
It returns an answer, exact citations, evidence status, and retrieval metadata.
