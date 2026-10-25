"""
Week 31 (06-03-2027 - 12-03-2027)
Task: Polish prompt and output quality

Why this matters:
Release output needs clear concise wording while still exposing evidence and
uncertainty. The check prevents presentation fields from drifting from the
graph-safe payload.

What this script does:
Runs prompt, display, and quality regression checks together.
"""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from ml.nlp.tests.test_combined_pipeline import CombinedPipelineTests


if __name__ == "__main__":
    names = ["test_creates_revision_specific_graph_and_display_payloads", "test_display_and_quality_contracts_accept_fixture_output"]
    suite = unittest.TestSuite(CombinedPipelineTests(name) for name in names)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    raise SystemExit(not result.wasSuccessful())
