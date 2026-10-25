"""
Week 14 (03-11-2026 - 13-11-2026)
Task: Test combined output against Harsh's schema

Why this matters:
Graph ingestion is the first durable consumer of extracted entities and action
items. This check verifies Garvit's output against the actual shared API rather
than relying only on a written schema.

What this script does:
Runs the focused NLP-to-graph API contract test.
"""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from ml.nlp.tests.test_combined_pipeline import CombinedPipelineTests


if __name__ == "__main__":
    suite = unittest.TestSuite([CombinedPipelineTests("test_accepted_graph_batch_is_accepted_by_the_shared_api")])
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    raise SystemExit(not result.wasSuccessful())
