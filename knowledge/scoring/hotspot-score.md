# Hotspot Score

## Purpose

Estimate maintenance risk using temporal and structural signals.

## Formula

hotspot_score =
  normalized_churn *
  normalized_complexity

## Additional Multipliers

+ contributor_count
+ rollback_frequency
+ temporal_coupling_strength

## Risk Thresholds

0-20   -> low
21-50  -> moderate
51-80  -> high
80+    -> critical

## Interpretation

High hotspot scores suggest:
- maintenance bottlenecks
- fragile modules
- elevated bug probability

## False Positive Adjustments

Reduce score for:
- generated code
- stable legacy systems
- orchestrator modules