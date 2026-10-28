"""Deterministic quality and provenance metadata for audio-derived records.

This module deliberately uses PCM bytes and transcript intervals only.  It is
an explainable triage signal, not a replacement for WER/DER measurements from
real recordings or a calibrated confidence model.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
import math
from typing import Any, Iterable


@dataclass(frozen=True)
class AudioQualityMetadata:
    sample_rate_hz: int
    channels: int
    duration_ms: int
    rms: float
    peak: float
    silence_ratio: float
    clipping_ratio: float
    source: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def pcm16_quality(
    pcm_s16le: bytes,
    *,
    sample_rate_hz: int,
    channels: int = 1,
    source: str = "unknown",
    silence_threshold: float = 0.01,
) -> AudioQualityMetadata:
    """Calculate bounded quality metadata from little-endian signed PCM16."""
    if not pcm_s16le or len(pcm_s16le) % 2:
        raise ValueError("PCM16 data must contain at least one complete sample")
    if sample_rate_hz <= 0 or channels <= 0:
        raise ValueError("sample_rate_hz and channels must be positive")
    if not source.strip():
        raise ValueError("source must not be empty")
    if not 0 <= silence_threshold <= 1:
        raise ValueError("silence_threshold must be between 0 and 1")

    values = [int.from_bytes(pcm_s16le[index:index + 2], "little", signed=True) for index in range(0, len(pcm_s16le), 2)]
    normalized = [abs(value) / 32768.0 for value in values]
    return AudioQualityMetadata(
        sample_rate_hz=sample_rate_hz,
        channels=channels,
        duration_ms=round(len(values) / channels * 1000 / sample_rate_hz),
        rms=math.sqrt(sum(value * value for value in normalized) / len(normalized)),
        peak=max(normalized),
        silence_ratio=sum(value < silence_threshold for value in normalized) / len(normalized),
        clipping_ratio=sum(value >= 0.999 for value in normalized) / len(normalized),
        source=source,
    )


def overlap_pairs(segments: Iterable[dict[str, Any]]) -> list[tuple[str, str]]:
    """Return deterministic pairs of intervals with positive intersection."""
    materialized = list(segments)
    pairs: list[tuple[str, str]] = []
    for index, left in enumerate(materialized):
        for right in materialized[index + 1:]:
            if min(int(left["end_ms"]), int(right["end_ms"])) > max(int(left["start_ms"]), int(right["start_ms"])):
                pairs.append((str(left["segment_id"]), str(right["segment_id"])))
    return pairs
