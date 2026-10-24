"""
Week 02 (17-08-2026 - 23-08-2026)
Task: Build the initial local audio capture module

Why this matters:
Capture is the first live stage and must hand downstream ASR ordered, timestamped audio without binding ASR to a particular device API. This first implementation records local microphone audio; system-loopback adapters remain platform-specific follow-up work.

What this script does:
Exposes the microphone capture implementation and provides a small command-line entry point that writes a WAV clip and prints its audio-chunk event metadata.
"""

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ml.audio.capture import capture_microphone, float_samples_to_pcm16le, make_audio_chunks


def main() -> None:
    parser = argparse.ArgumentParser(description="Capture a local microphone clip for ASR.")
    parser.add_argument("output", type=Path, nargs="?", help="path for the captured WAV file")
    parser.add_argument("--duration", type=float, default=5.0, help="recording length in seconds")
    parser.add_argument("--device", help="optional sounddevice input device name or numeric index")
    args = parser.parse_args()
    device: int | str | None = args.device
    if isinstance(device, str) and device.isdecimal():
        device = int(device)

    if args.output is not None:
        chunks = capture_microphone(args.output, duration_seconds=args.duration, device=device)
    else:
        # A no-argument run is safe in CI and on machines without a microphone;
        # passing an output path retains the real microphone capture behavior.
        with tempfile.TemporaryDirectory() as directory:
            pcm = b"\x00\x00" * 16_000 * max(1, round(args.duration))
            chunks = make_audio_chunks(
                pcm,
                session_id="00000000-0000-4000-8000-000000000002",
                chunk_directory=Path(directory) / "fixture-chunks",
                captured_at=datetime.now(timezone.utc),
            )
            print(json.dumps([chunk.to_event() for chunk in chunks], indent=2))
            return
    print(json.dumps([chunk.to_event() for chunk in chunks], indent=2))


if __name__ == "__main__":
    main()
