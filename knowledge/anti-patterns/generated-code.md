# Generated Code

## Problem

Generated files may appear unhealthy because they often have:

- huge file size
- high complexity
- high fan-out
- repetitive structures
- poor readability

## Examples

- protobuf output
- ORM clients
- OpenAPI generated SDKs
- GraphQL generated types

## Detection Signals

- generated comments
- auto-generated headers
- known generation folders
- deterministic structure

## Severity Rules

- reduce hotspot severity
- ignore cohesion metrics
- reduce complexity importance

## Investigation Questions

- Is the file manually edited?
- Is generation deterministic?
- Is generated code committed intentionally?