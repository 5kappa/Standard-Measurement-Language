# 033: Unit-expression resolution and normalization

Status: ACCEPTED  
Target: version 0.1 and later  
Depends on: SD-014, SD-022, SD-032  
Informed by: teammate proposal's attached unit syntax, named units, automatic unit algebra, and dimensionless `Scalar` results

## Decision

### Boundaries and whitespace

The opening `[` of a compound quantity must touch its number. Whitespace inside the brackets is insignificant and counts toward the 128-character content limit. Written unit-symbol occurrences are counted before normalization; an exponent does not multiply the factor count.

### Complete-symbol resolution

Every supported unit spelling is one complete, case-sensitive registry symbol. `km` and `kN` are single `IDENT` tokens and lookup keys, not prefix multiplication. A registry builder may generate prefixed entries, but source parsing never decomposes them.

Every written symbol resolves before cancellation or removal of zero powers. `unknown^0` and `unknown/unknown` therefore report unknown-unit errors.

### Exponents and normalization

Zero and negative integer unit exponents are valid within the SD-022 range. An explicit positive sign and decimal unit exponents are rejected.

Normalization proceeds in this order:

1. resolve every unit symbol;
2. expand registered definitions;
3. apply source exponents;
4. negate denominator exponents;
5. combine equal base dimensions;
6. remove zero exponents;
7. check normalized exponent bounds; and
8. compute the combined scale.

The compiler retains the source unit AST for diagnostics and display and uses a normalized exponent map and scale for checking.

### Dimensionless and equivalent forms

Plain numbers are valid dimensionless quantities. `m^0` and `m/m` also normalize to dimensionless. Empty annotations, numeric pseudo-units, and numeric scale factors inside units are rejected.

Named and expanded units with equal normalized dimensions and scales are equivalent for checking while retaining distinct source and preferred-display identities. Quantity-kind distinctions remain a later decision.

## Diagnostics

Every SD-022 resource or structural violation receives a local diagnostic that states the violated limit and points to the offending annotation, factor, exponent, slash, or group. Diagnostics must distinguish repeated division, nested division, excessive factors, exponent range, annotation length, normalized-exponent range, and unknown units.

## Validation

Fixtures must cover attachment, internal whitespace, pre-normalization factor counting, zero and negative powers, unknown units that would cancel, named-versus-expanded equivalence, dimensionless results, numeric pseudo-units, scale factors, and every hard-limit boundary.

## Open dependent decisions

Percentage and angle policy, preferred display selection, and quantity-kind metadata remain separate decisions. The initial base dimensions, named aliases, registry, and canonical scales are fixed by decision 030.
