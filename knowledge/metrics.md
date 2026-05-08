# Cyclomatic Complexity

Definition:
Measures the number of independent execution paths.

Formula:
M = E - N + 2P

In Practice:
Increment complexity for:
- if
- while
- for
- except
- case
- boolean chains

Risk Thresholds:
1-10   -> low
11-20  -> moderate
21-50  -> high
50+    -> critical

Limitations:
High complexity does not necessarily imply bad code.
Stable low-churn modules may tolerate higher complexity.