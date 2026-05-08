# Cohesion Investigation

## Questions

- Do methods operate on shared state?
- Are unrelated domains mixed?
- Is the public API excessively broad?

## Signals

- low attribute overlap
- disconnected responsibilities
- unrelated method groups

## Common Refactors

- extract services
- split responsibilities
- isolate domain logic