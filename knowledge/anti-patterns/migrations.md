# Migration Files

## Problem

Migration scripts frequently produce false positives.

## Typical Characteristics

- high churn during migrations
- schema manipulation complexity
- temporary instability

## Interpretation Rules

Migration directories should:
- be excluded from hotspot analysis
- reduce complexity severity
- ignore cohesion analysis

## Exceptions

Long-lived migration utilities may still deserve analysis.