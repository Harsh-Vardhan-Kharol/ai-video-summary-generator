"""Explicit runtime/provider configuration for local and live deployments."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class RuntimeConfig:
    database_url: str | None
    asr_provider: str
    diarization_provider: str
    llm_provider: str
    embedding_provider: str

    @classmethod
    def from_env(cls) -> "RuntimeConfig":
        return cls(
            database_url=os.getenv("DATABASE_URL"),
            asr_provider=os.getenv("ASR_PROVIDER", "fixture"),
            diarization_provider=os.getenv("DIARIZATION_PROVIDER", "fixture"),
            llm_provider=os.getenv("LLM_PROVIDER", "fixture"),
            embedding_provider=os.getenv("EMBEDDING_PROVIDER", "fixture"),
        )

    def provider_status(self) -> dict[str, str]:
        return {
            "database": "postgresql" if self.database_url else "sqlite_fixture",
            "asr": self.asr_provider,
            "diarization": self.diarization_provider,
            "llm": self.llm_provider,
            "embeddings": self.embedding_provider,
        }

