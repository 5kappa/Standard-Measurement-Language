# 014: Attached simple and bracketed compound quantities

Status: ACCEPTED  
Target: version 0.1  
Depends on: SD-010 through SD-013
Informed by: teammate proposal's attached simple literals and bracketed compound literals

## Decision

Simple quantities use attached spelling such as `100m` and tokenize as `NUMBER IDENT`. Their token spans or trivia metadata must show adjacency. Compound quantities use an adjacent opening bracket, such as `9.8[m/s^2]` and `8[kN/m]`; `9.8 [m/s^2]` is rejected. Whitespace inside the brackets is insignificant.

The lexer never consults the unit registry. Unknown unit names parse normally and fail during name resolution.

## Rejected alternatives

- Spaced suffixes do not visibly enforce the selected attached form.
- Brackets around every unit add punctuation to the common simple case.
- Constructor syntax requires call-like machinery too early.
- Unbracketed compound units create an avoidable boundary conflict with arithmetic operators.

## Validation

Required fixtures include `100m`, `100 m`, `100unknown`, `9.8[m/s^2]`, an empty annotation, a missing bracket, and `2[N*m] * 3m`.
