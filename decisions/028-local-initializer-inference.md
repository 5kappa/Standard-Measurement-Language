# 028: Local initializer inference and declaration initialization

Status: ACCEPTED FOR CURRENT DECLARATION GRAMMAR  
Target: current course lexer/parser; inference later  
Depends on: SD-024, SD-027, SD-035, SD-043  
Informed by: teammate proposal's inferred `let distance = 100m` and `let time = 9.58s` declarations

## Decision

The current parser enforces the declaration shape—one binding, an optional annotation, and the initializer rules below. It does not perform inference or validate an initializer's type or unit.

Every `let` and `const` declaration introduces one binding. A declaration annotation is optional.

- A `let` declaration may omit its initializer.
- A `const` declaration requires an initializer at its declaration.
- With an annotation and an initializer, the initializer is checked against the declared constraint.
- Without an annotation, an initialized declaration may infer its constraint from the initializer's checked result.
- Inferred unit-bearing quantities receive exact-unit constraints.
- Inference never uses later assignments, control-flow joins, callers, or global constraint solving.
- Function parameters and return values require explicit annotations.
- Multi-binding declarations are rejected.
- Definite assignment and the eventual constraint of an unannotated, uninitialized `let` are deferred semantic questions.

## Examples

```text
let count = 5;              // int
let pending: Length;        // annotated, uninitialized let
let untyped;                // constraint settled by later semantic rules
let ratio = 0.5;            // float
let span = 5m;              // [m]
let area = 6[m^2];          // [m^2]
let flexible: Length = 5m;  // explicit dimension constraint
```

## Reason

When an initializer exists, the checker can record its primitive type, dimension, and unit representation without global inference. Allowing an uninitialized `let` follows the accepted proposal surface while keeping `const` immediately bound. Definite-assignment and later constraint rules are not parser responsibilities.

## Validation

Fixtures must cover every primitive category, simple and compound inferred units, explicit dimension and exact-unit annotations, initialized and uninitialized `let` declarations, rejected uninitialized `const` declarations, invalid initializers, multiple bindings, and required function contracts.

## Revisit trigger

Broader inference requires a separate decision with motivating fixtures and must not silently weaken explicit conversion or function-boundary contracts.
