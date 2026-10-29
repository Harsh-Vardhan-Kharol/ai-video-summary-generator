"""
Week 28 (13-02-2027 - 19-02-2027)
Task: Test end-to-end user flows

Why this matters:
An uploaded revision must remain queryable, summarized, and inspectable from
one UI session before production deployment can be justified.

What this script does:
Records offline API and frontend-build verification paths.
"""

Backend pytest coverage provides the deterministic flow test. Browser-level
testing requires a running API, built frontend, and an approved test browser.
