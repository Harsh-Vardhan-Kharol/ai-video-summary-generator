# AI Realtime Video Summary Generator — Project Context for Codex (Garvit's copy)

This file gives you (the coding agent) full context on the project so you don't need it re-explained every session. Read this before making changes.

## What this project is

A system that captures video/audio — live meetings (Zoom/Meet/Teams), lectures, webinars, or uploaded recordings — transcribes it, and generates a running summary (decisions, action items, key points) instead of making the user wait until the end. It also keeps a memory across past sessions so users can ask natural-language questions like "what did we decide about X last month?" and get a cited answer.

**Core differentiators:**
- Bot-free capture where possible (system audio, not a visible bot joining the call)
- Cross-session memory via a knowledge graph + vector search (RAG), not just single-session transcripts
- Summaries update continuously, not only after the session ends

## Team & my role

4-person final-year B.Tech team. I'm **Garvit Agrawal — NLP**, owning:
- Summarization: turning raw transcripts into overview + decisions + action items
- Action-item and entity extraction (NER)
- Confidence/hallucination scoring — flagging when a summary claim isn't well-supported
- Prompt evaluation and quality tuning, for both summarization and (with Harsh) RAG answers
- Helping define how summaries/action items should be structured for frontend display

Other three members and their lanes (for context — don't touch their code without asking):
- **Harsh Vardhan Kharol — Team Lead** — architecture, knowledge graph, RAG pipeline, integration/deployment
- **Dhruv Vij** — audio capture, ASR (Whisper/Deepgram), speaker diarization (Pyannote)
- **Dev Tak** — backend (FastAPI), database, embeddings pipeline, frontend (React/Next.js)

## Architecture (high level)

```
Audio/Video Capture (bot-free or platform integration)      (Dhruv)
        ↓
ASR + Speaker Diarization (Whisper/Deepgram + Pyannote)      (Dhruv)
        ↓
Summarization + Action-Item Extraction (LLM-based)   <- YOUR PART
        ↓
Storage: Postgres + Vector DB + Knowledge Graph              (Dev + Harsh)
        ↓
RAG Query Layer (retrieval + generation, with citations)      (Harsh, you help tune answer quality)
        ↓
Frontend (React/Next.js — dashboard, search, summary view)   (Dev, you help define the data format)
```

Your output (summary + action items + confidence scores) is what gets stored, embedded, and eventually retrieved by the RAG layer — the quality and structure of what you produce directly shapes how good the final answers can be.

## Tech stack

| Layer | Tech |
|---|---|
| Summarization / extraction | LLM API (Claude or GPT), prompt-based |
| NER / action-item extraction | LLM-based or a lightweight NER library, your call |
| Storage | PostgreSQL + Pinecone/pgvector (Dev builds this, you define what gets stored) |
| Frontend | React.js / Next.js (Dev owns this, you advise on data shape) |

## Current status (as of today)

- Project start: Aug 10, 2026. Running behind schedule — actual coding is starting now (mid-September), not on the original date.
- Your work depends on Dhruv's transcripts. Until real transcripts exist, build and test against **mock/sample transcript text** so you're not blocked.

## Weekly file convention — READ BEFORE STARTING ANY WEEK

For **every week** below, create one file per week inside `/weekly/garvit/` at the repo root, named:

```
weekly/garvit/week_<NN>_<short-slug>.py
```

- `<NN>` is the two-digit week number (01, 02, ... 32).
- `<short-slug>` is a lowercase-hyphenated short version of the task (e.g. `week_01_summarization-research.py`).
- If a week's task is research/design rather than code, still create the file, but as `.md` instead of `.py`.
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

Then the actual implementation follows. Keep each week's script runnable/testable on its own using sample/mock transcript data.

## My weekly task breakdown (32 weeks, Aug 10 2026 - Mar 19 2027)

| Week | Dates | Task |
|---|---|---|
| 01 | 10-08-2026 to 16-08-2026 | Research summarization approaches: extractive vs abstractive |
| 02 | 17-08-2026 to 23-08-2026 | Draft initial prompt templates |
| 03 | 24-08-2026 to 30-08-2026 | Test prompts on sample transcripts |
| 04 | 31-08-2026 to 06-09-2026 | Refine prompts based on output quality |
| 05 | 07-09-2026 to 13-09-2026 | Finalize the prompt template set |
| 06 | 14-09-2026 to 20-09-2026 | Build the first working summarization pipeline |
| 07 | 21-09-2026 to 27-09-2026 | Run it on real transcripts from Dhruv's pipeline |
| 08 | 28-09-2026 to 04-10-2026 | Review summary quality, note gaps |
| 09 | 05-10-2026 to 11-10-2026 | Adjust prompts/logic based on findings |
| 10 | 12-10-2026 | Finalize the first working version |
| 11 | 13-10-2026 to 19-10-2026 | Build action-item extraction logic |
| 12 | 20-10-2026 to 26-10-2026 | Add NER for entities: people, dates, topics |
| 13 | 27-10-2026 to 02-11-2026 | Combine summarization and extraction into one flow |
| 14 | 03-11-2026 to 13-11-2026 | Test combined output against Harsh's schema |
| 15 | 14-11-2026 to 20-11-2026 | Research hallucination-detection approaches |
| 16 | 21-11-2026 to 29-11-2026 | Build a confidence-scoring mechanism |
| 17 | 30-11-2026 to 06-12-2026 | Test scoring against known-good/bad summaries |
| 18 | 07-12-2026 to 13-12-2026 | Tune thresholds for reliability |
| 19 | 14-12-2026 to 18-12-2026 | Finalize scoring integration |
| 20 | 19-12-2026 to 25-12-2026 | Evaluate summarization quality across more meetings |
| 21 | 26-12-2026 to 01-01-2027 | Evaluate RAG answer quality with Harsh |
| 22 | 02-01-2027 to 08-01-2027 | Adjust prompts based on evaluation results |
| 23 | 09-01-2027 to 15-01-2027 | Re-test and confirm improvements |
| 24 | 16-01-2027 to 22-01-2027 | Define how summaries/action items should be structured for display |
| 25 | 23-01-2027 to 29-01-2027 | Work with Dev on the frontend data format |
| 26 | 30-01-2027 to 05-02-2027 | Test how it looks and reads in the actual UI |
| 27 | 06-02-2027 to 12-02-2027 | Test across different meeting types and lengths |
| 28 | 13-02-2027 to 19-02-2027 | Log accuracy issues found |
| 29 | 20-02-2027 to 26-02-2027 | Report and prioritize fixes |
| 30 | 27-02-2027 to 05-03-2027 | Fix remaining summarization bugs |
| 31 | 06-03-2027 to 12-03-2027 | Polish prompt and output quality |
| 32 | 13-03-2027 to 19-03-2027 | Confirm the summarization pipeline is release-ready |

## Conventions / how to work with me

- Your output format (summary structure, action-item fields, confidence scores) is a contract other people's code depends on — flag changes loudly.
- Prefer well-documented, simple code over clever code — this is an academic thesis project that also needs to be explainable to a faculty panel.
- Build and test against mock/sample transcripts whenever real ones from Dhruv aren't ready yet.
- Flag any architectural decision that would be hard to explain/justify to a non-technical evaluator.
- When asked to "do week N," find week N in the table above, create/open `weekly/garvit/week_<N>_<slug>.py` (or `.md`), write the header block, then implement.
- At the end of each week, follow `WEEKLY_INTEGRATION.md` at the repo root to connect your output with the other three members' weekly output and confirm the pipeline still runs end-to-end.
