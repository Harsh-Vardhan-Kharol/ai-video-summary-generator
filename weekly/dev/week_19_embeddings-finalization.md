"""
Week 19 (14-12-2026 - 18-12-2026)
Task: Finalize the embeddings pipeline

Why this matters:
Harsh's RAG work depends on stable source identifiers, not a specific embedding
vendor. This boundary keeps retrieval replaceable and explainable.

What this script does:
Documents the finalized provenance and provider-replacement seam.
"""

The API exposes only derived match IDs and scores. RAG answers continue to cite
the corresponding canonical transcript revision.
