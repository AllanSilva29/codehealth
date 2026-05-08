# False Positive — Cache and Registry Modules

## Problem

Registry and cache modules naturally become highly connected.

They often:
- expose global access points
- aggregate references
- centralize lookup logic

## Examples

- service registries
- cache managers
- plugin registries
- dependency maps

## Typical Signals

- high fan-in
- high fan-out
- broad dependency visibility

## Risk

Graph analysis may incorrectly classify these as:
- unstable hubs
- god objects
- excessive coupling

## Investigation Questions

- Is the registry infrastructural?
- Is mutable state centralized dangerously?
- Is domain logic embedded?

## Severity Escalation

Increase severity when:
- registries contain workflow logic
- business decisions are centralized
- state mutation becomes uncontrolled