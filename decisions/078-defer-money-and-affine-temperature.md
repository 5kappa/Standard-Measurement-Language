# 078: Defer money and affine temperature

Status: ACCEPTED  
Target: current course proposal  
Depends on: decisions 030, 043, and 076  
Supersedes: decision 077  
Informed by: collective team scope review after considering the teammate proposal's currency and temperature design

## Decision

Money, currencies, exchange-rate declarations, affine temperature points, and temperature differences are deferred. They are not part of the current Measure proposal's keyword inventory, reserved annotations, unit registry, grammar, examples, or uniqueness claims.

The following spellings are therefore absent from the current language surface:

```text
rate Money Temperature
USD PHP EUR
C K dC
```

The optional noise word `to` remains accepted only for postfix physical-unit conversion. The current unit and dimension model remains the bounded physical Length-Mass-Time model with derived `Force`.

## Rationale

Currency conversion is contextual and would require policy for rate direction, scope, validity, and provenance. Affine temperature requires a separate point-versus-difference algebra. Both are valuable possible extensions, but including either would materially expand the proposal beyond its focused physical-unit design and make the lexical, syntactic, and semantic presentation harder to manage.

## Consequences

- `rate USD to PHP = 58.20;`, `250USD`, `20C`, and `5dC` are not valid examples in the current proposal.
- `Money` and `Temperature` cannot be declaration annotations.
- Currency and temperature rules from the teammate draft remain documented as deferred design input only.
- The accepted rules for dimensionless values, bounded physical-unit algebra, explicit `as` conversion, and the LMT-plus-Force model are unchanged.

## Revisit trigger

Reconsider either domain only through a separate scope decision that supplies its complete symbols, grammar, compatibility rules, conversions, examples, and diagnostics.
