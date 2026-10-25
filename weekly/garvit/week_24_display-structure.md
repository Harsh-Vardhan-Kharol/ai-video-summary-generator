"""
Week 24 (16-01-2027 - 22-01-2027)
Task: Define how summaries/action items should be structured for display

Why this matters:
The UI needs enough provenance to explain AI output without exposing storage
internals. A compact display contract lets Dev render summaries and action
items consistently while retaining a path back to transcript evidence.

What this script does:
Publishes the fields in `nlp-output-1.0.display` for Dev's frontend.
"""

# Display contract

`display.summary` is a string, `display.summary_support` is the support
assessment, and `display.evidence_turn_count` is an integer. Each
`display.action_items[]` entry contains `id`, `text`, nullable `owner`,
`owner_status`, nullable `due_date_text`, lifecycle `status`, extractor
`confidence`, deterministic `support`, and revision-specific `evidence`.

The frontend should show `review_required` and `rejected` status visibly rather
than styling every extraction as authoritative. It must use `owner_status` to
render unresolved owners, not infer identity from a speaker label. Clicking an
evidence reference should navigate to its `start_ms` transcript position.

The current frontend has hard-coded summary/action copy and no summary endpoint,
so Dev must add an API retrieval path before this contract can be rendered from
live data.
