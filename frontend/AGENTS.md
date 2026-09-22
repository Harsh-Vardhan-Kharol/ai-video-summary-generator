# AI Realtime Video Summary Generator — Project Context for Codex (Dev's copy)

This file gives you (the coding agent) full context on the project so you don't need it re-explained every session. Read this before making changes.

## What this project is

A system that captures video/audio — live meetings (Zoom/Meet/Teams), lectures, webinars, or uploaded recordings — transcribes it, and generates a running summary (decisions, action items, key points) instead of making the user wait until the end. It also keeps a memory across past sessions so users can ask natural-language questions like "what did we decide about X last month?" and get a cited answer.

**Core differentiators:**
- Bot-free capture where possible (system audio, not a visible bot joining the call)
- Cross-session memory via a knowledge graph + vector search (RAG), not just single-session transcripts
- Summaries update continuously, not only after the session ends

## Team & my role

4-person final-year B.Tech team. I'm **Dev Tak — Backend & Frontend**, owning:
- Repo setup, backend skeleton (FastAPI), database schema
- API endpoints for storing/retrieving transcripts
- Storage layer: PostgreSQL + vector DB
- Embeddings pipeline and vector DB indexing
- Backend support for RAG query endpoints
- The whole frontend: dashboard, search/query UI, React/Next.js
- Final frontend-backend integration and production deployment/CI-CD

Other three members and their lanes (for context — don't touch their code without asking):
- **Harsh Vardhan Kharol — Team Lead** — architecture, knowledge graph, RAG pipeline, integration/deployment
- **Dhruv Vij** — audio capture, ASR (Whisper/Deepgram), speaker diarization (Pyannote)
- **Garvit Agrawal** — NLP: summarization, action-item/NER extraction, confidence scoring

## Architecture (high level)

```
Audio/Video Capture (bot-free or platform integration)      (Dhruv)
        ↓
ASR + Speaker Diarization (Whisper/Deepgram + Pyannote)      (Dhruv)
        ↓
Summarization + Action-Item Extraction (LLM-based)           (Garvit)
        ↓
Storage: Postgres + Vector DB + Knowledge Graph      <- YOUR PART (storage), Harsh owns the graph logic
        ↓
RAG Query Layer (retrieval + generation, with citations)      (Harsh, you build the backend endpoint for it)
        ↓
Frontend (React/Next.js — dashboard, search, summary view)  <- YOUR PART
```

You're the backbone connecting everyone else's work — your APIs and storage layer are what Harsh's RAG pipeline and Garvit's summaries actually get stored in and served from.

## Tech stack

| Layer | Tech |
|---|---|
| Backend | Python (FastAPI) |
| Storage | PostgreSQL (metadata) + Pinecone/pgvector (embeddings) |
| Frontend | React.js / Next.js |
| Deployment | Cloud hosting (AWS/Railway/Render — decide early) + CI/CD |

## Current status (as of today)

- Project start: Aug 10, 2026. Running behind schedule — actual coding is starting now (mid-September), not on the original date.
- You're the first coder to actually start (repo/backend skeleton), and the last to finish (deployment) — your work brackets everyone else's. Get the repo and basic API scaffolding up fast so Dhruv, Garvit, and Harsh aren't blocked.

## Weekly file convention — READ BEFORE STARTING ANY WEEK

For **every week** below, create one file per week inside `/weekly/dev/` at the repo root, named:

```
weekly/dev/week_<NN>_<short-slug>.py
```

- `<NN>` is the two-digit week number (01, 02, ... 32).
- `<short-slug>` is a lowercase-hyphenated short version of the task (e.g. `week_01_repo-setup.py`).
- If a week's task is research/design/UI-only work, still create the file, but as `.md` (for design notes) — for frontend weeks, a `.py` isn't right either; use `.md` describing the components built plus a note on where the actual `.jsx`/`.tsx` files live in the real project structure.
- **Never skip a week's file, even if the work is small** — the full 32-file sequence is the build record for the thesis submission.

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

Then the actual implementation follows. Keep each week's script/notes runnable or verifiable on its own where possible.

## My weekly task breakdown (32 weeks, Aug 10 2026 - Mar 19 2027)

| Week | Dates | Task |
|---|---|---|
| 01 | 10-08-2026 to 16-08-2026 | Set up the project repository and dev environment |
| 02 | 17-08-2026 to 23-08-2026 | Build the backend skeleton with FastAPI |
| 03 | 24-08-2026 to 30-08-2026 | Design the initial database schema |
| 04 | 31-08-2026 to 06-09-2026 | Set up basic CI for the backend |
| 05 | 07-09-2026 to 13-09-2026 | Review and finalize the foundation setup |
| 06 | 14-09-2026 to 20-09-2026 | Build the transcript-upload API endpoint |
| 07 | 21-09-2026 to 27-09-2026 | Build the transcript-retrieval endpoint |
| 08 | 28-09-2026 to 04-10-2026 | Connect endpoints to the database |
| 09 | 05-10-2026 to 11-10-2026 | Test endpoints with sample transcript data |
| 10 | 12-10-2026 | Fix bugs, finalize transcript storage APIs |
| 11 | 13-10-2026 to 19-10-2026 | Set up PostgreSQL for structured data |
| 12 | 20-10-2026 to 26-10-2026 | Set up the vector DB for embeddings |
| 13 | 27-10-2026 to 02-11-2026 | Connect both to the backend |
| 14 | 03-11-2026 to 13-11-2026 | Test the storage layer end-to-end |
| 15 | 14-11-2026 to 20-11-2026 | Build the embedding-generation pipeline |
| 16 | 21-11-2026 to 29-11-2026 | Connect embeddings to vector DB indexing |
| 17 | 30-11-2026 to 06-12-2026 | Test indexing and retrieval speed |
| 18 | 07-12-2026 to 13-12-2026 | Optimize indexing for scale |
| 19 | 14-12-2026 to 18-12-2026 | Finalize the embeddings pipeline |
| 20 | 19-12-2026 to 25-12-2026 | Build the RAG query API endpoint |
| 21 | 26-12-2026 to 01-01-2027 | Connect the endpoint to Harsh's RAG pipeline |
| 22 | 02-01-2027 to 08-01-2027 | Test the query endpoint with sample questions |
| 23 | 09-01-2027 to 15-01-2027 | Fix bugs, finalize backend RAG support |
| 24 | 16-01-2027 to 22-01-2027 | Build the dashboard UI: meeting list, summaries |
| 25 | 23-01-2027 to 29-01-2027 | Build the search/query interface |
| 26 | 30-01-2027 to 05-02-2027 | Polish the UI, connect to backend APIs |
| 27 | 06-02-2027 to 12-02-2027 | Connect frontend to all backend APIs |
| 28 | 13-02-2027 to 19-02-2027 | Test end-to-end user flows |
| 29 | 20-02-2027 to 26-02-2027 | Fix integration bugs found during testing |
| 30 | 27-02-2027 to 05-03-2027 | Set up cloud hosting and the CI/CD pipeline |
| 31 | 06-03-2027 to 12-03-2027 | Deploy the application to production |
| 32 | 13-03-2027 to 19-03-2027 | Set up monitoring/logging, confirm stability |

## Conventions / how to work with me

- Your APIs and DB schema are contracts everyone else's code depends on — flag any breaking change loudly before making it.
- Prefer well-documented, simple code over clever code — this is an academic thesis project that also needs to be explainable to a faculty panel.
- Get a minimal end-to-end skeleton working early (even with fake/mock data flowing through it) so Dhruv, Garvit, and Harsh have real endpoints to build against.
- Flag any architectural decision that would be hard to explain/justify to a non-technical evaluator.
- When asked to "do week N," find week N in the table above, create/open `weekly/dev/week_<N>_<slug>.py` (or `.md`), write the header block, then implement.
- At the end of each week, follow `WEEKLY_INTEGRATION.md` at the repo root to connect your output with the other three members' weekly output and confirm the pipeline still runs end-to-end.
