"""
Week 25 (23-01-2027 - 29-01-2027)
Task: Work with Dev on the frontend data format

Why this matters:
The frontend format must be validated independently of React so NLP changes do
not silently break presentation. This keeps Garvit's display contribution
compatible with Dev's separate frontend ownership.

What this script does:
Runs the display contract regression check on a combined pipeline output.
"""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from ml.nlp.tests.test_combined_pipeline import CombinedPipelineTests


if __name__ == "__main__":
    suite = unittest.TestSuite([CombinedPipelineTests("test_display_and_quality_contracts_accept_fixture_output")])
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    raise SystemExit(not result.wasSuccessful())
