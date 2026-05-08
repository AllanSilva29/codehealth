# Hotspot Score

Formula:
hotspot_score = normalized_churn * normalized_complexity

Rationale:
Frequently modified complex files are statistically riskier.

Indicators:
- Large files
- High churn
- Many authors
- Frequent bugfix commits

False Positives:
- Migration periods
- Generated code