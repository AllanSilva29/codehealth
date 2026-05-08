# False Positive — Event-Driven Architecture

## Problem

Event-driven systems often appear loosely coupled
in static analysis while remaining operationally interconnected.

Conversely:
event dispatchers may appear overly connected.

## Examples

- Kafka consumers
- RabbitMQ handlers
- domain event buses
- pub/sub systems

## Typical Signals

- many handlers
- broad event subscriptions
- weak import relationships
- strong temporal relationships

## Risk

Static dependency graphs may underestimate coupling.

Temporal coupling analysis may overestimate architectural problems.

## Investigation Questions

- Is the co-change caused by shared workflows?
- Is event orchestration intentional?
- Are events domain boundaries or leakage?

## Severity Adjustment

Do not immediately classify:
- event hubs
- dispatchers
- subscriber registries

as god objects.