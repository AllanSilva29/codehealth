# False Positive — Shared Kernel Modules

## Problem

Shared kernel modules are intentionally reused across domains.

This naturally creates:
- high fan-in
- broad dependency reach
- architectural centrality

## Examples

- domain primitives
- shared contracts
- common DTOs
- utility abstractions

## Typical Signals

- many dependents
- architectural centrality
- stable dependency hubs

## Healthy Characteristics

Acceptable when:
- APIs remain stable
- abstractions are cohesive
- responsibilities are narrow

## Risk

Naive graph analysis may incorrectly classify:
- architectural bottlenecks
- god objects
- dangerous hubs

## Investigation Questions

- Is the shared kernel stable?
- Is domain leakage occurring?
- Is the abstraction boundary clear?

## Severity Adjustment

Reduce severity when:
- churn is low
- interfaces remain stable
- responsibilities are cohesive