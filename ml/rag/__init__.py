"""RAG package boundary used by the FastAPI adapter."""

from backend.app.rag import GroundedRAG, RetrievedEvidence

__all__ = ["GroundedRAG", "RetrievedEvidence"]
