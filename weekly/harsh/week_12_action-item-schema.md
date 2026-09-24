"""
Week 12 (20-10-2026 - 26-10-2026)
Task: Define action-item schema: owner, due date, status

Why this matters:
Action items connect decisions and discussion to accountable follow-up. The schema builds on Week 11's entity vocabulary and the immutable evidence references approved in Week 10, so later graph links and RAG answers can explain where each task came from.

What this script does:
This design note specifies an evidence-backed action-item record, with clear handling for unknown owners, dates, and status changes.
"""

# Week 12 — action-item contract (schema version 1)

An action item represents a requested or accepted task, not a general topic or
an inferred promise. Keep extracted claims separate from workflow state.

| Field | Type | Rule |
| --- | --- | --- |
| `action_item_id` | UUID | Stable ID for the task |
| `description` | string | Concise, faithful task statement |
| `owner_entity_id` | UUID or null | Person entity; null means unassigned/unknown |
| `owner_status` | enum | `assigned`, `unassigned`, `uncertain` |
| `due_at` | timestamp/date or null | ISO 8601; null when not stated/resolvable |
| `due_date_text` | string or null | Preserve the original phrase (e.g. “Friday”) |
| `status` | enum | `open`, `in_progress`, `blocked`, `completed`, `cancelled` |
| `confidence` | number 0..1 | Extraction confidence, not completion confidence |
| `evidence` | EvidenceRef[] | At least one source segment and revision |
| `related_decision_id` | UUID or null | Optional link to a supported decision |
| `created_at`, `updated_at` | timestamp | UTC timestamps |

### Semantics and lifecycle

- Unknown owner and due date stay null; do not invent them from the speaker or
  meeting date. Keep normalized date and original wording separately.
- Extraction initializes status to `open`. Only an explicit update or
  evidence-backed workflow event changes it; a summary's tense alone does not
  mark it completed.
- Status changes append an audit event (`from_status`, `to_status`, timestamp,
  actor/source, evidence). They do not erase the original extraction.
- Material changes to cited transcript revisions set the derived item to
  `needs_review` in its provenance/lifecycle metadata until re-extracted.
- An owner must reference a `person` entity. `SPEAKER_nn` alone is not a
  cross-session owner identity.

### Example

```json
{
  "action_item_id": "d7c1b179-6e4a-424f-8a76-42dfeb20a6b1",
  "description": "Prepare the deployment checklist",
  "owner_entity_id": null,
  "owner_status": "uncertain",
  "due_at": null,
  "due_date_text": "by Friday",
  "status": "open",
  "confidence": 0.81,
  "evidence": [{"segment_id": "segment-42", "revision": 2, "start_ms": 84120, "end_ms": 90680}],
  "related_decision_id": null
}
```

## WEEK OUTPUT CONTRACT

**Input:** Extracted action-item candidates with source segment references.

**Output:** Version-1 action-item records using stable person/decision IDs
where supported, nullable unknown values, and auditable status transitions.
