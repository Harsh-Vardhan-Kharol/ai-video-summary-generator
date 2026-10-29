"""
Week 26 (30-01-2027 - 05-02-2027)
Task: Polish the UI, connect to backend APIs

Why this matters:
Frontend fallback data must never be confused with confirmed backend state.
This avoids misleading users during a local demo or outage.

What this script does:
Documents API health indication, response validation, and responsive styling.
"""

Demo synchronization verifies every upload and summary response before showing
success. The layout adapts to tablet and mobile widths via styles.css.
