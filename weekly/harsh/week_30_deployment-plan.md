"""
Week 30 (27-02-2027 - 05-03-2027)
Task: Prepare the production deployment plan

Why this matters:
The modular monolith keeps deployment simple while PostgreSQL remains the
canonical store. Provider credentials and pgvector availability are explicit.

What this script does:
Records deployment prerequisites for the Harsh-owned runtime.
"""

Prerequisites: PostgreSQL with the versioned schema, `DATABASE_URL`, optional
provider configuration, migration backup, health check, and a fixture smoke
test. Do not deploy with fixture data as the production source of truth.

# WEEK OUTPUT CONTRACT:
# Input: tested application artifact and deployment configuration.
# Output: reviewable runbook and rollback conditions.
