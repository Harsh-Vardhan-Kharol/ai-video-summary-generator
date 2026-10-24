"""
Week 17 (30-11-2026 - 06-12-2026)
Task: Test linking logic on sample data

Why this matters:
Linking errors would create false cross-session memories. The backend test
suite exercises evidence validation, owner typing, and graph persistence.

What this script does:
Provides the standalone test command for Harsh's graph and RAG boundary.
"""

TEST_COMMAND = "python3 -m pytest -q backend/tests/test_graph_rag.py"

if __name__ == "__main__":
    print(TEST_COMMAND)

# WEEK OUTPUT CONTRACT:
# Input: graph fixture batches and transcript revisions.
# Output: repeatable validation of accepted, rejected, and review-required records.
