# Harsh implementation progress

The original checkout did not include the referenced `docs/` folder or a
runtime `ml/rag` module. The documented Weeks 1–15 design artifacts were
present, but graph persistence and RAG execution were still scaffolds.

Implemented in this pass:

- evidence-backed graph schema for SQLite and PostgreSQL;
- producer-compatible graph ingestion and records endpoint;
- revision-aware graph invalidation;
- offline-first cross-session retrieval and cited `/v1/query` endpoint;
- tests covering graph validation, citations, insufficient evidence, and
  revision correction behavior.

External LLM/embedding providers remain optional. The default path is fully
offline and safe for thesis demonstrations; provider integration should be
added behind the `GroundedRAG.answerer` seam after credentials and a real
embedding contract are agreed with Dev and Garvit.
