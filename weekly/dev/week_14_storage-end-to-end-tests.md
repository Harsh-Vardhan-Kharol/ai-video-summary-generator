"""
Week 14 (03-11-2026 - 13-11-2026)
Task: Test the storage layer end-to-end

Why this matters:
The same contract must work in deterministic CI and on PostgreSQL. Evidence
must remain traceable through transcript, summary, and vector storage.

What this script does:
Records the storage checks implemented in backend/tests and runtime_check.py.
"""

Coverage validates transcript acceptance, revisions, evidence-linked summaries,
and semantic retrieval. `scripts/runtime_check.py` additionally exercises a
configured PostgreSQL database without printing secrets.
