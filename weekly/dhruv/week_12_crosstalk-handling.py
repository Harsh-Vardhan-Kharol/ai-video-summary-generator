"""
Week 12 (20-10-2026 - 26-10-2026)
Task: Improve diarization handling for crosstalk

Why this matters:
Overlapping speaker intervals cannot be safely reduced to one identity because
that would turn uncertain audio into false ownership evidence. This week
extends the Week 8 transcript handoff with explicit overlap metadata while
keeping the existing primary speaker field compatible with Dev's API.

What this script does:
Runs a deterministic crosstalk fixture and asserts that the primary label,
secondary speakers, overlap ratio, and review flag are all preserved.
"""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ml.audio.week6_asr import TranscriptSegment
from ml.audio.week7_diarization import DiarizationSegment
from ml.audio.week8_transcript_pipeline import align_segments


def main() -> int:
    turns = align_segments(
        [TranscriptSegment("asr-1", 0, 1000, "We should ship this.")],
        [
            DiarizationSegment("spk-1", 0, 800, "SPEAKER_00"),
            DiarizationSegment("spk-2", 500, 1000, "SPEAKER_01"),
        ],
    )
    assert turns[0].speaker == "SPEAKER_00"
    assert turns[0].overlapping_speakers == ("SPEAKER_01",)
    assert turns[0].overlap_ratio == 0.5
    assert turns[0].needs_review is True
    print("[PASS] Dhruv Week 12: crosstalk is preserved and flagged for review")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


# WEEK OUTPUT CONTRACT:
# Input: timestamped ASR and diarization segments.
# Output: TranscriptTurn values with a compatible primary speaker plus
#         explicit overlapping speakers, overlap ratio, and review state.
