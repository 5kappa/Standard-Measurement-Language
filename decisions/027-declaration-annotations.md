# 027: Declaration annotation categories

Status: ACCEPTED FOR CURRENT PARSER GRAMMAR  
Target: current course lexer/parser; annotation checking later  
Depends on: SD-002, SD-014, SD-022, SD-023, SD-043  
Informed by: teammate proposal's `int`, `float`, dimension, unit, and `Length(m)` declaration examples

## Decision

The current parser enforces the mutually exclusive annotation grammar but does not resolve a dimension name, unit spelling, or assigned value.

A declaration may contain at most one annotation from three mutually exclusive categories:

1. a dimensionless primitive type: `int`, `float`, `bool`, or `text`;
2. a dimension constraint such as `Length`; or
3. an exact-unit constraint using brackets, such as `[m]` or `[m^2]`.

Combined forms such as `float[m]`, `Length(m)`, and `float Length` are rejected. A unit-bearing quantity does not separately declare a numeric representation type; numeric storage is governed by the language-wide numeric policy.

## Compatibility

A dimension-constrained variable accepts assigned values of the required dimension and retains each value's unit representation. An exact-unit-constrained variable requires the same representation or an explicit `as` conversion. Primitive numeric annotations are dimensionless.

## Examples

```text
let count: int = 5;
let distance: Length = 5m;
let exactDistance: [m] = 5m;
let area: [m^2] = 10[m^2];
```

## Open dependent decisions

Local initializer inference, initializer requirements, one binding per declaration, and explicit function contracts are governed by SD-028. Scope and mutation, named quantity-kind annotations, and the numeric representation remain separate decisions.

## Revisit trigger

Revisit if the completed function or quantity-kind design cannot express a required contract without combining annotation categories.
