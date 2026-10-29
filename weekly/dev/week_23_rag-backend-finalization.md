"""
Week 23 (09-01-2027 - 15-01-2027)
Task: Fix bugs, finalize backend RAG support

Why this matters:
The backend must preserve its API contract while Harsh can improve retrieval
internals independently.

What this script does:
Documents the finalized error and citation behavior at the API boundary.
"""

Malformed requests use the common validation envelope; unsupported questions
return HTTP 200 with `insufficient_evidence=true`, not invented information.
