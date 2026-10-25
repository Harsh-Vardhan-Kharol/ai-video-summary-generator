"""
Week 17 (30-11-2026 - 06-12-2026)
Task: Test scoring against known-good/bad summaries

Why this matters:
Confidence policy needs regression cases that distinguish grounded output from
unsupported additions. These tests protect the graph ingestion safety gate.

What this script does:
Runs the focused confidence and unsupported-claim regression tests.
"""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from ml.nlp.tests.test_combined_pipeline import CombinedPipelineTests


if __name__ == "__main__":
    names = ["test_support_score_exposes_explainable_components", "test_unsupported_words_are_not_sent_to_graph"]
    suite = unittest.TestSuite(CombinedPipelineTests(name) for name in names)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    raise SystemExit(not result.wasSuccessful())
