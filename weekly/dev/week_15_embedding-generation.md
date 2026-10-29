"""
Week 15 (14-11-2026 - 20-11-2026)
Task: Build the embedding-generation pipeline

Why this matters:
Embeddings make later cross-session retrieval efficient while transcripts
remain the authoritative evidence. The pipeline must work before a provider is
chosen.

What this script does:
Documents the deterministic hashing embedder in backend/app/embeddings.py.
"""

The `hashing-v1` fallback is dependency-free and normalizes vectors for cosine
search. A provider embedder can replace it behind `EmbeddingRepository` without
changing stored segment/revision provenance.
