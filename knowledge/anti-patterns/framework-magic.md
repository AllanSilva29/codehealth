# Framework Magic

## Problem

Some frameworks hide dependencies dynamically.

Examples:
- Django signals
- Spring reflection
- NestJS decorators
- dependency injection containers

## Consequence

Static dependency graphs may miss:
- runtime coupling
- implicit flows
- event-driven relations

## Investigation Guidance

Do not assume low coupling
based solely on import graphs.