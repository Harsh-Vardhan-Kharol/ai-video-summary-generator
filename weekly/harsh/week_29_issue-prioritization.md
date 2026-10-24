"""
Week 29 (20-02-2027 - 26-02-2027)
Task: Log and prioritize issues found in testing

Why this matters:
False memories are higher risk than a missed low-confidence result. Issues are
therefore prioritized by evidence correctness, data integrity, and UX impact.

What this script does:
Defines the issue priority policy for the RAG/graph lane.
"""

Priority: P0 = unsupported answer or citation mismatch; P1 = stale evidence
shown as current or cross-session identity error; P2 = ranking/coverage defect;
P3 = presentation or observability improvement.

# WEEK OUTPUT CONTRACT:
# Input: integration and quality-review findings.
# Output: reproducible issue with owner, evidence, severity, and regression test.
