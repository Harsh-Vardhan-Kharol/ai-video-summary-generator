"""
Week 02 (17-08-2026 - 23-08-2026)
Task: Draft initial prompt templates

Why this matters:
The summarizer consumes Dhruv's timestamped transcript segments and produces material stored and indexed by Dev, then cited by Harsh's RAG layer. The prompts set evidence and provenance requirements before an LLM provider is selected or prompt quality is evaluated.

What this script does:
Builds provider-neutral system/user prompt messages from transcript segments and prints an example prompt when run directly.
"""

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ml.nlp.prompts import build_summary_messages


SAMPLE_SEGMENTS = [
    {
        "segment_id": "seg-001",
        "speaker_id": "speaker-1",
        "start_ms": 0,
        "end_ms": 1800,
        "text": "Let's review the capture prototype next week.",
    },
    {
        "segment_id": "seg-002",
        "speaker_id": "speaker-2",
        "start_ms": 2200,
        "end_ms": 3600,
        "text": "I can review it by Friday and send notes.",
    },
]


def main() -> None:
    print(json.dumps(build_summary_messages(SAMPLE_SEGMENTS), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
