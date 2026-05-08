# Orchestrator Modules

## Problem

Coordinator/facade modules naturally exhibit:

- high fan-out
- many imports
- broad visibility

This does not necessarily imply poor architecture.

## Examples

- API gateways
- workflow coordinators
- service aggregators
- dependency injection containers

## Healthy Signals

- low business logic density
- clear orchestration responsibility
- low cyclomatic complexity

## Risk Signals

- orchestration mixed with domain logic
- branching explosion
- hidden state mutation

## Severity Adjustment

Lower severity when:
- module acts mainly as a router/coordinator