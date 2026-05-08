# False Positive — Configuration Modules

## Problem

Configuration modules naturally aggregate:
- environment variables
- integrations
- dependency wiring
- infrastructure setup

This may resemble:
- high fan-out
- low cohesion
- god objects

## Examples

- settings.py
- dependency containers
- app bootstrap modules
- startup configuration

## Typical Signals

- many imports
- large setup functions
- centralized initialization

## Healthy Characteristics

Acceptable when:
- business logic is minimal
- responsibilities are infrastructure-focused
- initialization is explicit

## Severity Adjustment

Reduce:
- fan-out severity
- cohesion penalties
- god-object classification

unless domain logic is centralized.