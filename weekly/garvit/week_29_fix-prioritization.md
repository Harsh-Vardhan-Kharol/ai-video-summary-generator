"""
Week 29 (20-02-2027 - 26-02-2027)
Task: Report and prioritize fixes

Why this matters:
Prioritization keeps the project focused on evidence integrity before cosmetic
improvements. The ordered list is based on user harm and integration impact.

What this script does:
Ranks the logged NLP issues and assigns the responsible integration owner.
"""

# Prioritized fixes

1. **P0, Dev + Garvit:** add summary write/read API and bind the frontend to
   `nlp-output-1.0.display`; without it, live summaries cannot be shown.
2. **P0, Garvit:** run the same acceptance suite against real provider output
   and calibrate thresholds using manually labeled claims.
3. **P1, Dhruv + Garvit:** provide meeting date/timezone metadata so relative
   due-date text can be normalized safely.
4. **P1, Harsh + Garvit:** add an explicit human-resolution workflow for
   people and review-required claims.
5. **P2, Garvit:** replace lexical support with a measured NLI verifier only
   after a labeled evaluation corpus exists.
