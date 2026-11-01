# 081: Add feet and inches

Status: ACCEPTED  
Target: current course proposal  
Depends on: decisions 030, 033, 043, and 080  
Amends: decision 030's initial unit registry  
Expands: decision 080's imperial-unit boundary  
Informed by: the structural-engineering focus and the team's request for feet and inches

## Decision

Add `ft` and `in` to the initial built-in unit registry as complete, case-sensitive Length symbols with exact scales:

```text
1in = 0.0254m = 127/5000 m
1ft = 12in = 0.3048m = 381/1250 m
```

Together with `mi`, these are the complete imperial-unit set in the current proposal. This decision does not add yards, pounds, pound-force, or a general imperial-unit system.

The lexer continues to emit `IDENT`; neither symbol adds a token type, prefix rule, or grammar production. Because registered unit symbols cannot be redeclared as value identifiers, `in` is unavailable as a user-defined name. SML's accepted C-style `for` grammar does not use `in` as a loop keyword.

## Examples

```measure
let height = 6ft;
let offset = 8in;
let total: [ft] = height + (offset as ft);
let metricHeight: [m] = height as m;
```

The conversion remains explicit:

```measure
let invalid = 2m + 6ft;          // rejected
let valid = 2m + (6ft as m);     // accepted
```

## Rationale

Feet and inches occur frequently in structural and construction measurements and have fixed exact relationships to meters. Adding them strengthens the domain examples without changing lexical or syntactic complexity.

## Validation

- `12in as ft` represents exactly `1ft`.
- `1ft as m` represents exactly `0.3048m`.
- `ft` and `in` resolve as complete Length symbols.
- Mixed metric/imperial addition requires explicit conversion.
- `yd`, `lb`, and `lbf` remain unregistered.

## Revisit trigger

Any additional imperial unit or a future use of `in` as grammar syntax requires a separate decision and a conflict review.
