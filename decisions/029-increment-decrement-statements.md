# 029: Increment and decrement statements

Status: ACCEPTED FOR CURRENT PARSER GRAMMAR  
Target: current course lexer/parser; mutation semantics later  
Depends on: SD-023, SD-027, SD-028, and later mutation rules  
Informed by: teammate proposal's prefix and postfix `++` and `--` operators

## Decision

The current parser enforces only the standalone postfix statement form. Mutability, numeric type, stored unit representation, and the effect of the update belong to a future semantic/runtime project.

Measure supports postfix `++` and `--` only as standalone mutation statements. They add or subtract one in the target's current unit representation and do not produce a value.

```text
count++;
length--;
```

Prefix forms and expression use are rejected:

```text
++count;
let old = count++;
print(count++);
```

Constants and nonnumeric bindings cannot be incremented or decremented.

## Unit behavior

`5m++` is not syntax because the target must be a mutable identifier. If `length` currently stores `5m`, `length++` produces `6m`; if a dimension-constrained binding currently stores `20cm`, it produces `21cm`.

## Reason

The current representation gives increment an unambiguous unit-aware meaning. Restricting it to a statement avoids old-versus-new return values, expression side effects, and extra precedence rules.

## Validation

Fixtures must cover dimensionless and unit-bearing targets, dimension-constrained targets whose current representations differ, constants, nonnumeric values, prefix syntax, and attempted expression use.
