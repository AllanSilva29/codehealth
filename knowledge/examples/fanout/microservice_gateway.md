# API Gateway Fan-out Example

## Module

gateway.ts

## Signals

- fan-out: 47
- many external service integrations
- high network orchestration

## Interpretation

API gateways frequently aggregate:
- authentication
- routing
- observability
- rate limiting
- service discovery

This is not inherently unhealthy.

## Risk Signals

Escalate severity if:
- business rules accumulate
- retry logic becomes complex
- state management leaks into gateway