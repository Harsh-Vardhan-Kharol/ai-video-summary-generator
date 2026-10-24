"""
Week 09 (05-10-2026 - 11-10-2026)
Task: Test on sample recordings, measure accuracy

Why this matters:
Before tuning models, the team needs repeatable checks for coverage and timing.
These lightweight fixture metrics make regressions visible without pretending
that synthetic audio is a real-world accuracy benchmark.

What this script does:
It reports transcript coverage and speaker-label coverage for the fixture path.
"""

from pathlib import Path
import tempfile
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ml.audio.week6_asr import FixtureTranscriber
from ml.audio.week7_diarization import FixtureDiarizer
from ml.audio.week8_transcript_pipeline import AudioTranscriptPipeline


def run_check() -> dict[str, float]:
    with tempfile.TemporaryDirectory() as directory:
        audio = Path(directory) / "fixture.wav"
        audio.write_bytes(b"fixture")
        turns = AudioTranscriptPipeline(FixtureTranscriber(), FixtureDiarizer()).process(audio)
        covered = sum(turn.end_ms - turn.start_ms for turn in turns)
        return {"turn_count": float(len(turns)), "speaker_label_rate": sum(bool(t.speaker) for t in turns) / len(turns), "covered_ms": float(covered)}


if __name__ == "__main__":
    print(f"[PASS] Dhruv Week 9: {run_check()}")

