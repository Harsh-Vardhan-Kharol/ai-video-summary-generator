"""
Week 06 (14-09-2026 - 20-09-2026)
Task: Integrate Whisper/Deepgram for transcription

Why this matters:
ASR converts capture chunks into timestamped text consumed by diarization and
summarization. The provider-neutral adapter keeps credentials and model choice
outside the weekly contract while making offline development repeatable.

What this script does:
It smoke-tests the deterministic ASR adapter against a local audio fixture.
"""

from pathlib import Path
import tempfile
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ml.audio.week6_asr import FixtureTranscriber


def run_check() -> list[dict[str, object]]:
    with tempfile.TemporaryDirectory() as directory:
        audio = Path(directory) / "fixture.wav"
        audio.write_bytes(b"fixture")
        segments = FixtureTranscriber().transcribe(audio)
        assert segments and all(segment.end_ms > segment.start_ms for segment in segments)
        return [segment.to_dict() for segment in segments]


if __name__ == "__main__":
    print(f"[PASS] Dhruv Week 6: {run_check()}")

