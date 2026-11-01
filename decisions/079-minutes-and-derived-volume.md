# 079: Minutes and derived volume

Status: ACCEPTED  
Target: current course proposal  
Depends on: decisions 022, 030, and 033  
Amends: decision 030's initial unit registry  
Informed by: team review of the proposal introduction and initial unit coverage

## Decision

Add `min` to the initial built-in unit registry as a complete, case-sensitive Time-unit symbol with exact scale:

```text
1min = 60s
```

The lexer continues to emit `IDENT`; no special token or prefix rule is introduced. Resolution treats `min` as one registered symbol.

Volume remains the derived dimension `Length^3`. The language expresses and constrains volume with bounded compound-unit syntax such as `[m^3]`; it does not reserve or introduce a named `Volume` annotation.

## Examples

```measure
let duration: Time = 5min;
let durationSeconds: [s] = duration as s;

let length = 3m;
let width = 2m;
let height = 4m;
let volume: [m^3] = length * width * height;
```

## Rationale

Minutes are common, have a fixed exact relationship to seconds, and add no lexical or grammatical complexity. Volume is already representable by the accepted unit algebra, so a named dimension would add vocabulary without adding expressive power.

## Validation

- `5min` resolves as a Time quantity.
- `1min as s` produces the same represented duration as `60s`.
- `min` is not decomposed into prefixes or other symbols.
- `[m^3]` is accepted within the existing exponent and annotation limits.
- `Volume` remains available as an ordinary identifier rather than a reserved annotation name.

## Revisit trigger

Adding other time units or a named `Volume` annotation requires a separate decision and updated registry, keyword, example, and fixture inventories.
