"""
Week 19 (14-12-2026 - 18-12-2026)
Task: Finalize scoring integration

Why this matters:
The final output must carry support information through both graph and display
paths without overwriting the extractor's own confidence value.

What this script does:
Verifies that support assessments are attached to graph properties and UI data.
"""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from ml.nlp.tests.test_combined_pipeline import CombinedPipelineTests


if __name__ == "__main__":
    suite = unittest.TestSuite([CombinedPipelineTests("test_creates_revision_specific_graph_and_display_payloads")])
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    raise SystemExit(not result.wasSuccessful())
