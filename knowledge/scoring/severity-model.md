# Severity Model

## Objective

Provide consistent severity classification
for architectural and maintainability risks.

Severity must reflect:
- operational impact
- maintenance risk
- architectural influence
- socio-technical fragility

---

# Severity Levels

## Critical

Conditions:
- hotspot + dependency cycle
- high churn + high complexity
- unstable core module
- god object with many contributors
- strong temporal coupling across domains

Characteristics:
- elevated incident probability
- risky refactors
- difficult debugging
- architecture degradation spreading

Recommended Action:
Immediate investigation and prioritization.

---

## High

Conditions:
- large SCCs
- severe fan-out
- low cohesion in core modules
- unstable dependency chains
- concentrated business logic

Characteristics:
- increasing maintenance cost
- growing architectural fragility
- high cognitive load

Recommended Action:
Planned remediation.

---

## Medium

Conditions:
- moderate complexity
- moderate temporal coupling
- localized architectural smells
- stable but poorly structured legacy code

Characteristics:
- manageable risk
- localized maintainability problems

Recommended Action:
Monitor and refactor opportunistically.

---

## Low

Conditions:
- stable modules
- low churn
- isolated smells
- intentional orchestration patterns

Characteristics:
- acceptable technical debt
- low operational risk

Recommended Action:
No immediate action required.

---

# Severity Escalation Rules

Increase severity when:
- multiple independent signals correlate
- structural and temporal signals align
- socio-technical instability exists

Examples:
- hotspot + ownership fragmentation
- cycle + high churn
- low cohesion + temporal coupling

---

# Severity Reduction Rules

Reduce severity when:
- code is generated
- modules are intentionally orchestration-focused
- legacy modules are stable
- churn is migration-driven

---

# Confidence Model

High confidence:
- multiple corroborating signals
- repeated temporal evidence
- strong graph indicators

Low confidence:
- single isolated metric
- monorepo-wide commits
- framework-generated structures

Always distinguish:
- confirmed architectural risks
- heuristic suspicions
- contextual anomalies