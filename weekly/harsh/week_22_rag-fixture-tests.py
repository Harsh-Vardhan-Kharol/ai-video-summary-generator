"""
Week 22 (02-01-2027 - 08-01-2027)
Task: Test the RAG pipeline on sample questions

Why this matters:
Fixture questions make answer quality reproducible without credentials or
network access. The graph/RAG API tests are the executable acceptance suite.

What this script does:
Points to the deterministic test module for query, citation, and no-evidence cases.
"""

TEST_MODULE = "backend/tests/test_graph_rag.py"

# WEEK OUTPUT CONTRACT:
# Input: sample transcript and question cases.
# Output: grounded answers or explicit insufficient-evidence responses.
