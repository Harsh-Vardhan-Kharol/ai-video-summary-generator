"""
Week 04 (31-08-2026 - 06-09-2026)
Task: Align with team on what APIs each service exposes

Why this matters:
The pipeline can only be integrated when modules agree on payload shape,
versioning, and error behavior. This contract translates the Week 2 boundaries
into practical APIs that can be implemented independently against fixtures.

What this script does:
This design note defines the proposed internal event contracts and public
backend endpoints requiring team confirmation before implementation.
"""

# Week 4 — API alignment proposal

## Internal event contract

All internal producers emit the Week 2 JSON envelope. The backend validates
`schema_version` and required identifiers before persistence. Event names and
minimum `payload` fields are:

| Event | Producer | Required payload |
| --- | --- | --- |
| `audio.chunk` | Capture | `sequence`, `started_at`, `duration_ms`, `audio_uri` |
| `transcript.segment` | ASR | `segment_id`, `revision`, `is_final`, `start_ms`, `end_ms`, `speaker_label`, `text`, `asr_confidence` |
| `summary.update` | NLP | `summary_id`, `version`, `text`, `covered_segment_ids`, `is_final` |
| `extraction.update` | NLP | `items[]: {id, type, text, confidence, evidence_segment_ids}` |
| `graph.linked` | Graph linker | `relationship_id`, `source_id`, `target_id`, `relationship_type`, `evidence_segment_ids`, `confidence` |

`type` for extraction is initially one of `person`, `topic`, `decision`, or
`action_item`. New types require a schema-version change, not an undocumented
string.

## Public backend API proposal

| Method and path | Consumer | Purpose | Response guarantee |
| --- | --- | --- | --- |
| `POST /v1/sessions` | Frontend | Create an upload/live session | Returns `session_id` and initial status |
| `GET /v1/sessions/{session_id}` | Frontend | Fetch session state | Returns transcript, current summary, and processing statuses |
| `GET /v1/sessions/{session_id}/updates` | Frontend | Receive live updates via SSE initially | Ordered events with event IDs; reconnect can resume from `after_event_id` |
| `POST /v1/query` | Frontend | Ask across sessions | Returns cited answer, citations, and evidence status |
| `GET /v1/sessions/{session_id}/records` | Frontend | Display extracted decisions/action items | Returns evidence-linked structured records |

Example query request:

```json
{
  "question": "What did we decide about the deployment date?",
  "session_ids": [],
  "top_k": 8
}
```

Example answer response:

```json
{
  "answer": "The team proposed 6 March, subject to integration testing.",
  "citations": [{"session_id": "...", "segment_id": "...", "start_ms": 184200}],
  "insufficient_evidence": false
}
```

## Error and compatibility rules

- Validation failures return a machine-readable error code and field details.
- An unsupported schema version is rejected clearly; consumers must not guess
  how to parse it.
- Temporary upstream unavailability is reported as `processing` or `failed`
  session status, not as an empty successful result.
- `POST /v1/query` returns `insufficient_evidence: true` when retrieval cannot
  support an answer.
- Public endpoints are versioned under `/v1`; internal event versioning is
  independent and explicit in every envelope.

## Team confirmation checklist

- Dhruv confirms transcript timing units, speaker-label policy, revision rules,
  and confidence scale.
- Garvit confirms extraction item fields, permissible values, and evidence IDs.
- Dev confirms persistence IDs, event delivery mechanism, endpoint ownership,
  and frontend update transport.
- Harsh confirms graph-link payload and citation fields are sufficient for RAG.

These are proposed contracts until the four owners confirm them. Real provider
payloads must be adapted at the service boundary rather than leaking into
downstream code.

## WEEK OUTPUT CONTRACT

**Input:** Week 2 boundaries and Week 3 diagrams.

**Output:** A versioned internal event proposal and `/v1` frontend-facing API
proposal, with a concrete checklist for team sign-off.
