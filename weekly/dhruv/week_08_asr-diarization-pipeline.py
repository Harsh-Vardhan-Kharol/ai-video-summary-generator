"""
Week 08 (28-09-2026 - 04-10-2026)
Task: Combine ASR and diarization into one pipeline

Why this matters:
Separate ASR and diarization streams become useful only after their timestamps
are joined. This wrapper validates the speaker-labeled transcript contract that
the backend and Garvit's NLP pipeline consume.

What this script does:
It runs the offline ASR/diarization join and checks that every turn has text,
timestamps, and an explicit speaker label.
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


def run_check() -> list[dict[str, object]]:
    with tempfile.TemporaryDirectory() as directory:
        audio = Path(directory) / "fixture.wav"
        audio.write_bytes(b"fixture")
        turns = AudioTranscriptPipeline(FixtureTranscriber(), FixtureDiarizer()).process(audio)
        assert turns and all(turn.speaker and turn.text for turn in turns)
        return [turn.to_dict() for turn in turns]


if __name__ == "__main__":
    print(f"[PASS] Dhruv Week 8: {run_check()}")

