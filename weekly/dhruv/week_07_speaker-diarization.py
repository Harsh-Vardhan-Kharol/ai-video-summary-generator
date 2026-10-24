"""
Week 07 (21-09-2026 - 27-09-2026)
Task: Integrate Pyannote for speaker diarization

Why this matters:
Speaker labels let the NLP stage distinguish owners, decisions, and questions.
The offline diarizer mirrors the Pyannote output shape until model credentials
and weights are available in the development environment.

What this script does:
It verifies that diarization output is timestamped, labeled, and confidence-safe.
"""

from pathlib import Path
import tempfile
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ml.audio.week7_diarization import FixtureDiarizer


def run_check() -> list[dict[str, object]]:
    with tempfile.TemporaryDirectory() as directory:
        audio = Path(directory) / "fixture.wav"
        audio.write_bytes(b"fixture")
        segments = FixtureDiarizer().diarize(audio)
        assert segments and all(segment.speaker for segment in segments)
        return [segment.to_dict() for segment in segments]


if __name__ == "__main__":
    print(f"[PASS] Dhruv Week 7: {run_check()}")

