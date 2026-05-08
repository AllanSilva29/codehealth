# False Positive — Framework Decorators

## Problem

Decorator-heavy frameworks often hide behavior
behind metadata and annotations.

Static analysis may underestimate:
- runtime coupling
- implicit flows
- lifecycle complexity

Or overestimate:
- dependency count
- orchestration complexity

## Examples

- Django decorators
- FastAPI dependency injection
- NestJS decorators
- Spring annotations

## Typical Signals

- many imports
- indirect execution paths
- reflection-based resolution

## False Positive Risk

High fan-out may be framework-driven rather than architectural degradation.

## Investigation Questions

- Is the complexity business-related?
- Is the framework generating orchestration automatically?
- Are dependencies explicit or metadata-driven?

## Severity Adjustment

Lower confidence for:
- reflection-heavy frameworks
- annotation-driven orchestration