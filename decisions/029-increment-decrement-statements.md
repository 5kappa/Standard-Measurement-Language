# 029: Increment and decrement statements

Status: ACCEPTED FOR CURRENT PARSER GRAMMAR  
Target: current course lexer/parser; mutation semantics later  
Depends on: SD-023, SD-027, SD-028, and later mutation rules  
Informed by: teammate proposal's prefix and postfix `++` and `--` operators

## Decision

The current parser accepts standalone prefix and postfix statement forms. Mutability, numeric type, unit information, and the effect of the update belong to a future semantic/runtime project.

SML supports prefix and postfix `++` and `--` as standalone mutation statements. They do not produce expression values.

```text
++count;
--count;
count++;
count--;
```

Expression use is rejected:

```text
let old = count++;
print(count++);
```

Constants and nonnumeric bindings cannot be incremented or decremented.

## Unit behavior

The target must be a mutable, dimensionless numeric identifier. A unit-bearing variable cannot use either update form; it must state the increment with a compatible unit, such as `length += 1m;`. The parser records the identifier target but does not determine whether it carries a unit.

## Reason

Supporting both positions follows the proposal surface. Restricting updates to standalone statements avoids old-versus-new expression values, expression side effects, and extra precedence rules. Restricting them semantically to dimensionless targets avoids inventing an implicit unit for the literal one.

## Validation

Parser fixtures must cover prefix and postfix statements plus attempted expression use. Later checking fixtures must cover dimensionless targets, rejected unit-bearing targets, constants, and nonnumeric values.
