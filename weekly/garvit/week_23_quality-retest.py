"""
Week 23 (09-01-2027 - 15-01-2027)
Task: Re-test and confirm improvements

Why this matters:
Prompt and scoring changes require regression verification before consumers can
rely on the new output version. The test covers quality safety, UI payloads,
and graph compatibility together.

What this script does:
Runs Garvit's complete deterministic NLP test suite.
"""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from ml.nlp.tests.test_combined_pipeline import CombinedPipelineTests


if __name__ == "__main__":
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(CombinedPipelineTests))
    raise SystemExit(not result.wasSuccessful())
