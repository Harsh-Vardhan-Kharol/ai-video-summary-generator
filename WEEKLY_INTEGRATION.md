# WEEKLY_INTEGRATION.md — End-of-Week Sync Instructions

Read this whenever any team member's Codex session finishes a week's work, and whenever anyone is asked to "sync the week" or "run the weekly demo."

## Why this file exists

Each member (Harsh, Dhruv, Garvit, Dev) has their own weekly task file under `weekly/<name>/week_NN_*.py`, built independently, often against mock data since real upstream output isn't ready yet. Working in isolation is fine week-to-week, but **the four pieces have to actually connect** — this file defines how, and how the team confirms it's still connected after every week.

## Folder structure this assumes

```
/weekly/
    /harsh/    week_01_*.py ... week_32_*.py
    /dhruv/    week_01_*.py ... week_32_*.py
    /garvit/   week_01_*.py ... week_32_*.py
    /dev/      week_01_*.py ... week_32_*.py
    /integration/
        week_NN_integration.py   <- created fresh each week, see below
/fixtures/
    sample_audio.wav
    sample_transcript.json
    sample_summary.json
    (add to this folder as real output formats stabilize)
```

## The pipeline everyone's weekly work has to chain into

```
Dhruv's capture/ASR output (transcript + speaker labels)
        ↓
Garvit's summarization output (summary + action items + confidence scores)
        ↓
Dev's storage layer (Postgres + vector DB) + Harsh's knowledge graph
        ↓
Harsh's RAG query layer (retrieval + generation + citations)
        ↓
Dev's frontend (displays it all)
```

## Prerequisite: one shared Git remote

This plan assumes all 4 of you push to the **same GitHub (or GitLab) repository**, even though each of you runs Codex locally on your own machine. Local Codex sessions are fine and expected — what matters is that the *code* ends up in one shared place, not four disconnected local folders. Set this up once at the start:

- One shared repo, everyone clones it locally (`git clone <repo-url>`)
- Each person works on their own branch (e.g., `harsh-dev`, `dhruv-dev`) or commits directly to `main` if you're comfortable with that for a 4-person project
- **Nobody runs the integration script against their own local-only code** — it only means something once everyone's latest work is actually merged together

## End-of-week ritual (do this every week, all 4 people)

0. **Everyone pushes their week's work to the shared repo first.** Whoever is doing integration that week (default: Harsh) then runs `git pull` (or merges everyone's branches) so their local copy actually contains all 4 people's latest code before step 3 below. Skipping this step is the most common way "integration" quietly becomes fake — running a script against only your own code and calling it integrated.

1. **Each person finishes their own `weekly/<name>/week_NN_*.py` first**, following their own AGENTS.md file. Use fixtures/mock data for anything upstream that isn't real yet.

2. **Each person defines a clear input/output contract for that week's script** — literally write it as a comment or a small function signature at the bottom of their week file, e.g.:
 ```python
 # WEEK OUTPUT CONTRACT:
 # Input: raw audio file path (str)
 # Output: {"transcript": [...], "speakers": [...], "timestamps": [...]}
 ```
 This is what makes automated integration possible instead of everyone guessing each other's formats.

3. **Whoever is doing the integration that week (default: Harsh, since he owns integration) creates `weekly/integration/week_NN_integration.py`**, which:
 - Imports or calls each of the four members' latest relevant week script
 - Feeds one's output into the next one's input, following the pipeline order above
 - Runs the full chain against a fixture (real or mock) and prints/logs the output at each stage
 - Clearly reports **which stages succeeded and which failed or are still using mock data**

 Header format for this file:
 ```python
 """
 Week <NN> Integration Check

 Connects: <list which members' week_NN files are being chained this week>
 Still mocked: <list anything not yet real, e.g. "Garvit's summarizer -- using fixture until Sprint 3">

 Result: <PASS / PARTIAL / FAIL, updated each time this is run>
 """
 ```

4. **Run the integration script and actually look at the output** — don't just check that it runs without crashing. The point is to *see* each stage's result (print the transcript, print the summary, print the RAG answer) so the team can visually confirm quality, not just that the code executes.

5. **If a stage fails or a contract mismatch is found** (e.g., Garvit's script expects a different transcript format than Dhruv now produces), log it as an issue in the week's integration file under a `# KNOWN ISSUES` comment, and flag it in your next team sync — don't silently patch around it in the integration script only, since that hides the real mismatch from whoever owns that piece.

6. **Once a week's integration passes end-to-end (even with some stages still mocked), tag it** — e.g., a short line at the top of `weekly/integration/week_NN_integration.py`: `# STATUS: full pipeline runs, Sprint 4 knowledge-graph stage still mocked`. This tag is what you'll point to when demoing progress to your mentor or faculty panel.

## Quick "show me everyone's work this week" command

Whoever's running the sync should be able to do this in one shot:

```bash
python weekly/integration/week_NN_integration.py
```

...and see, in order: capture status → transcript output → summary output → storage confirmation → RAG answer (or whichever stages exist so far) → any KNOWN ISSUES logged. If this single command can't show that, the week isn't actually integrated yet — it's four people's separate scripts that happen to sit in the same repo.

## Notes

- Early weeks (1-10 or so) will have a lot of "still mocked" — that's expected, since Dhruv's and Garvit's real pipelines aren't built yet. Don't force premature integration; the point is to have the *scaffolding* ready so that as each real piece comes online, it slots into a contract that already exists.
- If the team's weekly sync meeting happens, this integration script's printed output is the material for that meeting — it's a much better demo than four people describing their week verbally.
