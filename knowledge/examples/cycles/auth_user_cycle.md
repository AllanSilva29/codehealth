# Circular Dependency Example

auth.py -> user.py
user.py -> notification.py
notification.py -> auth.py

## Risks

- Import-order fragility
- Runtime initialization failures
- Hidden architectural coupling
- Difficult testing

## Interpretation

This cycle indicates poor separation between:
- authentication
- user management
- notifications

## Suggested Refactors

- Introduce interfaces/events
- Extract shared contracts
- Apply dependency inversion