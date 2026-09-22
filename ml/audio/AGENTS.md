# AI Realtime Video Summary Generator — Project Context for Codex (Dhruv's copy)

This file gives you (the coding agent) full context on the project so you don't need it re-explained every session. Read this before making changes.

## What this project is

A system that captures video/audio — live meetings (Zoom/Meet/Teams), lectures, webinars, or uploaded recordings — transcribes it, and generates a running summary (decisions, action items, key points) instead of making the user wait until the end. It also keeps a memory across past sessions so users can ask natural-language questions like "what did we decide about X last month?" and get a cited answer.

**Core differentiators:**
- Bot-free capture where possible (system audio, not a visible bot joining the call)
- Cross-session memory via a knowledge graph + vector search (RAG), not just single-session transcripts
- Summaries update continuously, not only after the session ends

## Team & my role

4-person final-year B.Tech team. I'm **Dhruv Vij — Speech & Audio Processing**, owning:
- Bot-free / system-audio capture, plus Zoom/Meet platform integration
- ASR (Whisper/Deepgram) and speaker diarization (Pyannote)
- Handling messy real-world audio: overlapping speech, accents, noise
- Audio-derived metadata that feeds into the knowledge graph
- Playback-transcript sync in the UI

Other three members and their lanes (for context — don't touch their code without asking):
- **Harsh Vardhan Kharol — Team Lead** — architecture, knowledge graph, RAG pipeline, integration/deployment
- **Garvit Agrawal** — NLP: summarization, action-item/NER extraction, confidence scoring
- **Dev Tak** — backend (FastAPI), database, embeddings pipeline, frontend (React/Next.js)

## Architecture (high level)

```
Audio/Video Capture (bot-free or platform integration)   <- YOUR PART STARTS HERE
        ↓
ASR + Speaker Diarization (Whisper/Deepgram + Pyannote)  <- YOUR PART
        ↓
Summarization + Action-Item Extraction (LLM-based)        (Garvit)
        ↓
Storage: Postgres + Vector DB + Knowledge Graph            (Dev + Harsh)
        ↓
RAG Query Layer (retrieval + generation, with citations)   (Harsh)
        ↓
Frontend (React/Next.js — dashboard, search, summary view) (Dev, with your playback-sync piece)
```

Your output (clean, speaker-labeled transcript + audio metadata) is what everyone downstream depends on — accuracy here compounds through the whole pipeline.

## Tech stack

| Layer | Tech |
|---|---|
| Capture | System-audio capture (bot-free) + Zoom/Meet SDK integration |
| ASR | Whisper (self-hostable) or Deepgram (streaming, low-latency) |
| Diarization | Pyannote |
| Frontend | React.js / Next.js (Dev owns this, you contribute the playback-sync piece) |
| Backend | Python (FastAPI) |
| Storage | PostgreSQL + Pinecone/pgvector |

## Current status (as of today)

- Project start: Aug 10, 2026. Running behind schedule — actual coding is starting now (mid-September), not on the original date.
- Your work is first in the pipeline — everyone else is waiting on real transcript output from you before their own work has real data to run against. Prioritize getting *something* working end-to-end early, even at low accuracy, over perfecting one stage before moving on.

## Weekly file convention — READ BEFORE STARTING ANY WEEK

For **every week** below, create one file per week inside `/weekly/dhruv/` at the repo root, named:

```
weekly/dhruv/week_<NN>_<short-slug>.py
```

- `<NN>` is the two-digit week number (01, 02, ... 32).
- `<short-slug>` is a lowercase-hyphenated short version of the task (e.g. `week_01_system-audio-research.py`).
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

Then the actual implementation follows. Keep each week's script runnable/testable on its own with sample audio files where possible.

## My weekly task breakdown (32 weeks, Aug 10 2026 - Mar 19 2027)

| Week | Dates | Task |
|---|---|---|
| 01 | 10-08-2026 to 16-08-2026 | Research system-audio capture APIs for bot-free recording |
| 02 | 17-08-2026 to 23-08-2026 | Build the initial local audio capture module |
| 03 | 24-08-2026 to 30-08-2026 | Add Zoom/Meet integration for platform-based capture |
| 04 | 31-08-2026 to 06-09-2026 | Test capture reliability across both methods |
| 05 | 07-09-2026 to 13-09-2026 | Fix bugs and finalize the capture module |
| 06 | 14-09-2026 to 20-09-2026 | Integrate Whisper/Deepgram for transcription |
| 07 | 21-09-2026 to 27-09-2026 | Integrate Pyannote for speaker diarization |
| 08 | 28-09-2026 to 04-10-2026 | Combine ASR and diarization into one pipeline |
| 09 | 05-10-2026 to 11-10-2026 | Test on sample recordings, measure accuracy |
| 10 | 12-10-2026 | Tune settings for better transcription quality |
| 11 | 13-10-2026 to 19-10-2026 | Test the pipeline on overlapping-speech samples |
| 12 | 20-10-2026 to 26-10-2026 | Improve diarization handling for crosstalk |
| 13 | 27-10-2026 to 02-11-2026 | Test on varied accents and noisy audio |
| 14 | 03-11-2026 to 13-11-2026 | Document known limitations and fixes applied |
| 15 | 14-11-2026 to 20-11-2026 | Identify audio metadata useful for the knowledge graph |
| 16 | 21-11-2026 to 29-11-2026 | Build the metadata-tagging logic |
| 17 | 30-11-2026 to 06-12-2026 | Connect tagged metadata to Harsh's entity schema |
| 18 | 07-12-2026 to 13-12-2026 | Test metadata flow into the graph |
| 19 | 14-12-2026 to 18-12-2026 | Fix issues found during integration |
| 20 | 19-12-2026 to 25-12-2026 | Review how audio quality affects RAG retrieval accuracy |
| 21 | 26-12-2026 to 01-01-2027 | Optimize preprocessing: noise reduction, normalization |
| 22 | 02-01-2027 to 08-01-2027 | Re-test the pipeline with RAG queries |
| 23 | 09-01-2027 to 15-01-2027 | Finalize audio pipeline improvements |
| 24 | 16-01-2027 to 22-01-2027 | Build playback-transcript sync logic |
| 25 | 23-01-2027 to 29-01-2027 | Test sync accuracy with Dev's frontend |
| 26 | 30-01-2027 to 05-02-2027 | Fix sync bugs and polish the feature |
| 27 | 06-02-2027 to 12-02-2027 | Collect a varied set of test recordings |
| 28 | 13-02-2027 to 19-02-2027 | Run accuracy tests and log results |
| 29 | 20-02-2027 to 26-02-2027 | Report findings, flag issues for fixing |
| 30 | 27-02-2027 to 05-03-2027 | Run final performance tests on the capture pipeline |
| 31 | 06-03-2027 to 12-03-2027 | Fix remaining bugs |
| 32 | 13-03-2027 to 19-03-2027 | Confirm pipeline stability for release |

## Conventions / how to work with me

- Your output format (transcript + speaker labels + timestamps) is a contract other people's code depends on — if you change it, flag it loudly, don't just change it quietly.
- Prefer well-documented, simple code over clever code — this is an academic thesis project that also needs to be explainable to a faculty panel.
- Get a rough end-to-end version working early (even low accuracy) rather than perfecting one piece before others can build on it.
- Flag any architectural decision that would be hard to explain/justify to a non-technical evaluator.
- When asked to "do week N," find week N in the table above, create/open `weekly/dhruv/week_<N>_<slug>.py` (or `.md`), write the header block, then implement.
- At the end of each week, follow `WEEKLY_INTEGRATION.md` at the repo root to connect your output with the other three members' weekly output and confirm the pipeline still runs end-to-end.
