# 012: Numeric signs are parser operators

Status: ACCEPTED  
Target: version 0.1  
Depends on: SD-012, SD-020
Informed by: teammate proposal's signed-integer rule and unary-operator table; revised to use one parser-level sign rule

## Decision

`NUMBER` contains no leading sign. `-5m` tokenizes as `MINUS NUMBER("5") IDENT("m")`; unary `+` and `-` are parser-level operators.

## Reason

One rule then covers negative literals, subtraction, grouped negation, and signed unit exponents without contextual number tokenization.

## Validation

Token and parse fixtures must distinguish `-5m`, `a-5m`, `-(5m)`, and `m^-2` locally and deterministically.
