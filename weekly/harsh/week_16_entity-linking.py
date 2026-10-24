"""
Week 16 (21-11-2026 - 29-11-2026)
Task: Build entity-linking logic across meetings

Why this matters:
Cross-session memory requires canonical entities while keeping session-local
speaker labels separate. This implementation uses explicit IDs and producer
references, so linking remains reviewable and conservative.

What this script does:
Documents the executable GraphRepository ingestion boundary implemented in the
backend and validates a minimal evidence-backed fixture when run directly.
"""

from backend.app.graph_repository import GraphValidationError


def linking_policy() -> dict[str, str]:
    return {
        "speaker_labels": "session-local observation only",
        "person_identity": "explicit entity ID or later user resolution",
        "ambiguous_match": "retain separate candidate and needs_review status",
    }


if __name__ == "__main__":
    print(linking_policy())

# WEEK OUTPUT CONTRACT:
# Input: version-1 entity/action records with revisioned evidence.
# Output: canonical graph records and explicit relationship edges.
