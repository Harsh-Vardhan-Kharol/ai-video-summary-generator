from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.transcript_repository import transcript_repository


client = TestClient(app)
SESSION = "graph-rag-session"


def setup_function():
    transcript_repository.clear()


def upload(segment_id="seg-graph-1", revision=1, text="We decided to ship the audio pipeline on Friday."):
    return client.post("/v1/transcript-segments", json={
        "schema_version": "1.0",
        "event_id": f"event-{segment_id}-{revision}",
        "session_id": SESSION,
        "created_at": "2026-10-24T10:00:00Z",
        "payload": {
            "segment_id": segment_id, "revision": revision, "is_final": True,
            "start_ms": 100, "end_ms": 2200, "speaker_id": "SPEAKER_01",
            "text": text, "asr_confidence": 0.96,
        },
    })


def test_graph_ingest_requires_real_evidence_and_preserves_unknown_owner():
    assert upload().status_code == 201
    response = client.post("/v1/graph/records", json={
        "session_id": SESSION,
        "entities": [{
            "id": "person-1", "type": "person", "text": "Priya", "confidence": 0.8,
            "evidence_segment_ids": ["seg-graph-1"],
        }],
        "action_items": [{
            "id": "action-1", "text": "Ship the audio pipeline on Friday", "confidence": 0.9,
            "evidence_segment_ids": ["seg-graph-1"], "due_date": "Friday", "owner": "SPEAKER_01",
        }],
    })
    assert response.status_code == 201
    assert response.json()["action_items"][0]["status"] == "open"
    records = client.get(f"/v1/sessions/{SESSION}/records")
    assert records.status_code == 200
    action = next(item for item in records.json()["records"] if item["record_type"] == "action_item")
    assert action["metadata"]["owner_text"] == "SPEAKER_01"
    assert action["evidence"][0]["segment_revision"] == 1


def test_query_returns_exact_citations_and_insufficient_evidence():
    assert upload().status_code == 201
    assert client.post("/v1/graph/records", json={
        "session_id": SESSION,
        "entities": [{"id": "topic-release", "type": "topic", "text": "release checklist", "confidence": 0.8, "evidence_segment_ids": ["seg-graph-1"]}],
    }).status_code == 201
    graph_expanded = client.post("/v1/query", json={"question": "Where is the release checklist?"})
    assert graph_expanded.status_code == 200
    assert graph_expanded.json()["citations"][0]["segment_id"] == "seg-graph-1"
    answer = client.post("/v1/query", json={"question": "What did we decide about the pipeline?"})
    assert answer.status_code == 200
    body = answer.json()
    assert body["insufficient_evidence"] is False
    assert body["citations"][0]["segment_id"] == "seg-graph-1"
    assert body["citations"][0]["revision"] == 1
    empty = client.post("/v1/query", json={"question": "What did we decide about the budget?"})
    assert empty.status_code == 200
    assert empty.json()["insufficient_evidence"] is True


def test_new_transcript_revision_marks_graph_claim_for_review():
    assert upload().status_code == 201
    assert client.post("/v1/graph/records", json={
        "session_id": SESSION,
        "action_items": [{"id": "action-revision", "text": "Ship it", "confidence": 0.8, "evidence_segment_ids": ["seg-graph-1"]}],
    }).status_code == 201
    assert upload(revision=2, text="We decided to delay the audio pipeline.").status_code == 201
    records = client.get(f"/v1/sessions/{SESSION}/records").json()["records"]
    assert all(record["status"] == "needs_review" for record in records)
