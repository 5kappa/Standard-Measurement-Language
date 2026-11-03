# 026: Dimensionless numbers and numeric powers

Status: ACCEPTED FOR STAGED PARSER GRAMMAR  
Target: current course lexer/parser; semantic checks later  
Depends on: SD-020, SD-021, SD-031, SD-041  
Informed by: teammate proposal's plain `Scalar` values and numeric `^` operator

## Decision

For the current project, this record selects syntax and AST structure only. The parser does not determine whether a base is dimensioned or whether an exponent is semantically permitted; those checks belong to a future project.

Measure does not require every number or numerical variable to carry a unit. A unitless numeric value is a valid dimensionless quantity; `Scalar` is descriptive terminology, not a separate base dimension.

Numeric exponentiation uses `^` in a later expression layer:

- the exponent must be dimensionless;
- a unary sign is permitted on the exponent, so negative exponents such as `x ^ -2` are syntactically valid;
- a dimensionless base may have an integer or decimal exponent;
- a dimensioned base requires a compile-time integer exponent;
- a decimal exponent is never part of a unit expression.

Exact root operations may later accept dimensioned arguments only when every dimension exponent divides evenly by the root degree.

## Reason

Engineering formulas frequently raise dimensionless coefficients and ratios to decimal powers. Allowing those operations does not create fractional physical dimensions. Requiring compile-time integer powers for dimensioned bases keeps dimension inference exact and static.

## Validation

- `16 ^ 0.5` is valid and dimensionless.
- `2 ^ -3` is syntactically valid and dimensionless.
- `3m ^ 2` has dimension `Length^2`.
- `3m ^ -2` has dimension `Length^-2`.
- `2 ^ 3m` parses as a power expression but is rejected during checking because the exponent carries a unit.
- `3m ^ 0.5` is rejected during checking.
- Future `sqrt(9[m^2])` may produce `3m`; `sqrt(9m)` is rejected.

## Open dependent decisions

Numeric representation, approximation, negative-base behavior, overflow, and rounding remain SD-041 and SD-045 decisions.
