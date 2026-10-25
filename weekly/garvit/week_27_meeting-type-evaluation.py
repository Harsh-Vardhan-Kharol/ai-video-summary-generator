"""
Week 27 (06-02-2027 - 12-02-2027)
Task: Test across different meeting types and lengths

Why this matters:
The NLP contract must not depend on one planning-meeting phrasing. Short
stand-ups, lectures, and conditional planning require different extraction
behaviour while retaining the same evidence rules.

What this script does:
Runs the combined pipeline on three deterministic meeting-shaped fixtures.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from ml.nlp.combined_pipeline import MeetingNlpPipeline
from ml.nlp.evaluation import evaluate_output


CASES = [
    ("standup", [{"segment_id": "s1", "revision": 1, "is_final": True, "start_ms": 0, "end_ms": 1000, "speaker_label": "S1", "text": "Ravi will fix the login error today.", "asr_confidence": 0.98}], {"text": "Ravi will fix the login error today.", "covered_segment_ids": ["s1"]}, {"items": [{"id": "a1", "type": "action_item", "text": "Ravi will fix the login error today.", "confidence": 0.98, "evidence_segment_ids": ["s1"]}]}),
    ("lecture", [{"segment_id": "l1", "revision": 1, "is_final": True, "start_ms": 0, "end_ms": 2000, "speaker_label": "S1", "text": "Today the lecture explains retrieval augmented generation and citations.", "asr_confidence": 0.97}], {"text": "The lecture explains retrieval augmented generation and citations.", "covered_segment_ids": ["l1"]}, {"items": [{"id": "t1", "type": "topic", "text": "Retrieval augmented generation and citations.", "confidence": 0.95, "evidence_segment_ids": ["l1"]}]}),
    ("conditional-planning", [{"segment_id": "p1", "revision": 1, "is_final": True, "start_ms": 0, "end_ms": 2000, "speaker_label": "S1", "text": "We could release Friday if QA passes.", "asr_confidence": 0.96}], {"text": "A Friday release remains conditional on QA passing.", "covered_segment_ids": ["p1"]}, {"items": [{"id": "t2", "type": "topic", "text": "A Friday release is conditional on QA passing.", "confidence": 0.94, "evidence_segment_ids": ["p1"]}]}),
]


if __name__ == "__main__":
    for name, segments, summary, extraction in CASES:
        replies = iter((summary, extraction))
        output = MeetingNlpPipeline(lambda _messages: next(replies)).process(session_id=name, segments=segments)
        report = evaluate_output(output, segments)
        assert report["passed"], (name, report["errors"])
    print("PASS: stand-up, lecture, and conditional-planning fixtures satisfy NLP output safety checks.")
