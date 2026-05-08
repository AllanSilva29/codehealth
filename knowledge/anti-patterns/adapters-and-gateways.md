# Adapters and Gateways

## Problem

Adapters, gateways and integration layers
naturally exhibit structural patterns
that resemble architectural smells.

Typical characteristics:
- high fan-out
- multiple external dependencies
- broad protocol handling
- orchestration responsibilities

## Examples

- payment gateways
- API adapters
- infrastructure connectors
- message brokers
- HTTP clients

## Healthy Characteristics

These modules are acceptable when:
- business logic remains minimal
- responsibilities are integration-focused
- orchestration is explicit
- domain boundaries are preserved

## Risk Indicators

Severity should increase when:
- domain logic leaks into adapters
- branching complexity becomes excessive
- retry/fallback logic dominates the module
- adapters mutate business state directly

## Common False Positives

- "too many imports"
- "high dependency count"
- "large switch/case integrations"

These may be expected integration behavior.

## Suggested Analysis

Evaluate:
- complexity density
- business logic concentration
- coupling direction
- dependency isolation

## Recommended Severity Adjustment

Reduce fan-out severity for:
- infrastructure boundaries
- integration facades
- protocol translation layers