# God Object Example

## Module

OrderManager.java

## Signals

- 4200 LOC
- 87 methods
- fan-out: 34
- complexity: 91

## Responsibilities

- order validation
- payment processing
- inventory reservation
- invoice generation
- notification dispatch
- analytics
- refunds
- shipping
- retry policies

## Interpretation

This module centralizes too many responsibilities.

Indicators strongly suggest:
- god object
- low cohesion
- excessive coupling

## Risks

- impossible testing surface
- high regression probability
- slow onboarding
- refactoring paralysis

## Suggested Refactors

- extract domain services
- separate workflows
- isolate infrastructure concerns
- introduce domain events