# Aggregate Boundary Confusion

## Module

CustomerAggregate.kt

## Signals

- aggregate handles:
  - subscriptions
  - payments
  - support tickets
  - notifications
  - marketing preferences

## Interpretation

Domain boundaries likely collapsed.

The aggregate accumulated multiple bounded contexts.

## Risks

- transactional explosion
- excessive state coupling
- scaling difficulties

## Suggested Refactors

- redefine aggregate boundaries
- isolate transactional responsibilities
- split domain contexts