"""
Week 25 (23-01-2027 - 29-01-2027)
Task: Build the search/query interface

Why this matters:
Cross-session memory is visible to users only through a query interface that
shows source citations rather than opaque generated text.

What this script does:
Documents the query form and cited answer panel in frontend/src/App.jsx.
"""

The form calls `POST /v1/query`, renders loading and insufficient-evidence
states, and shows citation times and quoted transcript evidence.
