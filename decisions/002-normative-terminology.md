# 002: Normative quantity terminology

Status: ACCEPTED  
Target: version 0.1 and later  
Depends on: SD-001
Informed by: teammate proposal's treatment of units as part of numeric meaning, refined to separate units, dimensions, kinds, and types

## Decision

The normative glossary is maintained in `PROJECT.md` Section 6.1. The language distinguishes magnitude, numeric value, quantity, unit symbol, unit definition, unit expression, dimension, quantity kind, scale, canonical unit, display unit, conversion, normalization, and evaluation.

Two compatibility terms are used deliberately:

- **dimension-compatible** means equal normalized dimensions;
- **operation-compatible** means the operands satisfy every rule for the particular operation, including explicit conversion and any applicable kind rule.

`Scalar` is shorthand for a dimensionless quantity, not a separate base dimension. `Unit`, `dimension`, `quantity kind`, and `type` are not synonyms.

## Deferred consequences

This terminology does not itself select those policies. Base dimensions and canonical unit scales are now fixed by decision 030; numeric representation and the version 0.1 quantity-kind enforcement level remain SD-041 and SD-050 decisions.

## Revisit trigger

Revise a definition only when a later accepted semantic feature cannot be described without contradiction. Preserve the distinction between physical-unit conversion and contextual operations such as currency exchange.
