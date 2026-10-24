"""
Week 19 (14-12-2026 - 18-12-2026)
Task: Finalize the knowledge graph structure for RAG

Why this matters:
RAG needs durable entities and action items, but transcript evidence remains
the source of truth. The finalized relational graph preserves that distinction.

What this script does:
Publishes the production graph decision: PostgreSQL tables with an adapter seam,
not a mandatory separate graph database.
"""

Canonical records are `graph_entities`, `graph_action_items`,
`graph_relationships`, and `graph_evidence`. Every derived claim has at least
one `(session_id, segment_id, segment_revision)` reference. Source revisions
remain immutable and invalidate dependent claims for re-evaluation.

# WEEK OUTPUT CONTRACT:
# Input: validated graph-input v1 records.
# Output: relational graph rows usable by retrieval and audit views.
