"""
Week 20 (19-12-2026 - 25-12-2026)
Task: Set up retrieval logic over the knowledge graph/embeddings

Why this matters:
Retrieval must work before external embeddings are configured. The offline
retriever provides deterministic lexical evidence while leaving a provider seam.

What this script does:
Exposes the GroundedRAG retrieval contract used by `/v1/query`.
"""

from backend.app.rag import GroundedRAG

__all__ = ["GroundedRAG"]

# WEEK OUTPUT CONTRACT:
# Input: question, optional session IDs, and top_k.
# Output: ranked transcript evidence with immutable citations.
