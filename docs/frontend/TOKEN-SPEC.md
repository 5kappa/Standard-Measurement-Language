# Standard Measurement Language Token Specification

Status: accepted  
Applies to: Standard Measurement Language (SML) version 0.1 lexer and token fixtures

## Purpose

This document translates the lexical rules in [`LANGUAGE-SPECIFICATION.md`](../../LANGUAGE-SPECIFICATION.md) into one implementation-facing contract. Source locations follow [`SOURCE-LOCATIONS.md`](SOURCE-LOCATIONS.md).

## Token model

Every emitted token contains:

~~~text
Token
    kind: TokenKind
    lexeme: original source text
    span: SourceSpan
~~~

The lexeme is decoded from exactly the token's original half-open UTF-8 byte span. Keywords, operators, and delimiters retain their source spelling.

Token adjacency is derived from spans:

~~~text
previous.span.end_byte == current.span.start_byte
~~~

The parser uses adjacency for quantity literals. Tokens contain no unit-registry or semantic classification.

## Scanning contract

The lexer scans the original UTF-8 source from beginning to end:

1. Preserve original bytes and calculate locations using `SOURCE-LOCATIONS.md`.
2. Decode a complete well-formed UTF-8 scalar value when possible; otherwise report and consume exactly the current invalid byte before continuing.
3. Skip whitespace and comments while retaining their effects on locations and adjacency.
4. Scan identifiers completely, then classify exact reserved spellings.
5. Scan numeric candidates using the decimal and malformed-number rules below.
6. Scan strings.
7. Recognize comments and operators by maximal munch.
8. Recognize single-character delimiters.
9. Report any remaining character as a lexical error.
10. Emit exactly one `EOF` token at the physical end of the source.

Recognition never depends on whether a name denotes a registered unit, declared value, function, or dimension.

The lexer continues after a lexical failure by consuming the complete malformed candidate or smallest invalid source range assigned to that diagnostic. It may therefore report multiple independent lexical errors in one source file and must still reach the physical end and emit `EOF`. A lexing result succeeds only when it contains no lexical diagnostics; only a successful result may be passed to the parser.

## Value and name tokens

| Kind | Recognition | Notes |
| --- | --- | --- |
| `NUMBER` | `(0|[1-9][0-9]*)(\.[0-9]+)?` | Signs are separate tokens. |
| `STRING` | Complete double-quoted, single-line string | No escapes or multiline strings. |
| `IDENT` | `[A-Za-z][A-Za-z0-9_]*` not matching a reserved spelling | Case-sensitive. |
| `TRUE` | Exact identifier lexeme `true` | Boolean literal. |
| `FALSE` | Exact identifier lexeme `false` | Boolean literal. |

An underscore cannot begin an identifier. Consecutive and trailing underscores are permitted after the first ASCII letter.

Unit spellings use `IDENT`. For example, `m`, `kg`, `kN`, and `foo` have the same lexical category. The lexer does not split prefixes or consult a unit registry.

## Reserved identifier spellings

The lexer first scans the complete identifier lexeme, then performs an exact case-sensitive lookup.

| Lexemes | Token kinds |
| --- | --- |
| `let const fn return` | `LET CONST FN RETURN` |
| `if else for while break continue` | `IF ELSE FOR WHILE BREAK CONTINUE` |
| `print input assert as` | `PRINT INPUT ASSERT AS` |
| `int float bool text` | `INT FLOAT BOOL TEXT` |
| `Length Mass Time Force` | `LENGTH MASS TIME FORCE` |
| `to then do` | `TO THEN DO` |
| `true false` | `TRUE FALSE` |

`to`, `then`, and `do` are reserved noise words. `main` is an ordinary `IDENT`. Case variants such as `Let`, `length`, and `TRUE` remain `IDENT`.

The words `rate`, `Money`, `Temperature`, `Scalar`, `unit`, and `dimension` are not reserved in version 0.1.

## Numeric candidates

Accepted numbers are unsigned decimal integers and fixed-point decimals:

~~~regex
(0|[1-9][0-9]*)(\.[0-9]+)?
~~~

Accepted examples are `0`, `5`, `125`, `5.0`, `0.5`, and `123.456`.

Leading `+` and `-` are separate operator tokens:

~~~text
-5m -> MINUS NUMBER("5") IDENT("m") EOF
~~~

### Malformed decimal forms

These are lexical errors rather than shorter successful tokens:

- a leading zero followed by another digit: `00`, `0123`, `01.5`;
- a decimal point without a following digit: `5.`;
- a leading decimal point: `.5`; and
- an underscore used as a numeric separator: `1_000`.

Numeric literals have no separator or grouping characters. In particular, `_` and `,` are never part of a `NUMBER`. A comma remains a `COMMA` token only where the grammar permits a list separator, so `1,000` is not one numeric literal and is rejected when used as one.

A malformed numeric candidate is not decomposed merely to avoid reporting the lexical error.

The lexer consumes the longest recognizable malformed numeric candidate and stops before source text that clearly begins a separate ordinary token. `DIAGNOSTICS.md` fixes the ambiguous candidate boundaries, and `RECOVERY.md` fixes the resulting partial-token behavior.

### Unsupported numeric notations

Version 0.1 does not support scientific notation or alternate number systems, including hexadecimal and binary. Recognizable forms are reserved as malformed numeric candidates:

~~~text
2.5e3   1E6   3e-2   4E+9
0x10    0XFF
0b1010  0B11
~~~

The lexer reports one malformed-number error for the complete numeric-looking candidate. It must not reinterpret these examples as `NUMBER("2.5") IDENT("e3")` or `NUMBER("0") IDENT("x10")`.

The exponent rule applies when an accepted decimal prefix is immediately followed by `e` or `E` and then a decimal digit or sign. The base-prefix rule applies when `0` is immediately followed by `x`, `X`, `b`, or `B`.

These are explicit lexical exceptions to the general `NUMBER IDENT` boundary. Ordinary attached identifiers remain valid:

~~~text
10foo -> NUMBER("10") IDENT("foo") EOF
12kN  -> NUMBER("12") IDENT("kN") EOF
5e    -> NUMBER("5") IDENT("e") EOF
~~~

Exact diagnostic codes and the accepted ambiguous-candidate spans are defined in `DIAGNOSTICS.md`; general post-error continuation belongs in `RECOVERY.md`. Token fixtures must treat unsupported numeric forms as lexical failures.

As specified by `RECOVERY.md`, a successful lexical result exposes its complete token list. A failed result exposes valid tokens outside malformed ranges as a partial token list ending in physical `EOF`; that list exists for lexer fixtures and debugging and must never be passed to the parser.

## Strings

A string begins and ends with `"`. Its contents may contain canonical ASCII characters other than `"`, `CR`, or `LF`.

Version 0.1 has no escape sequences, multiline strings, or implicit concatenation. The `STRING` lexeme includes both quotes. An unclosed string is a lexical error at the line ending or EOF. Its primary span stops before a terminating newline. Backslash has no escape behavior and is outside the canonical character set. Invalid source characters are diagnosed even inside a string; if a later closing quote is present, that character error does not also make the string unclosed.

## Whitespace and comments

Whitespace consists of space, horizontal tab, `CR`, and `LF`. It is skipped.

Line comments begin with `//` and end before the next `CR`, `LF`, or EOF. Block comments begin with `/*` and end at the first following `*/`. Block comments may cross lines and do not nest. Reaching EOF before `*/` is a lexical error.

The canonical-character rules apply inside comments. An unterminated block-comment diagnostic labels the opening `/*` as its primary cause and uses the zero-width `EOF` location as a secondary label showing where scanning stopped.

Comments are not emitted as grammar tokens and behave like whitespace:

~~~text
10m          -> adjacent NUMBER IDENT
10 m         -> non-adjacent NUMBER IDENT
10/*x*/m     -> non-adjacent NUMBER IDENT
~~~

The slash prefix is resolved in this order: `//`, `/*`, `/=`, then `/`.

## Operators

The lexer emits the longest valid operator at the current position.

| Lexeme | Kind | Lexeme | Kind |
| --- | --- | --- | --- |
| `+` | `PLUS` | `++` | `PLUS_PLUS` |
| `-` | `MINUS` | `--` | `MINUS_MINUS` |
| `*` | `STAR` | `/` | `SLASH` |
| `%` | `PERCENT` | `^` | `CARET` |
| `!` | `BANG` | `=` | `ASSIGN` |
| `+=` | `PLUS_ASSIGN` | `-=` | `MINUS_ASSIGN` |
| `*=` | `STAR_ASSIGN` | `/=` | `SLASH_ASSIGN` |
| `<` | `LESS` | `<=` | `LESS_EQUAL` |
| `>` | `GREATER` | `>=` | `GREATER_EQUAL` |
| `==` | `EQUAL_EQUAL` | `!=` | `BANG_EQUAL` |
| `&&` | `AND_AND` | `||` | `OR_OR` |

A lone `&` or `|` is a lexical error.

Maximal-munch examples:

~~~text
--5  -> MINUS_MINUS NUMBER("5") EOF
++x  -> PLUS_PLUS IDENT("x") EOF
a<=b -> IDENT("a") LESS_EQUAL IDENT("b") EOF
~~~

The parser decides whether the resulting tokens are valid in context. `MINUS_MINUS` is not reinterpreted as two unary `MINUS` tokens.

## Delimiters

| Lexeme | Kind |
| --- | --- |
| `(` `)` | `LPAREN RPAREN` |
| `{` `}` | `LBRACE RBRACE` |
| `[` `]` | `LBRACKET RBRACKET` |
| `;` | `SEMICOLON` |
| `:` | `COLON` |
| `,` | `COMMA` |

A standalone `.` is not a token; it is valid only inside `NUMBER`. An underscore is valid only after the first letter of `IDENT`. Other uses are lexical errors.

## End of file

The lexer emits exactly one `EOF` token:

~~~text
kind:   EOF
lexeme: ""
span:   [source_byte_length, source_byte_length)
~~~

Trailing trivia precedes this position and does not change the zero-width EOF location.

## Complete token inventory

~~~text
NUMBER STRING IDENT
TRUE FALSE

LET CONST FN RETURN
IF ELSE FOR WHILE BREAK CONTINUE
PRINT INPUT ASSERT AS
INT FLOAT BOOL TEXT
LENGTH MASS TIME FORCE
TO THEN DO

PLUS MINUS STAR SLASH PERCENT CARET BANG
PLUS_PLUS MINUS_MINUS
ASSIGN PLUS_ASSIGN MINUS_ASSIGN STAR_ASSIGN SLASH_ASSIGN
LESS LESS_EQUAL GREATER GREATER_EQUAL EQUAL_EQUAL BANG_EQUAL
AND_AND OR_OR
LPAREN RPAREN LBRACE RBRACE LBRACKET RBRACKET
SEMICOLON COLON COMMA EOF
~~~

Version 0.1 has no `UNIT`, unit-prefix, `DOT`, signed-number, hexadecimal-number, binary-number, or scientific-number token.

## Minimum conformance fixtures

Fixtures must cover:

- every token kind and reserved spelling;
- case-sensitive keyword near misses;
- identifiers containing digits and underscores;
- every accepted and malformed numeric category;
- `2.5e3`, `0x10`, and `0b1010` as lexical errors;
- signs as separate tokens;
- every maximal-munch boundary and lone `&`/`|` errors;
- complete and unterminated strings and comments;
- non-nesting block-comment behavior;
- whitespace and comment effects on adjacency;
- canonical and invalid source characters;
- exact lexemes and byte spans; and
- zero-width `EOF`.

## Acceptance rule

An implementation conforms only when it produces the token kinds, original lexemes, spans, adjacency outcomes, and lexical failures required here. Tokenization changes require deliberate amendments here and, when the language surface changes, in `LANGUAGE-SPECIFICATION.md`.
