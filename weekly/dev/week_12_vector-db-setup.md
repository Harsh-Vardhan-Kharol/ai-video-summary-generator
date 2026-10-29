"""
Week 12 (20-10-2026 to 26-10-2026)
Task: Set up the vector DB for embeddings

Why this matters:
Transcript revisions are the canonical evidence for every later summary and
RAG citation. The vector index is a rebuildable projection of that evidence,
so it must retain both a segment identifier and its exact revision without
becoming a second source of truth.

What this script does:
Documents the pgvector production table and the offline-compatible embedding
index implemented in backend/app/embeddings.py, with API tests in
backend/tests/test_embeddings_and_summaries.py.
"""

## Implementation record

`schema_postgres.sql` provisions `transcript_embeddings` with pgvector's
`vector(1536)` type and an HNSW cosine index. The SQLite fixture now contains
the same key and provenance columns, storing the deterministic development
vector as JSON so CI does not need an external provider.

`TranscriptRepository.accept()` indexes each accepted immutable transcript
revision atomically with its canonical row. `EmbeddingRepository.search()`
returns only the latest revision for each segment and can limit to selected
sessions. It is deliberately a derived, replaceable index; the graph/RAG layer
continues to cite canonical transcript evidence.

## WEEK OUTPUT CONTRACT

Input: accepted transcript segment `{segment_id, revision, text}`.

Output: one derived embedding keyed by `{segment_id, segment_revision}` and a
semantic-retrieval seam that returns those immutable evidence identifiers.
