"""Offline-first, evidence-grounded retrieval and answer generation."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable

from backend.app.graph_repository import GraphRepository
from backend.app.transcript_repository import PersistedSegment, TranscriptRepository

STOP_WORDS = {"a", "an", "and", "are", "about", "did", "do", "for", "in", "is", "it", "of", "on", "the", "to", "was", "we", "what", "who", "when", "where", "with", "our", "i"}


def _terms(text: str) -> set[str]:
    terms = {word.lower() for word in re.findall(r"[a-zA-Z0-9]+", text) if word.lower() not in STOP_WORDS}
    # Keep the dependency-free retriever tolerant of simple inflections.
    return {term[:-1] if len(term) > 5 and term.endswith("s") else term for term in terms}


@dataclass(frozen=True)
class RetrievedEvidence:
    session_id: str
    segment: PersistedSegment
    score: float


class GroundedRAG:
    """Hybrid-shaped retriever with a deterministic extractive fallback.

    ``answerer`` can be injected later for a provider-backed model.  The
    default intentionally never invents facts: it quotes the highest scoring
    stored turns and always returns their exact citations.
    """

    def __init__(self, transcripts: TranscriptRepository, graph: GraphRepository, answerer=None) -> None:
        self.transcripts = transcripts
        self.graph = graph
        self.answerer = answerer

    def retrieve(self, question: str, session_ids: Iterable[str] = (), top_k: int = 8) -> list[RetrievedEvidence]:
        allowed = set(session_ids)
        candidates: dict[tuple[str, str, int], RetrievedEvidence] = {}
        question_terms = _terms(question)
        if not question_terms:
            return []
        for session_id in self.transcripts.list_session_ids():
            if allowed and session_id not in allowed:
                continue
            for segment in self.transcripts.list_segments(session_id, include_revisions=False):
                overlap = question_terms & _terms(segment.text)
                if overlap:
                    score = len(overlap) / max(len(question_terms), 1)
                    key = (session_id, segment.segment_id, segment.revision)
                    candidates[key] = RetrievedEvidence(session_id, segment, score)

            # Graph records act as a lightweight expansion index.  A match on
            # a decision/action/topic brings its exact cited transcript turns
            # into the result, while the transcript remains citation source of
            # truth and the score only receives a modest boost.
            all_revisions = self.transcripts.list_segments(session_id, include_revisions=True)
            by_revision = {(item.segment_id, item.revision): item for item in all_revisions}
            for record in self.graph.list_session_records(session_id):
                graph_overlap = question_terms & _terms(record.text)
                if not graph_overlap:
                    continue
                graph_score = min(0.95, 0.55 + (len(graph_overlap) / max(len(question_terms), 1)) * 0.25)
                for ref in record.evidence:
                    segment = by_revision.get((ref["segment_id"], ref["segment_revision"]))
                    if segment is None:
                        continue
                    key = (session_id, segment.segment_id, segment.revision)
                    current = candidates.get(key)
                    candidates[key] = RetrievedEvidence(session_id, segment, max(graph_score, current.score if current else 0))
        ranked = sorted(candidates.values(), key=lambda item: (-item.score, item.segment.start_ms, item.segment.segment_id))
        return ranked[: max(1, min(top_k, 20))]

    def answer(self, question: str, session_ids: Iterable[str] = (), top_k: int = 8) -> dict:
        evidence = self.retrieve(question, session_ids, top_k)
        if not evidence:
            return {"answer": "I could not find enough stored evidence to answer that question.", "citations": [], "insufficient_evidence": True, "retrieval_metadata": {"evidence_count": 0, "query_scope": "selected_sessions" if session_ids else "all_sessions", "retriever": "token_overlap"}}
        if self.answerer:
            answer = self.answerer(question, evidence)
        else:
            answer = "Based on the available evidence: " + " ".join(item.segment.text for item in evidence[:3])
        citations = [{"session_id": item.session_id, "segment_id": item.segment.segment_id, "revision": item.segment.revision, "start_ms": item.segment.start_ms, "end_ms": item.segment.end_ms, "quote": item.segment.text} for item in evidence]
        return {"answer": answer, "citations": citations, "insufficient_evidence": False, "retrieval_metadata": {"evidence_count": len(citations), "query_scope": "selected_sessions" if session_ids else "all_sessions", "retriever": "token_overlap"}}

