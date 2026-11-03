# 088: Bytewise invalid UTF-8 handling

Status: ACCEPTED FOR THE CURRENT LEXER CONTRACT  
Target: Standard Measurement Language version 0.1 lexer and source locations  
Depends on: `docs/frontend/TOKEN-SPEC.md`, `docs/frontend/SOURCE-LOCATIONS.md`, `docs/frontend/DIAGNOSTICS.md`, `docs/frontend/RECOVERY.md`, and decision 086

## Decision

The lexer handles malformed UTF-8 one byte at a time. At the current byte offset:

- if a complete well-formed UTF-8 scalar value begins there, the lexer decodes that complete value and applies the canonical-character rules;
- otherwise, the lexer emits one `LEX001 INVALID_UTF8` diagnostic whose primary span covers exactly the current byte, consumes exactly that byte, advances the display column by one, emits no token for it, and resumes at the following byte.

Consequently, a malformed multi-byte sequence may produce several `LEX001` diagnostics. Each diagnosed byte counts independently toward the twenty-diagnostic lexical limit. A later well-formed UTF-8 sequence, ASCII character, or newline is never consumed by the preceding error.

CR, LF, and CRLF remain well-formed ASCII newline sequences and follow the ordinary newline rules. A valid non-ASCII Unicode scalar value is decoded as one value, advances one display column, and produces `LEX002 INVALID_SOURCE_CHARACTER` rather than `LEX001`.

`LEX001.data.invalid_bytes` retains its existing name but contains exactly the one diagnosed byte. In fixture JSON it is encoded as exactly two lowercase hexadecimal digits.

The lexer does not insert `U+FFFD`, an `ERROR` token, or any replacement byte. One-column advancement is location bookkeeping only.

## Reason

Bytewise failure handling is the simplest deterministic policy for a handwritten academic lexer. It guarantees progress with one unconditional byte advance, requires no maximal-subpart grouping algorithm, preserves every later valid byte, and makes diagnostic spans and display columns direct to test. The tradeoff is that one corrupted intended character may yield several diagnostics and consume several positions in the diagnostic cap.

## Rejected alternatives

- Unicode maximal-subpart grouping was rejected for version 0.1 because it requires additional grouping rules and tests for only a modest diagnostic-quality improvement in this academic prototype.
- Grouping an entire malformed run was rejected because it is harder to define locally and risks consuming unrelated bytes.
- Zero-width or unknown-column treatment was rejected because later human-readable positions must remain deterministic.
- Platform-dependent replacement-character width was rejected because source positions must not depend on a terminal, font, or external width library.

## Validation

Fixtures must cover at least:

- an isolated continuation byte;
- an invalid leading byte followed by ASCII;
- a truncated two-, three-, and four-byte prefix at EOF;
- a bad continuation followed by a valid ASCII character;
- an overlong encoding;
- an encoding of a surrogate code point;
- an encoding above `U+10FFFF`;
- consecutive invalid bytes followed by a valid multibyte scalar; and
- enough invalid bytes to exercise the twenty-diagnostic limit and continued scanning afterward.

