"""
Week 23 (09-01-2027 - 15-01-2027)
Task: Refine answer accuracy and citation quality

Why this matters:
Quality is improved by measuring support, not by making the model sound more
confident. The current baseline uses overlap ranking and exact source quotes.

What this script does:
Defines the review dimensions for future provider-backed evaluation.
"""

QUALITY_CHECKS = ("answer_supported", "citation_exact", "revision_current", "insufficient_evidence_honest")

# WEEK OUTPUT CONTRACT:
# Input: answer and citations plus reference evidence.
# Output: review findings separated from extraction confidence.
