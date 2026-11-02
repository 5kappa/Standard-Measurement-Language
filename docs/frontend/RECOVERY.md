# Standard Measurement Language Lexical Continuation and Parser Failure Contract

Status: accepted  
Applies to: Standard Measurement Language (SML) version 0.1 lexer, parser, and failure fixtures  
Depends on: [`TOKEN-SPEC.md`](TOKEN-SPEC.md), [`SOURCE-LOCATIONS.md`](SOURCE-LOCATIONS.md), [`DIAGNOSTICS.md`](DIAGNOSTICS.md), and [decision 086](../../decisions/086-diagnostic-and-failure-policy.md)

## Purpose

This document defines how the frontend proceeds after malformed input. Version 0.1 uses a middle-ground policy:

- the lexer continues after lexical failures and may report multiple independent diagnostics;
- the parser runs only after lexing succeeds; and
- the parser stops at its first syntax error and returns no AST.

Lexical continuation does not repair source or infer programmer intent. Parser synchronization and recovered trees are deliberately outside version 0.1.

## Lexical result

```text
LexResult
    Success
        tokens: List<Token>

    | Failure
        partial_tokens: List<Token>
        diagnostics: List<Diagnostic>        // one through twenty
        diagnostics_truncated: boolean
```

Both variants end their token collection with exactly one real physical-end `EOF` token. `Failure.partial_tokens` contains every valid token recognized outside malformed ranges, in source order, followed by `EOF`. It contains no `ERROR` token, placeholder token, or synthetic token.

The parser accepts only `Success.tokens`. Supplying `Failure.partial_tokens` to the parser violates the frontend contract, even if the remaining tokens happen to form valid grammar.

Partial tokens exist for lexer testing, diagnostics, and debugging. They are not a recovered program.

`Failure` is not subdivided by cause because one scan may encounter several different lexical failures. Its ordered diagnostics identify each cause with `LEX001` through `LEX010`; every returned diagnostic has phase `LEXER`. A malformed-source failure is ordinary result data rather than an exception.

## General continuation invariants

After each lexical failure, the lexer must:

1. emit or suppress the diagnostic according to the twenty-record limit;
2. consume a nonempty malformed byte range;
3. resume at the first byte not owned by that malformed range;
4. preserve every later valid token's original lexeme and span; and
5. eventually emit physical-end `EOF`.

The same consumption and continuation behavior applies after the diagnostic limit is reached. Suppression changes only the returned diagnostic collection, not scanning, tokens, locations, or `diagnostics_truncated`.

The lexer never rewinds into an already consumed malformed range. It never reinterprets a malformed candidate as shorter valid tokens merely to continue.

## Continuation by diagnostic family

### `LEX001 INVALID_UTF8`

- When no complete well-formed UTF-8 scalar value begins at the current offset, diagnose exactly the current byte.
- Consume exactly that one byte and advance the display column by one.
- Resume UTF-8 decoding at the following byte.
- Emit no token or replacement character for the invalid byte.
- Remain in the current ordinary, string, line-comment, or block-comment scanning state.

Every later invalid byte is an independent diagnostic, subject to the twenty-record limit. A malformed multi-byte sequence may therefore produce multiple `LEX001` records. Valid ASCII or UTF-8 text after an invalid byte retains its physical byte offsets, and a following newline is processed normally.

### `LEX002 INVALID_SOURCE_CHARACTER`

Outside strings and comments:

- diagnose and consume the complete UTF-8 byte sequence of the invalid character;
- emit no token for it; and
- resume ordinary scanning immediately afterward.

For a leading underscore, consume only `_`; following ASCII letters or digits are scanned normally. For example, `_name` produces one `LEX002` diagnostic for `_`, followed by partial token `IDENT("name")`.

Inside a string:

- diagnose each invalid character independently, subject to the limit;
- continue scanning in string state until the closing quote, newline, or EOF; and
- emit no `STRING` token for any string containing a lexical failure.

Inside a comment:

- diagnose each invalid character independently;
- remain in the current line- or block-comment state; and
- emit no token, because comments are trivia.

### `LEX003` through `LEX007` numeric failures

Consume the complete malformed numeric candidate defined by `TOKEN-SPEC.md` and `DIAGNOSTICS.md`. Emit no `NUMBER` or other token for any part of that candidate. Resume at its first unconsumed byte.

The accepted ambiguous cases are:

| Source | Consumed malformed range | Later partial tokens |
| --- | --- | --- |
| `1__0` | `1__0` | `EOF` |
| `0x` | `0x` | `EOF` |
| `0xG` | `0xG` | `EOF` |
| `3e+` | `3e+` | `EOF` |
| `2.5e3foo` | `2.5e3` | `IDENT("foo")`, `EOF` |
| `5..2` | `5..2` | `EOF` |

A comma is not owned by a numeric candidate. It is scanned as `COMMA`; surrounding numeric spellings are scanned independently.

### `LEX008 UNCLOSED_STRING`

At `CR`, `LF`, or `CRLF`:

- consume the string from its opening quote through the last byte before the newline;
- emit no `STRING` token;
- leave the newline unconsumed by string recovery; and
- resume ordinary scanning after the normal whitespace scanner consumes that complete newline sequence.

At EOF, consume through the final source byte, emit no `STRING`, and then emit `EOF`.

If invalid characters were already reported inside the same string, `LEX008` remains an independent diagnostic when no closing quote exists.

### `LEX009 UNTERMINATED_BLOCK_COMMENT`

Consume from the opening `/*` through the final source byte. Emit no token, report the opening delimiter primarily and physical EOF secondarily, then emit `EOF`. No later source exists to scan.

### `LEX010 INCOMPLETE_LOGICAL_OPERATOR`

Consume the lone `&` or `|`, emit no token for it, and resume at the following byte. A following character that is not part of the same operator is scanned independently.

## Comments and slash prefixes

The accepted prefix order remains:

```text
//  then  /*  then  /=  then  /
```

Once `/*` begins a block comment, a nested `/*` is ordinary comment content. Only the first following `*/` closes the comment. Continuation never treats a nested opener as a second comment needing recovery.

## Adjacency in partial tokens

Partial-token adjacency is still computed from physical spans:

```text
previous.span.end_byte == current.span.start_byte
```

Skipped malformed bytes therefore remain visible as a span gap. The lexer does not close gaps or fabricate trivia. This rule exists for fixture accuracy only because partial tokens are never parsed.

## Diagnostic limit behavior

The first twenty lexical diagnostics in the ordering defined by `DIAGNOSTICS.md` are returned. On detecting a twenty-first lexical failure:

- set `diagnostics_truncated` to true;
- suppress that and all later diagnostic records;
- continue applying the same consumption rules; and
- continue producing later valid partial tokens and final `EOF`.

If the source contains exactly twenty lexical failures, `diagnostics_truncated` is false.

## Parser phase gate

```text
LexResult.Success(tokens)  -> parser may run
LexResult.Failure(...)     -> parser must not run
```

No parser diagnostic may be produced for a lexically failed source. This prevents malformed byte or token gaps from causing secondary syntax errors.

## Parser failure behavior

For lexically successful input, the parser either returns one successful `SourceFile` AST or its first syntax diagnostic.

On syntax failure, the parser:

- selects the specialized or general code required by `DIAGNOSTICS.md`;
- records real source spans or a zero-width expected-syntax location;
- returns exactly one diagnostic;
- returns no partial or recovered AST;
- creates no synthetic token;
- skips no token in an attempt to resume; and
- performs no statement, delimiter, list, expression, or unit synchronization.

A zero-width location for an absent `)`, `]`, `}`, `;`, operand, or other construct is diagnostic metadata only. It is not inserted into the token stream or AST.

## Deferred parser-recovery guidance

The following previously approved ideas are explicitly deferred and have no version 0.1 implementation effect:

- synthesizing only unambiguous closing `)`, `]`, `}`, or `;` markers;
- source-file synchronization at `fn` or `EOF`;
- statement synchronization at `;` or `}`;
- list synchronization at `,` or the closing delimiter;
- expression synchronization at its closing delimiter or statement boundary; and
- unit-annotation synchronization at `]` or the surrounding expression boundary.

Adding any of these requires a new decision and corresponding recovered-result schema. It must not change successful token or AST fixtures.

## Fixture requirements

Recovery and failure fixtures must cover:

- every lexical diagnostic family's consumed range and next scanning position;
- valid tokens before and after an invalid UTF-8 range or invalid character;
- leading `_` followed by a valid identifier remainder;
- invalid characters inside closed and unclosed strings;
- invalid characters inside line and block comments;
- string continuation at `CR`, `LF`, `CRLF`, and EOF;
- unterminated block comment through EOF;
- all accepted malformed-number boundaries and partial-token results;
- lone `&` and `|` followed by valid tokens;
- a malformed gap between otherwise adjacent-looking tokens;
- exactly twenty versus more than twenty lexical failures;
- later valid partial tokens after diagnostic truncation;
- one physical-end `EOF` in every success and failure token collection;
- rejection of `Failure.partial_tokens` by the parser phase gate;
- exactly one syntax diagnostic for lexically valid input containing multiple syntax errors; and
- no token synthesis or AST result after syntax failure.

## Acceptance rule

An implementation does not conform if it stops lexing before physical EOF except because the source itself ends, reparses malformed candidates as shorter valid tokens, emits `ERROR` or synthetic tokens, loses later valid partial tokens, invokes the parser after lexical failure, reports more than one syntax diagnostic, or returns an AST after syntax failure.
