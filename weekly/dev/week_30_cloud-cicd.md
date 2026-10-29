"""
Week 30 (27-02-2027 - 05-03-2027)
Task: Set up cloud hosting and the CI/CD pipeline

Why this matters:
Repeatable container builds and CI checks are prerequisites for an explainable
deployment, independent of the selected cloud account.

What this script does:
Documents Docker/Compose assets and GitHub Actions validation.
"""

`backend/Dockerfile`, `frontend/Dockerfile`, and `docker-compose.yml` provide
a local production-like stack. CI runs backend tests and a frontend build.
Cloud credentials and a target account are intentionally not stored here.
