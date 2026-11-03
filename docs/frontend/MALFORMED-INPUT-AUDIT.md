# Standard Measurement Language Malformed-Input Audit

Status: completed historical audit; not an implementation contract  
Applies to: rationale for `DIAGNOSTICS.md` and `RECOVERY.md`

## Purpose

This document records the malformed-input audit that led to the accepted front-end contracts. It preserves the questions considered and prevents historical uncertainty from being mistaken for current implementation freedom. Normative behavior belongs in `TOKEN-SPEC.md`, `GRAMMAR.ebnf`, `SOURCE-LOCATIONS.md`, `DIAGNOSTICS.md`, and `RECOVERY.md`.

## Clarifications accepted after the audit

- Prefix and postfix `++` and `--` are standalone statement syntax.
- Either update form is invalid for a variable with an associated unit. That determination requires later name resolution and checking, not lexing or parsing. Source must instead use an explicit unit-bearing operation such as `x += 1m`, with the appropriate unit for `x`.
- Lexical continuation is required: after a lexical error, the lexer resumes at a documented boundary and may find later lexical errors. Parser recovery is deferred; the parser stops at its first syntax error. Neither policy infers intended semantics.
- A simple or compound quantity must be attached to its magnitude. `100 m`, `100/*comment*/m`, and `9.8 [m/s^2]` are parser errors.
- Numeric literals have no underscore or comma separators. Scientific notation and alternate number systems are outside version 0.1.
- A comma remains a grammar token for separating parameters, arguments, and print expressions. It is never part of a `NUMBER`; therefore `1,000` is not one numeric literal.
- All current frontend diagnostics have severity `error`, one primary span, and a stable code and category. Secondary labels, notes, and corrections are optional; exact English wording is not normative.
- Detached quantities and misplaced noise words receive specialized local diagnostics.
- Invalid source characters are diagnosed even inside strings and comments. An unclosed string's primary span stops before its terminating newline. An unterminated block comment labels its opening `/*` primarily and `EOF` secondarily.
- The lexer continues after lexical failures, may collect multiple errors in source order, and still emits physical-end `EOF`.
- A lexical result contains at most twenty diagnostics and records whether additional diagnostics were suppressed.
- A failed lexical result exposes valid partial tokens outside malformed ranges, ending in real `EOF`; the parser accepts only a successful lexical result.
- The parser runs only if lexing has no diagnostics. It stops at its first syntax error and returns no AST.
- Version 0.1 has no parser synchronization, token synthesis, skipped-token representation, or recovered AST.

## Established malformed-input families

The accepted documents already assign these families to the lexer or parser:

- invalid UTF-8 and valid non-ASCII characters outside the canonical grammar;
- malformed decimals, leading zeros, underscore separators, and recognized unsupported numeric notation;
- unclosed strings and block comments;
- lone `&` or `|`, standalone `.`, leading `_`, and otherwise unknown characters;
- detached quantities;
- malformed functions, blocks, statements, declarations, annotations, expressions, calls, and control-flow headers;
- missing operands, separators, terminators, and closing delimiters;
- expression-valued assignment or update and chained assignment;
- invalid `input()` placement and insufficient declaration annotations for direct input;
- malformed unit products, quotients, grouping, factors, and exponents;
- unit-expression factor, exponent, and source-length limit violations;
- misplaced `to`, `then`, or `do`; and
- context-invalid `return`, `break`, or `continue`.

## Accepted malformed-number boundaries

The lexer consumes the longest recognizable malformed numeric candidate and stops before text that clearly begins a separate ordinary token. `DIAGNOSTICS.md` fixes these cases:

- `1__0`;
- `0x` and `0xG`;
- `3e+`;
- `2.5e3foo`; and
- `5..2`.

`RECOVERY.md` now fixes the general continuation rule for every lexical family. Decision 088 later selected bytewise invalid UTF-8 handling: each `LEX001` consumes one byte and advances one display column before scanning resumes. Lexical failures expose partial tokens for fixtures but never reach the parser.

## Conformance work completed after the audit

`DIAGNOSTICS.md` fixes the stable code inventory, label policy, deterministic ordering, and twenty-record lexical limit. The complete machine-readable suite now covers malformed functions, every statement family, lexical continuation, phase gating, and all active lexical and syntactic diagnostic codes. `TRACEABILITY.md` records the reciprocal coverage links.

## Accepted failure and continuation policy

`RECOVERY.md` documents:

- the exact lexer continuation rule for each lexical failure family;
- the guarantee that each lexical failure consumes a nonempty malformed range before scanning resumes;
- parser phase gating on a lexically clean result; and
- fail-fast parser behavior after one syntax diagnostic.

The previously approved parser-recovery starting points—synthesizing only `)`, `]`, `}`, or `;` and synchronizing at grammar-local boundaries—are deferred rather than active. They apply only if a future decision introduces parser recovery.

## Scope exclusions

Unknown units, undefined functions, argument mismatch, unit compatibility, Boolean condition typing, update-target mutability or dimensionality, conversion validity, and other semantic failures are not lexer or parser diagnostics. A future semantic phase may reject them, but the current frontend must accept their syntax when it otherwise matches the grammar.
