# 028: Local initializer inference

Status: ACCEPTED FOR CURRENT DECLARATION GRAMMAR  
Target: current course lexer/parser; inference later  
Depends on: SD-024, SD-027, SD-035, SD-043  
Informed by: teammate proposal's inferred `let distance = 100m` and `let time = 9.58s` declarations

## Decision

The current parser enforces the declaration shape—one binding, an optional annotation, and a required initializer. It does not perform inference or validate the initializer's type or unit.

Every `let` and `const` declaration introduces one binding and requires one initializer. A declaration annotation is optional.

- With an annotation, the initializer is checked against the declared constraint.
- Without an annotation, the compiler infers the constraint solely from the initializer's checked result.
- Inferred unit-bearing quantities receive exact-unit constraints.
- Inference never uses later assignments, control-flow joins, callers, or global constraint solving.
- Function parameters and return values require explicit annotations.
- Uninitialized and multi-binding declarations are rejected.

## Examples

```text
let count = 5;              // int
let ratio = 0.5;            // float
let span = 5m;              // [m]
let area = 6[m^2];          // [m^2]
let flexible: Length = 5m;  // explicit dimension constraint
```

## Reason

The checker already computes the initializer's primitive type, dimension, and unit representation. Recording that checked result on one binding adds little machinery while avoiding repetitive annotations. Mandatory initializers avoid definite-assignment analysis and default values.

## Validation

Fixtures must cover every primitive category, simple and compound inferred units, explicit dimension and exact-unit annotations, invalid initializers, attempted later type changes, missing initializers, multiple bindings, and required function contracts.

## Revisit trigger

Broader inference requires a separate decision with motivating fixtures and must not silently weaken explicit conversion or function-boundary contracts.
