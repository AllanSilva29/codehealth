# False Positive — CLI Command Modules

## Problem

CLI and management command modules
often centralize procedural workflows.

This naturally creates:
- high branching
- high fan-out
- procedural orchestration

## Examples

- migration commands
- batch processors
- admin scripts
- ETL pipelines

## Typical Signals

- procedural flow explosion
- large execution methods
- infrastructure orchestration

## Risk

Static analyzers may incorrectly classify:
- god objects
- excessive coupling
- low cohesion

## Investigation Questions

- Is the complexity workflow-driven?
- Is the module operational rather than domain-centric?
- Is orchestration separated from business rules?

## Severity Adjustment

Reduce severity when:
- orchestration is explicit
- workflows are isolated
- business logic remains externalized