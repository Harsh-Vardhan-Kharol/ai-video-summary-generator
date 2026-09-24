"""
Week 13 (27-10-2026 - 02-11-2026)
Task: Cross-check schema against Garvit's summarization output

Why this matters:
The graph schema only works if upstream extraction can provide the fields and provenance it requires. This cross-check uses a representative mock output because Garvit's week 13 artifact is not present in this checkout; it records compatibility and the small adapter expectations for later integration.

What this script does:
This design note maps a mock summary/action/entity payload to the Week 11–12 contracts and records unresolved producer questions.
"""

# Week 13 — producer compatibility review

## Review input

No `weekly/garvit/week_13_*` output or shared extraction fixture exists in this
checkout. The following representative producer shape is therefore a mock,
not a claim about Garvit's implementation:

```json
{
  "decisions": [{"text": "Use PostgreSQL as the canonical store", "confidence": 0.9, "evidence": [{"segment_id": "seg-1", "revision": 1}]}],
  "action_items": [{"text": "Harsh will document the schema by Friday", "owner": "Harsh", "due_date": "Friday", "confidence": 0.84, "evidence": [{"segment_id": "seg-2", "revision": 1}]}],
  "entities": [{"text": "PostgreSQL", "type": "topic", "evidence": [{"segment_id": "seg-1", "revision": 1}]}]
}
```

## Compatibility mapping

| Producer value | Contract target | Assessment |
| --- | --- | --- |
| `text` | decision `statement` / action `description` / entity `display_name` | Direct mapping; normalize only whitespace |
| `type` | entity type enum | Accept only `person`, `topic`, `decision`; reject/flag unknown values |
| `owner` | resolved `owner_entity_id` | Requires person resolution; retain raw text as a candidate until resolved |
| `due_date` | `due_date_text`, optionally normalized `due_at` | Preserve original; normalization needs session timezone/date context |
| `confidence` | `confidence` | Require numeric 0..1 and retain producer/version metadata |
| `evidence` | `EvidenceRef[]` | Compatible only when segment ID and revision are both present |

### Required adapter behavior

1. Assign canonical UUIDs in the storage/graph boundary; producer mention IDs
   may be retained as external IDs but are not global canonical IDs.
2. Convert raw owner names into person candidates; do not auto-resolve based on
   a diarization label or first-name match.
3. Keep relative due-date text if date normalization lacks session time zone
   or a trustworthy meeting date.
4. Reject unsupported confidence values and records without evidence. Log the
   reason for review instead of dropping them silently.
5. Preserve unknown extraction fields in producer metadata during the adapter
   transition, avoiding a brittle lockstep dependency.

## Questions for upstream confirmation

- Does each evidence reference include immutable segment revision and optional
  timestamps?
- Are confidence values consistently calibrated to 0..1, and which producer
  version generated them?
- Does extraction distinguish an assigned owner from a person merely
  mentioned in the same sentence?
- What session timezone and meeting-start metadata are available for dates?

## WEEK OUTPUT CONTRACT

**Input:** Mock summarization output above; actual Garvit output remains
unavailable in the repository.

**Output:** A compatibility mapping and adapter requirements. Status is
provisional until confirmed against a real versioned producer payload.
