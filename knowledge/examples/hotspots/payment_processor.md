# Hotspot Example — payment_processor.py

## Signals

- 412 modifications in 6 months
- Cyclomatic complexity: 84
- 17 contributors
- Frequently reverted
- Temporal coupling with:
  - billing.py
  - refunds.py
  - invoices.py

## Interpretation

This file is likely a critical hotspot.

The combination of:
- high churn
- high complexity
- multiple contributors
- rollback frequency

suggests elevated maintenance risk.

## Possible Root Causes

- Missing domain decomposition
- Excessive business rules concentration
- Shared mutable state
- Poor module boundaries

## Suggested Actions

- Extract bounded contexts
- Split payment flows
- Introduce orchestration layer
- Increase automated tests