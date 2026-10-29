"""
Week 29 (20-02-2027 - 26-02-2027)
Task: Fix integration bugs found during testing

Why this matters:
Session-local ASR identifiers must not collide in a cross-session memory
system, and successful UI state must correspond to real API responses.

What this script does:
Records the storage-key and demo-sync fixes applied in this implementation.
"""

Transcript, embedding, and evidence keys include session ID. The UI reports a
sync success only after all transcript and summary writes succeed.
