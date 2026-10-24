"""SQLite-backed transcript persistence used by the Week 7 and 8 APIs."""

from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from threading import Lock

from backend.app.database import open_configured_database, open_fixture_database
from backend.app.transcript_store import StaleTranscriptRevisionError, StoredTranscriptEvent


class SessionNotFoundError(Exception):
    """Raised when retrieval is requested for a session that does not exist."""


@dataclass(frozen=True)
class PersistedSegment:
    segment_id: str
    revision: int
    is_final: bool
    start_ms: int
    end_ms: int
    speaker_id: str
    text: str
    asr_confidence: float | None
    created_at: str


class TranscriptRepository:
    """Portable persistence boundary for transcript API contracts."""

    def __init__(self, connection: sqlite3.Connection | None = None) -> None:
        self._connection = connection or open_fixture_database()
        self._lock = Lock()

    @property
    def _postgres(self) -> bool:
        """Whether this connection is the optional psycopg production backend."""
        return self._connection.__class__.__module__.startswith("psycopg")

    def accept(self, *, event_id: str, session_id: str, created_at: str,
               segment_id: str, revision: int, is_final: bool, start_ms: int,
               end_ms: int, speaker_id: str, text: str,
               asr_confidence: float | None) -> tuple[StoredTranscriptEvent, bool]:
        """Persist an event once and only allow revisions to advance."""
        with self._lock:
            placeholder = "%s" if self._postgres else "?"
            existing = self._connection.execute(
                f"SELECT session_id, payload FROM domain_events WHERE event_id = {placeholder}", (event_id,)
            ).fetchone()
            if existing is not None:
                payload = json.loads(existing["payload"])
                return StoredTranscriptEvent(event_id, existing["session_id"], payload["segment_id"], payload["revision"]), False

            latest = self._connection.execute(
                f"SELECT MAX(revision) AS revision FROM transcript_segments WHERE session_id = {placeholder} AND segment_id = {placeholder}",
                (session_id, segment_id),
            ).fetchone()["revision"]
            if latest is not None and revision <= latest:
                raise StaleTranscriptRevisionError(latest)

            try:
                self._connection.execute("BEGIN") if not self._postgres else None
                self._connection.execute(
                    "INSERT INTO sessions(session_id, created_at, updated_at) VALUES (%s, %s, %s) ON CONFLICT (session_id) DO NOTHING" if self._postgres else "INSERT OR IGNORE INTO sessions(session_id, created_at, updated_at) VALUES (?, ?, ?)",
                    (session_id, created_at, created_at),
                )
                self._connection.execute(
                    "UPDATE sessions SET status = 'processing', updated_at = %s WHERE session_id = %s" if self._postgres else "UPDATE sessions SET status = 'processing', updated_at = ? WHERE session_id = ?",
                    (created_at, session_id),
                )
                self._connection.execute(
                    """INSERT INTO transcript_segments
                       (segment_id, session_id, revision, is_final, start_ms, end_ms, speaker_id, text, asr_confidence, created_at)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""" if self._postgres else """INSERT INTO transcript_segments
                       (segment_id, session_id, revision, is_final, start_ms, end_ms, speaker_id, text, asr_confidence, created_at)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (segment_id, session_id, revision, is_final if self._postgres else int(is_final), start_ms, end_ms, speaker_id, text, asr_confidence, created_at),
                )
                self._connection.execute(
                    """INSERT INTO speaker_attributions
                       (attribution_id, segment_id, segment_revision, speaker_label, created_at)
                       VALUES (%s, %s, %s, %s, %s)""" if self._postgres else """INSERT INTO speaker_attributions
                       (attribution_id, segment_id, segment_revision, speaker_label, created_at)
                       VALUES (?, ?, ?, ?, ?)""",
                    (f"{segment_id}:r{revision}:primary", segment_id, revision, speaker_id, created_at),
                )
                self._connection.execute(
                    """INSERT INTO domain_events(event_id, session_id, event_type, schema_version, payload, created_at)
                       VALUES (%s, %s, 'transcript.segment', '1.0', %s::jsonb, %s)""" if self._postgres else """INSERT INTO domain_events(event_id, session_id, event_type, schema_version, payload, created_at)
                       VALUES (?, ?, 'transcript.segment', '1.0', ?, ?)""",
                    (event_id, session_id, json.dumps({"segment_id": segment_id, "revision": revision}), created_at),
                )
                # A corrected source revision invalidates derived graph claims
                # that cited an older revision; immutable history is retained.
                self._connection.execute(
                    """UPDATE graph_entities SET status = 'needs_review', updated_at = ?
                       WHERE entity_id IN (
                           SELECT record_id FROM graph_evidence
                           WHERE record_type = 'entity' AND segment_id = ? AND segment_revision < ?
                       )""" if not self._postgres else """UPDATE graph_entities SET status = 'needs_review', updated_at = %s
                       WHERE entity_id IN (
                           SELECT record_id FROM graph_evidence
                           WHERE record_type = 'entity' AND segment_id = %s AND segment_revision < %s
                       )""",
                    (created_at, segment_id, revision),
                )
                self._connection.execute(
                    """UPDATE graph_action_items SET status = 'needs_review', updated_at = ?
                       WHERE action_item_id IN (
                           SELECT record_id FROM graph_evidence
                           WHERE record_type = 'action_item' AND segment_id = ? AND segment_revision < ?
                       )""" if not self._postgres else """UPDATE graph_action_items SET status = 'needs_review', updated_at = %s
                       WHERE action_item_id IN (
                           SELECT record_id FROM graph_evidence
                           WHERE record_type = 'action_item' AND segment_id = %s AND segment_revision < %s
                       )""",
                    (created_at, segment_id, revision),
                )
                self._connection.commit() if not self._postgres else None
            except Exception:
                self._connection.rollback()
                raise
            return StoredTranscriptEvent(event_id, session_id, segment_id, revision), True

    def list_segments(self, session_id: str, *, include_revisions: bool) -> list[PersistedSegment]:
        with self._lock:
            placeholder = "%s" if self._postgres else "?"
            if self._connection.execute(f"SELECT 1 FROM sessions WHERE session_id = {placeholder}", (session_id,)).fetchone() is None:
                raise SessionNotFoundError(session_id)
            if include_revisions:
                query = f"SELECT * FROM transcript_segments WHERE session_id = {placeholder} ORDER BY start_ms, end_ms, segment_id, revision"
            else:
                query = f"""SELECT segment.* FROM transcript_segments AS segment
                           WHERE segment.session_id = {placeholder} AND segment.revision = (
                               SELECT MAX(candidate.revision) FROM transcript_segments AS candidate
                               WHERE candidate.session_id = segment.session_id AND candidate.segment_id = segment.segment_id
                           ) ORDER BY segment.start_ms, segment.end_ms, segment.segment_id"""
            rows = self._connection.execute(query, (session_id,)).fetchall()
            return [PersistedSegment(row["segment_id"], row["revision"], bool(row["is_final"]), row["start_ms"], row["end_ms"], row["speaker_id"], row["text"], row["asr_confidence"], row["created_at"]) for row in rows]

    def list_session_ids(self) -> list[str]:
        """Return known sessions in stable order for cross-session retrieval."""
        with self._lock:
            rows = self._connection.execute("SELECT session_id FROM sessions ORDER BY created_at, session_id").fetchall()
            return [row["session_id"] for row in rows]

    def clear(self) -> None:
        """Reset application fixture data; used by isolated API tests."""
        with self._lock:
            for table in ("graph_evidence", "graph_relationships", "graph_action_items", "graph_entities", "derived_record_evidence", "derived_records", "speaker_attributions", "domain_events", "transcript_segments", "sessions"):
                self._connection.execute(f"DELETE FROM {table}")
            self._connection.commit()


transcript_repository = TranscriptRepository(open_configured_database())
