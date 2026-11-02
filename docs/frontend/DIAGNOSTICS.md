# Standard Measurement Language Diagnostic Contract

Status: accepted  
Applies to: Standard Measurement Language (SML) version 0.1 lexer, parser, diagnostic fixtures, and renderers  
Depends on: [`TOKEN-SPEC.md`](TOKEN-SPEC.md), [`GRAMMAR.ebnf`](GRAMMAR.ebnf), [`SOURCE-LOCATIONS.md`](SOURCE-LOCATIONS.md), [`AST-SCHEMA.md`](AST-SCHEMA.md), and [decision 086](../../decisions/086-diagnostic-and-failure-policy.md)

## Purpose

This document defines the stable lexical and syntactic diagnostic interface. It fixes diagnostic codes, phase ownership, severity, source-label requirements, ordering, limits, and parser failure behavior. Exact English rendering is deliberately non-normative.

The current frontend reports malformed source syntax only. It does not diagnose unknown units, undefined functions, argument mismatch, dimensional incompatibility, invalid conversions, update-target mutability or dimensionality, Boolean condition types, or runtime behavior.

## Diagnostic data model

```text
Diagnostic
    code: DiagnosticCode
    phase: LEXER | PARSER | INTERNAL
    severity: ERROR
    primary: DiagnosticLabel?             // required for LEX and SYN
    secondary: List<DiagnosticLabel>
    notes: List<DiagnosticNote>
    data: DiagnosticData

DiagnosticLabel
    span: SourceSpan
    role: PRIMARY
          | encountered_instead
          | opened_here
          | magnitude
          | detached_unit
          | reached_eof
          | insufficient_annotation
          | limit_started_here

DiagnosticNote
    role: stable note-role identifier
```

All source spans follow `SOURCE-LOCATIONS.md`. Label and note text may be derived from their stable roles by a renderer and is not part of conformance. A renderer may also add non-normative correction wording without changing the diagnostic record.

Every source diagnostic has exactly one label with role `PRIMARY`. Required secondary labels remain in the order named by this document. The structured version 0.1 diagnostic record permits only the label roles above and requires no note roles; its `notes` collection is therefore empty. A renderer may show additional explanatory prose, but that prose is not structured diagnostic data. Version 0.1 defines only `ERROR` severity; it has no lexer or parser warnings.

Internal failures are not source diagnostics. `ICE001` may omit a source label when no trustworthy source location exists.

### Stable diagnostic data

`DiagnosticData` is a code-specific record containing values required to understand or test the diagnostic without parsing its English rendering. Codes without entries below use an empty record.

| Codes | Required stable data |
| --- | --- |
| `LEX001` | `invalid_bytes` |
| `LEX002` | `character_bytes` |
| `LEX003` through `LEX007` | `candidate_lexeme` |
| `LEX008` | `termination: CR | LF | CRLF | EOF` |
| `LEX010` | `operator_lexeme` |
| `SYN002` | ordered nonempty `expected_kinds`, plus `actual_kind` |
| `SYN003` | `actual_kind` |
| `SYN004` | `actual_kind` |
| `SYN005` | `actual_kind` |
| `SYN006` | `actual_kind` |
| `SYN018`, `SYN019` | `operator_kind` |
| `SYN020` | `noise_word_kind`, `allowed_context` |
| `SYN033` | `exponent_lexeme` |
| `SYN034` | `source_exponent`, `minimum: -16`, `maximum: 16` |
| `SYN035` | `reason` |
| `SYN036` | `factor_count: 9`, `maximum: 8` |
| `SYN037` | `content_length`, `maximum: 128` |

`actual_kind` is `EOF` when failure occurs at physical EOF. `SYN002.expected_kinds` follows the token-inventory order in `TOKEN-SPEC.md`. The accepted `SYN020.allowed_context` values are `AFTER_AS`, `AFTER_IF_CONDITION`, and `AFTER_LOOP_HEADER`. The accepted `SYN035.reason` values are `REPEATED_DIVISION`, `NESTED_DIVISION`, `GROUPED_NUMERATOR`, `GROUP_POWER`, `IMPLICIT_MULTIPLICATION`, `NUMERIC_FACTOR`, and `UNPARENTHESIZED_PRODUCT_DENOMINATOR`.

## Result and phase policy

```text
LexResult
    Success
        tokens: List<Token>

    | Failure
        partial_tokens: List<Token>
        diagnostics: List<Diagnostic>    // one through twenty
        diagnostics_truncated: boolean

ParseResult
    Success(SourceFile)
    | Failure(Diagnostic)                // exactly one diagnostic, no AST
```

`RECOVERY.md` defines the exact token treatment during a failed lexical scan. In summary:

- the lexer continues after lexical failures;
- it consumes a nonempty malformed range for every lexical error;
- it reaches physical EOF;
- a failure exposes valid tokens outside malformed ranges as `partial_tokens`, ending in `EOF`;
- partial tokens are never passed to the parser;
- it produces at most twenty lexical diagnostic records;
- `diagnostics_truncated` is true exactly when additional lexical failures were suppressed; and
- the parser is invoked only for `LexResult.Success(tokens)`.

`LexResult.Failure` is one overall failed-scan variant, not one variant per error category. Its `diagnostics` collection classifies the individual causes: every record has phase `LEXER` and one code from `LEX001` through `LEX010`, and different codes may coexist in one result. Code-specific `DiagnosticData` supplies the stable details. Malformed source is returned as `Failure`; it is not an internal exception. File I/O failures occur outside the lexer, and implementation invariant failures must not be disguised as lexical diagnostics.

The parser stops at its first syntax error. It emits one diagnostic, returns no AST, performs no synchronization, skips no parser tokens for recovery, and synthesizes no tokens or AST nodes.

## Diagnostic ordering and limit

Lexical diagnostics are ordered by:

1. `primary.span.start_byte` ascending;
2. `primary.span.end_byte` ascending; and
3. diagnostic code ascending.

The lexer stores at most twenty diagnostics. After the twentieth record, it continues consuming and scanning source so that progress and physical-EOF behavior remain deterministic, but suppresses additional diagnostic records and sets `diagnostics_truncated` to true. The cap limits output and memory; the nonempty-consumption rule, not the cap, guarantees termination.

Parser ordering is trivial because a parse produces at most one diagnostic.

## General label rules

### Unexpected existing source

When an existing token or character is invalid, the primary label covers that source element's real span.

### Expected absent syntax

When required syntax is absent, the primary label is zero-width at the position where it was expected. At EOF this is `[source_byte_length, source_byte_length)`. The location is diagnostic data, not a synthetic token.

If an existing non-EOF token demonstrates the omission, it receives the secondary role `encountered_instead`.

### Expressions and delimiters

A missing operand at EOF uses the zero-width EOF location. A token that cannot begin the required operand is labeled with its real span. A missing closing delimiter uses a zero-width primary location and labels the corresponding opening delimiter secondarily with role `opened_here`.

### Detached quantities

For a detached simple or compound quantity, the primary label covers the separating bytes between the `NUMBER` and `IDENT` or `LBRACKET`. The magnitude and attempted unit-start tokens receive secondary roles `magnitude` and `detached_unit`.

### Limits

When a count or length limit is exceeded, the primary label covers the first source element beyond the accepted limit. The first contributing factor or opening bracket receives secondary role `limit_started_here`.

## Lexical diagnostic codes

| Code | Stable name | Required primary label |
| --- | --- | --- |
| `LEX001` | `INVALID_UTF8` | Exactly one byte at which no complete well-formed UTF-8 scalar value begins. |
| `LEX002` | `INVALID_SOURCE_CHARACTER` | Complete UTF-8 byte span of the invalid character. |
| `LEX003` | `LEADING_ZERO` | Complete malformed numeric candidate. |
| `LEX004` | `MALFORMED_DECIMAL` | Complete malformed decimal candidate, including leading/trailing or repeated decimal points. |
| `LEX005` | `NUMERIC_SEPARATOR` | Complete numeric candidate containing `_`. |
| `LEX006` | `SCIENTIFIC_NOTATION` | Complete recognized scientific-notation candidate. |
| `LEX007` | `ALTERNATE_NUMBER_BASE` | Complete recognized hexadecimal- or binary-looking candidate. |
| `LEX008` | `UNCLOSED_STRING` | From opening quote through the last content byte, excluding a terminating newline. |
| `LEX009` | `UNTERMINATED_BLOCK_COMMENT` | Opening `/*`; secondary `reached_eof` labels zero-width EOF. |
| `LEX010` | `INCOMPLETE_LOGICAL_OPERATOR` | Lone `&` or `|`. |

`LEX002` covers otherwise unknown characters, standalone leading `_`, backslash, and invalid canonical characters inside strings or comments. A standalone `.` or leading-decimal spelling uses `LEX004` rather than `LEX002`.

Each `LEX001` record covers and consumes one byte. Its `invalid_bytes` data therefore contains exactly that byte; fixture JSON writes it as two lowercase hexadecimal digits. A malformed multi-byte sequence may produce multiple ordered `LEX001` diagnostics.

An invalid source character inside an otherwise closed string produces `LEX002` and not `LEX008`. If the same string is also unclosed, both independent lexical conditions may be diagnosed subject to ordering and the twenty-record limit.

## Malformed numeric boundaries

Malformed numeric recognition produces one diagnostic for each complete candidate:

| Source | Code | Primary byte span | Scanning resumes at |
| --- | --- | --- | --- |
| `1__0` | `LEX005` | `[0, 4)` | EOF |
| `0x` | `LEX007` | `[0, 2)` | EOF |
| `0xG` | `LEX007` | `[0, 3)` | EOF |
| `3e+` | `LEX006` | `[0, 3)` | EOF |
| `2.5e3foo` | `LEX006` | `[0, 5)` | `f` at byte 5; `foo` is scanned as `IDENT` |
| `5..2` | `LEX004` | `[0, 4)` | EOF |

These cases refine the general longest-recognizable-malformed-candidate rule in `TOKEN-SPEC.md`. A comma is never part of `NUMBER`; it remains `COMMA` where the grammar permits it. Consequently `1,000` is not one numeric literal, but comma handling does not create a lexical numeric-separator code.

## General syntax diagnostic codes

| Code | Stable name | Use |
| --- | --- | --- |
| `SYN002` | `EXPECTED_TOKEN` | A required delimiter, separator, keyword, operator, or terminator is absent. Expected token kinds are stable diagnostic data. |
| `SYN003` | `EXPECTED_IDENTIFIER` | A required declaration, parameter, function, assignment, update, or unit name is absent. |
| `SYN004` | `EXPECTED_EXPRESSION` | An expression or operand is absent. |
| `SYN005` | `EXPECTED_STATEMENT` | A token cannot begin a statement inside a block. |
| `SYN006` | `EXPECTED_FUNCTION` | A non-`fn` token occurs at source-file level. |

`SYN002` covers missing `(`, `)`, `{`, `}`, `[`, `]`, `:`, `,`, `;`, assignment operators, and required grammar keywords when no specialized code below applies. Missing operands and empty required expression lists use `SYN004`, not `SYN002`.

Whenever a specialized code describes the failure, the parser must emit that code rather than `SYN002` through `SYN006`. Among the general codes, the most specific applicable expected construct wins: identifier, expression, statement, or function before generic `EXPECTED_TOKEN`.

Version 0.1 intentionally has no generic `UNEXPECTED_TOKEN` code. Every parser state names an expected token or construct, or uses a specialized diagnostic. `SYN001` remains unused so the accepted codes do not require cascading renumbering.

## Specialized syntax diagnostic codes

| Code | Stable name | Required primary label |
| --- | --- | --- |
| `SYN010` | `DETACHED_QUANTITY` | Separating whitespace or comment bytes. |
| `SYN011` | `CONST_INITIALIZER_REQUIRED` | Zero-width position after the declaration annotation or name. |
| `SYN012` | `INVALID_DECLARATION_ANNOTATION` | First token that cannot belong to the one permitted annotation category. |
| `SYN013` | `INVALID_INPUT_POSITION` | `input` token outside a complete declaration initializer or simple-assignment value. |
| `SYN014` | `INPUT_ARGUMENTS_NOT_ALLOWED` | First token between `input(` and the required `)`. |
| `SYN015` | `INPUT_ANNOTATION_REQUIRED` | `input` token; declaration annotation, when present, has secondary role `insufficient_annotation`. |
| `SYN016` | `ASSIGNMENT_NOT_EXPRESSION` | Assignment operator used where an expression is required. |
| `SYN017` | `UPDATE_NOT_EXPRESSION` | Prefix or postfix update operator used inside an expression. |
| `SYN018` | `CHAINED_RELATIONAL_OPERATOR` | Second relational operator. |
| `SYN019` | `CHAINED_EQUALITY_OPERATOR` | Second equality operator. |
| `SYN020` | `MISPLACED_NOISE_WORD` | Misplaced `to`, `then`, or `do` token. |
| `SYN021` | `BREAK_OUTSIDE_LOOP` | `break` token. |
| `SYN022` | `CONTINUE_OUTSIDE_LOOP` | `continue` token. |
| `SYN023` | `RETURN_VALUE_REQUIRED` | Semicolon or other token encountered where the annotated function requires a return expression. |
| `SYN024` | `RETURN_VALUE_FORBIDDEN` | First token of the return expression in a function without a return annotation. |

`SYN015` applies to an unannotated declaration initialized by `input()` and to one having only a dimension annotation. Confirming the target of `name = input();` requires later name resolution and is not a parser diagnostic.

Unit-bearing, constant, or nonnumeric targets of syntactically valid prefix or postfix updates are also later checking errors, not `SYN017`. `SYN017` is reserved for expression-valued update syntax such as `print(count++)`.

## Unit-expression diagnostic codes

| Code | Stable name | Required primary label |
| --- | --- | --- |
| `SYN030` | `EMPTY_UNIT_ANNOTATION` | Closing `]` encountered before a unit expression. |
| `SYN031` | `EXPECTED_UNIT_FACTOR` | Zero-width expected position or encountered token after `*`, `/`, or `(`. |
| `SYN032` | `MISSING_UNIT_EXPONENT` | Zero-width position after `^`. |
| `SYN033` | `INVALID_UNIT_EXPONENT` | Explicit `+` or decimal `NUMBER` used as a unit exponent. |
| `SYN034` | `UNIT_EXPONENT_OUT_OF_RANGE` | Complete signed source exponent outside `-16...16`. |
| `SYN035` | `INVALID_UNIT_STRUCTURE` | Token demonstrating repeated/nested division, grouped numerator, group power, implicit multiplication, numeric factor, or unparenthesized multi-factor denominator. |
| `SYN036` | `TOO_MANY_UNIT_FACTORS` | Ninth written unit factor. |
| `SYN037` | `UNIT_ANNOTATION_TOO_LONG` | First content byte beyond the 128-character limit. |

Missing closing `]` or denominator `)` uses `SYN002` with secondary role `opened_here`. An unknown but syntactically valid `IDENT`, including one raised to zero or later cancelled, is not a parser diagnostic.

`SYN035` describes source structure only. The normalized-dimension exponent bound and whether a unit name exists belong to later semantic processing.

## Internal failure code

| Code | Stable name | Use |
| --- | --- | --- |
| `ICE001` | `INTERNAL_FRONTEND_FAILURE` | An invariant failure or unreachable frontend state not caused by malformed SML source. |

An implementation must not convert malformed source into `ICE001`. Internal failures are implementation defects and are not part of ordinary malformed-input conformance fixtures.

## Fixture requirements

Diagnostic fixtures must cover:

- every code in this document except `ICE001`;
- every malformed numeric boundary table row;
- two or more independent lexical errors ordered by source location;
- exactly twenty lexical diagnostics with `diagnostics_truncated == false`;
- more than twenty lexical failures with exactly twenty records and `diagnostics_truncated == true`;
- invalid source characters inside a closed string and inside comments;
- unclosed strings at `CR`, `LF`, `CRLF`, and EOF;
- unterminated block-comment primary and secondary labels;
- detached simple and compound quantities separated by whitespace and comments;
- absent syntax at a real token and at EOF;
- every unit-expression structural and hard-limit boundary;
- invalid input placement and annotation constraints;
- control-transfer context errors;
- phase gating that prevents parser invocation after lexical diagnostics;
- exactly one parser diagnostic for a lexically valid source containing multiple syntax errors; and
- no AST after any syntax diagnostic.

Fixtures compare codes, phases, severity, label roles, spans, note roles, ordering, truncation, phase gating, and AST presence. They do not compare rendered English sentences.

## Acceptance rule

An implementation does not conform if it changes a stable code's meaning, emits a parser diagnostic after lexical failure, emits more than one syntax diagnostic, returns an AST after syntax failure, changes required label spans or roles, exceeds the lexical diagnostic cap, or makes exact English wording part of frontend behavior without deliberately amending this contract.
