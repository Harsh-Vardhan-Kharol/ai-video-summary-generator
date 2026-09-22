# AI Realtime Video Summary Generator — Project Context for Codex

This file gives you (the coding agent) full context on the project so you don't need it re-explained every session. Read this before making changes.

## What this project is

A system that captures video/audio — live meetings (Zoom/Meet/Teams), lectures, webinars, or uploaded recordings — transcribes it, and generates a running summary (decisions, action items, key points) instead of making the user wait until the end. It also keeps a memory across past sessions so users can ask natural-language questions like "what did we decide about X last month?" and get a cited answer.

**Core differentiators:**
- Bot-free capture where possible (system audio, not a visible bot joining the call)
- Cross-session memory via a knowledge graph + vector search (RAG), not just single-session transcripts
- Summaries update continuously, not only after the session ends

## Team & my role

4-person final-year B.Tech team. I'm **Harsh Vardhan Kharol — Team Lead**, owning:
- Overall system architecture
- The knowledge graph (entities, action items, cross-session linking)
- The RAG query pipeline (the part that answers questions across past sessions with citations)
- Integration between frontend and backend, and final integration testing / deployment

Other three members and their lanes (for context — don't touch their code without asking):
- **Dhruv Vij** — audio capture, ASR (Whisper/Deepgram), speaker diarization (Pyannote)
- **Garvit Agrawal** — NLP: summarization, action-item/NER extraction, confidence scoring
- **Dev Tak** — backend (FastAPI), database, embeddings pipeline, frontend (React/Next.js)

## Architecture (high level)

```
Audio/Video Capture (bot-free or platform integration)
        ↓
ASR + Speaker Diarization (Whisper/Deepgram + Pyannote)
        ↓
Summarization + Action-Item Extraction (LLM-based)
        ↓
Storage: Postgres (metadata) + Vector DB (embeddings) + Knowledge Graph (entity links)
        ↓
RAG Query Layer (retrieval + LLM generation, with citations)
        ↓
Frontend (React/Next.js — dashboard, search, summary view)
```

## Tech stack

| Layer | Tech |
|---|---|
| Frontend | React.js / Next.js |
| Backend | Python (FastAPI) |
| ASR / Diarization | Whisper or Deepgram + Pyannote |
| Summarization / RAG generation | LLM API (Claude or GPT) |
| Storage | PostgreSQL (metadata) + Pinecone/pgvector (embeddings) |
| Knowledge graph | Entity/action-item linking across sessions (my part — likely a lightweight graph structure in Postgres or Neo4j, not yet finalized) |

## Current status (as of today)

- Project start: Aug 10, 2026. Running behind schedule — actual coding is starting now (mid-September), not on the original date.
- My work is sequenced *after* Dhruv's capture/ASR and Garvit's summarization produce real output — so early weeks will be architecture, schema design, and scaffolding against **mock/sample transcript data**, not live audio yet.

## Weekly file convention — READ BEFORE STARTING ANY WEEK

For **every week** below, create one file per week inside a `/weekly/harsh/` directory at the repo root, named:

```
weekly/harsh/week_<NN>_<short-slug>.py
```

(Each teammate has their own subfolder under `/weekly/` — `dhruv/`, `garvit/`, `dev/` — so week numbers don't collide across people. See `WEEKLY_INTEGRATION.md` for how these all get connected at the end of each week.)

- `<NN>` is the two-digit week number (01, 02, ... 32) from the table below.
- `<short-slug>` is a lowercase-hyphenated short version of the task (e.g. `week_01_architecture-review.py`).
- If a week's task is research/design rather than code (e.g. "review existing architectures"), still create the file, but as `.md` instead of `.py`, containing the write-up/decisions instead of code.
- **Never skip a week's file, even if the work is small** — the full 32-file sequence is the record of how the system was built, and it needs to be complete for the thesis submission.

**Every file must start with a header block before any code/content**, in this format:

```python
"""
Week <NN> (<start date> - <end date>)
Task: <the task description from the table below>

Why this matters:
<2-3 sentences on how this week's work fits into the overall pipeline —
what it depends on from previous weeks, and what later weeks will build on it>

What this script does:
<a short, concrete description of what the code below actually implements
or tests>
"""
```

Then the actual implementation follows. Keep each week's script runnable/testable on its own where possible (use mock data/fixtures for anything that depends on a teammate's not-yet-built component).

## My weekly task breakdown (32 weeks, Aug 10 2026 - Mar 19 2027)

| Week | Dates | Task |
|---|---|---|
| 01 | 10-08-2026 to 16-08-2026 | Review existing meeting-tool architectures, sketch the high-level design |
| 02 | 17-08-2026 to 23-08-2026 | Define service boundaries: capture, ASR, summarization, storage, frontend |
| 03 | 24-08-2026 to 30-08-2026 | Draft architecture docs and component diagrams |
| 04 | 31-08-2026 to 06-09-2026 | Align with team on what APIs each service exposes |
| 05 | 07-09-2026 to 13-09-2026 | Lock the architecture plan before Sprint 2 begins |
| 06 | 14-09-2026 to 20-09-2026 | Review early ASR/diarization output from Dhruv |
| 07 | 21-09-2026 to 27-09-2026 | Spot design gaps based on real transcript quality |
| 08 | 28-09-2026 to 04-10-2026 | Adjust data model to handle diarization edge cases |
| 09 | 05-10-2026 to 11-10-2026 | Update architecture docs to reflect the revised design |
| 10 | 12-10-2026 | Sign off on the updated design before Sprint 3 |
| 11 | 13-10-2026 to 19-10-2026 | Define entity types: people, topics, decisions |
| 12 | 20-10-2026 to 26-10-2026 | Define action-item schema: owner, due date, status |
| 13 | 27-10-2026 to 02-11-2026 | Cross-check schema against Garvit's summarization output |
| 14 | 03-11-2026 to 13-11-2026 | Finalize and document the schema |
| 15 | 14-11-2026 to 20-11-2026 | Set up the graph database structure |
| 16 | 21-11-2026 to 29-11-2026 | Build entity-linking logic across meetings |
| 17 | 30-11-2026 to 06-12-2026 | Test linking logic on sample data |
| 18 | 07-12-2026 to 13-12-2026 | Refine graph relationships from test results |
| 19 | 14-12-2026 to 18-12-2026 | Finalize the knowledge graph structure for RAG |
| 20 | 19-12-2026 to 25-12-2026 | Set up retrieval logic over the knowledge graph/embeddings |
| 21 | 26-12-2026 to 01-01-2027 | Build the answer-generation step with citations |
| 22 | 02-01-2027 to 08-01-2027 | Test the RAG pipeline on sample questions |
| 23 | 09-01-2027 to 15-01-2027 | Refine answer accuracy and citation quality |
| 24 | 16-01-2027 to 22-01-2027 | Define the RAG-frontend API contract with Dev |
| 25 | 23-01-2027 to 29-01-2027 | Build the integration endpoints |
| 26 | 30-01-2027 to 05-02-2027 | Test the end-to-end query flow, frontend to RAG backend |
| 27 | 06-02-2027 to 12-02-2027 | Coordinate integration testing across all modules |
| 28 | 13-02-2027 to 19-02-2027 | Review RAG answer quality across test cases |
| 29 | 20-02-2027 to 26-02-2027 | Log and prioritize issues found in testing |
| 30 | 27-02-2027 to 05-03-2027 | Prepare the production deployment plan |
| 31 | 06-03-2027 to 12-03-2027 | Deploy the system to production |
| 32 | 13-03-2027 to 19-03-2027 | Set up monitoring/logging, confirm system stability |

## Conventions / how to work with me

- Keep services loosely coupled — my knowledge graph and RAG layer should be swappable/testable independently of Dhruv's and Garvit's pipelines, since their output format may still change.
- Prefer well-documented, simple code over clever code — this is an academic thesis project that also needs to be explainable to a faculty panel.
- When scaffolding something that depends on another teammate's not-yet-built component (e.g., RAG pipeline needing real summaries), use a small mock/fixture dataset so I can build and test in isolation.
- Flag any architectural decision that would be hard to explain/justify to a non-technical evaluator — simplicity and clarity matter as much as capability here.
- When asked to "do week N," find week N in the table above, create/open `weekly/harsh/week_<N>_<slug>.py` (or `.md`), write the header block, then implement.
- At the end of each week, follow `WEEKLY_INTEGRATION.md` at the repo root to connect my output with the other three members' weekly output and confirm the pipeline still runs end-to-end.
