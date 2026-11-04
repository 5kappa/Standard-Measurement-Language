# Standard Measurement Language Front-End Development Charter

Status: documentation hardening and lexer implementation complete; parser implementation not started
Target: Standard Measurement Language (SML) version 0.1 lexer and parser

## Purpose

This directory turns the accepted language proposal into an implementation-facing contract for the Standard Measurement Language (SML) front end. The project ends after lexical and syntactic analysis:

```text
UTF-8 source
    -> lexer
    -> tokens with original lexemes and source spans
    -> parser
    -> source-located AST or lexical/syntax diagnostics
```

The implementation does not perform name or unit resolution, dimensional checking, conversion, unit normalization, evaluation, code generation, or other runtime behavior.

## Authority

[`LANGUAGE-SPECIFICATION.md`](../../LANGUAGE-SPECIFICATION.md) is the normative authority for the language surface.

The following documents provide rationale and history but do not override the normative specification:

- [`PROJECT.md`](../../PROJECT.md)
- [`SPECIFICATION-ROADMAP.md`](../../SPECIFICATION-ROADMAP.md)
- [`decisions/`](../../decisions/)
- [`Teammate_made_Draft.md`](<../../proposal files/Teammate_made_Draft.md>)

If an implementation-facing document conflicts with `LANGUAGE-SPECIFICATION.md`, development stops at the conflict. The specification is either followed or deliberately amended before implementation continues; the implementation must not silently choose a different language.

## Final project boundary

The front end owns:

- source-character validation and token boundaries;
- token kinds, original lexemes, adjacency information, and source spans;
- comment and whitespace handling;
- grammar recognition, precedence, associativity, and grouping;
- structural limits of unit expressions;
- construction of a source-located AST;
- lexical and syntactic diagnostics;
- lexical continuation after malformed candidates; and
- fail-fast parser behavior after the first syntax diagnostic.

The front end does not own:

- whether an identifier or unit spelling is declared or registered;
- whether dimensions or quantity kinds are compatible;
- simplification or normalization of unit expressions;
- whether a conversion target is dimensionally compatible;
- numeric calculation, rounding, overflow, or display-unit selection;
- interpretation, compilation, or code generation; or
- runtime behavior of statements and functions.

These exclusions are final for this project. Examples of later semantic behavior may remain in the proposal as explanation, but they are not implementation requirements or acceptance criteria for the lexer and parser.

## Syntax versus meaning

The lexer and parser validate how source text is written and structured. They do not decide whether a structurally valid program is meaningful.

| Source | Front-end result | Reason |
| --- | --- | --- |
| `10foo` | Accept as an attached simple quantity | `foo` has the lexical form `IDENT`; registration is not checked. |
| `10 foo` | Reject during parsing | A simple quantity's `NUMBER` and `IDENT` must be adjacent. |
| `10m + 5s` | Accept as an addition AST | Dimension compatibility is outside the front end. |
| `5m as s` | Accept as a conversion AST | Conversion compatibility is outside the front end. |
| `1[m^2/m]` | Accept and preserve the unit-expression AST | Simplifying the unit to `m` would be semantic normalization. |
| `1[kg/m/m/m/m]` | Reject during parsing | The unit grammar permits at most one top-level division. |
| `1[kg/(m*m*m*m)]` | Accept and preserve the unit-expression AST | The denominator is a structurally valid grouped product; whether the resulting dimension is useful is not a parser decision. |

## Structural unit-expression checks

The parser enforces only rules derivable from source spelling and grammar, including:

- at most one top-level division;
- no repeated or nested division;
- a grouped denominator only where the grammar permits it;
- no powers applied to grouped unit expressions;
- no numeric scale factors inside unit expressions;
- at most eight written unit-factor occurrences;
- source exponents from `-16` through `16`; and
- at most 128 ASCII characters inside a bracketed unit annotation.

The parser preserves unit names, products, quotients, powers, grouping required by the unit grammar, and their source spans. It does not combine factors, cancel exponents, expand named units, or calculate a normalized dimension.

## Hardening artifacts

The implementation contract is divided into these accepted, reviewable documents:

1. [`TOKEN-SPEC.md`](TOKEN-SPEC.md) — accepted token kinds, recognition rules, maximal munch, trivia, adjacency, and required token fields.
2. [`GRAMMAR.ebnf`](GRAMMAR.ebnf) — the complete version 0.1 grammar without historical alternatives.
3. [`SOURCE-LOCATIONS.md`](SOURCE-LOCATIONS.md) — accepted offsets, line and column conventions, newline handling, tabs, and zero-width locations.
4. [`AST-SCHEMA.md`](AST-SCHEMA.md) — accepted source AST node kinds, fields, retained token references, repeated structures, and spans.
5. [`DIAGNOSTICS.md`](DIAGNOSTICS.md) — accepted lexical and syntactic codes, labels, stable data, ordering, limits, and phase behavior.
6. [`RECOVERY.md`](RECOVERY.md) — accepted lexical continuation boundaries, partial-token failure results, phase gating, and fail-fast parser policy.
7. [`fixtures/README.md`](fixtures/README.md) — accepted version 1 JSON format and complete 93-case token, AST, diagnostic, and recovery conformance suite.
8. [`TRACEABILITY.md`](TRACEABILITY.md) — completed rule registry and reverse indexes linking all 112 implementation-facing requirements to fixture evidence or an explicit process-level rationale.

[`MALFORMED-INPUT-AUDIT.md`](MALFORMED-INPUT-AUDIT.md) is the non-normative historical inventory that led to the accepted diagnostic and recovery contracts.

[`IMPLEMENTATION.md`](IMPLEMENTATION.md) records the accepted Python engineering baseline. It is subordinate to the language-independent contracts above and cannot change their observable behavior.

An artifact becomes authoritative for implementation only after it is marked accepted and agrees with `LANGUAGE-SPECIFICATION.md`.

## Development readiness gate

Implementation begins only after the relevant contract is frozen:

- Lexer work requires an accepted token specification and source-location policy.
- Parser work requires the lexer contracts, consolidated grammar, and AST schema.
- Diagnostic and failure-handling work requires the accepted diagnostic and lexical-continuation documents.
- Full conformance testing requires machine-readable fixtures covering all accepted grammar surfaces.

The lexer implementation began with the deliberately small slice:

```sml
10m
```

That slice established the exact `NUMBER`, `IDENT`, and physical `EOF` token stream, byte spans, source positions, and quantity adjacency without consulting a unit registry or performing parsing or semantic analysis. The completed R0–R10 lexer now passes the full lexer-only conformance gate. Expression precedence, unit-expression structure, and AST construction remain work for later parser slices.
