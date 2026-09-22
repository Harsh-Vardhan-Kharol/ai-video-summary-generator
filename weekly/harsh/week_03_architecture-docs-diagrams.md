"""
Week 03 (24-08-2026 - 30-08-2026)
Task: Draft architecture docs and component diagrams

Why this matters:
The Week 2 boundaries need a single visual representation that the team and
faculty can use to check data ownership and evidence flow. These diagrams
become the reference for API alignment in Week 4 and architecture sign-off in
Week 5.

What this script does:
This design note documents the component, live-update, and historical-query
flows in Mermaid diagrams with the assumptions used for early mock work.
"""

# Week 3 — architecture documentation and diagrams

## Component diagram

```mermaid
flowchart LR
    C[Capture] --> A[ASR and diarization]
    A --> N[Summarization and extraction]
    A --> S[(PostgreSQL)]
    N --> S
    S --> E[Embedding/index worker]
    E --> V[(Vector index)]
    S --> G[Knowledge graph linker]
    G --> K[(Graph relationships)]
    F[Next.js frontend] --> B[FastAPI backend]
    B --> R[RAG query service]
    R --> S
    R --> V
    R --> K
    R --> B
    B --> F
```

## Live meeting update flow

```mermaid
sequenceDiagram
    participant Capture
    participant ASR as ASR/Diarization
    participant NLP as Summary/Extraction
    participant Store as Storage
    participant UI as Frontend

    Capture->>ASR: ordered audio chunk
    ASR->>Store: transcript.segment (provisional/final)
    ASR->>NLP: stable transcript segment
    NLP->>Store: summary.update + extraction.update
    Store-->>UI: live transcript/summary update
    Note over Store: Evidence IDs retained on every derived record
```

## Historical question flow

```mermaid
sequenceDiagram
    participant User
    participant API as Backend API
    participant RAG
    participant DB as Postgres + Vector Index + Graph

    User->>API: question and optional session filters
    API->>RAG: validated query
    RAG->>DB: hybrid retrieval and graph expansion
    DB-->>RAG: ranked evidence with source IDs
    RAG-->>API: answer, citations, confidence/status
    API-->>User: cited answer or insufficient-evidence response
```

## Storage model at this stage

PostgreSQL stores sessions, transcript segments, summary versions, extracted
records, and citation provenance. The vector index stores embeddings for
searchable records and references their canonical IDs. The graph stores
relationships such as `PERSON MENTIONED_IN SESSION`, `ACTION_ITEM OWNED_BY
PERSON`, and `DECISION SUPPORTED_BY SEGMENT`. It does not become an alternate
copy of raw transcript data.

## Assumptions for early fixtures

- Audio, ASR, and LLM providers are swappable adapters, not architecture
  dependencies.
- Speaker labels may be anonymous (for example, `SPEAKER_00`) until identity
  resolution is available.
- Search and answer generation must return an explicit insufficient-evidence
  result instead of inventing a response.

## WEEK OUTPUT CONTRACT

**Input:** Week 2 service and payload boundaries.

**Output:** Reusable component and sequence diagrams plus a storage-role
statement. The diagrams describe the expected chain for the eventual weekly
integration demo.
