"""Offline evaluation helpers for summary/extraction quality regression checks."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any


def evaluate_output(
    output: Mapping[str, Any],
    segments: Sequence[Mapping[str, Any]],
    must_not_claim: Sequence[str] = (),
) -> dict[str, Any]:
    """Evaluate contract safety and forbidden-claim regressions deterministically."""
    valid_ids = {segment.get("segment_id") for segment in segments}
    summary = output.get("summary", {})
    summary_text = str(summary.get("text", ""))
    errors: list[str] = []
    source_ids = summary.get("source_segment_ids", summary.get("covered_segment_ids", []))
    if summary_text and (not isinstance(source_ids, list) or not source_ids):
        errors.append("non-empty summary has no source segment IDs")
    if isinstance(source_ids, list) and set(source_ids) - valid_ids:
        errors.append("summary references unknown source segments")

    records = list(output.get("entities", [])) + list(output.get("action_items", []))
    review_count = 0
    for index, record in enumerate(records):
        evidence = record.get("evidence", []) if isinstance(record, Mapping) else []
        evidence_ids = {item.get("segment_id") for item in evidence if isinstance(item, Mapping)}
        if not evidence_ids or evidence_ids - valid_ids:
            errors.append(f"record {index} has missing or unknown evidence")
        support = record.get("properties", {}).get("support_assessment", {}) if isinstance(record, Mapping) else {}
        if support.get("status") != "accepted":
            review_count += 1

    haystack = " ".join(
        [summary_text] + [str(record.get("display_name", record.get("description", ""))) for record in records if isinstance(record, Mapping)]
    ).casefold()
    forbidden_hits = [claim for claim in must_not_claim if claim.casefold() in haystack]
    if forbidden_hits:
        errors.extend(f"forbidden claim present: {claim}" for claim in forbidden_hits)
    return {
        "passed": not errors,
        "errors": errors,
        "forbidden_claim_hits": forbidden_hits,
        "records_requiring_review": review_count,
        "source_segment_count": len(valid_ids),
    }
