# Instability Score

## Definition

Measures dependency instability.

Formula:
I = FanOut / (FanIn + FanOut)

## Interpretation

Near 1:
- highly unstable
- depends on many modules
- few depend on it

Near 0:
- highly stable
- central dependency

## Critical Risk

Core modules with:
- high instability
- high churn
- broad architectural influence