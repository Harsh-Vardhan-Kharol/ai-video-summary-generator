from __future__ import annotations

import json
import unittest
from pathlib import Path

from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.transcript_repository import transcript_repository
from ml.nlp.combined_pipeline import MeetingNlpPipeline
from ml.nlp.confidence import ConfidencePolicy, assess_support
from ml.nlp.display_contract import validate_display_payload
from ml.nlp.evaluation import evaluate_output


ROOT = Path(__file__).resolve().parents[3]
FIXTURE = ROOT / "ml" / "nlp" / "fixtures" / "week_03_sample_transcripts.json"


class CombinedPipelineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.case = json.loads(FIXTURE.read_text(encoding="utf-8"))["cases"][1]
        transcript_repository.clear()

    def _pipeline(self) -> MeetingNlpPipeline:
        responses = iter((self.case["reference_summary"], self.case["reference_extraction"]))
        return MeetingNlpPipeline(lambda _messages: next(responses))

    def test_creates_revision_specific_graph_and_display_payloads(self) -> None:
        output = self._pipeline().process(
            session_id="session-contract-001", segments=self.case["transcript_segments"]
        )
        self.assertEqual(output["schema_version"], "1.0")
        self.assertEqual(output["summary"]["evidence"][0]["revision"], 1)
        self.assertEqual(output["display"]["evidence_turn_count"], 3)
        self.assertEqual(output["graph_batch"]["producer"], "garvit")
        self.assertTrue(output["graph_batch"]["action_items"])
        self.assertEqual(output["graph_batch"]["action_items"][0]["evidence"][0]["segment_id"], "scope-seg-002")

    def test_unsupported_words_are_not_sent_to_graph(self) -> None:
        segments = self.case["transcript_segments"]
        responses = iter((
            {"text": "The team decided to buy a helicopter.", "covered_segment_ids": ["scope-seg-001"]},
            {"items": [{"id": "bad-action", "type": "action_item", "text": "Buy a helicopter.", "confidence": 0.99, "evidence_segment_ids": ["scope-seg-001"]}]},
        ))
        output = MeetingNlpPipeline(lambda _messages: next(responses)).process(
            session_id="session-contract-002", segments=segments
        )
        self.assertEqual(output["action_items"][0]["properties"]["support_assessment"]["status"], "rejected")
        self.assertEqual(output["graph_batch"]["action_items"], [])

    def test_support_score_exposes_explainable_components(self) -> None:
        assessment = assess_support(
            "Ravi will document API changes by Monday.", ["scope-seg-002"], self.case["transcript_segments"], model_confidence=0.98
        )
        self.assertEqual(assessment["status"], "accepted")
        self.assertIn("lexical_coverage", assessment["components"])
        self.assertEqual(assessment["model_confidence"], 0.98)

    def test_policy_can_mark_borderline_claim_for_review(self) -> None:
        assessment = assess_support(
            "Ravi will document API changes by Monday promptly.", ["scope-seg-002"], self.case["transcript_segments"],
            policy=ConfidencePolicy(accept_threshold=0.95, review_threshold=0.45),
        )
        self.assertEqual(assessment["status"], "review_required")

    def test_accepted_graph_batch_is_accepted_by_the_shared_api(self) -> None:
        session_id = "nlp-graph-contract-session"
        client = TestClient(app)
        for index, segment in enumerate(self.case["transcript_segments"]):
            response = client.post("/v1/transcript-segments", json={
                "schema_version": "1.0",
                "event_id": f"nlp-contract-event-{index}",
                "session_id": session_id,
                "created_at": "2026-10-25T10:00:00Z",
                "payload": {
                    "segment_id": segment["segment_id"], "revision": segment["revision"],
                    "is_final": segment["is_final"], "start_ms": segment["start_ms"],
                    "end_ms": segment["end_ms"], "speaker_id": segment["speaker_label"],
                    "text": segment["text"], "asr_confidence": segment["asr_confidence"],
                },
            })
            self.assertEqual(response.status_code, 201)
        output = self._pipeline().process(session_id=session_id, segments=self.case["transcript_segments"])
        response = client.post("/v1/graph/records", json=output["graph_batch"])
        self.assertEqual(response.status_code, 201, response.text)
        self.assertTrue(response.json()["action_items"])

    def test_display_and_quality_contracts_accept_fixture_output(self) -> None:
        output = self._pipeline().process(
            session_id="session-contract-003", segments=self.case["transcript_segments"]
        )
        self.assertEqual(validate_display_payload(output), [])
        evaluation = evaluate_output(output, self.case["transcript_segments"], self.case["must_not_claim"])
        self.assertTrue(evaluation["passed"], evaluation["errors"])


if __name__ == "__main__":
    unittest.main()
