# 017: Optional noise words

Status: ACCEPTED  
Target: version 0.1 and later  
Depends on: SD-013, SD-020, and later control-flow grammar  
Informed by: teammate proposal's `to`, `then`, and `do` noise words

## Decision

Measure reserves three optional noise words that do not affect program meaning:

- `to` may appear after `as`: `distance as to km`;
- `then` may appear after an `if` condition and before its required block;
- `do` may appear after a loop header and before its required block.

The parser accepts each word only in its assigned position. The words do not produce semantic AST nodes, although their source spans may be retained for formatting or diagnostics. They cannot be used as identifiers.

## Validation

- `3mi as km` and `3mi as to km` must produce equivalent checked expressions.
- A misplaced noise word must produce a local syntax diagnostic.
- `then`, `do`, and `to` must not resolve as user identifiers.

## Revisit trigger

Revisit if the optional forms create materially confusing diagnostics or grammar conflicts in the completed statement language.
