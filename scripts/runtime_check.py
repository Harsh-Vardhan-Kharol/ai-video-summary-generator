"""Show configured runtime dependencies without printing secret values."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.app.runtime_config import RuntimeConfig
from backend.app.database import open_configured_database
from backend.app.transcript_repository import TranscriptRepository


if __name__ == "__main__":
    config = RuntimeConfig.from_env()
    print(config.provider_status())
    if config.database_url:
        connection = open_configured_database()
        tables = [row["table_name"] for row in connection.execute(
            "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name"
        ).fetchall()]
        assert "transcript_embeddings" in tables
        repository = TranscriptRepository(connection)
        repository.accept(
            event_id="runtime-check-event", session_id="runtime-check-session",
            created_at="2026-10-21T12:00:00Z", segment_id="runtime-check-segment",
            revision=1, is_final=True, start_ms=0, end_ms=500,
            speaker_id="SPEAKER_00", text="Runtime check passed.", asr_confidence=1.0,
        )
        print(f"[PASS] PostgreSQL schema and round trip ({len(tables)} tables)")

