"""Week 12 helpers for normalizing evidence-backed NER records.

LLM-extracted people, topics, decisions, and action items are translated into
the existing graph-ingestion contract. Explicit date mentions are retained as
evidence-linked annotations; they are not silently interpreted as calendar
dates because the transcript may not provide a meeting date or year.
"""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from typing import Any


DATE_PATTERN = re.compile(
    r"\b(?:\d{4}-\d{2}-\d{2}|(?:January|February|March|April|May|June|July|"
    r"August|September|October|November|December)\s+\d{1,2}(?:,\s*\d{4})?|"
    r"(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday))\b",
    re.IGNORECASE,
)
ENTITY_TYPES = {"person", "topic", "decision"}


def extract_date_mentions(segments: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    """Find explicit date-like text, retaining its source segment ID."""
    mentions: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    for segment in segments:
        segment_id = segment.get("segment_id")
        text = segment.get("text")
        if not isinstance(segment_id, str) or not isinstance(text, str):
            raise ValueError("segments require string segment_id and text fields")
        for match in DATE_PATTERN.finditer(text):
            value = match.group(0)
            key = (value.casefold(), segment_id)
            if key not in seen:
                mentions.append({"text": value, "evidence_segment_ids": [segment_id]})
                seen.add(key)
    return mentions


def normalize_extraction(
    extraction: Mapping[str, Any], segments: Sequence[Mapping[str, Any]]
) -> dict[str, list[dict[str, Any]]]:
    """Map Week 6 extraction records to Harsh's graph batch payload shape."""
    valid_ids = {segment.get("segment_id") for segment in segments}
    if not valid_ids or not all(isinstance(value, str) and value for value in valid_ids):
        raise ValueError("segments must have non-empty segment_id values")
    items = extraction.get("items")
    if not isinstance(items, list):
        raise ValueError("extraction.items must be a list")

    # Resolve owners only when a person record is explicitly named in the task
    # text and shares source evidence with the action item.
    people = [
        item for item in items
        if isinstance(item, Mapping) and item.get("type") == "person"
    ]

    entities: list[dict[str, Any]] = []
    actions: list[dict[str, Any]] = []
    for index, item in enumerate(items):
        if not isinstance(item, Mapping):
            raise ValueError(f"extraction.items[{index}] must be an object")
        item_type, evidence = item.get("type"), item.get("evidence_segment_ids")
        if (
            not isinstance(evidence, list)
            or not evidence
            or not all(isinstance(value, str) for value in evidence)
            or set(evidence) - valid_ids
        ):
            raise ValueError(f"extraction.items[{index}] has invalid evidence_segment_ids")
        common = {
            "id": item.get("id"),
            "confidence": item.get("confidence"),
            "evidence_segment_ids": evidence,
        }
        if item_type in ENTITY_TYPES:
            entity = {**common, "entity_type": item_type, "display_name": item.get("text")}
            entities.append(entity)
        elif item_type == "action_item":
            description = item.get("text")
            supporting_segments = [segment for segment in segments if segment.get("segment_id") in evidence]
            date_texts = [
                match.group(0)
                for segment in supporting_segments
                for match in DATE_PATTERN.finditer(str(segment.get("text", "")))
                if isinstance(description, str) and match.group(0).casefold() in description.casefold()
            ]
            matching_people = [
                person for person in people
                if isinstance(description, str)
                and isinstance(person.get("text"), str)
                and person["text"].casefold() in description.casefold()
                and isinstance(person.get("evidence_segment_ids"), list)
                and set(person["evidence_segment_ids"]) & set(evidence)
            ]
            owner = matching_people[0] if len(matching_people) == 1 else None
            actions.append({
                **common,
                "description": description,
                "owner_entity_id": owner.get("id") if owner else None,
                "owner_status": "assigned" if owner else "unassigned",
                "due_date_text": date_texts[0] if len(date_texts) == 1 else None,
                "status": "open",
            })
        else:
            raise ValueError(f"extraction.items[{index}] has unsupported type")

    return {
        "entities": entities,
        "action_items": actions,
        "date_mentions": extract_date_mentions(segments),
    }
