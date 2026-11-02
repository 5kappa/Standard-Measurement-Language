# Standard Measurement Language Source-Location Contract

Status: accepted  
Applies to: Standard Measurement Language (SML) version 0.1 lexer, parser, AST, diagnostics, and fixtures

## Purpose

Every token, source AST node, and lexical or syntactic diagnostic must identify the original source text precisely. This contract fixes one location model for all front-end documents and implementations.

## Source preservation

The front end retains the original UTF-8 source bytes for the duration of lexing, parsing, and diagnostic rendering. It must not normalize line endings, tabs, Unicode characters, or other source text before calculating locations.

SML accepts UTF-8 source files and defines an ASCII canonical grammar. A valid UTF-8 character outside that grammar is still located according to this contract before being reported as an invalid source character. At an offset where no complete well-formed UTF-8 scalar value begins, the invalid UTF-8 diagnostic covers exactly the current byte. The lexer then consumes that one byte and resumes at the following byte.

## Byte spans

A source span is a half-open UTF-8 byte range:

```text
[start_byte, end_byte)
```

`start_byte` is included and `end_byte` is excluded. Both are zero-based offsets into the original UTF-8 byte sequence.

Required invariants:

- `0 <= start_byte <= end_byte <= source_byte_length`;
- the byte length of a span is `end_byte - start_byte`;
- two source elements are byte-adjacent when the first element's `end_byte` equals the second element's `start_byte`;
- a zero-width location is represented by `[n, n)`; and
- a span never includes bytes merely to make a diagnostic highlight wider.

For ASCII source `10foo`:

```text
NUMBER("10")  [0, 2)
IDENT("foo")  [2, 5)
EOF           [5, 5)
```

The exclusive end makes token length and adjacency direct arithmetic rather than special cases.

## Human-readable positions

Diagnostics pair byte spans with 1-based line and column positions:

```text
SourcePosition
    byte_offset: zero-based UTF-8 byte offset
    line:        one-based logical line number
    column:      one-based display column
```

The start position refers to the first source byte in the span. The end position refers to the position immediately after the span. A zero-width span has equal start and end positions.

Byte offsets are authoritative for slicing source. Line and column positions are for people and diagnostic rendering.

## Lines and newlines

The following sequences each count as one logical newline:

- line feed (`LF`);
- carriage return (`CR`); and
- carriage return followed by line feed (`CRLF`).

For `CRLF`, both bytes belong to the newline, but the pair advances the position only once. After any logical newline, the next source character begins on the next line at column 1.

The original newline bytes remain unchanged, so later spans still address the original source exactly.

## Columns and tabs

Ordinary ASCII characters advance the display column by one.

A horizontal tab advances to the next four-column tab stop. With one-based columns, the stops are columns 1, 5, 9, 13, and so on. Therefore:

- a tab beginning at column 1 ends at column 5;
- a tab beginning at column 4 ends at column 5; and
- a tab beginning at column 5 ends at column 9.

A valid non-ASCII Unicode scalar value advances the display column by one before the lexer reports that the character is outside SML's canonical grammar. Its UTF-8 byte length may be greater than one, which is why byte offsets and display columns are stored separately.

Each byte diagnosed as invalid UTF-8 also advances the display column by one. This bookkeeping does not decode the byte as a character or insert a replacement character. Because recovery consumes only the current byte, a following ASCII newline or well-formed UTF-8 scalar value retains its ordinary line and column behavior.

## Tokens and trivia

Every emitted token records at least:

```text
Token
    kind
    lexeme
    span
```

The `lexeme` is decoded from exactly the token's original byte span. `EOF` has an empty lexeme and the zero-width span at the end of the source.

Whitespace and comments are not emitted as grammar tokens, but their bytes still affect token spans and human-readable positions. The implementation must retain enough boundary information to determine whether two tokens were adjacent in the original source.

Adjacency is defined only by byte spans:

```text
previous.span.end_byte == current.span.start_byte
```

Consequently:

```sml
10m          // NUMBER and IDENT are adjacent
10 m         // separated by whitespace
10/*note*/m  // separated by a comment
10//note
m            // separated by a comment and newline
```

Only the first form satisfies the simple-quantity adjacency rule. Comments behave like whitespace and cannot preserve attachment.

This contract does not require trivia to be represented as tokens. The later token specification may choose leading-trivia spans or a derived adjacency flag, provided the result is computed from the original byte spans and produces the same observable behavior.

## AST spans

Every source AST node records a span covering the complete source construct represented by that node.

`SourceFile` is the one deliberate whole-source case: its span is `[0, source_byte_length)`, including leading and trailing trivia. This makes an empty file's span equal to its zero-width `EOF` location. Other nodes exclude whitespace or comments that merely surround the construct.

General composition rules:

- a leaf node uses the span of its source token;
- a prefix expression begins at its operator and ends at its operand;
- a postfix expression begins at its operand and ends at its final target;
- a binary expression begins at its left operand and ends at its right operand;
- a parenthesized or bracketed construct includes both delimiters when present;
- a statement span includes its terminating semicolon when the grammar requires one; and
- a block span includes its opening and closing braces when present.

The source AST preserves explicit grouping. Operators, delimiters, keywords, separators, statement terminators, and optional noise words required by `AST-SCHEMA.md` are retained as token references with their original spans. Noise words do not create semantic AST nodes.

## Missing-syntax diagnostic locations

When the parser expects an absent token, its diagnostic uses a zero-width location at the position where the token was expected. It must not borrow the span of the following token.

Example:

```sml
9.8[m/s^2
```

The expected `]` is located at EOF with `[source_byte_length, source_byte_length)`. A diagnostic may label the existing unit annotation separately. The zero-width location identifies an expectation; it is not a synthetic token.

The frontend must distinguish:

- a real token with a non-empty source span;
- a real zero-width `EOF` token; and
- a zero-width diagnostic location for absent syntax.

The version 0.1 parser stops after its first syntax diagnostic and returns no AST. It does not synthesize missing tokens or construct recovered/error nodes. `AST-SCHEMA.md` therefore contains only real token references from successful parses.

## Phase ownership

The lexer calculates token spans and source positions while scanning the original bytes. The parser does not recalculate token locations.

On success, the parser composes token spans into AST spans. On failure, it may calculate a zero-width expected-syntax location for its single diagnostic but does not create a token there. Diagnostic rendering consumes recorded locations without changing them.

## Conformance examples

All location fixtures must assert byte spans. Fixtures involving newlines, tabs, invalid non-ASCII characters, or invalid UTF-8 must also assert line and column positions.

Minimum location fixtures include:

- an empty source and its zero-width `EOF`;
- adjacent `10foo`;
- detached `10 foo`;
- comment-separated `10/*note*/foo`;
- `LF`, `CR`, and `CRLF` line endings;
- a tab before a token and a tab between tokens;
- a disallowed multibyte Unicode character;
- an invalid UTF-8 byte sequence;
- a missing closing delimiter at EOF; and
- a multi-line block comment followed by a token.

## Acceptance rule

Any lexer or parser implementation that reports different byte spans, line numbers, columns, newline behavior, tab behavior, or attachment results does not conform to this contract unless this document and the normative specification are deliberately amended first.
