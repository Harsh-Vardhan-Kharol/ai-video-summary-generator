"""
Week 17 (30-11-2026 - 06-12-2026)
Task: Test indexing and retrieval speed

Why this matters:
Retrieval must return current evidence and honor the requested session scope.
The test path needs to reveal accidental cross-session collisions.

What this script does:
Records semantic-search coverage, including session-local segment identifiers.
"""

`test_embeddings_and_summaries.py` verifies current-revision retrieval and
asserts that identical segment IDs in different sessions remain independent.
