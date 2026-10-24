# Architecture and Harsh-owned runtime boundary

The system is a modular monolith with explicit event contracts:

```text
capture/ASR -> revisioned transcript evidence -> NLP extraction
                                      |              |
                                      +--> PostgreSQL/SQLite canonical store
                                                       |
                                      graph records <--+
                                                       |
                                      /v1/query -> cited grounded answer
```

PostgreSQL is the production canonical store. The local SQLite fixture uses the
same logical schema so tests are deterministic. Graph entities, action items,
relationships, and evidence are relational records rather than a mandatory
Neo4j dependency; this keeps the design explainable and replaceable.

Harsh's boundary is `backend/app/graph_repository.py` and `backend/app/rag.py`:

- Graph ingestion accepts Garvit-compatible entity/action-item payloads, maps
  shorthand evidence IDs to revision 1, rejects unsupported records, and never
  guesses an owner or due date.
- A higher transcript revision preserves old evidence but marks dependent graph
  records `needs_review`.
- `/v1/query` performs deterministic token-overlap retrieval in the offline
  fixture and returns an answer only with exact segment, revision, timing, and
  quote citations. A provider-backed answerer can be injected later.
- The frontend consumes `/v1/query` and `/v1/sessions/{id}/records`; it never
  accesses graph or storage tables directly.
