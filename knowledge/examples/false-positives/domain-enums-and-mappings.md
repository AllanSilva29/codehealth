# False Positive — Domain Enums and Mapping Files

## Problem

Large mapping files may appear:
- oversized
- repetitive
- poorly cohesive

while actually representing:
- stable domain knowledge
- lookup structures
- protocol mappings

## Examples

- permission maps
- country tables
- tax code mappings
- protocol registries

## Typical Signals

- many constants
- large switch/case blocks
- repetitive structures

## Risk

Naive analyzers may classify these as:
- god objects
- low cohesion modules
- excessive complexity

## Investigation Questions

- Is the complexity algorithmic or declarative?
- Does the file mainly encode stable mappings?
- Is business behavior centralized here?

## Severity Adjustment

Reduce severity when:
- logic density is low
- mappings are stable
- behavior complexity is minimal