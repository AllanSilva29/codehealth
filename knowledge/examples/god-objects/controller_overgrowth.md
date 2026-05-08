# Controller Overgrowth Example

## Module

CheckoutController.cs

## Signals

- 1800 LOC
- contains:
  - validation
  - retries
  - fraud logic
  - persistence
  - metrics
  - DTO mapping

## Interpretation

Controller responsibilities exceeded presentation concerns.

Business logic leaked into delivery layer.

## Risks

- difficult testing
- duplicated logic
- presentation-domain coupling

## Suggested Refactors

- move business logic to services
- isolate validation pipeline
- extract mapping layer