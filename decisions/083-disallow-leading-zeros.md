# 083: Disallow leading zeros in numeric literals

Status: ACCEPTED  
Target: numeric-literal grammar  
Depends on: decisions 012, 076, and 082

## Decision

An integer part is either the single digit `0` or a nonzero digit followed by zero or more digits:

```ini
Digits         = { 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 }
NonZeroDigit   = { 1, 2, 3, 4, 5, 6, 7, 8, 9 }
IntegerLiteral = 0 | NonZeroDigit Digits*
DecimalLiteral = IntegerLiteral . Digits+
NumberLiteral  = IntegerLiteral | DecimalLiteral
```

The corresponding combined regular expression is:

```regex
(0|[1-9][0-9]*)(\.[0-9]+)?
```

Thus, `0`, `125`, `0.5`, and `12.50` are valid, while `00`, `0123`, and `01.5` are invalid. A leading `+` or `-` remains an expression operator rather than part of the numeric literal.

## Rationale

Rejecting leading zeros gives each ordinary decimal magnitude a canonical spelling and avoids suggesting that a leading zero selects another number base. Separating `0` from nonzero-leading forms also keeps the rule explicit and straightforward to recognize with a finite-state lexical machine.
