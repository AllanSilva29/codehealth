# Test Files

## Problem

Test files often produce misleading structural metrics.

They may exhibit:
- high complexity
- duplicated setup code
- broad dependency usage
- high churn

Without representing architectural degradation.

## Typical Characteristics

- extensive mocking
- fixture orchestration
- scenario branching
- repetitive assertions

## Common False Positives

- high cyclomatic complexity
- high fan-out
- low cohesion

## Interpretation Rules

Test code should be analyzed differently from production code.

## Recommended Adjustments

Reduce severity for:
- complexity
- fan-out
- duplication

When files are clearly test-related.

## Exceptions

Escalate severity when:
- test architecture becomes unmaintainable
- test utilities become god objects
- integration tests create hidden dependency webs

## Detection Signals

- tests/
- __tests__/
- *.spec.*
- *.test.*

## Investigation Questions

- Is the complexity scenario-driven?
- Is the test code reusable?
- Is the fixture setup excessive?