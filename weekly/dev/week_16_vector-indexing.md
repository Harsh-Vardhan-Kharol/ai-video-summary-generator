"""
Week 16 (21-11-2026 - 29-11-2026)
Task: Connect embeddings to vector DB indexing

Why this matters:
Every accepted transcript revision needs an index entry, otherwise retrieval
can silently lag behind the transcript visible to the user.

What this script does:
Documents automatic revision indexing and pgvector HNSW schema support.
"""

Embedding rows are keyed by session, segment, and revision. PostgreSQL uses
`vector(1536)` plus HNSW cosine indexing; SQLite stores the same projection as
JSON for offline verification.
