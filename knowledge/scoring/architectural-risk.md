# Architectural Risk Score

## Inputs

- cycles
- fan-out
- instability
- hotspot severity
- temporal coupling
- cohesion

## Formula

risk =
  (cycles * 4) +
  (fan_out * 2) +
  (hotspot_score * 3) +
  (temporal_coupling * 2)

## Critical Combinations

Very high severity when:
- hotspot + cycle
- high churn + god object
- low cohesion + many contributors

## Goal

Prioritize architectural remediation.