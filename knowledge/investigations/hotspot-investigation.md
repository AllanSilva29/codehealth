# Hotspot Investigation

When a hotspot is detected, investigate:

## Structural Questions

- Is the module too large?
- Is business logic concentrated?
- Are responsibilities mixed?

## Temporal Questions

- Why does this file change frequently?
- Is churn caused by migrations?
- Are many teams touching this file?

## Dependency Questions

- Does the module have excessive fan-out?
- Is it part of dependency cycles?

## Operational Questions

- Are incidents associated with this module?
- Are rollbacks frequent?

## Goal

Determine whether:
- the hotspot is legitimate
- temporary
- organizational
- architectural