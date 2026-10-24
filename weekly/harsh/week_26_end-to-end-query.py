"""
Week 26 (30-01-2027 - 05-02-2027)
Task: Test the end-to-end query flow, frontend to RAG backend

Why this matters:
The API tests now exercise the same path the frontend uses: transcript upload,
query request, and citation response.

What this script does:
Identifies the end-to-end test module and its covered assertions.
"""

E2E_TEST = "backend/tests/test_graph_rag.py::test_query_returns_exact_citations_and_insufficient_evidence"

# WEEK OUTPUT CONTRACT:
# Input: frontend-shaped HTTP requests.
# Output: HTTP 200 grounded result with citations or honest insufficiency.
