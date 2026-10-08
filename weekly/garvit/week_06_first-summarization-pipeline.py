"""
Week 06 (14-09-2026 - 20-09-2026)
Task: Build the first working summarization pipeline

Why this matters:
The Week 5 prompt set defines the summary and extraction contracts, but prompt builders alone do not turn model responses into safe downstream records. This pipeline validates final transcript evidence and checks both JSON responses before producing the combined NLP output that storage and RAG can consume.

What this script does:
This runner demonstrates the pipeline on a sample transcript with deterministic fixture responses. It validates response shapes and evidence references without making an external provider call.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
NLP_DIR = REPO_ROOT / "ml" / "nlp"
if str(NLP_DIR) not in sys.path:
    sys.path.insert(0, str(NLP_DIR))

from week6_summarization_pipeline import SummarizationPipeline  # noqa: E402


FIXTURE_PATH = NLP_DIR / "fixtures" / "week_03_sample_transcripts.json"


def load_fixture() -> dict[str, Any]:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def load_fixture_responses() -> tuple[list[dict[str, Any]], dict[str, Any], dict[str, Any]]:
    case = load_fixture()["cases"][0]
    return (
        case["transcript_segments"],
        case["reference_summary"],
        case["reference_extraction"],
    )


def main() -> int:
    segments, summary_response, extraction_response = load_fixture_responses()
    responses = iter((summary_response, extraction_response))

    def fixture_generator(messages: list[dict[str, str]]) -> str:
        # Consume one hand-written expected response per prompt invocation.
        try:
            response = next(responses)
        except StopIteration as error:
            raise RuntimeError("pipeline requested more fixture responses than expected") from error
        if [message["role"] for message in messages] != ["system", "user"]:
            raise RuntimeError("pipeline did not provide the expected system/user messages")
        return json.dumps(response, ensure_ascii=False)

    result = SummarizationPipeline(fixture_generator).process(segments)
    print("Week 06 fixture-backed summarization pipeline")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print("PASS: summary and extraction responses satisfy the current output/evidence contract.")
    print("LIMITATION: responses are hand-written fixtures; no LLM provider or generated quality was evaluated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


# WEEK OUTPUT CONTRACT:
# Input: Week 3 sample transcript fixture and its hand-written reference outputs.
# Output: Validated summary and extraction objects with evidence segment IDs.
#         The pipeline accepts a provider callable but this demo uses fixtures.
