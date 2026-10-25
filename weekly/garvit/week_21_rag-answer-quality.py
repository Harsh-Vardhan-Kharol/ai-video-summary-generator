"""
Week 21 (26-12-2026 - 01-01-2027)
Task: Evaluate RAG answer quality with Harsh

Why this matters:
Garvit's evidence policy should also hold when extracted facts are retrieved
by Harsh's RAG layer. This check ensures answers have source-revision citations
instead of relying on an uncited summary.

What this script does:
Runs Harsh's evidence and insufficient-evidence RAG regression tests.
"""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from backend.tests.test_graph_rag import (
    test_query_returns_exact_citations_and_insufficient_evidence,
)


if __name__ == "__main__":
    suite = unittest.TestSuite([unittest.FunctionTestCase(test_query_returns_exact_citations_and_insufficient_evidence)])
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    raise SystemExit(not result.wasSuccessful())
