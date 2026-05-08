# Framework Core Fan-out Example

## Module

application_container.py

## Signals

- fan-out: 58
- imports most application services

## Interpretation

Dependency injection containers naturally aggregate dependencies.

This should not automatically be classified as unhealthy.

## Investigation Questions

- Is business logic centralized here?
- Is this merely wiring/bootstrap logic?
- Is runtime behavior predictable?

## Severity Adjustment

Reduce severity when:
- logic complexity remains low
- module acts primarily as composition root