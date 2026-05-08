# Architecture Smells

## Excessive Coupling

Definition:
A module depends excessively on other modules,
increasing ripple effects and maintenance cost.

Detection Heuristics:
- High fan-out
- High temporal coupling
- Frequent co-changes
- Circular dependencies

Possible Metrics:
- Fan-out > 15
- Imports from multiple unrelated domains
- Frequently modified alongside many modules

False Positives:
- Facade/orchestrator modules
- API gateways