# 022: Bounded unit-expression grammar

Status: ACCEPTED  
Target: version 0.1 and later  
Depends on: SD-014, SD-015  
Informed by: teammate proposal's bracketed compound units using `*`, `/`, and integer `^`

## Decision

A compound unit is one product optionally divided by one denominator. The denominator is either one powered unit or one parenthesized product. Nested division, repeated division, powers on groups, implicit multiplication, and numeric scale factors inside units are rejected.

Normative bounds:

- at most one `/`;
- at most eight written unit-factor occurrences;
- at most one denominator-parenthesis level;
- source exponents from `-16` through `16`;
- normalized dimension exponents from `-32` through `32`;
- at most 128 ASCII characters in the annotation, including whitespace.

The exponent sign may be `-` or absent; an explicit `+` is rejected. The exponent token must have an integer lexeme.

## Accepted examples

```text
m^2
N*m
N/m^2
kg/(m*s^2)
```

## Rejected examples

```text
kg/m/s^2
m/(kg/s)
(m/s)^2
N m
1000*m
```

## Reason

The bounded numerator-over-denominator form covers anticipated structural units while keeping the grammar, normalization, diagnostics, and implementation resources predictable.

## Validation

Boundary fixtures must cover one versus two divisions, seven through nine factors, exponents at `-17`, `-16`, `16`, and `17`, 128 versus 129 annotation characters, nested division, and a multi-factor denominator without parentheses.

## Revisit trigger

Revisit only when a concrete engineering unit cannot be expressed clearly within the bounds and cannot be registered as a named unit.
