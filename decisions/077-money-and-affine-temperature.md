# 077: Money and affine-temperature support

Status: SUPERSEDED by decision 078  
Target: current course proposal  
Depends on: decisions 002, 017, 027, 030, 043, and 076  
Amends: decisions 030 and 076  
Informed by: the teammate proposal's visible exchange rates and temperature point/difference distinction

Historical note: this decision was reversed before final drafting. Decision 078 defers money and affine temperature from the current proposal.

## Decision

Measure includes `Money` and `Temperature` as built-in nominal domains. They are not additional LMT base dimensions and do not alter the accepted Length-Mass-Time vector model or the derived `Force` dimension.

### Money

The initial registered currencies are `USD`, `PHP`, and `EUR`. A currency symbol is a complete, case-sensitive unit symbol. Currency symbols cannot occur in compound unit algebra.

Currency conversion is explicit with `as` and requires a positive, dimensionless exchange rate declared in the conversion's written direction:

```measure
rate USD to PHP = 58.20;
let cost: Money = 100USD;
let pesos: [PHP] = cost as PHP;
```

`rate` is a keyword. `to` remains an optional noise word. A rate is immutable, lexically scoped, and directional; a reverse conversion needs a reverse declaration. `Money` accepts any registered currency, while an exact-unit annotation fixes one currency.

Money values in the same representation may be added, subtracted, compared, and assigned. Money may be multiplied or divided by a dimensionless number, and same-currency division produces a dimensionless result. Multiplication of two money values is rejected.

### Temperature

The initial temperature-point units are `C` and `K`; the initial temperature-difference unit is `dC`. These are complete, case-sensitive symbols and are not permitted in compound unit algebra in this proposal.

`Temperature` accepts point values in `C` or `K`. Exact `[C]` and `[K]` annotations constrain point representation; `[dC]` constrains a difference. Conversion between `C` and `K` is explicit with `as` and uses the built-in affine relationship.

Accepted operation categories are:

- point minus point produces a difference;
- point plus difference, difference plus point, and point minus difference produce a point;
- difference plus or minus difference produces a difference; and
- a difference may be multiplied or divided by a dimensionless number.

Adding two points, subtracting a point from a difference, or multiplying, dividing, or exponentiating a point is rejected.

## Rationale

These rules adopt the teammate design's two domain-specific contributions while preserving lexical and syntactic manageability. Money uses an explicit declaration because exchange is contextual, not a fixed physical scale. Temperature uses point-versus-difference rules because Celsius and Kelvin points are affine rather than ordinary multiplicative units.

## Scope limits

This decision does not add live rate lookup, rate timestamps, currency symbols beyond the initial registry, Fahrenheit, temperature-difference units beyond `dC`, user-defined units or dimensions, an implementation, or a runtime numeric representation.

## Validation examples

```measure
rate USD to PHP = 58.20;
let budget: Money = 5000PHP;
let price = 80USD;
let converted = price as PHP;

let morning: Temperature = 20C;
let noon: Temperature = 28C;
let rise = noon - morning;
let bad = morning + noon;       // rejected
let warmer = morning + 5dC;
let absolute: [K] = morning as K;
```

## Revisit trigger

Adding a new currency or temperature unit, automatic reverse rates, rate validity metadata, or temperature units in compound algebra requires a separate decision and updated lexical/syntactic fixtures.
