"""
Week 10 (12-10-2026)
Task: Sign off on the updated design before Sprint 3

Why this matters:
Sprint 3 begins entity, decision, and action-item schema work. A final
decision on revision, speaker attribution, and evidence semantics prevents
that work from encoding assumptions invalidated by real-time ASR behavior.

What this script does:
This design note freezes the revised transcript-evidence architecture and
lists the outstanding external validation needed as real ASR output arrives.
"""

# Week 10 — updated-design sign-off

## Approved Sprint 3 baseline

The team will proceed with the following data and architecture rules:

1. Transcript evidence is immutable by `(segment_id, revision)`; current state
   is a view, not an overwrite.
2. Speaker attribution is separate from transcript text, and an anonymous
   diarization label is never automatically a cross-session person identity.
3. All generated summaries, extractions, graph links, embeddings, and RAG
   citations retain exact source segment IDs and revisions.
4. A material evidence revision marks dependent derived records for
   re-evaluation rather than allowing a stale answer to remain authoritative.
5. PostgreSQL is the canonical store; vector search and graph relationships are
   derived, replaceable layers.
6. The public backend contract stays under `/v1`, while internal events carry
   an explicit schema version.

## Decision record

| Decision | Status | Basis |
| --- | --- | --- |
| Modular asynchronous pipeline | Approved | Weeks 1-5 architecture baseline |
| Revision-aware evidence model | Approved | Week 7 quality-gap analysis and Week 8 model |
| Separate speaker-attribution records | Approved | Prevents identity/diarization conflation |
| Evidence-required RAG citations | Approved | Required for auditable answers to users and faculty |
| Graph as a lightweight derived relationship layer | Approved | Keeps the system simple and explainable |

## Outstanding validation, not a blocker to design

The current checkout still has no real ASR fixture. When it is supplied, the
team must validate timing units, revision delivery, diarization confidence,
overlap behavior, and confidence-scale semantics against the signed-off model.
If it reveals a contract-breaking difference, update the schema version and
log it in the relevant weekly integration script; do not silently alter data.

## Sprint 3 entry criteria

- Entity, decision, and action-item schemas use the Week 8 evidence shape.
- Mock fixtures include anonymous speakers and revision-aware segments.
- No component relies on a stable global identity for `SPEAKER_nn` labels.
- The team can explain why each RAG citation identifies both a segment and its
  source revision.

## WEEK OUTPUT CONTRACT

**Input:** Weeks 6-9 ASR-quality review, edge-case data model, and revised
architecture reference.

**Output:** The approved Sprint 3 design baseline. New schema work begins from
this record unless a versioned contract change is agreed by the affected owner.
