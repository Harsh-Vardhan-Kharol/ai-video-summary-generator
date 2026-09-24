"""
Week 14 (03-11-2026 - 13-11-2026)
Task: Finalize and document the schema

Why this matters:
Later graph storage and entity linking need a stable, explainable contract. This note consolidates the entity and action-item schemas while preserving the Week 13 finding that upstream payload compatibility remains to be confirmed against real output.

What this script does:
This design note publishes the version-1 canonical schema summary, validation rules, and migration policy for the knowledge graph boundary.
"""

# Week 14 — canonical graph-input schema v1

## Canonical records

This schema is a small, typed relationship layer over PostgreSQL's canonical
records. It does not require a separate graph database. Every record has a
UUID, type, lifecycle status, confidence where extracted, timestamps, and one
or more revision-specific evidence references.

### Entity types

- **Person:** identity-resolution state plus optional session-local speaker
  references. Speaker labels never serve as global IDs.
- **Topic:** normalized subject, optional description/keywords, and optional
  parent topic. Parent relationships must remain acyclic.
- **Decision:** statement, decision status (`proposed`, `accepted`,
  `reversed`, `superseded`), optional decision time and superseded decision.

### Action item

Description, nullable person owner ID, owner-resolution state, nullable
normalized due time, original due-date wording, workflow status, confidence,
evidence references, and optional related decision. New extractions start
`open`; later status changes are auditable events.

### Evidence and lifecycle

An evidence reference is `{segment_id, revision, start_ms?, end_ms?}`. Missing
or unsupported evidence prevents a record from becoming active. A superseded
source revision does not delete a derived record: mark it `needs_review`, then
create/update a replacement only after producer re-evaluation. Keep confidence
semantics and producer version alongside extracted records.

## Validation invariants

1. All IDs are UUIDs at the canonical storage boundary.
2. Entity type/status/action status values are restricted to the enums above.
3. Confidence is numeric and within `[0, 1]`.
4. Every active extracted record has at least one valid evidence reference.
5. Owner and related-decision IDs point to records of the correct type.
6. Unknown owner/date values remain null, not guessed values.
7. Revision history and status transitions are append-only/auditable.
8. Cross-session merges require explicit resolution evidence or user action.

## Versioning and compatibility

Contract identifier: `meeting_graph_input`, version `1`. Producers may add
optional fields without a version change. Renaming fields, changing enum
semantics, weakening evidence requirements, or changing confidence meaning
requires a new version and an adapter. Week 13 compatibility was checked only
against mock payloads; acceptance by Garvit is pending a real sample.

## WEEK OUTPUT CONTRACT

**Input:** Week 11 entity definitions, Week 12 action-item definition, and
Week 13 mock compatibility review.

**Output:** Canonical version-1 graph-input contract. It is ready for Week 15
storage scaffolding; upstream payload conformance remains an explicit
integration check, not an assumed fact.
