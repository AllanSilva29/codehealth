# Temporal Coupling

Definition:
Two files frequently modified together.

Detection:
1. Extract commit file lists
2. Count co-occurrences
3. Build co-change matrix

Example:
auth.py + billing.py
appearing together in 87% of commits

Possible Meaning:
- Hidden dependency
- Shared business rule
- Missing abstraction

False Positives:
- Large refactors
- Formatting commits