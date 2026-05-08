# Excessive Fan-out Example

## Module

payment_service.py

## Signals

- Imports: 42 modules
- Direct integrations:
  - Stripe
  - PayPal
  - Kafka
  - Redis
  - Analytics
  - Fraud detection
  - Notifications
  - Feature flags
  - Email
  - Metrics
  - Audit

## Complexity

Cyclomatic Complexity: 37

## Interpretation

This module exhibits excessive fan-out.

The module depends on many unrelated concerns:
- payment processing
- analytics
- notifications
- fraud systems
- observability
- feature toggles

This increases:
- ripple effects
- testing complexity
- deployment fragility
- cognitive load

## Architectural Smells

- excessive coupling
- orchestration mixed with business logic
- low modularity

## Suggested Refactors

- extract notification orchestration
- isolate analytics concerns
- introduce event-driven integration
- separate fraud evaluation pipeline

## False Positive Checks

Before escalating severity:
- verify whether this module is intended as a workflow coordinator
- inspect business logic density