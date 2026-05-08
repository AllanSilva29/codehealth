# False Positive — Serializer Aggregation

## Problem

Serializer modules frequently aggregate:
- validation logic
- transformation logic
- nested serializers
- framework adapters

This naturally increases:
- fan-out
- branching
- dependency density

## Examples

- Django REST Framework serializers
- Marshmallow schemas
- Pydantic models

## Typical Signals

- many imports
- nested validation
- field transformation logic

## Risk

Complex serializers may be framework-driven rather than architectural decay.

## Investigation Questions

- Is business logic leaking into serializers?
- Is validation complexity domain-related?
- Are serializers orchestrating workflows?

## Severity Escalation

Increase severity when:
- serializers mutate domain state
- workflows are embedded
- orchestration logic accumulates