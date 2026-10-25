"""Validation for the frontend-safe portion of the NLP output contract."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any


def validate_display_payload(payload: Mapping[str, Any]) -> list[str]:
    """Return user-facing contract errors without importing frontend code."""
    errors: list[str] = []
    display = payload.get("display")
    if not isinstance(display, Mapping):
        return ["display must be an object"]
    if not isinstance(display.get("summary"), str):
        errors.append("display.summary must be a string")
    if not isinstance(display.get("evidence_turn_count"), int) or display["evidence_turn_count"] < 0:
        errors.append("display.evidence_turn_count must be a non-negative integer")
    actions = display.get("action_items")
    if not isinstance(actions, list):
        return errors + ["display.action_items must be a list"]
    for index, action in enumerate(actions):
        label = f"display.action_items[{index}]"
        if not isinstance(action, Mapping):
            errors.append(f"{label} must be an object")
            continue
        if not isinstance(action.get("text"), str) or not action["text"].strip():
            errors.append(f"{label}.text must be non-empty")
        if action.get("owner_status") not in {"assigned", "unassigned", "uncertain"}:
            errors.append(f"{label}.owner_status is invalid")
        if action.get("status") not in {"open", "in_progress", "blocked", "completed", "cancelled", "needs_review"}:
            errors.append(f"{label}.status is invalid")
        if action.get("support", {}).get("status") not in {"accepted", "review_required", "rejected"}:
            errors.append(f"{label}.support.status is invalid")
        if not isinstance(action.get("evidence"), list) or not action["evidence"]:
            errors.append(f"{label}.evidence must be non-empty")
    return errors
