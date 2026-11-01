# 043: Compatible-unit conversion is explicit

Status: ACCEPTED  
Target: version 0.1  
Depends on: SD-032, SD-040, SD-041, SD-042
Informed by: teammate proposal's No Silent Conversion principle and `as` operator

## Decision

For the current project, only the postfix `as` syntax and AST shape are enforced. The parser accepts cross-dimension forms such as `5m as s`; compatibility is a future semantic check.

Operations requiring a common unit representation do not silently convert differently represented compatible quantities. Source code uses postfix `as`, for example `5km + (3mi as km)`.

Multiplication and division continue to derive dimensions and units automatically; they do not require operands to share a unit. Conversion targets must have a compatible dimension.

## Validation

`5km + 3mi` must produce a conversion-oriented diagnostic. `5km + (3mi as km)` must type-check. Invalid cross-dimension conversion, such as `5m as s`, must be rejected.


## Open dependent decisions

Numeric conversion arithmetic, precision loss, runtime magnitude representation, and result display remain SD-041 through SD-045 concerns. Canonical base units and exact registry scales are fixed by decision 030.
