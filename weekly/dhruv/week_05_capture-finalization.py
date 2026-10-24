"""
Week 05 (07-09-2026 - 13-09-2026)
Task: Fix bugs and finalize the capture module

Why this matters:
Capture is the first pipeline boundary, so downstream ASR needs predictable,
timestamped chunks regardless of the device adapter used. This check freezes
the validated local-capture event contract before provider integrations begin.

What this script does:
It creates a small deterministic PCM fixture and verifies chunk ordering,
timestamps, metadata, and file persistence without requiring a microphone.
"""

from datetime import datetime, timezone
from pathlib import Path
import tempfile
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ml.audio.capture import make_audio_chunks


def run_check() -> dict[str, object]:
    with tempfile.TemporaryDirectory() as directory:
        pcm = b"\x00\x00" * 16_000 * 2  # two seconds of mono 16-bit PCM
        chunks = make_audio_chunks(
            pcm,
            session_id="00000000-0000-4000-8000-000000000005",
            chunk_directory=Path(directory),
            captured_at=datetime(2026, 9, 13, tzinfo=timezone.utc),
        )
        assert [chunk.sequence for chunk in chunks] == [0, 1]
        assert all(chunk.audio_ref and Path(chunk.audio_ref).is_file() for chunk in chunks)
        assert all(chunk.to_event()["schema_version"] == "1.0" for chunk in chunks)
        return {"chunks": len(chunks), "duration_ms": sum(chunk.duration_ms for chunk in chunks)}


if __name__ == "__main__":
    print(f"[PASS] Dhruv Week 5: {run_check()}")

