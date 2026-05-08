# Blob Service Example

## Module

user_service.py

## Signals

- grows continuously
- touched by multiple teams
- handles unrelated concerns

## Responsibilities

- authentication
- profile editing
- avatar upload
- email dispatch
- billing checks
- recommendation engine hooks
- feature flags

## Interpretation

This service evolved into a "blob".

The module became the default place
for unrelated user-related features.

## Common Root Causes

- lack of domain ownership
- convenience-driven development
- unclear architectural boundaries

## Suggested Actions

- define subdomains
- separate infrastructure concerns
- establish ownership boundaries