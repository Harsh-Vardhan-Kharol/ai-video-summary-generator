"""
Week 18 (07-12-2026 - 13-12-2026)
Task: Refine graph relationships from test results

Why this matters:
The relationship vocabulary must remain small enough to explain and strict
enough to avoid accidental claims. Invalid endpoints and relationship types
are rejected at ingestion.

What this script does:
Records the accepted relationship set and review policy.
"""

Allowed relationships: `mentions`, `about`, `supports`, `contradicts`,
`supersedes`, `parent_of`, and `related_to`. Relationship evidence is stored
as JSON and relationship confidence is bounded to 0..1. Self-links are
rejected; ambiguous links remain `needs_review` rather than being merged.

# WEEK OUTPUT CONTRACT:
# Input: candidate entity relationships with evidence.
# Output: validated, typed relationship rows or an explicit validation error.
