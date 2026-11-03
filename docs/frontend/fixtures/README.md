# Standard Measurement Language Machine-Readable Fixture Format

Status: accepted  
Format version: 1  
Language version: 0.1  
Applies to: Standard Measurement Language lexer and parser conformance fixtures  
Depends on: [`TOKEN-SPEC.md`](../TOKEN-SPEC.md), [`SOURCE-LOCATIONS.md`](../SOURCE-LOCATIONS.md), [`AST-SCHEMA.md`](../AST-SCHEMA.md), [`DIAGNOSTICS.md`](../DIAGNOSTICS.md), [`RECOVERY.md`](../RECOVERY.md), and [decision 087](../../../decisions/087-machine-readable-fixture-format.md)

## Purpose

This document defines the JSON data exchanged between the version 0.1 frontend specification and conforming test harnesses. It does not change SML source syntax or require the SML frontend itself to parse JSON.

The format is designed for independent implementations. A harness must reject malformed fixture data rather than silently ignoring fields or inferring an unstated expectation.

## Suite layout

Fixtures are stored in moderately sized files grouped by their principal concern:

```text
fixtures/
    README.md
    index.json
    lexer/
        tokens.json
        numbers.json
        strings-comments.json
        lexical-failures.json
        continuation.json
    parser/
        expressions.json
        units.json
        declarations.json
        statements.json
        functions.json
        syntax-failures.json
    locations/
        source-locations.json
    frontend/
        phase-gating.json
        diagnostic-limit.json
```

The exact category boundaries may be refined as cases are added. Moving a fixture must not change its ID or behavior.

`index.json` is the authoritative file list:

```json
{
  "format_version": 1,
  "language_version": "0.1",
  "fixture_files": [
    "lexer/tokens.json",
    "parser/expressions.json",
    "frontend/phase-gating.json"
  ]
}
```

Paths are relative to the directory containing `index.json`, use `/` separators, remain within the fixture directory, and appear exactly once. Their array order gives deterministic loading and reporting order but does not create dependencies between fixtures.

Every listed fixture file has this envelope:

```json
{
  "format_version": 1,
  "language_version": "0.1",
  "fixtures": []
}
```

Only format version `1` and language version `0.1` are currently accepted. The fixture format and language version are independent: either may change without necessarily changing the other.

## JSON rules

- Fixture files are valid JSON encoded as UTF-8 without a byte-order mark.
- JSON comments and trailing commas are not permitted.
- Object-member order is not significant.
- Array order is significant.
- Numeric format fields, byte offsets, counts, and token indices are nonnegative JSON integers unless a field explicitly permits a signed value.
- Unknown fields are errors.
- Duplicate JSON object keys are errors.
- A loader must validate the complete fixture before using it as a conformance case.

Descriptions and source-control formatting are non-normative. IDs, source bytes, expected results, array order, and coverage identifiers are normative fixture data.

## Fixture record

Every fixture has exactly these top-level fields:

```text
Fixture
    id: string
    description: string
    entrypoint: LEXER | FRONTEND
    source: SourceInput
    expected: LexerExpectation | FrontendExpectation
    covers: Coverage
```

Example:

```json
{
  "id": "frontend-number-scientific-before-ident",
  "description": "The malformed exponent candidate ends before a following identifier.",
  "entrypoint": "frontend",
  "source": {
    "kind": "utf8",
    "text": "2.5e3foo"
  },
  "expected": {},
  "covers": {
    "token_kinds": ["IDENT", "EOF"],
    "ast_kinds": [],
    "diagnostic_codes": ["LEX006"],
    "rules": [
      "DIAGNOSTICS.malformed-numeric-boundaries",
      "RECOVERY.numeric-failures",
      "RECOVERY.parser-phase-gate"
    ]
  }
}
```

The abbreviated empty `expected` object above illustrates record placement only and is not itself valid fixture data.

### Fixture IDs

An ID:

- is globally unique across every indexed file;
- contains only lowercase ASCII letters, decimal digits, and hyphens;
- begins with a lowercase letter;
- uses a descriptive phase or subject prefix such as `lex-`, `parse-`, or `frontend-`;
- remains unchanged when its file or description changes; and
- is treated as an opaque address rather than parsed to determine behavior.

The accepted pattern is:

```text
[a-z][a-z0-9]*(?:-[a-z0-9]+)*
```

`description` is a nonempty human explanation. It is not compared with frontend output and may be clarified without changing fixture identity.

## Source input

`source` is exactly one tagged variant.

### UTF-8 text

```json
{
  "kind": "utf8",
  "text": "fn main() {\r\n    print(10m);\r\n}"
}
```

The decoded JSON string is encoded as UTF-8 without a byte-order mark and passed to the lexer unchanged. JSON escape sequences therefore distinguish `LF`, `CR`, and `CRLF`. No newline, Unicode, or source normalization occurs after JSON decoding.

### Arbitrary source bytes

```json
{
  "kind": "bytes_hex",
  "hex": "6c657420ff783b"
}
```

`hex` contains an even, possibly zero, number of lowercase hexadecimal digits with exactly two digits per byte and no spaces, prefix, or separators. This variant is required for invalid UTF-8. It may also be used when a fixture needs byte spelling to be visually explicit.

The two source variants have no other fields.

## Entry points and phase expectations

`entrypoint` determines which public contract is invoked.

### Lexer entry point

A `lexer` fixture runs only the lexer:

```text
LexerExpectation
    lex: LexSuccess | LexFailure
```

Its `expected` object contains exactly `lex` and must not contain `parse`. Parser behavior is outside that fixture's assertion.

### Frontend entry point

A `frontend` fixture begins from source bytes and applies the phase gate:

```text
FrontendExpectation
    lex: LexSuccess | LexFailure
    parse: ParseSuccess | ParseFailure | ParseNotRun
```

The valid combinations are:

| Lex result | Parse result |
| --- | --- |
| `success` | `success` or `failure` |
| `failure` | `not_run` with reason `lexical_failure` |

No other combination is valid.

Raw parser entry points and hand-authored input token streams are outside the normative fixture format. Implementation-specific parser unit tests may use them, but conformance fixtures begin from source bytes.

## Lexical expectations

### Success

```json
{
  "status": "success",
  "tokens": []
}
```

`tokens` is the complete ordered token collection and ends with exactly one physical-end `EOF` token.

### Failure

```json
{
  "status": "failure",
  "partial_tokens": [],
  "diagnostics": [],
  "diagnostics_truncated": false
}
```

`partial_tokens` contains every valid token outside malformed ranges, in source order, and ends with exactly one physical-end `EOF`. `diagnostics` contains between one and twenty ordered lexical diagnostics. `diagnostics_truncated` follows `RECOVERY.md`: it is true exactly when one or more additional diagnostic records were suppressed.

The failure variant is not specialized by cause. Each diagnostic in the array has phase `LEXER` and a code from `LEX001` through `LEX010`; one array may contain different codes. The code and its stable `data` record are the machine-readable failure classification.

A success has no diagnostics or truncation field. A failure has no `tokens` field.

## Tokens

Every expected token has exactly these required fields and one optional location assertion:

```text
ExpectedToken
    kind: TokenKind
    lexeme: string
    span: SourceSpan
    positions: PositionRange?
```

Example:

```json
{
  "kind": "NUMBER",
  "lexeme": "10",
  "span": {
    "start_byte": 0,
    "end_byte": 2
  }
}
```

`kind` is one exact token kind from `TOKEN-SPEC.md`. `lexeme` is decoded from exactly the original token bytes. A non-`EOF` token has a nonempty span. `EOF` has an empty lexeme and span `[source_byte_length, source_byte_length)`.

Adjacency is not stored separately. A harness derives it from adjacent token spans as required by `SOURCE-LOCATIONS.md`.

## Source spans and positions

Every `SourceSpan` is:

```json
{
  "start_byte": 0,
  "end_byte": 4
}
```

It must satisfy:

```text
0 <= start_byte <= end_byte <= source_byte_length
```

Position assertions supplement rather than replace byte spans:

```json
{
  "start": {
    "byte_offset": 5,
    "line": 2,
    "column": 5
  },
  "end": {
    "byte_offset": 6,
    "line": 2,
    "column": 6
  }
}
```

Byte offsets are zero-based; lines and display columns are one-based. The position byte offsets must equal the corresponding span boundaries. In a dedicated fixture involving newlines, tabs, invalid non-ASCII characters, or invalid UTF-8, `positions` is required on every expected token and diagnostic label in that fixture. A diagnostic using a zero-width location must include `positions` on that label. AST nodes remain byte-span assertions unless the fixture deliberately includes their optional `positions`. Position assertions are permitted but not required in other fixtures.

## Parse expectations

### Success

```json
{
  "status": "success",
  "ast": {}
}
```

The AST follows the JSON mapping below. This variant has no diagnostic.

### Failure

```json
{
  "status": "failure",
  "diagnostic": {}
}
```

The diagnostic is exactly the first syntax diagnostic. This variant has no AST.

### Not run

```json
{
  "status": "not_run",
  "reason": "lexical_failure"
}
```

This variant is valid only in a `frontend` fixture whose lexical result is `failure`. It proves phase gating rather than merely omitting a parse assertion.

## AST mapping

An expected successful AST maps `AST-SCHEMA.md` into JSON as follows:

- every tagged record variant has a `kind` equal to its schema node name;
- schema field names are retained;
- every AST node contains its required `span` and may contain `positions` for a location assertion;
- an absent optional field is present with JSON `null`;
- every repeated field is present as an array, including when empty;
- nonempty collections contain at least one item;
- array order preserves source and schema order; and
- every retained `TokenRef` becomes a `FixtureTokenRef`.

```text
FixtureTokenRef
    token_index: nonnegative integer
```

Example:

```json
{
  "operator": {
    "token_index": 3
  }
}
```

The zero-based index refers to the `tokens` array of the same fixture's successful lexical result. It must not refer to `EOF` unless the AST schema explicitly permits that reference. The referenced token supplies the unchanged kind, lexeme, and span required by `TokenRef`.

AST fixtures do not duplicate complete tokens inside nodes, assign string handles to tokens, or find tokens by span. A parse success is therefore valid only after lexical success in the same `frontend` fixture.

## Diagnostic mapping

Diagnostics use the structured contract from `DIAGNOSTICS.md`:

```json
{
  "code": "LEX006",
  "phase": "LEXER",
  "severity": "ERROR",
  "primary": {
    "role": "PRIMARY",
    "span": {
      "start_byte": 0,
      "end_byte": 5
    }
  },
  "secondary": [],
  "notes": [],
  "data": {
    "candidate_lexeme": "2.5e3"
  }
}
```

Every source diagnostic has one `primary` label. A label contains exactly `role`, `span`, and optional `positions`. Secondary labels are ordered. Version 0.1 defines no structured note roles, so `notes` is always `[]`. `data` is always present, including as `{}` for a code with no required stable data. A label may have `positions` under the source-position rules above.

The byte-valued `invalid_bytes` and `character_bytes` diagnostic-data fields use the same canonical lowercase hexadecimal spelling as `SourceInput.bytes_hex`, but without a surrounding source-variant object. Under decision 088, `LEX001.invalid_bytes` is exactly two hexadecimal digits because each diagnostic owns one byte. `LEX002.character_bytes` contains the complete UTF-8 encoding of its one valid scalar value and may therefore contain multiple byte pairs. Other diagnostic-data fields use the strings, integers, booleans, or arrays specified by `DIAGNOSTICS.md`.

Rendered titles, sentences, hints, and correction wording are not fixture fields and must not be compared for conformance.

## Coverage metadata

Every fixture has:

```text
Coverage
    token_kinds: List<TokenKind>
    ast_kinds: List<AstKind>
    diagnostic_codes: List<DiagnosticCode>
    rules: List<RuleId>
```

Example:

```json
{
  "token_kinds": ["IDENT", "EOF"],
  "ast_kinds": [],
  "diagnostic_codes": ["LEX006"],
  "rules": [
    "DIAGNOSTICS.malformed-numeric-boundaries",
    "RECOVERY.numeric-failures"
  ]
}
```

Values within each array are unique. Token kinds, AST kinds, and diagnostic codes must be defined by the accepted contracts and must occur in or be directly exercised by the fixture. Rule IDs use `DOCUMENT.rule-name`, where `DOCUMENT` is the uppercase filename stem and `rule-name` is a stable lowercase-hyphenated identifier. Rule names do not change merely because a Markdown heading is reworded. `TRACEABILITY.md` will become their registry and reverse index.

Coverage metadata supports completeness checks and fixture selection. It does not replace or modify the expected result.

## Strict validation

Before running a fixture, a loader must reject:

- invalid JSON, duplicate object keys, or an unsupported format or language version;
- an unindexed file, missing indexed file, duplicate path, absolute path, or path escaping the fixture directory;
- an unknown or missing field;
- a duplicate or malformed fixture ID;
- an invalid source variant or malformed hexadecimal bytes;
- an entry-point/result mismatch;
- an invalid lexical/parse result combination;
- an invalid span or position range;
- a missing, misplaced, or duplicated physical `EOF`;
- diagnostics with wrong phase, ordering, count, or truncation shape;
- a parse result other than `not_run` after lexical failure;
- `not_run` after lexical success;
- an AST after any failure;
- an out-of-range or schema-invalid AST token index;
- an omitted AST optional or repeated field;
- an unknown token, AST, diagnostic, or coverage identifier; or
- duplicate values inside a coverage array.

Strict fixture validation is test-harness work, not lexer or parser behavior. A conforming implementation may use ordinary code rather than a JSON Schema validator.

## Optional JSON Schema

A future `fixture.schema.json` may provide editor completion and preflight validation. It is an aid, not a required runtime dependency. If it conflicts with this document, this document and the accepted frontend contracts control until the conflict is deliberately resolved.

## Pilot fixture gate (completed)

Before the full suite was populated, a small pilot was required to demonstrate all format mechanisms:

- lexer success with a complete token stream and physical `EOF`;
- lexer failure with diagnostics, valid partial tokens, and frontend parser `not_run`;
- bytewise invalid UTF-8 using `bytes_hex`, including exact diagnostic spans and display-column advancement;
- parse success with an AST that uses `token_index` references, explicit nulls, arrays, and node spans;
- parse failure with exactly one syntax diagnostic and no AST;
- a source-location case with required line and display-column assertions; and
- coverage arrays naming tokens, AST nodes, diagnostics, and specification rules.

The pilot alone was not sufficient for acceptance. The subsequent fixture population and coverage audit satisfied every minimum-fixture section in the accepted frontend documents.

### Current pilot set

The version 1 pilot is structurally accepted and indexed by [`index.json`](index.json):

| Fixture ID | Principal mechanism |
| --- | --- |
| `lex-pilot-attached-quantity-tokens` | Lexer success, complete adjacent token stream, and physical `EOF` |
| `frontend-pilot-invalid-utf8-phase-gate` | `bytes_hex`, bytewise lexical failure, valid partial tokens, exact positions across a newline, and parser `not_run` |
| `frontend-pilot-uninitialized-let-ast` | Parse success with token references, explicit nulls, ordered arrays, and complete node spans |
| `frontend-pilot-const-initializer-required` | Parse failure with one structured syntax diagnostic and no AST |

These fixtures establish the representation and expected behavior before implementation. Their JSON, index relationships, IDs, spans, locations, token references, coverage identifiers, phase combinations, and duplicate-key absence have been audited. Executing them against the frontend remains pending because lexer and parser code do not yet exist.

## Complete version 0.1 suite

The documentation-hardening suite contains 93 fixtures across eight files listed by [`index.json`](index.json). Its completed static audit covers:

- all 62 token kinds and reserved spellings;
- all 53 tagged source-AST node kinds;
- `LEX001` through `LEX010`;
- all 28 active `SYN` codes (`SYN001` is intentionally unused);
- every malformed-number boundary, lexical-continuation family, diagnostic-limit boundary, and parser phase-gating rule;
- successful functions, declarations, annotations, statements, control flow, expression precedence, quantities, conversions, and unit structures;
- every required source-location boundary; and
- all 112 traceability rules through fixture evidence or an explicit process-level `N/A` rationale.

Static validation does not claim that an implementation already passes. Once the frontend exists, its fixture loader and conformance tests must execute these same expectations without weakening them.

## Acceptance rule

A fixture suite does not conform if its meaning depends on JSON object order, host-language types, rendered diagnostic wording, inferred absent fields, external unit registries, semantic checking, parser execution after lexical failure, synthetic or error tokens, recovered ASTs, or behavior not present in the accepted frontend contracts.

