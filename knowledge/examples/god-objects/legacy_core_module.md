# Stable Legacy Core Example

## Module

legacy_core.c

## Signals

- 9000 LOC
- high complexity
- many dependencies

## Temporal Analysis

- churn very low
- minimal contributor count
- stable for years

## Interpretation

Despite structural problems,
operational risk may currently be low.

## Important Insight

Not every god object should be aggressively rewritten.

## Recommended Approach

- avoid large rewrites
- prioritize isolation
- refactor incrementally around boundaries
- increase observability/tests first