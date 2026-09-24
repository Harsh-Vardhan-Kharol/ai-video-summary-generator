"""
Week 15 (14-11-2026 - 20-11-2026)
Task: Set up the graph database structure

Why this matters:
The finalized Week 14 schema needs a concrete persistence shape before cross-meeting linking begins. This scaffold uses PostgreSQL tables and foreign keys because PostgreSQL is already the canonical store; a lightweight relationship table keeps the graph replaceable and easy to explain.

What this script does:
This standard-library script prints PostgreSQL DDL for evidence-backed entities, action items, and typed relationships without connecting to or modifying a database.
"""

"""Week 15 PostgreSQL knowledge-graph schema scaffold.

Run with `python weekly/harsh/week_15_graph-database-structure.py` to print the
DDL. The project has no configured database driver or connection in this
checkout, so applying migrations is intentionally left to the storage owner.
"""

POSTGRES_DDL = r"""
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS graph_entities (
    entity_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entity_type TEXT NOT NULL CHECK (entity_type IN ('person', 'topic', 'decision')),
    display_name TEXT NOT NULL CHECK (length(trim(display_name)) > 0),
    aliases JSONB NOT NULL DEFAULT '[]'::jsonb,
    properties JSONB NOT NULL DEFAULT '{}'::jsonb,
    status TEXT NOT NULL DEFAULT 'active'
        CHECK (status IN ('active', 'needs_review', 'superseded')),
    confidence DOUBLE PRECISION NOT NULL CHECK (confidence BETWEEN 0 AND 1),
    producer TEXT NOT NULL,
    producer_version TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS graph_action_items (
    action_item_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    description TEXT NOT NULL CHECK (length(trim(description)) > 0),
    owner_entity_id UUID REFERENCES graph_entities(entity_id),
    owner_status TEXT NOT NULL CHECK (owner_status IN ('assigned', 'unassigned', 'uncertain')),
    due_at TIMESTAMPTZ,
    due_date_text TEXT,
    status TEXT NOT NULL DEFAULT 'open'
        CHECK (status IN ('open', 'in_progress', 'blocked', 'completed', 'cancelled', 'needs_review')),
    confidence DOUBLE PRECISION NOT NULL CHECK (confidence BETWEEN 0 AND 1),
    related_decision_id UUID REFERENCES graph_entities(entity_id),
    producer TEXT NOT NULL,
    producer_version TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CHECK (owner_status <> 'assigned' OR owner_entity_id IS NOT NULL)
);

CREATE TABLE IF NOT EXISTS graph_evidence (
    evidence_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entity_id UUID REFERENCES graph_entities(entity_id),
    action_item_id UUID REFERENCES graph_action_items(action_item_id),
    segment_id UUID NOT NULL,
    segment_revision INTEGER NOT NULL CHECK (segment_revision > 0),
    start_ms BIGINT,
    end_ms BIGINT,
    CHECK ((entity_id IS NOT NULL) <> (action_item_id IS NOT NULL)),
    CHECK (start_ms IS NULL OR start_ms >= 0),
    CHECK (end_ms IS NULL OR end_ms >= 0),
    CHECK (start_ms IS NULL OR end_ms IS NULL OR end_ms >= start_ms)
);

CREATE TABLE IF NOT EXISTS graph_relationships (
    relationship_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_entity_id UUID NOT NULL REFERENCES graph_entities(entity_id),
    relationship_type TEXT NOT NULL CHECK (relationship_type IN (
        'mentions', 'about', 'supports', 'contradicts', 'supersedes', 'parent_of', 'related_to'
    )),
    target_entity_id UUID NOT NULL REFERENCES graph_entities(entity_id),
    status TEXT NOT NULL DEFAULT 'active'
        CHECK (status IN ('active', 'needs_review', 'superseded')),
    confidence DOUBLE PRECISION NOT NULL CHECK (confidence BETWEEN 0 AND 1),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CHECK (source_entity_id <> target_entity_id)
);

CREATE TABLE IF NOT EXISTS graph_action_status_events (
    event_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    action_item_id UUID NOT NULL REFERENCES graph_action_items(action_item_id),
    from_status TEXT,
    to_status TEXT NOT NULL CHECK (to_status IN ('open', 'in_progress', 'blocked', 'completed', 'cancelled')),
    event_source TEXT NOT NULL,
    evidence_segment_id UUID,
    evidence_revision INTEGER,
    occurred_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CHECK ((evidence_segment_id IS NULL) = (evidence_revision IS NULL))
);

CREATE INDEX IF NOT EXISTS graph_entities_type_status_idx ON graph_entities(entity_type, status);
CREATE INDEX IF NOT EXISTS graph_evidence_segment_idx ON graph_evidence(segment_id, segment_revision);
CREATE INDEX IF NOT EXISTS graph_relationship_source_idx ON graph_relationships(source_entity_id, relationship_type);
CREATE INDEX IF NOT EXISTS graph_relationship_target_idx ON graph_relationships(target_entity_id, relationship_type);
CREATE INDEX IF NOT EXISTS graph_action_owner_status_idx ON graph_action_items(owner_entity_id, status);
"""


def main() -> None:
    """Print the proposed migration for review or piping into migration tooling."""
    print(POSTGRES_DDL.strip())


if __name__ == "__main__":
    main()

# WEEK OUTPUT CONTRACT:
# Input: validated version-1 entities/action items with evidence references.
# Output: PostgreSQL DDL for canonical graph entities, action items, evidence,
# relationships, and append-only action status events; this script does not
# apply the DDL or claim connection to an unconfigured database.
