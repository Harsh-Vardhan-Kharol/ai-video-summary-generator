"""
Week 21 (26-12-2026 - 01-01-2027)
Task: Connect the endpoint to Harsh's RAG pipeline

Why this matters:
Harsh owns grounded retrieval and answer generation; Dev owns its HTTP and UI
integration point. The handoff must not duplicate graph logic.

What this script does:
Records the GroundedRAG dependency injection in the FastAPI app.
"""

`/v1/query` delegates to `GroundedRAG` and returns its cited response model.
The offline fallback is deterministic until a provider answerer is approved.
