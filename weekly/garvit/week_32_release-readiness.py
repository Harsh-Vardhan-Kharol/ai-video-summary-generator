"""
Week 32 (13-03-2027 - 19-03-2027)
Task: Confirm the summarization pipeline is release-ready

Why this matters:
The final readiness check confirms all deterministic contracts that Garvit owns
are stable: final-only input, grounded output, review gating, graph handoff,
and display payload validation.

What this script does:
Runs the full offline Garvit NLP acceptance suite.
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
