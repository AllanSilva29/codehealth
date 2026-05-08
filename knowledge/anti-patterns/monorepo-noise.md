# Monorepo Noise

## Problem

Monorepositories naturally generate noisy architectural signals.

Large-scale synchronized changes may produce:
- artificial temporal coupling
- inflated churn
- misleading hotspot correlations

## Common Sources

- dependency upgrades
- formatting commits
- shared configuration updates
- workspace migrations
- lockfile changes

## Risk

Naive co-change analysis may incorrectly infer:
- hidden dependencies
- architectural coupling
- module instability

## Detection Signals

- very large commits
- many unrelated files modified together
- automated tooling commits
- repository-wide formatting changes

## Recommended Adjustments

Reduce temporal coupling confidence when:
- commit size is abnormally large
- changes span unrelated domains
- files changed are mostly configuration

## Investigation Questions

- Is the co-change operational or architectural?
- Is the commit generated automatically?
- Does the repository use mass refactors frequently?

## Examples

False positive:
- ESLint migration touching 1200 files

Legitimate signal:
- billing and invoices changing together
across many independent commits