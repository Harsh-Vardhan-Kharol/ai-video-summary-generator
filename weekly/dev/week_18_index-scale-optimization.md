"""
Week 18 (07-12-2026 - 13-12-2026)
Task: Optimize indexing for scale

Why this matters:
The production index must avoid scanning transcript text for every semantic
lookup as the meeting archive grows.

What this script does:
Records the HNSW cosine index and bounded public search contract.
"""

The pgvector schema creates an HNSW index and `top_k` is bounded to 20 at the
API boundary. Performance targets require a representative production corpus.
