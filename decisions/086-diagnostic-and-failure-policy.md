# 086: Diagnostic and failure policy

Status: ACCEPTED FOR CURRENT FRONT-END CONTRACT  
Target: Standard Measurement Language version 0.1 lexer and parser  
Depends on: `docs/frontend/TOKEN-SPEC.md`, `docs/frontend/SOURCE-LOCATIONS.md`, `docs/frontend/GRAMMAR.ebnf`, and `docs/frontend/AST-SCHEMA.md`

## Diagnostic contract

- Every current frontend diagnostic has severity `error`; version 0.1 defines no lexer or parser warnings.
- Stable diagnostic codes, categories, and source labels form the conformance contract. Exact English message wording may improve without changing the language contract.
- Every diagnostic has one primary source span and may have secondary labels, notes, or correction guidance.
- Independent diagnostics are ordered by source position, then by end byte, then by diagnostic code as fixed in `DIAGNOSTICS.md`.
- Detached quantities and misplaced optional noise words receive specialized local diagnostics.
- Invalid source characters are diagnosed even inside strings and comments because the canonical-character rule covers the complete source file.
- An unclosed string's primary span ends before the newline that terminates scanning of that string.
- An unterminated block comment labels its opening `/*` as the primary cause and the zero-width `EOF` location as a secondary stopping point.
- Semantic failures such as unknown units, invalid conversions, call mismatch, or unit-bearing update targets are not lexer or parser diagnostics.
- Version 0.1 has no generic `SYN001 UNEXPECTED_TOKEN`: every parser state reports an expected token or construct, or a specialized code. The number remains unused rather than renumbering the accepted `SYN002` and later codes.

The lexer exposes at most twenty diagnostic records. It continues scanning after the cap, suppresses further records, and marks the lexical result as truncated. The cap bounds diagnostic output and memory; the rule that every lexical failure consumes a nonempty source range guarantees progress.

## Phase policy

The lexer continues after each lexical failure, consumes the documented malformed candidate or invalid source range, and may report multiple independent lexical errors. It always reaches the physical end of the source and emits one real `EOF` token. Decision 088 later fixed invalid UTF-8 handling at exactly one diagnostic, one consumed byte, and one display-column advance per invalid byte.

The lexing result succeeds only if it contains no lexical diagnostics. The parser is invoked only after successful lexing.

A successful lexical result contains its complete token stream. A failed lexical result contains partial tokens recognized outside malformed ranges, its diagnostics, and its truncation flag. Both token collections end in physical `EOF`. Partial tokens contain no error or synthetic tokens and are exposed for testing and debugging only; the parser must reject the failure variant.

The parser is fail-fast. Its first syntax error produces exactly one syntax diagnostic, stops parsing, and returns no AST. A zero-width expected-token location is diagnostic data, not a synthetic token.

## Malformed numeric candidates

The lexer reports one error for the longest recognizable malformed numeric candidate and stops before text that clearly begins a separate ordinary token. `DIAGNOSTICS.md` fixes the exact boundary for `1__0`, `0x`, `0xG`, `3e+`, `2.5e3foo`, and `5..2`; fixtures must reproduce those results.

## Deferred parser recovery

Version 0.1 does not synchronize after syntax errors, skip unexpected parser tokens, synthesize missing tokens, or expose recovered AST nodes.

If parser recovery is proposed later, the preferred starting policy is:

- synthesize only unambiguous closing `)`, `]`, `}`, or `;` markers;
- synchronize at grammar-local boundaries such as `fn`/`EOF`, `;`/`}`, commas and closing list delimiters, closing expression delimiters, and unit-annotation `]`;
- guarantee progress by consuming input or returning at a synchronization boundary; and
- preserve the successful AST schema unchanged.

These points are deferred guidance, not current implementation requirements.

## Reason

This middle-ground design provides multiple useful lexical diagnostics while keeping the handwritten parser and successful AST easy to understand. Phase gating prevents skipped malformed text from causing parser cascades. Parser fail-fast behavior also removes the need for error nodes, synthetic tokens, synchronization tables, and a parser diagnostic cap in version 0.1.

## Validation

Fixtures must establish that:

- multiple independent lexical errors may be reported in source order;
- a lexically invalid source never reaches the parser;
- a lexically valid source with multiple syntax errors reports only the first;
- a syntax failure returns no AST;
- an absent delimiter may be diagnosed at a zero-width location without creating a token; and
- successful token streams and ASTs are unchanged by the failure policy.
