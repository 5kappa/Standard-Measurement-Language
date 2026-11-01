# 020: Staged operators and conversion precedence

Status: ACCEPTED  
Target: version 0.1 and later  
Depends on: SD-012, SD-014, SD-015
Informed by: teammate proposal's operator inventory and precedence tables; revised for staged delivery and postfix conversion precedence  
Extended by: decision 076 and `LANGUAGE-SPECIFICATION.md`

## Decision

Version 0.1 includes unary `+` and `-`, binary `+`, `-`, `*`, and `/`, parentheses, and postfix `as`. Precedence from strongest to weakest is primary, postfix conversion, unary sign, multiplication/division, and addition/subtraction.

Numeric exponentiation and standalone postfix increment/decrement were initially staged under SD-026 and SD-029. Modulo, assignment, comparison, equality, and logical operators were also staged pending their dependent decisions. Unit exponents do not by themselves imply numeric exponentiation.

Decision 076 completed the proposal surface: `%`, comparisons, equality, `!`, `&&`, and `||` are included; assignment remains a statement; and postfix `++`/`--` remain standalone statements. The consolidated precedence table in `LANGUAGE-SPECIFICATION.md` supersedes this record's earlier partial table.

## Validation

`3m as cm + 2cm` groups as `(3m as cm) + 2cm`. Grouping fixtures demonstrate arithmetic precedence independently of unit resolution.
