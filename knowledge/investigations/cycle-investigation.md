# Circular Dependency Investigation

## Questions

- Is the cycle domain-related?
- Is the cycle caused by utilities/shared code?
- Can interfaces/events break the cycle?
- Is runtime initialization affected?

## Risk Indicators

High risk when:
- cycle includes hotspots
- cycle spans multiple domains
- cycle affects core modules

## Suggested Refactors

- dependency inversion
- event-driven communication
- contract extraction