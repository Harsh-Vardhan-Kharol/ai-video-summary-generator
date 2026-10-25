"""
Week 15 (14-11-2026 - 20-11-2026)
Task: Research hallucination-detection approaches

Why this matters:
The project must not persist attractive but unsupported meeting claims. The
research informs the confidence signal used before extraction reaches Harsh's
knowledge graph and before summaries are shown to users.

What this script does:
Records the selected explainable, offline-first reliability approach and its
limitations.
"""

# Hallucination-detection decision

The chosen first-line check is evidence-based claim verification: every summary
or extraction record cites transcript segment IDs, and a deterministic scorer
compares its content tokens to the cited text. The score also reports average
ASR quality, so weak source transcription is visible instead of being confused
with model certainty.

This deliberately does not claim to prove factuality. Paraphrases and implicit
context can be lexically weak even when correct, while copied words can still
be misleading. Therefore it has three outcomes: `accepted`, `review_required`,
and `rejected`. Only accepted extraction records enter the graph batch;
review-required records remain available to the UI for human review.

A later provider-backed natural-language-inference verifier can be added behind
the same `support_assessment` field after an evaluation set and credentials are
available. It must retain the evidence-first rule and must not overwrite the
original extraction confidence.
