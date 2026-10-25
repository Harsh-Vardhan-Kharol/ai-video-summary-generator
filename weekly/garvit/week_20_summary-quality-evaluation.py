"""
Week 20 (19-12-2026 - 25-12-2026)
Task: Evaluate summarization quality across more meetings

Why this matters:
Quality needs repeatable evidence and safety checks across conditional planning
and explicit decisions, rather than a single successful demonstration.

What this script does:
Evaluates the representative fixture suite for evidence validity and forbidden
claims using the combined output contract.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from ml.nlp.combined_pipeline import MeetingNlpPipeline
from ml.nlp.evaluation import evaluate_output


if __name__ == "__main__":
    cases = json.loads((ROOT / "ml/nlp/fixtures/week_03_sample_transcripts.json").read_text(encoding="utf-8"))["cases"]
    reports = []
    for case in cases:
        responses = iter((case["reference_summary"], case["reference_extraction"]))
        output = MeetingNlpPipeline(lambda _messages: next(responses)).process(session_id=case["case_id"], segments=case["transcript_segments"])
        report = evaluate_output(output, case["transcript_segments"], case["must_not_claim"])
        assert report["passed"], report["errors"]
        reports.append({"case_id": case["case_id"], **report})
    print(json.dumps(reports, indent=2))
    print("PASS: fixture quality checks found no unsupported forbidden claim or broken evidence.")
