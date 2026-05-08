# Temporal Coupling Example

## Co-change Frequency

auth.py + billing.py
appeared together in 91% of commits.

## Interpretation

Possible hidden dependency.

Even without direct imports,
these modules evolve together.

## Possible Causes

- Shared business workflow
- Cross-cutting concerns
- Missing abstraction layer
- Duplicated business rules

## Suggested Investigation

- Inspect commit diffs
- Analyze shared responsibilities
- Check event flow