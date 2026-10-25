"""
Week 18 (07-12-2026 - 13-12-2026)
Task: Tune thresholds for reliability

Why this matters:
Thresholds define when records can enter durable graph storage and when they
need review. Keeping the policy explicit makes the trade-off defensible during
thesis evaluation.

What this script does:
Validates the default policy and demonstrates its review-required band.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from ml.nlp.confidence import DEFAULT_POLICY, ConfidencePolicy, assess_support


if __name__ == "__main__":
    DEFAULT_POLICY.validate()
    segments = [{"segment_id": "s1", "text": "Ravi will document API changes by Monday.", "asr_confidence": 0.96}]
    result = assess_support(
        "Ravi will document API changes by Monday promptly.", ["s1"], segments,
        policy=ConfidencePolicy(accept_threshold=0.95, review_threshold=0.45),
    )
    assert result["status"] == "review_required"
    print("PASS: policy", DEFAULT_POLICY, "marks the borderline fixture as", result["status"])
