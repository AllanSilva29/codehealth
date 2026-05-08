# Healthy High Fan-out Example

## Module

checkout_workflow.py

## Signals

- Imports: 31 modules
- High fan-out

## Complexity

Cyclomatic Complexity: 6

## Interpretation

High fan-out alone does not necessarily indicate poor design.

This module primarily:
- coordinates workflows
- delegates responsibilities
- avoids business rule concentration

## Healthy Indicators

- low branching complexity
- minimal internal state
- thin orchestration layer
- dependency delegation

## Severity Adjustment

Lower severity.

This is likely an intentional orchestration module.