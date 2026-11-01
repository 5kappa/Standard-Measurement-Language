# 080: Add the mile unit

Status: ACCEPTED; EXPANDED by decision 081  
Target: current course proposal  
Depends on: decisions 030, 033, and 043  
Amends: decision 030's initial unit registry  
Informed by: the teammate proposal's `km`/`mi` explicit-conversion example

Expansion note: decision 081 later adds `ft` and `in`. The “mile only” boundary below records the state at the time of this decision rather than the current registry.

## Decision

Add `mi` to the initial built-in unit registry as a complete, case-sensitive Length-unit symbol with exact scale:

```text
1mi = 1609.344m = 201168/125 m
```

This decision originally added only `mi`. Decision 081 later expands the accepted imperial set to `in`, `ft`, and `mi`. Neither decision adds yards, pounds, pound-force, or an imperial prefix/conversion system.

The lexer continues to emit `IDENT`; no special token or grammar production is introduced. Resolution treats `mi` as one complete registered symbol.

## Examples

```measure
let route = 3mi;
let routeMetric: [km] = route as km;
let total = 5km + (3mi as km);
```

The following remains invalid because conversion is not silent:

```measure
let total = 5km + 3mi;
```

## Rationale

The mile gives the No Silent Conversion rule a clear cross-system example while adding no lexical or syntactic complexity. Restricting the change to `mi` avoids expanding the proposal into a general imperial-unit library.

## Validation

- `3mi` resolves as a Length quantity.
- `1mi as m` represents exactly `1609.344m`.
- `mi` is not decomposed as a prefix expression.
- `5km + 3mi` requires an explicit conversion.
- `yd`, `lb`, and `lbf` remain unregistered in the current proposal.

## Revisit trigger

Any additional imperial unit requires a separate registry decision and updated examples and fixtures.
