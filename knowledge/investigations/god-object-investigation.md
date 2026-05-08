# God Object Investigation

## Objective

Determine whether a large module
represents legitimate orchestration
or harmful responsibility concentration.

## Structural Questions

- How many responsibilities exist?
- Are unrelated domains mixed?
- Is the public API excessively broad?
- Does the module centralize workflows?

## Dependency Questions

- Does the module have extreme fan-out?
- Is it depended upon by many modules?
- Does it participate in cycles?

## Complexity Questions

- Is complexity uniformly distributed?
- Are there branching explosions?
- Are multiple workflows embedded together?

## Temporal Questions

- Does the file change frequently?
- Do many teams modify it?
- Is ownership fragmented?

## Strong Risk Indicators

High risk when:
- high complexity
- high churn
- many responsibilities
- many contributors
- temporal coupling with multiple domains

## Common Root Causes

- missing service boundaries
- insufficient domain decomposition
- premature centralization
- legacy accumulation

## False Positives

Do not immediately classify as god object:
- orchestrators
- composition roots
- dependency injection containers
- workflow coordinators

## Suggested Refactors

- extract bounded contexts
- split workflows
- isolate domain services
- introduce events/interfaces
- reduce mutable shared state