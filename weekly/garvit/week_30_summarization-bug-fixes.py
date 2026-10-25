"""
Week 30 (27-02-2027 - 05-03-2027)
Task: Fix remaining summarization bugs

Why this matters:
The final safety fixes address package-import reliability and malformed source
handling, which otherwise fail before any provider response can be assessed.

What this script does:
Checks package imports and verifies provisional transcript input is rejected.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from ml.nlp.combined_pipeline import MeetingNlpPipeline


if __name__ == "__main__":
    provisional = [{"segment_id": "s1", "revision": 1, "is_final": False, "start_ms": 0, "end_ms": 1000, "speaker_label": "S1", "text": "Do not persist this yet.", "asr_confidence": 0.9}]
    try:
        MeetingNlpPipeline(lambda _messages: {}).process(session_id="bug-check", segments=provisional)
    except ValueError:
        print("PASS: package import works and provisional transcript evidence is rejected.")
    else:
        raise SystemExit("FAIL: provisional transcript was accepted")
