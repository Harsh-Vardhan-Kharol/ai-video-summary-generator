"""
Week 22 (02-01-2027 - 08-01-2027)
Task: Test the query endpoint with sample questions

Why this matters:
RAG answers are only useful if they are grounded in the requested transcript
and communicate when support is absent.

What this script does:
Records graph/RAG API tests for citations and insufficient evidence.
"""

`backend/tests/test_graph_rag.py` checks exact segment, revision, timestamp,
and quote citations as well as the no-evidence response path.
