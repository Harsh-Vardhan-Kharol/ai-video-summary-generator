"""
Week 16 (21-11-2026 - 29-11-2026)
Task: Build a confidence-scoring mechanism

Why this matters:
Extractor confidence alone does not show whether generated wording is grounded
in the cited transcript. A separate support score makes the safety decision
auditable without changing the graph's extraction-confidence semantics.

What this script does:
Scores one supported and one unsupported claim against the same source turn.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from ml.nlp.confidence import assess_support


if __name__ == "__main__":
    segments = [{"segment_id": "s1", "text": "Ravi will document the API changes by Monday.", "asr_confidence": 0.96}]
    supported = assess_support("Ravi will document the API changes by Monday.", ["s1"], segments)
    unsupported = assess_support("Buy a helicopter urgently.", ["s1"], segments)
    assert supported["status"] == "accepted"
    assert unsupported["status"] == "rejected"
    print("PASS:", {"supported": supported, "unsupported": unsupported})
