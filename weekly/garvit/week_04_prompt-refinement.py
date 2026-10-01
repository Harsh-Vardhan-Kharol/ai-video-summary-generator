"""
Week 04 (31-08-2026 - 06-09-2026)
Task: Refine prompts based on output quality

Why this matters:
The Week 3 checks use hand-written reference outputs and do not call a model, so they cannot establish generated-output quality. They did expose a contract-alignment need: the initial prompts must use the project event fields and preserve uncertainty around tentative plans, speaker labels, and action ownership. Refining these rules now gives later provider-backed evaluation a consistent baseline.

What this script does:
This weekly runner checks the revised NLP prompts against the current summary and extraction payload fields, sample transcript evidence, and rejection behavior for provisional or incomplete input.
"""

from __future__ import annotations

import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
NLP_DIR = REPO_ROOT / "ml" / "nlp"
sys.path.insert(0, str(NLP_DIR))

from week4_prompt_refinement import run_checks  # noqa: E402


REFINEMENTS = [
    "Split summary.update and extraction.update into separate prompt outputs.",
    "Use covered_segment_ids and evidence_segment_ids from the project contract.",
    "Require the transcript segment fields, including session-local speaker_label and ASR confidence.",
    "Reject provisional segments for durable summary and extraction prompts.",
    "Keep conditional plans distinct from decisions; do not infer people from diarization labels.",
    "Define extraction confidence as evidence support, not ASR confidence or a calibrated probability.",
]


def main() -> int:
    failures = run_checks()
    if failures:
        print(f"FAIL: {len(failures)} prompt-refinement check(s)")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Week 04 prompt refinements:")
    for refinement in REFINEMENTS:
        print(f"- {refinement}")
    print("PASS: revised prompt contract and input-edge-case checks.")
    print("LIMITATION: no model output was available; this is not a generated-quality comparison.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


# WEEK OUTPUT CONTRACT:
# Input: Current contract-shaped transcript segments and Week 3 sample fixtures.
# Output: Refined summary/extraction prompt builders plus a pass/fail check of
#         their field names, evidence references, and input validation behavior.
