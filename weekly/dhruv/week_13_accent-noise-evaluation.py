"""
Week 13 (27-10-2026 - 02-11-2026)
Task: Test the pipeline on varied accents and noisy audio

Why this matters:
Provider accuracy cannot be established from synthetic fixtures alone, but the
pipeline can still make noisy-input behavior measurable and repeatable. These
checks protect the ASR boundary from malformed audio and expose quality flags
that downstream review and graph metadata can retain.

What this script does:
Runs deterministic clean, noisy, silent, and clipped PCM fixtures through the
preprocessing and quality-report helpers, and validates the transcript contract
with the offline ASR/diarization pipeline.
"""

from pathlib import Path
import sys
import struct
import tempfile

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ml.audio.preprocess import prepare_pcm_for_asr
from ml.audio.quality import pcm16_quality
from ml.audio.week6_asr import FixtureTranscriber
from ml.audio.week7_diarization import FixtureDiarizer
from ml.audio.week8_transcript_pipeline import AudioTranscriptPipeline


def samples(values: list[int]) -> bytes:
    return b"".join(struct.pack("<h", value) for value in values)


def run_check() -> dict[str, object]:
    fixtures = {
        "clean": samples([1200, -1200, 900, -900]),
        "noisy": samples([100, -80, 120, -100, 1200, -1200, 900, -900]),
        "silent": samples([0, 0, 0, 0]),
        "clipped": samples([32767, -32768, 32767, -32768]),
    }
    reports = {name: pcm16_quality(data, sample_rate_hz=1000).to_dict() for name, data in fixtures.items()}
    assert "mostly_silent" in reports["silent"]["quality_flags"]
    assert "clipping" in reports["clipped"]["quality_flags"]
    prepared = prepare_pcm_for_asr(fixtures["noisy"], noise_threshold=0.01)
    assert pcm16_quality(prepared, sample_rate_hz=1000).peak > 0

    with tempfile.TemporaryDirectory() as directory:
        audio = Path(directory) / "fixture.wav"
        audio.write_bytes(b"offline-fixture")
        turns = AudioTranscriptPipeline(FixtureTranscriber(), FixtureDiarizer()).process(audio)
    assert turns and all(turn.to_nlp_segment()["speaker_label"] for turn in turns)
    return {"quality_reports": reports, "transcript_turns": len(turns)}


if __name__ == "__main__":
    print(f"[PASS] Dhruv Week 13: {run_check()}")


# WEEK OUTPUT CONTRACT:
# Input: PCM16 fixtures and an audio file accepted by the ASR/diarization adapters.
# Output: quality metadata with review flags plus the unchanged speaker-labeled
#         transcript contract for Garvit and Dev.
