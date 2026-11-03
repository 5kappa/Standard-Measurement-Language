# 087: Machine-readable fixture format

Status: ACCEPTED FOR THE CURRENT FRONT-END CONFORMANCE SUITE  
Target: Standard Measurement Language version 0.1 lexer and parser fixtures  
Depends on: `docs/frontend/TOKEN-SPEC.md`, `docs/frontend/SOURCE-LOCATIONS.md`, `docs/frontend/AST-SCHEMA.md`, `docs/frontend/DIAGNOSTICS.md`, and `docs/frontend/RECOVERY.md`

## Decision

The version 0.1 conformance suite uses strict JSON format version 1. JSON is a test-data interchange format only; the SML lexer and parser do not parse JSON and do not depend on a JSON library.

Fixtures are divided among moderately sized files grouped by frontend concern. A required `index.json` lists those files in deterministic order. Every fixture is self-contained, has a globally unique descriptive lowercase-hyphenated ID, and declares either a `lexer` or `frontend` entry point.

Source is a tagged variant:

- `utf8` stores readable source text that is encoded as UTF-8 without a byte-order mark; or
- `bytes_hex` stores arbitrary source bytes as canonical lowercase hexadecimal, permitting invalid UTF-8 fixtures.

Results use explicit tagged variants. Lexing produces `success` with complete tokens or `failure` with partial tokens, diagnostics, and the truncation flag. A frontend fixture also records parsing as `success`, `failure`, or `not_run`; `not_run` is permitted only after lexical failure and carries reason `lexical_failure`.

Expected token collections contain complete token records and physical `EOF`. Successful AST expectations use the node kinds and field names in `AST-SCHEMA.md`. A retained `TokenRef` is encoded as a zero-based `token_index` into that fixture's successful lexical token array. Optional AST fields are present with `null`, repeated fields are present as arrays, and every AST node records its byte span.

Byte spans are mandatory wherever the accepted contracts require a source span. Position assertions supplement spans in location-sensitive fixtures involving newlines, tabs, non-ASCII characters, invalid UTF-8, or zero-width locations. Diagnostic fixtures compare structured fields and never rendered English messages.

Every fixture contains non-behavioral `covers` metadata for token kinds, AST kinds, diagnostic codes, and named specification rules. This metadata supports coverage and traceability audits but does not replace the expected result.

Fixtures are trusted, version-controlled conformance data. A test loader validates only enough structure to decode and execute the indexed fixture cases required by the current implementation milestone. Exhaustive rejection of hostile or deliberately corrupted fixture data is not an implementation requirement. JSON object-member order is not significant; array order is significant.

The complete format is defined in `docs/frontend/fixtures/README.md`.

## Rejected alternatives

- YAML and TOML were rejected because they are less universally available and are awkward or dependency-heavy for recursive AST data.
- JSON Lines was rejected because deeply nested AST fixtures would become difficult to review.
- A custom fixture language was rejected because it would require another lexer and parser before the SML frontend exists.
- Host-language test objects were rejected because they would bind conformance data to one implementation language.
- One monolithic file was rejected because it would grow difficult to review; one file per fixture was rejected because it would create excessive file and boilerplate overhead.
- Base64 and decimal byte arrays were rejected in favor of more inspectable hexadecimal source bytes.
- Embedded AST token copies, token string handles, and span-based token lookup were rejected in favor of local token-array indices.
- Rendered diagnostic snapshots were rejected as normative fixtures because exact English wording is deliberately non-normative.

## Reason

The selected representation maps directly to ordinary records, tagged variants, arrays, strings, integers, booleans, and null values. It is readable in version control, portable across likely implementation languages, and usable without a parser generator or specialized AST package. Explicit phase results make lexical continuation, parser gating, fail-fast syntax behavior, and AST absence mechanically testable.

## Validation

Before the full suite is populated, pilot fixtures must demonstrate:

- successful lexing with physical `EOF`;
- failed lexing with partial tokens and parser `not_run`;
- invalid UTF-8 through `bytes_hex`;
- successful parsing with AST token indices;
- one syntax failure with no AST;
- byte spans and a location-sensitive position assertion; and
- coverage metadata for tokens, AST nodes, diagnostics, and named rules.

