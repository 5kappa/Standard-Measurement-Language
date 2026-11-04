# Standard Measurement Language Frontend Traceability Registry

Status: accepted and complete for the version 0.1 frontend specification  
Applies to: SML version 0.1 frontend contracts, conformance fixtures, and planned implementation modules  
Depends on: all accepted documents in this directory and decisions 085 through 089

## Purpose

This document assigns stable identifiers to implementation-facing rules and traces each rule to its controlling specification, decision history, required conformance evidence, fixture IDs, and planned Python module. It is the registry for every value stored in a fixture's `covers.rules` array.

This registry does not create language behavior. If a fixture exposes a conflict or missing rule, the controlling specification must be clarified before this table or the fixture is completed.

## Registry conventions

A rule ID has the form:

```text
DOCUMENT.rule-name
```

`DOCUMENT` is the uppercase document namespace. `rule-name` is a stable lowercase hyphenated identifier. Rewording a heading does not rename a rule. Renaming or removing an accepted rule ID requires a deliberate traceability update and fixture review.

Namespaces are:

| Namespace | Controlling document |
| --- | --- |
| `TOKEN-SPEC` | [`TOKEN-SPEC.md`](TOKEN-SPEC.md) |
| `SOURCE-LOCATIONS` | [`SOURCE-LOCATIONS.md`](SOURCE-LOCATIONS.md) |
| `GRAMMAR` | [`GRAMMAR.ebnf`](GRAMMAR.ebnf) |
| `AST-SCHEMA` | [`AST-SCHEMA.md`](AST-SCHEMA.md) |
| `DIAGNOSTICS` | [`DIAGNOSTICS.md`](DIAGNOSTICS.md) |
| `RECOVERY` | [`RECOVERY.md`](RECOVERY.md) |
| `FIXTURES` | [`fixtures/README.md`](fixtures/README.md) |
| `IMPLEMENTATION` | [`IMPLEMENTATION.md`](IMPLEMENTATION.md) |

Evidence values are:

- `TOKEN`: token-stream or partial-token expectation;
- `AST`: successful source-AST expectation;
- `DIAGNOSTIC`: structured lexical or syntax diagnostic expectation;
- `RECOVERY`: continuation, truncation, phase-gating, or failure-result expectation;
- `FORMAT`: fixture decoding or execution evidence; and
- `PROCESS`: documentation or tooling verification rather than a frontend behavior fixture.

`PENDING` in the Fixture IDs column is an explicit incomplete requirement. `N/A` means the rule is a process or implementation constraint that does not require a language-conformance fixture. Fixtures are trusted, version-controlled conformance data. The test loader validates only enough structure to decode and execute the indexed fixture cases. Exhaustive validation of the fixture format is not part of the lexer implementation.

Module paths follow decision 089 as revised by the trusted-fixture policy. The completed lexer decodes the required lexer-success and lexical-failure records. Test-loader paths for parser and AST variants identify where those records will be decoded when parser implementation begins; they do not imply current parser support.

## Token rules

| Rule ID | Controlling section | Decision basis | Evidence | Fixture IDs | Planned module |
| --- | --- | --- | --- | --- | --- |
| `TOKEN-SPEC.token-model` | Token model | 076, 086 | TOKEN | `lex-pilot-attached-quantity-tokens`, `lex-all-token-kinds` | `sml_frontend/token.py` |
| `TOKEN-SPEC.scanning-contract` | Scanning contract | 076, 086, 088 | TOKEN, RECOVERY | `lex-pilot-attached-quantity-tokens`, `lex-all-token-kinds` | `sml_frontend/lexer.py` |
| `TOKEN-SPEC.identifiers` | Value and name tokens | 076 | TOKEN | `lex-pilot-attached-quantity-tokens`, `lex-keyword-near-misses-identifiers` | `sml_frontend/lexer.py` |
| `TOKEN-SPEC.reserved-spellings` | Reserved identifier spellings | 017, 076, 084 | TOKEN | `lex-all-token-kinds`, `lex-keyword-near-misses-identifiers` | `sml_frontend/lexer.py` |
| `TOKEN-SPEC.numbers` | Numeric candidates | 012, 076, 083 | TOKEN | `lex-pilot-attached-quantity-tokens`, `lex-accepted-numbers-and-signs`, `lex-ordinary-attached-e-identifier` | `sml_frontend/lexer.py` |
| `TOKEN-SPEC.malformed-decimals` | Malformed decimal forms | 083, 086 | TOKEN, DIAGNOSTIC, RECOVERY | `lex-leading-zero`, `lex-malformed-leading-decimal`, `lex-malformed-trailing-decimal`, `lex-malformed-repeated-decimal`, `lex-numeric-separator`, `lex-numeric-separator-exact-boundary`, `lex-repeated-decimal-exact-boundary` | `sml_frontend/lexer.py` |
| `TOKEN-SPEC.unsupported-number-notation` | Unsupported numeric notations | 076, 086 | TOKEN, DIAGNOSTIC, RECOVERY | `lex-ordinary-attached-e-identifier`, `lex-scientific-boundary`, `lex-scientific-notation`, `lex-scientific-incomplete-sign`, `lex-alternate-base-empty`, `lex-hex-notation`, `lex-hex-boundary`, `lex-hex-invalid-digit-exact-boundary`, `lex-binary-notation` | `sml_frontend/lexer.py` |
| `TOKEN-SPEC.strings` | Strings | 076, 086 | TOKEN, DIAGNOSTIC, RECOVERY | `lex-complete-strings`, `lex-invalid-character-closed-string`, `lex-invalid-character-unclosed-string`, `lex-unclosed-string-lf`, `lex-unclosed-string-cr`, `lex-unclosed-string-crlf`, `lex-unclosed-string-eof` | `sml_frontend/lexer.py` |
| `TOKEN-SPEC.trivia-comments` | Whitespace and comments | 076, 086 | TOKEN, DIAGNOSTIC, RECOVERY | `lex-comments-adjacency-and-nonnesting`, `lex-invalid-character-line-comment`, `lex-invalid-character-block-comment`, `lex-unterminated-block-comment`, `location-comment-detached-quantity-boundary`, `location-multiline-block-comment` | `sml_frontend/lexer.py` |
| `TOKEN-SPEC.operators-maximal-munch` | Operators | 020, 029, 076, 084 | TOKEN | `lex-all-token-kinds`, `lex-accepted-numbers-and-signs`, `lex-maximal-munch-boundaries`, `lex-incomplete-logical-operators` | `sml_frontend/lexer.py` |
| `TOKEN-SPEC.delimiters` | Delimiters | 076, 084 | TOKEN | `lex-all-token-kinds` | `sml_frontend/lexer.py` |
| `TOKEN-SPEC.eof` | End of file | 076, 086 | TOKEN, RECOVERY | `lex-pilot-attached-quantity-tokens`, `lex-all-token-kinds`, `location-empty-source` | `sml_frontend/lexer.py` |
| `TOKEN-SPEC.inventory` | Complete token inventory | 076, 084 | TOKEN | `lex-all-token-kinds` | `sml_frontend/token.py` |

## Source-location rules

| Rule ID | Controlling section | Decision basis | Evidence | Fixture IDs | Planned module |
| --- | --- | --- | --- | --- | --- |
| `SOURCE-LOCATIONS.source-preservation` | Source preservation | 076, 088 | TOKEN, DIAGNOSTIC | `lex-pilot-attached-quantity-tokens`, `lex-all-token-kinds` | `sml_frontend/source.py` |
| `SOURCE-LOCATIONS.byte-spans` | Byte spans | 076 | TOKEN, AST, DIAGNOSTIC | `lex-pilot-attached-quantity-tokens`, `lex-all-token-kinds`, `location-empty-source`, `frontend-pilot-invalid-utf8-phase-gate` | `sml_frontend/source.py` |
| `SOURCE-LOCATIONS.human-positions` | Human-readable positions | 076 | DIAGNOSTIC | `location-newline-and-tab-forms`, `frontend-pilot-invalid-utf8-phase-gate` | `sml_frontend/source.py` |
| `SOURCE-LOCATIONS.newlines` | Lines and newlines | 076 | TOKEN, DIAGNOSTIC | `location-newline-and-tab-forms`, `location-multiline-block-comment`, `frontend-pilot-invalid-utf8-phase-gate` | `sml_frontend/source.py` |
| `SOURCE-LOCATIONS.columns-tabs` | Columns and tabs | 076, 088 | TOKEN, DIAGNOSTIC | `location-newline-and-tab-forms`, `location-multiline-block-comment`, `location-invalid-unicode-scalar` | `sml_frontend/source.py` |
| `SOURCE-LOCATIONS.trivia-adjacency` | Tokens and trivia | 014, 076 | TOKEN, DIAGNOSTIC | `lex-pilot-attached-quantity-tokens`, `lex-comments-adjacency-and-nonnesting`, `location-adjacent-quantity-boundary`, `location-space-detached-quantity-boundary`, `location-comment-detached-quantity-boundary` | `sml_frontend/source.py` |
| `SOURCE-LOCATIONS.ast-spans` | AST spans | 085 | AST | `frontend-pilot-uninitialized-let-ast`, `parse-empty-source-ast`, `parse-functions-parameters-declarations`, `parse-assignment-update-call-io-statements`, `parse-expression-and-quantity-forms`, `parse-conditionals-and-loops`, `parse-unit-expression-structures` | `sml_frontend/syntax.py` |
| `SOURCE-LOCATIONS.missing-syntax` | Missing-syntax diagnostic locations | 086 | DIAGNOSTIC | `frontend-pilot-const-initializer-required`, `parse-missing-closing-brace-eof`, `parse-missing-unit-bracket-eof` | `sml_frontend/parser.py` |
| `SOURCE-LOCATIONS.phase-ownership` | Phase ownership | 085, 086 | TOKEN, AST, DIAGNOSTIC | `frontend-pilot-invalid-utf8-phase-gate` | `sml_frontend/lexer.py`, `sml_frontend/parser.py` |

## Grammar rules

| Rule ID | Controlling production or constraint | Decision basis | Evidence | Fixture IDs | Planned module |
| --- | --- | --- | --- | --- | --- |
| `GRAMMAR.program-functions` | `source_file` through `return_annotation` | 023, 027, 084 | AST, DIAGNOSTIC | `frontend-pilot-uninitialized-let-ast`, `parse-empty-source-ast`, `parse-functions-parameters-declarations`, `parse-assignment-update-call-io-statements`, `parse-expression-and-quantity-forms`, `parse-conditionals-and-loops`, `parse-unit-expression-structures` | `sml_frontend/parser.py` |
| `GRAMMAR.blocks-statements` | `block`, `statement` | 023, 076 | AST, DIAGNOSTIC | `frontend-pilot-uninitialized-let-ast`, `parse-empty-source-ast`, `parse-functions-parameters-declarations`, `parse-assignment-update-call-io-statements`, `parse-expression-and-quantity-forms`, `parse-conditionals-and-loops`, `parse-unit-expression-structures` | `sml_frontend/parser.py` |
| `GRAMMAR.declarations` | `declaration` through `declaration_value` | 027, 028 | AST, DIAGNOSTIC | `frontend-pilot-uninitialized-let-ast`, `frontend-pilot-const-initializer-required`, `parse-functions-parameters-declarations`, `parse-expression-and-quantity-forms`, `parse-unit-expression-structures` | `sml_frontend/parser.py` |
| `GRAMMAR.assignments-updates` | identifier statements through `assignment_core` | 020, 023, 029 | AST, DIAGNOSTIC | `parse-assignment-update-call-io-statements`, `parse-conditionals-and-loops` | `sml_frontend/parser.py` |
| `GRAMMAR.output-calls` | `print_statement`, call statement alternatives | 023, 076 | AST, DIAGNOSTIC | `parse-assignment-update-call-io-statements` | `sml_frontend/parser.py` |
| `GRAMMAR.conditionals` | `if_statement` | 017, 023, 076 | AST, DIAGNOSTIC | `parse-conditionals-and-loops` | `sml_frontend/parser.py` |
| `GRAMMAR.loops` | `while_statement` through `for_update` | 017, 023, 076 | AST, DIAGNOSTIC | `parse-conditionals-and-loops` | `sml_frontend/parser.py` |
| `GRAMMAR.transfer-assertion` | return, break, continue, assert | 023, 076 | AST, DIAGNOSTIC | `parse-functions-parameters-declarations`, `parse-assignment-update-call-io-statements`, `parse-conditionals-and-loops` | `sml_frontend/parser.py` |
| `GRAMMAR.annotations` | declaration and return annotations | 027, 084 | AST, DIAGNOSTIC | `parse-functions-parameters-declarations`, `parse-expression-and-quantity-forms`, `parse-unit-expression-structures` | `sml_frontend/parser.py` |
| `GRAMMAR.expression-precedence` | `expression` through `primary` | 020, 026, 076 | AST, DIAGNOSTIC | `parse-functions-parameters-declarations`, `parse-assignment-update-call-io-statements`, `parse-expression-and-quantity-forms`, `parse-conditionals-and-loops`, `parse-unit-expression-structures` | `sml_frontend/parser.py` |
| `GRAMMAR.nonchaining-comparisons` | `equality`, `relational` | 020, 076 | AST, DIAGNOSTIC | `parse-chained-relational`, `parse-chained-equality` | `sml_frontend/parser.py` |
| `GRAMMAR.quantities` | `numeric_primary`, `quantity_suffix` | 014, 076 | AST, DIAGNOSTIC | `parse-assignment-update-call-io-statements`, `parse-expression-and-quantity-forms`, `parse-unit-expression-structures` | `sml_frontend/parser.py` |
| `GRAMMAR.calls` | `identifier_primary`, `call_suffix`, `argument_list` | 023, 076 | AST, DIAGNOSTIC | `parse-assignment-update-call-io-statements`, `parse-expression-and-quantity-forms` | `sml_frontend/parser.py` |
| `GRAMMAR.input-syntax` | `input_expression`, constraint C5 | 027, 076 | AST, DIAGNOSTIC | `parse-functions-parameters-declarations`, `parse-assignment-update-call-io-statements` | `sml_frontend/parser.py` |
| `GRAMMAR.unit-expressions` | `unit_expression` through `unit_power` | 022, 076 | AST, DIAGNOSTIC | `parse-functions-parameters-declarations`, `parse-assignment-update-call-io-statements`, `parse-expression-and-quantity-forms`, `parse-unit-expression-structures` | `sml_frontend/parser.py` |
| `GRAMMAR.unit-exponents` | `unit_exponent`, constraint C2 | 022, 026 | AST, DIAGNOSTIC | `parse-functions-parameters-declarations`, `parse-assignment-update-call-io-statements`, `parse-expression-and-quantity-forms`, `parse-unit-expression-structures` | `sml_frontend/parser.py` |
| `GRAMMAR.quantity-attachment` | constraint C1 | 014, 076 | AST, DIAGNOSTIC | `parse-assignment-update-call-io-statements`, `parse-expression-and-quantity-forms`, `parse-unit-expression-structures` | `sml_frontend/parser.py` |
| `GRAMMAR.unit-limits` | constraints C3 and C4 | 022, 076 | DIAGNOSTIC | `parse-functions-parameters-declarations`, `parse-assignment-update-call-io-statements`, `parse-expression-and-quantity-forms`, `parse-unit-expression-structures` | `sml_frontend/parser.py` |
| `GRAMMAR.control-transfer-context` | constraint C6 | 023, 086 | AST, DIAGNOSTIC | `parse-functions-parameters-declarations`, `parse-assignment-update-call-io-statements`, `parse-conditionals-and-loops` | `sml_frontend/parser.py` |
| `GRAMMAR.semantic-boundary` | constraint C7 | 026, 029, 075, 076 | AST | `parse-assignment-update-call-io-statements` | `sml_frontend/parser.py` |
| `GRAMMAR.annotation-consistency` | constraint C8 | 027 | AST, DIAGNOSTIC | `parse-functions-parameters-declarations`, `parse-expression-and-quantity-forms`, `parse-unit-expression-structures` | `sml_frontend/parser.py` |

## AST rules

| Rule ID | Controlling section | Decision basis | Evidence | Fixture IDs | Planned module |
| --- | --- | --- | --- | --- | --- |
| `AST-SCHEMA.source-references` | Source references | 085 | AST | `frontend-pilot-uninitialized-let-ast`, `parse-empty-source-ast`, `parse-functions-parameters-declarations`, `parse-assignment-update-call-io-statements`, `parse-expression-and-quantity-forms`, `parse-conditionals-and-loops`, `parse-unit-expression-structures` | `sml_frontend/syntax.py` |
| `AST-SCHEMA.separated-collections` | Separated collections | 085 | AST | `parse-functions-parameters-declarations`, `parse-assignment-update-call-io-statements`, `parse-expression-and-quantity-forms` | `sml_frontend/syntax.py` |
| `AST-SCHEMA.source-file-functions` | Source file and functions | 085 | AST | `frontend-pilot-uninitialized-let-ast`, `parse-empty-source-ast`, `parse-functions-parameters-declarations`, `parse-assignment-update-call-io-statements`, `parse-expression-and-quantity-forms`, `parse-conditionals-and-loops`, `parse-unit-expression-structures` | `sml_frontend/syntax.py` |
| `AST-SCHEMA.blocks-statements` | Blocks and statements | 085 | AST | `frontend-pilot-uninitialized-let-ast`, `parse-empty-source-ast`, `parse-functions-parameters-declarations`, `parse-assignment-update-call-io-statements`, `parse-expression-and-quantity-forms`, `parse-conditionals-and-loops`, `parse-unit-expression-structures` | `sml_frontend/syntax.py` |
| `AST-SCHEMA.declarations` | Declarations | 028, 085 | AST | `frontend-pilot-uninitialized-let-ast`, `parse-functions-parameters-declarations`, `parse-expression-and-quantity-forms`, `parse-unit-expression-structures` | `sml_frontend/syntax.py` |
| `AST-SCHEMA.assignments-updates` | Assignments and updates | 029, 085 | AST | `parse-assignment-update-call-io-statements`, `parse-conditionals-and-loops` | `sml_frontend/syntax.py` |
| `AST-SCHEMA.output-calls` | Output and call statements | 085 | AST | `parse-assignment-update-call-io-statements` | `sml_frontend/syntax.py` |
| `AST-SCHEMA.conditionals` | Conditional statements | 085 | AST | `parse-conditionals-and-loops` | `sml_frontend/syntax.py` |
| `AST-SCHEMA.loops` | Loops | 085 | AST | `parse-conditionals-and-loops` | `sml_frontend/syntax.py` |
| `AST-SCHEMA.transfer-assertion` | Transfer and assertion statements | 085, 086 | AST | `parse-functions-parameters-declarations`, `parse-assignment-update-call-io-statements`, `parse-conditionals-and-loops` | `sml_frontend/syntax.py` |
| `AST-SCHEMA.annotations` | Declaration annotations | 027, 085 | AST | `parse-functions-parameters-declarations`, `parse-expression-and-quantity-forms`, `parse-unit-expression-structures` | `sml_frontend/syntax.py` |
| `AST-SCHEMA.expressions` | Expressions and leaves | 020, 026, 085 | AST | `parse-functions-parameters-declarations`, `parse-assignment-update-call-io-statements`, `parse-expression-and-quantity-forms`, `parse-conditionals-and-loops`, `parse-unit-expression-structures` | `sml_frontend/syntax.py` |
| `AST-SCHEMA.grouping-calls` | Grouping and calls | 085 | AST | `parse-assignment-update-call-io-statements`, `parse-expression-and-quantity-forms` | `sml_frontend/syntax.py` |
| `AST-SCHEMA.operators-conversions` | Operators and conversions | 020, 043, 085 | AST | `parse-expression-and-quantity-forms`, `parse-conditionals-and-loops` | `sml_frontend/syntax.py` |
| `AST-SCHEMA.unit-expressions` | Unit expressions | 022, 085 | AST | `parse-functions-parameters-declarations`, `parse-assignment-update-call-io-statements`, `parse-expression-and-quantity-forms`, `parse-unit-expression-structures` | `sml_frontend/syntax.py` |
| `AST-SCHEMA.span-composition` | Span composition | 085 | AST | `frontend-pilot-uninitialized-let-ast`, `parse-empty-source-ast`, `parse-functions-parameters-declarations`, `parse-assignment-update-call-io-statements`, `parse-expression-and-quantity-forms`, `parse-conditionals-and-loops`, `parse-unit-expression-structures` | `sml_frontend/parser.py` |
| `AST-SCHEMA.success-invariants` | Successful-AST invariants | 085 | AST | `frontend-pilot-uninitialized-let-ast`, `parse-empty-source-ast`, `parse-functions-parameters-declarations`, `parse-assignment-update-call-io-statements`, `parse-expression-and-quantity-forms`, `parse-conditionals-and-loops`, `parse-unit-expression-structures` | `sml_frontend/parser.py` |
| `AST-SCHEMA.failure-boundary` | Failure boundary | 085, 086 | DIAGNOSTIC, RECOVERY | `frontend-pilot-const-initializer-required`, `parse-missing-closing-brace-eof`, `parse-missing-unit-bracket-eof`, `parse-expected-identifier`, `parse-expected-expression`, `parse-expected-statement`, `parse-expected-function`, `parse-detached-simple-quantity`, `parse-detached-simple-quantity-comment`, `parse-detached-compound-quantity-space`, `parse-detached-compound-quantity`, `parse-const-initializer-required-again`, `parse-invalid-declaration-annotation`, `parse-invalid-input-position`, `parse-input-arguments-not-allowed`, `parse-input-annotation-required`, `parse-assignment-not-expression`, `parse-update-not-expression`, `parse-chained-relational`, `parse-chained-equality`, `parse-misplaced-to`, `parse-misplaced-then`, `parse-misplaced-do`, `parse-break-outside-loop`, `parse-continue-outside-loop`, `parse-return-value-required`, `parse-return-value-forbidden`, `parse-empty-unit-annotation`, `parse-expected-unit-factor`, `parse-missing-unit-exponent`, `parse-invalid-unit-exponent-plus`, `parse-unit-exponent-out-of-range`, `parse-unit-repeated-division`, `parse-unit-nested-division`, `parse-unit-grouped-numerator`, `parse-unit-group-power`, `parse-unit-implicit-multiplication`, `parse-unit-numeric-factor`, `parse-unit-unparenthesized-product-denominator`, `parse-too-many-unit-factors`, `parse-unit-annotation-too-long` | `sml_frontend/parser.py` |

## Diagnostic rules

| Rule ID | Controlling section | Decision basis | Evidence | Fixture IDs | Planned module |
| --- | --- | --- | --- | --- | --- |
| `DIAGNOSTICS.data-model` | Diagnostic data model | 086 | DIAGNOSTIC | `lex-invalid-leading-underscore` | `sml_frontend/diagnostic.py` |
| `DIAGNOSTICS.stable-data` | Stable diagnostic data | 086 | DIAGNOSTIC | `lex-invalid-leading-underscore` | `sml_frontend/diagnostic.py` |
| `DIAGNOSTICS.result-phase-policy` | Result and phase policy | 086 | DIAGNOSTIC, RECOVERY | `lex-leading-zero`, `lex-malformed-leading-decimal`, `lex-malformed-trailing-decimal`, `lex-malformed-repeated-decimal`, `lex-numeric-separator`, `lex-numeric-separator-exact-boundary`, `lex-scientific-boundary`, `lex-scientific-notation`, `lex-scientific-incomplete-sign`, `lex-alternate-base-empty`, `lex-hex-notation`, `lex-hex-boundary`, `lex-hex-invalid-digit-exact-boundary`, `lex-binary-notation`, `lex-repeated-decimal-exact-boundary`, `lex-invalid-leading-underscore`, `lex-invalid-character-closed-string`, `lex-invalid-character-unclosed-string`, `lex-invalid-character-line-comment`, `lex-invalid-character-block-comment`, `lex-malformed-gap-preserves-spans`, `lex-unclosed-string-lf`, `lex-unclosed-string-cr`, `lex-unclosed-string-crlf`, `lex-unclosed-string-eof`, `lex-unterminated-block-comment`, `lex-incomplete-logical-operators`, `lex-diagnostic-limit-exactly-twenty`, `lex-diagnostic-limit-truncated-continues`, `location-invalid-unicode-scalar`, `frontend-pilot-invalid-utf8-phase-gate` | `sml_frontend/lexer.py`, `sml_frontend/parser.py` |
| `DIAGNOSTICS.ordering-limit` | Diagnostic ordering and limit | 086 | DIAGNOSTIC, RECOVERY | `lex-diagnostic-limit-exactly-twenty`, `lex-diagnostic-limit-truncated-continues` | `sml_frontend/lexer.py` |
| `DIAGNOSTICS.unexpected-source-labels` | Unexpected existing source | 086 | DIAGNOSTIC | `lex-invalid-leading-underscore` | `sml_frontend/diagnostic.py` |
| `DIAGNOSTICS.absent-syntax-labels` | Expected absent syntax | 086 | DIAGNOSTIC | `frontend-pilot-const-initializer-required` | `sml_frontend/parser.py` |
| `DIAGNOSTICS.expression-delimiter-labels` | Expressions and delimiters | 086 | DIAGNOSTIC | `parse-missing-unit-bracket-eof` | `sml_frontend/parser.py` |
| `DIAGNOSTICS.detached-quantity-labels` | Detached quantities | 014, 086 | DIAGNOSTIC | `parse-detached-simple-quantity`, `parse-detached-simple-quantity-comment`, `parse-detached-compound-quantity-space`, `parse-detached-compound-quantity` | `sml_frontend/parser.py` |
| `DIAGNOSTICS.limit-labels` | Limits | 022, 086 | DIAGNOSTIC | `parse-too-many-unit-factors`, `parse-unit-annotation-too-long` | `sml_frontend/parser.py` |
| `DIAGNOSTICS.lexical-codes` | Lexical diagnostic codes | 086, 088 | DIAGNOSTIC | `frontend-pilot-invalid-utf8-phase-gate` | `sml_frontend/lexer.py` |
| `DIAGNOSTICS.malformed-numeric-boundaries` | Malformed numeric boundaries | 083, 086 | TOKEN, DIAGNOSTIC, RECOVERY | `lex-leading-zero`, `lex-malformed-leading-decimal`, `lex-malformed-trailing-decimal`, `lex-malformed-repeated-decimal`, `lex-numeric-separator`, `lex-numeric-separator-exact-boundary`, `lex-scientific-boundary`, `lex-scientific-notation`, `lex-scientific-incomplete-sign`, `lex-alternate-base-empty`, `lex-hex-notation`, `lex-hex-boundary`, `lex-hex-invalid-digit-exact-boundary`, `lex-binary-notation`, `lex-repeated-decimal-exact-boundary` | `sml_frontend/lexer.py` |
| `DIAGNOSTICS.general-syntax-codes` | General syntax diagnostic codes | 086 | DIAGNOSTIC | `parse-missing-closing-brace-eof`, `parse-missing-unit-bracket-eof`, `parse-expected-identifier`, `parse-expected-expression`, `parse-expected-statement`, `parse-expected-function` | `sml_frontend/parser.py` |
| `DIAGNOSTICS.specialized-syntax-codes` | Specialized syntax diagnostic codes | 086 | DIAGNOSTIC | `frontend-pilot-const-initializer-required`, `parse-detached-simple-quantity`, `parse-detached-simple-quantity-comment`, `parse-detached-compound-quantity-space`, `parse-detached-compound-quantity`, `parse-const-initializer-required-again`, `parse-invalid-declaration-annotation`, `parse-invalid-input-position`, `parse-input-arguments-not-allowed`, `parse-input-annotation-required`, `parse-assignment-not-expression`, `parse-update-not-expression`, `parse-chained-relational`, `parse-chained-equality`, `parse-misplaced-to`, `parse-misplaced-then`, `parse-misplaced-do`, `parse-break-outside-loop`, `parse-continue-outside-loop`, `parse-return-value-required`, `parse-return-value-forbidden` | `sml_frontend/parser.py` |
| `DIAGNOSTICS.unit-syntax-codes` | Unit-expression diagnostic codes | 022, 086 | DIAGNOSTIC | `parse-empty-unit-annotation`, `parse-expected-unit-factor`, `parse-missing-unit-exponent`, `parse-invalid-unit-exponent-plus`, `parse-unit-exponent-out-of-range`, `parse-unit-repeated-division`, `parse-unit-nested-division`, `parse-unit-grouped-numerator`, `parse-unit-group-power`, `parse-unit-implicit-multiplication`, `parse-unit-numeric-factor`, `parse-unit-unparenthesized-product-denominator`, `parse-too-many-unit-factors`, `parse-unit-annotation-too-long` | `sml_frontend/parser.py` |
| `DIAGNOSTICS.internal-failure` | Internal failure code | 086, 089 | PROCESS | N/A | `sml_frontend/diagnostic.py`, `sml_frontend/__main__.py` |

## Recovery and phase-gating rules

| Rule ID | Controlling section | Decision basis | Evidence | Fixture IDs | Planned module |
| --- | --- | --- | --- | --- | --- |
| `RECOVERY.lexical-result` | Lexical result | 086 | TOKEN, DIAGNOSTIC, RECOVERY | `lex-leading-zero`, `lex-malformed-leading-decimal`, `lex-malformed-trailing-decimal`, `lex-malformed-repeated-decimal`, `lex-numeric-separator`, `lex-numeric-separator-exact-boundary`, `lex-scientific-boundary`, `lex-scientific-notation`, `lex-scientific-incomplete-sign`, `lex-alternate-base-empty`, `lex-hex-notation`, `lex-hex-boundary`, `lex-hex-invalid-digit-exact-boundary`, `lex-binary-notation`, `lex-repeated-decimal-exact-boundary`, `lex-invalid-leading-underscore`, `lex-invalid-character-closed-string`, `lex-invalid-character-unclosed-string`, `lex-invalid-character-line-comment`, `lex-invalid-character-block-comment`, `lex-malformed-gap-preserves-spans`, `lex-unclosed-string-lf`, `lex-unclosed-string-cr`, `lex-unclosed-string-crlf`, `lex-unclosed-string-eof`, `lex-unterminated-block-comment`, `lex-incomplete-logical-operators`, `lex-diagnostic-limit-exactly-twenty`, `lex-diagnostic-limit-truncated-continues`, `location-invalid-unicode-scalar`, `frontend-pilot-invalid-utf8-phase-gate` | `sml_frontend/lexer.py` |
| `RECOVERY.progress-invariants` | General continuation invariants | 086 | RECOVERY | `lex-leading-zero`, `lex-malformed-leading-decimal`, `lex-malformed-trailing-decimal`, `lex-malformed-repeated-decimal`, `lex-numeric-separator`, `lex-numeric-separator-exact-boundary`, `lex-scientific-boundary`, `lex-scientific-notation`, `lex-scientific-incomplete-sign`, `lex-alternate-base-empty`, `lex-hex-notation`, `lex-hex-boundary`, `lex-hex-invalid-digit-exact-boundary`, `lex-binary-notation`, `lex-repeated-decimal-exact-boundary`, `lex-invalid-leading-underscore`, `lex-invalid-character-closed-string`, `lex-invalid-character-unclosed-string`, `lex-invalid-character-line-comment`, `lex-invalid-character-block-comment`, `lex-malformed-gap-preserves-spans`, `lex-unclosed-string-lf`, `lex-unclosed-string-cr`, `lex-unclosed-string-crlf`, `lex-unclosed-string-eof`, `lex-unterminated-block-comment`, `lex-incomplete-logical-operators`, `lex-diagnostic-limit-exactly-twenty`, `lex-diagnostic-limit-truncated-continues`, `location-invalid-unicode-scalar`, `frontend-pilot-invalid-utf8-phase-gate` | `sml_frontend/lexer.py` |
| `RECOVERY.invalid-utf8` | `LEX001 INVALID_UTF8` | 088 | TOKEN, DIAGNOSTIC, RECOVERY | `frontend-pilot-invalid-utf8-phase-gate` | `sml_frontend/lexer.py` |
| `RECOVERY.invalid-source-character` | `LEX002 INVALID_SOURCE_CHARACTER` | 086 | TOKEN, DIAGNOSTIC, RECOVERY | `lex-invalid-leading-underscore`, `lex-invalid-character-closed-string`, `lex-invalid-character-unclosed-string`, `lex-invalid-character-line-comment`, `lex-invalid-character-block-comment`, `lex-malformed-gap-preserves-spans`, `location-invalid-unicode-scalar` | `sml_frontend/lexer.py` |
| `RECOVERY.numeric-failures` | `LEX003` through `LEX007` | 083, 086 | TOKEN, DIAGNOSTIC, RECOVERY | `lex-leading-zero`, `lex-malformed-leading-decimal`, `lex-malformed-trailing-decimal`, `lex-malformed-repeated-decimal`, `lex-numeric-separator`, `lex-numeric-separator-exact-boundary`, `lex-scientific-boundary`, `lex-scientific-notation`, `lex-scientific-incomplete-sign`, `lex-alternate-base-empty`, `lex-hex-notation`, `lex-hex-boundary`, `lex-hex-invalid-digit-exact-boundary`, `lex-binary-notation`, `lex-repeated-decimal-exact-boundary` | `sml_frontend/lexer.py` |
| `RECOVERY.unclosed-string` | `LEX008 UNCLOSED_STRING` | 086 | TOKEN, DIAGNOSTIC, RECOVERY | `lex-invalid-character-unclosed-string`, `lex-unclosed-string-lf`, `lex-unclosed-string-cr`, `lex-unclosed-string-crlf`, `lex-unclosed-string-eof` | `sml_frontend/lexer.py` |
| `RECOVERY.unterminated-block-comment` | `LEX009 UNTERMINATED_BLOCK_COMMENT` | 086 | TOKEN, DIAGNOSTIC, RECOVERY | `lex-unterminated-block-comment` | `sml_frontend/lexer.py` |
| `RECOVERY.incomplete-logical-operator` | `LEX010 INCOMPLETE_LOGICAL_OPERATOR` | 086 | TOKEN, DIAGNOSTIC, RECOVERY | `lex-incomplete-logical-operators` | `sml_frontend/lexer.py` |
| `RECOVERY.slash-prefix-order` | Comments and slash prefixes | 076, 086 | TOKEN, RECOVERY | `lex-comments-adjacency-and-nonnesting` | `sml_frontend/lexer.py` |
| `RECOVERY.partial-token-adjacency` | Adjacency in partial tokens | 086 | TOKEN, RECOVERY | `lex-malformed-gap-preserves-spans` | `sml_frontend/lexer.py` |
| `RECOVERY.diagnostic-limit` | Diagnostic limit behavior | 086 | DIAGNOSTIC, RECOVERY | `lex-diagnostic-limit-exactly-twenty`, `lex-diagnostic-limit-truncated-continues` | `sml_frontend/lexer.py` |
| `RECOVERY.parser-phase-gate` | Parser phase gate | 086 | RECOVERY | `lex-leading-zero`, `lex-malformed-leading-decimal`, `lex-malformed-trailing-decimal`, `lex-malformed-repeated-decimal`, `lex-numeric-separator`, `lex-numeric-separator-exact-boundary`, `lex-scientific-boundary`, `lex-scientific-notation`, `lex-scientific-incomplete-sign`, `lex-alternate-base-empty`, `lex-hex-notation`, `lex-hex-boundary`, `lex-hex-invalid-digit-exact-boundary`, `lex-binary-notation`, `lex-repeated-decimal-exact-boundary`, `lex-invalid-leading-underscore`, `lex-invalid-character-closed-string`, `lex-invalid-character-unclosed-string`, `lex-invalid-character-line-comment`, `lex-invalid-character-block-comment`, `lex-malformed-gap-preserves-spans`, `lex-unclosed-string-lf`, `lex-unclosed-string-cr`, `lex-unclosed-string-crlf`, `lex-unclosed-string-eof`, `lex-unterminated-block-comment`, `lex-incomplete-logical-operators`, `lex-diagnostic-limit-exactly-twenty`, `lex-diagnostic-limit-truncated-continues`, `location-invalid-unicode-scalar`, `frontend-pilot-invalid-utf8-phase-gate` | `sml_frontend/__main__.py` |
| `RECOVERY.parser-failure` | Parser failure behavior | 086 | DIAGNOSTIC, RECOVERY | `frontend-pilot-const-initializer-required`, `parse-missing-closing-brace-eof`, `parse-missing-unit-bracket-eof`, `parse-expected-identifier`, `parse-expected-expression`, `parse-expected-statement`, `parse-expected-function`, `parse-detached-simple-quantity`, `parse-detached-simple-quantity-comment`, `parse-detached-compound-quantity-space`, `parse-detached-compound-quantity`, `parse-const-initializer-required-again`, `parse-invalid-declaration-annotation`, `parse-invalid-input-position`, `parse-input-arguments-not-allowed`, `parse-input-annotation-required`, `parse-assignment-not-expression`, `parse-update-not-expression`, `parse-chained-relational`, `parse-chained-equality`, `parse-misplaced-to`, `parse-misplaced-then`, `parse-misplaced-do`, `parse-break-outside-loop`, `parse-continue-outside-loop`, `parse-return-value-required`, `parse-return-value-forbidden`, `parse-empty-unit-annotation`, `parse-expected-unit-factor`, `parse-missing-unit-exponent`, `parse-invalid-unit-exponent-plus`, `parse-unit-exponent-out-of-range`, `parse-unit-repeated-division`, `parse-unit-nested-division`, `parse-unit-grouped-numerator`, `parse-unit-group-power`, `parse-unit-implicit-multiplication`, `parse-unit-numeric-factor`, `parse-unit-unparenthesized-product-denominator`, `parse-too-many-unit-factors`, `parse-unit-annotation-too-long` | `sml_frontend/parser.py` |
| `RECOVERY.deferred-parser-recovery` | Deferred parser-recovery guidance | 086 | PROCESS | N/A | N/A |

## Fixture-format rules

| Rule ID | Controlling section | Decision basis | Evidence | Fixture IDs | Planned module |
| --- | --- | --- | --- | --- | --- |
| `FIXTURES.suite-layout` | Suite layout | 087 | FORMAT | `lex-pilot-attached-quantity-tokens` | `tests/fixture_loader.py` |
| `FIXTURES.strict-json` | JSON rules | 087 | FORMAT | `lex-pilot-attached-quantity-tokens` | `tests/fixture_loader.py` |
| `FIXTURES.fixture-record` | Fixture record and IDs | 087 | FORMAT | `lex-pilot-attached-quantity-tokens` | `tests/fixture_loader.py` |
| `FIXTURES.source-input` | Source input | 087 | FORMAT | `frontend-pilot-invalid-utf8-phase-gate` | `tests/fixture_loader.py` |
| `FIXTURES.entrypoints` | Entry points and phase expectations | 086, 087 | FORMAT, RECOVERY | `frontend-pilot-invalid-utf8-phase-gate` | `tests/fixture_loader.py` |
| `FIXTURES.lexical-expectations` | Lexical expectations | 086, 087 | FORMAT, TOKEN, DIAGNOSTIC | `lex-pilot-attached-quantity-tokens`, `lex-leading-zero`, `lex-malformed-leading-decimal`, `lex-malformed-trailing-decimal`, `lex-malformed-repeated-decimal`, `lex-numeric-separator`, `lex-numeric-separator-exact-boundary`, `lex-scientific-boundary`, `lex-scientific-notation`, `lex-scientific-incomplete-sign`, `lex-alternate-base-empty`, `lex-hex-notation`, `lex-hex-boundary`, `lex-hex-invalid-digit-exact-boundary`, `lex-binary-notation`, `lex-repeated-decimal-exact-boundary`, `lex-invalid-leading-underscore`, `lex-invalid-character-closed-string`, `lex-invalid-character-unclosed-string`, `lex-invalid-character-line-comment`, `lex-invalid-character-block-comment`, `lex-malformed-gap-preserves-spans`, `lex-unclosed-string-lf`, `lex-unclosed-string-cr`, `lex-unclosed-string-crlf`, `lex-unclosed-string-eof`, `lex-unterminated-block-comment`, `lex-incomplete-logical-operators`, `lex-diagnostic-limit-exactly-twenty`, `lex-diagnostic-limit-truncated-continues`, `location-invalid-unicode-scalar`, `frontend-pilot-invalid-utf8-phase-gate` | `tests/fixture_loader.py` |
| `FIXTURES.token-mapping` | Tokens | 087 | FORMAT, TOKEN | `lex-pilot-attached-quantity-tokens`, `lex-all-token-kinds` | `tests/fixture_loader.py` |
| `FIXTURES.location-mapping` | Source spans and positions | 087 | FORMAT, DIAGNOSTIC | `frontend-pilot-invalid-utf8-phase-gate` | `tests/fixture_loader.py` |
| `FIXTURES.parse-expectations` | Parse expectations | 086, 087 | FORMAT, AST, DIAGNOSTIC | `frontend-pilot-uninitialized-let-ast`, `frontend-pilot-const-initializer-required`, `parse-empty-source-ast`, `parse-functions-parameters-declarations`, `parse-assignment-update-call-io-statements`, `parse-expression-and-quantity-forms`, `parse-conditionals-and-loops`, `parse-unit-expression-structures` | `tests/fixture_loader.py` |
| `FIXTURES.ast-mapping` | AST mapping | 085, 087 | FORMAT, AST | `frontend-pilot-uninitialized-let-ast`, `parse-empty-source-ast`, `parse-functions-parameters-declarations`, `parse-assignment-update-call-io-statements`, `parse-expression-and-quantity-forms`, `parse-conditionals-and-loops`, `parse-unit-expression-structures` | `tests/fixture_loader.py` |
| `FIXTURES.diagnostic-mapping` | Diagnostic mapping | 086, 087, 088 | FORMAT, DIAGNOSTIC | `lex-leading-zero`, `lex-malformed-leading-decimal`, `lex-malformed-trailing-decimal`, `lex-malformed-repeated-decimal`, `lex-numeric-separator`, `lex-numeric-separator-exact-boundary`, `lex-scientific-boundary`, `lex-scientific-notation`, `lex-scientific-incomplete-sign`, `lex-alternate-base-empty`, `lex-hex-notation`, `lex-hex-boundary`, `lex-hex-invalid-digit-exact-boundary`, `lex-binary-notation`, `lex-repeated-decimal-exact-boundary`, `lex-invalid-leading-underscore`, `lex-invalid-character-closed-string`, `lex-invalid-character-unclosed-string`, `lex-invalid-character-line-comment`, `lex-invalid-character-block-comment`, `lex-malformed-gap-preserves-spans`, `lex-unclosed-string-lf`, `lex-unclosed-string-cr`, `lex-unclosed-string-crlf`, `lex-unclosed-string-eof`, `lex-unterminated-block-comment`, `lex-incomplete-logical-operators`, `lex-diagnostic-limit-exactly-twenty`, `lex-diagnostic-limit-truncated-continues`, `location-invalid-unicode-scalar`, `frontend-pilot-invalid-utf8-phase-gate`, `frontend-pilot-const-initializer-required` | `tests/fixture_loader.py` |
| `FIXTURES.coverage-metadata` | Coverage metadata | 087 | PROCESS | `lex-pilot-attached-quantity-tokens` | `docs/frontend/TRACEABILITY.md` |
| `FIXTURES.strict-validation` | Trusted fixture loading | 087 | PROCESS | N/A | N/A |

## Implementation-process rules

| Rule ID | Controlling section | Decision basis | Evidence | Fixture IDs | Planned module or check |
| --- | --- | --- | --- | --- | --- |
| `IMPLEMENTATION.python-version` | Technology baseline | 089 | PROCESS | N/A | `python --version` must report `3.11.9` |
| `IMPLEMENTATION.byte-source-boundary` | Source boundary | 088, 089 | TOKEN, DIAGNOSTIC | `frontend-pilot-invalid-utf8-phase-gate` | `sml_frontend/lexer.py` |
| `IMPLEMENTATION.result-records` | Core Python records | 086, 089 | TOKEN, DIAGNOSTIC, RECOVERY | `lex-invalid-leading-underscore` | `sml_frontend/token.py`, `sml_frontend/diagnostic.py`, `sml_frontend/lexer.py` |
| `IMPLEMENTATION.failure-classification` | Failure classification | 086, 089 | DIAGNOSTIC, RECOVERY | `lex-invalid-leading-underscore` | `sml_frontend/diagnostic.py`, `sml_frontend/lexer.py` |
| `IMPLEMENTATION.handwritten-lexer` | Lexer architecture | 089 | PROCESS | N/A | design review |
| `IMPLEMENTATION.fixture-tests` | Fixture and test architecture | 087, 089 | FORMAT, PROCESS | N/A | `tests/test_fixtures.py` after implementation begins; no source fixture can prove test-runner architecture |
| `IMPLEMENTATION.repository-layout` | Repository layout | 089 | PROCESS | N/A | path review |
| `IMPLEMENTATION.recursive-descent-parser` | Later parser strategy | 089 | PROCESS | N/A | design review before parser code |
| `IMPLEMENTATION.zero-runtime-dependencies` | Technology baseline and deferred tools | 089 | PROCESS | N/A | environment and dependency review |

## Reverse indexes

### Fixture to rule

Every indexed fixture appears here, and every ID in a registry row resolves to exactly one fixture record. This reverse index describes the complete version 0.1 suite.

| Fixture ID | Fixture file | Covered rule IDs |
| --- | --- | --- |
| `lex-pilot-attached-quantity-tokens` | `lexer/pilot.json` | `TOKEN-SPEC.token-model`, `TOKEN-SPEC.scanning-contract`, `TOKEN-SPEC.identifiers`, `TOKEN-SPEC.numbers`, `TOKEN-SPEC.eof`, `SOURCE-LOCATIONS.source-preservation`, `SOURCE-LOCATIONS.byte-spans`, `SOURCE-LOCATIONS.trivia-adjacency`, `FIXTURES.suite-layout`, `FIXTURES.strict-json`, `FIXTURES.fixture-record`, `FIXTURES.lexical-expectations`, `FIXTURES.token-mapping`, `FIXTURES.coverage-metadata` |
| `lex-all-token-kinds` | `lexer/tokens.json` | `TOKEN-SPEC.token-model`, `TOKEN-SPEC.scanning-contract`, `TOKEN-SPEC.inventory`, `SOURCE-LOCATIONS.source-preservation`, `SOURCE-LOCATIONS.byte-spans`, `FIXTURES.token-mapping`, `TOKEN-SPEC.reserved-spellings`, `TOKEN-SPEC.operators-maximal-munch`, `TOKEN-SPEC.delimiters`, `TOKEN-SPEC.eof` |
| `lex-keyword-near-misses-identifiers` | `lexer/tokens.json` | `TOKEN-SPEC.identifiers`, `TOKEN-SPEC.reserved-spellings` |
| `lex-accepted-numbers-and-signs` | `lexer/tokens.json` | `TOKEN-SPEC.numbers`, `TOKEN-SPEC.operators-maximal-munch` |
| `lex-complete-strings` | `lexer/tokens.json` | `TOKEN-SPEC.strings` |
| `lex-comments-adjacency-and-nonnesting` | `lexer/tokens.json` | `TOKEN-SPEC.trivia-comments`, `SOURCE-LOCATIONS.trivia-adjacency`, `RECOVERY.slash-prefix-order` |
| `lex-maximal-munch-boundaries` | `lexer/tokens.json` | `TOKEN-SPEC.operators-maximal-munch` |
| `lex-ordinary-attached-e-identifier` | `lexer/tokens.json` | `TOKEN-SPEC.numbers`, `TOKEN-SPEC.unsupported-number-notation` |
| `lex-leading-zero` | `lexer/lexical-failures.json` | `DIAGNOSTICS.result-phase-policy`, `RECOVERY.lexical-result`, `RECOVERY.progress-invariants`, `RECOVERY.parser-phase-gate`, `FIXTURES.lexical-expectations`, `FIXTURES.diagnostic-mapping`, `TOKEN-SPEC.malformed-decimals`, `DIAGNOSTICS.malformed-numeric-boundaries`, `RECOVERY.numeric-failures` |
| `lex-malformed-leading-decimal` | `lexer/lexical-failures.json` | `DIAGNOSTICS.result-phase-policy`, `RECOVERY.lexical-result`, `RECOVERY.progress-invariants`, `RECOVERY.parser-phase-gate`, `FIXTURES.lexical-expectations`, `FIXTURES.diagnostic-mapping`, `TOKEN-SPEC.malformed-decimals`, `DIAGNOSTICS.malformed-numeric-boundaries`, `RECOVERY.numeric-failures` |
| `lex-malformed-trailing-decimal` | `lexer/lexical-failures.json` | `DIAGNOSTICS.result-phase-policy`, `RECOVERY.lexical-result`, `RECOVERY.progress-invariants`, `RECOVERY.parser-phase-gate`, `FIXTURES.lexical-expectations`, `FIXTURES.diagnostic-mapping`, `TOKEN-SPEC.malformed-decimals`, `DIAGNOSTICS.malformed-numeric-boundaries`, `RECOVERY.numeric-failures` |
| `lex-malformed-repeated-decimal` | `lexer/lexical-failures.json` | `DIAGNOSTICS.result-phase-policy`, `RECOVERY.lexical-result`, `RECOVERY.progress-invariants`, `RECOVERY.parser-phase-gate`, `FIXTURES.lexical-expectations`, `FIXTURES.diagnostic-mapping`, `TOKEN-SPEC.malformed-decimals`, `DIAGNOSTICS.malformed-numeric-boundaries`, `RECOVERY.numeric-failures` |
| `lex-numeric-separator` | `lexer/lexical-failures.json` | `DIAGNOSTICS.result-phase-policy`, `RECOVERY.lexical-result`, `RECOVERY.progress-invariants`, `RECOVERY.parser-phase-gate`, `FIXTURES.lexical-expectations`, `FIXTURES.diagnostic-mapping`, `TOKEN-SPEC.malformed-decimals`, `DIAGNOSTICS.malformed-numeric-boundaries`, `RECOVERY.numeric-failures` |
| `lex-numeric-separator-exact-boundary` | `lexer/lexical-failures.json` | `DIAGNOSTICS.result-phase-policy`, `RECOVERY.lexical-result`, `RECOVERY.progress-invariants`, `RECOVERY.parser-phase-gate`, `FIXTURES.lexical-expectations`, `FIXTURES.diagnostic-mapping`, `TOKEN-SPEC.malformed-decimals`, `DIAGNOSTICS.malformed-numeric-boundaries`, `RECOVERY.numeric-failures` |
| `lex-scientific-boundary` | `lexer/lexical-failures.json` | `DIAGNOSTICS.result-phase-policy`, `RECOVERY.lexical-result`, `RECOVERY.progress-invariants`, `RECOVERY.parser-phase-gate`, `FIXTURES.lexical-expectations`, `FIXTURES.diagnostic-mapping`, `TOKEN-SPEC.unsupported-number-notation`, `DIAGNOSTICS.malformed-numeric-boundaries`, `RECOVERY.numeric-failures` |
| `lex-scientific-notation` | `lexer/lexical-failures.json` | `DIAGNOSTICS.result-phase-policy`, `RECOVERY.lexical-result`, `RECOVERY.progress-invariants`, `RECOVERY.parser-phase-gate`, `FIXTURES.lexical-expectations`, `FIXTURES.diagnostic-mapping`, `TOKEN-SPEC.unsupported-number-notation`, `DIAGNOSTICS.malformed-numeric-boundaries`, `RECOVERY.numeric-failures` |
| `lex-scientific-incomplete-sign` | `lexer/lexical-failures.json` | `DIAGNOSTICS.result-phase-policy`, `RECOVERY.lexical-result`, `RECOVERY.progress-invariants`, `RECOVERY.parser-phase-gate`, `FIXTURES.lexical-expectations`, `FIXTURES.diagnostic-mapping`, `TOKEN-SPEC.unsupported-number-notation`, `DIAGNOSTICS.malformed-numeric-boundaries`, `RECOVERY.numeric-failures` |
| `lex-alternate-base-empty` | `lexer/lexical-failures.json` | `DIAGNOSTICS.result-phase-policy`, `RECOVERY.lexical-result`, `RECOVERY.progress-invariants`, `RECOVERY.parser-phase-gate`, `FIXTURES.lexical-expectations`, `FIXTURES.diagnostic-mapping`, `TOKEN-SPEC.unsupported-number-notation`, `DIAGNOSTICS.malformed-numeric-boundaries`, `RECOVERY.numeric-failures` |
| `lex-hex-notation` | `lexer/lexical-failures.json` | `DIAGNOSTICS.result-phase-policy`, `RECOVERY.lexical-result`, `RECOVERY.progress-invariants`, `RECOVERY.parser-phase-gate`, `FIXTURES.lexical-expectations`, `FIXTURES.diagnostic-mapping`, `TOKEN-SPEC.unsupported-number-notation`, `DIAGNOSTICS.malformed-numeric-boundaries`, `RECOVERY.numeric-failures` |
| `lex-hex-boundary` | `lexer/lexical-failures.json` | `DIAGNOSTICS.result-phase-policy`, `RECOVERY.lexical-result`, `RECOVERY.progress-invariants`, `RECOVERY.parser-phase-gate`, `FIXTURES.lexical-expectations`, `FIXTURES.diagnostic-mapping`, `TOKEN-SPEC.unsupported-number-notation`, `DIAGNOSTICS.malformed-numeric-boundaries`, `RECOVERY.numeric-failures` |
| `lex-hex-invalid-digit-exact-boundary` | `lexer/lexical-failures.json` | `DIAGNOSTICS.result-phase-policy`, `RECOVERY.lexical-result`, `RECOVERY.progress-invariants`, `RECOVERY.parser-phase-gate`, `FIXTURES.lexical-expectations`, `FIXTURES.diagnostic-mapping`, `TOKEN-SPEC.unsupported-number-notation`, `DIAGNOSTICS.malformed-numeric-boundaries`, `RECOVERY.numeric-failures` |
| `lex-binary-notation` | `lexer/lexical-failures.json` | `DIAGNOSTICS.result-phase-policy`, `RECOVERY.lexical-result`, `RECOVERY.progress-invariants`, `RECOVERY.parser-phase-gate`, `FIXTURES.lexical-expectations`, `FIXTURES.diagnostic-mapping`, `TOKEN-SPEC.unsupported-number-notation`, `DIAGNOSTICS.malformed-numeric-boundaries`, `RECOVERY.numeric-failures` |
| `lex-repeated-decimal-exact-boundary` | `lexer/lexical-failures.json` | `DIAGNOSTICS.result-phase-policy`, `RECOVERY.lexical-result`, `RECOVERY.progress-invariants`, `RECOVERY.parser-phase-gate`, `FIXTURES.lexical-expectations`, `FIXTURES.diagnostic-mapping`, `TOKEN-SPEC.malformed-decimals`, `DIAGNOSTICS.malformed-numeric-boundaries`, `RECOVERY.numeric-failures` |
| `lex-invalid-leading-underscore` | `lexer/lexical-failures.json` | `DIAGNOSTICS.result-phase-policy`, `RECOVERY.lexical-result`, `RECOVERY.progress-invariants`, `RECOVERY.parser-phase-gate`, `FIXTURES.lexical-expectations`, `FIXTURES.diagnostic-mapping`, `RECOVERY.invalid-source-character`, `DIAGNOSTICS.data-model`, `DIAGNOSTICS.stable-data`, `DIAGNOSTICS.unexpected-source-labels`, `IMPLEMENTATION.result-records`, `IMPLEMENTATION.failure-classification` |
| `lex-invalid-character-closed-string` | `lexer/lexical-failures.json` | `DIAGNOSTICS.result-phase-policy`, `RECOVERY.lexical-result`, `RECOVERY.progress-invariants`, `RECOVERY.parser-phase-gate`, `FIXTURES.lexical-expectations`, `FIXTURES.diagnostic-mapping`, `TOKEN-SPEC.strings`, `RECOVERY.invalid-source-character` |
| `lex-invalid-character-unclosed-string` | `lexer/lexical-failures.json` | `DIAGNOSTICS.result-phase-policy`, `RECOVERY.lexical-result`, `RECOVERY.progress-invariants`, `RECOVERY.parser-phase-gate`, `FIXTURES.lexical-expectations`, `FIXTURES.diagnostic-mapping`, `TOKEN-SPEC.strings`, `RECOVERY.invalid-source-character`, `RECOVERY.unclosed-string` |
| `lex-invalid-character-line-comment` | `lexer/lexical-failures.json` | `DIAGNOSTICS.result-phase-policy`, `RECOVERY.lexical-result`, `RECOVERY.progress-invariants`, `RECOVERY.parser-phase-gate`, `FIXTURES.lexical-expectations`, `FIXTURES.diagnostic-mapping`, `TOKEN-SPEC.trivia-comments`, `RECOVERY.invalid-source-character` |
| `lex-invalid-character-block-comment` | `lexer/lexical-failures.json` | `DIAGNOSTICS.result-phase-policy`, `RECOVERY.lexical-result`, `RECOVERY.progress-invariants`, `RECOVERY.parser-phase-gate`, `FIXTURES.lexical-expectations`, `FIXTURES.diagnostic-mapping`, `TOKEN-SPEC.trivia-comments`, `RECOVERY.invalid-source-character` |
| `lex-malformed-gap-preserves-spans` | `lexer/lexical-failures.json` | `DIAGNOSTICS.result-phase-policy`, `RECOVERY.lexical-result`, `RECOVERY.progress-invariants`, `RECOVERY.parser-phase-gate`, `FIXTURES.lexical-expectations`, `FIXTURES.diagnostic-mapping`, `RECOVERY.invalid-source-character`, `RECOVERY.partial-token-adjacency` |
| `lex-unclosed-string-lf` | `lexer/lexical-failures.json` | `DIAGNOSTICS.result-phase-policy`, `RECOVERY.lexical-result`, `RECOVERY.progress-invariants`, `RECOVERY.parser-phase-gate`, `FIXTURES.lexical-expectations`, `FIXTURES.diagnostic-mapping`, `TOKEN-SPEC.strings`, `RECOVERY.unclosed-string` |
| `lex-unclosed-string-cr` | `lexer/lexical-failures.json` | `DIAGNOSTICS.result-phase-policy`, `RECOVERY.lexical-result`, `RECOVERY.progress-invariants`, `RECOVERY.parser-phase-gate`, `FIXTURES.lexical-expectations`, `FIXTURES.diagnostic-mapping`, `TOKEN-SPEC.strings`, `RECOVERY.unclosed-string` |
| `lex-unclosed-string-crlf` | `lexer/lexical-failures.json` | `DIAGNOSTICS.result-phase-policy`, `RECOVERY.lexical-result`, `RECOVERY.progress-invariants`, `RECOVERY.parser-phase-gate`, `FIXTURES.lexical-expectations`, `FIXTURES.diagnostic-mapping`, `TOKEN-SPEC.strings`, `RECOVERY.unclosed-string` |
| `lex-unclosed-string-eof` | `lexer/lexical-failures.json` | `DIAGNOSTICS.result-phase-policy`, `RECOVERY.lexical-result`, `RECOVERY.progress-invariants`, `RECOVERY.parser-phase-gate`, `FIXTURES.lexical-expectations`, `FIXTURES.diagnostic-mapping`, `TOKEN-SPEC.strings`, `RECOVERY.unclosed-string` |
| `lex-unterminated-block-comment` | `lexer/lexical-failures.json` | `DIAGNOSTICS.result-phase-policy`, `RECOVERY.lexical-result`, `RECOVERY.progress-invariants`, `RECOVERY.parser-phase-gate`, `FIXTURES.lexical-expectations`, `FIXTURES.diagnostic-mapping`, `TOKEN-SPEC.trivia-comments`, `RECOVERY.unterminated-block-comment` |
| `lex-incomplete-logical-operators` | `lexer/lexical-failures.json` | `DIAGNOSTICS.result-phase-policy`, `RECOVERY.lexical-result`, `RECOVERY.progress-invariants`, `RECOVERY.parser-phase-gate`, `FIXTURES.lexical-expectations`, `FIXTURES.diagnostic-mapping`, `TOKEN-SPEC.operators-maximal-munch`, `RECOVERY.incomplete-logical-operator` |
| `lex-diagnostic-limit-exactly-twenty` | `lexer/lexical-failures.json` | `DIAGNOSTICS.result-phase-policy`, `RECOVERY.lexical-result`, `RECOVERY.progress-invariants`, `RECOVERY.parser-phase-gate`, `FIXTURES.lexical-expectations`, `FIXTURES.diagnostic-mapping`, `DIAGNOSTICS.ordering-limit`, `RECOVERY.diagnostic-limit` |
| `lex-diagnostic-limit-truncated-continues` | `lexer/lexical-failures.json` | `DIAGNOSTICS.result-phase-policy`, `RECOVERY.lexical-result`, `RECOVERY.progress-invariants`, `RECOVERY.parser-phase-gate`, `FIXTURES.lexical-expectations`, `FIXTURES.diagnostic-mapping`, `DIAGNOSTICS.ordering-limit`, `RECOVERY.diagnostic-limit` |
| `location-empty-source` | `locations/source-locations.json` | `SOURCE-LOCATIONS.byte-spans`, `TOKEN-SPEC.eof` |
| `location-adjacent-quantity-boundary` | `locations/source-locations.json` | `SOURCE-LOCATIONS.trivia-adjacency` |
| `location-space-detached-quantity-boundary` | `locations/source-locations.json` | `SOURCE-LOCATIONS.trivia-adjacency` |
| `location-comment-detached-quantity-boundary` | `locations/source-locations.json` | `SOURCE-LOCATIONS.trivia-adjacency`, `TOKEN-SPEC.trivia-comments` |
| `location-newline-and-tab-forms` | `locations/source-locations.json` | `SOURCE-LOCATIONS.human-positions`, `SOURCE-LOCATIONS.newlines`, `SOURCE-LOCATIONS.columns-tabs` |
| `location-multiline-block-comment` | `locations/source-locations.json` | `SOURCE-LOCATIONS.newlines`, `SOURCE-LOCATIONS.columns-tabs`, `TOKEN-SPEC.trivia-comments` |
| `location-invalid-unicode-scalar` | `locations/source-locations.json` | `DIAGNOSTICS.result-phase-policy`, `RECOVERY.lexical-result`, `RECOVERY.progress-invariants`, `RECOVERY.parser-phase-gate`, `FIXTURES.lexical-expectations`, `FIXTURES.diagnostic-mapping`, `SOURCE-LOCATIONS.columns-tabs`, `RECOVERY.invalid-source-character` |
| `frontend-pilot-invalid-utf8-phase-gate` | `frontend/pilot.json` | `SOURCE-LOCATIONS.byte-spans`, `SOURCE-LOCATIONS.human-positions`, `SOURCE-LOCATIONS.newlines`, `SOURCE-LOCATIONS.phase-ownership`, `DIAGNOSTICS.result-phase-policy`, `DIAGNOSTICS.lexical-codes`, `RECOVERY.lexical-result`, `RECOVERY.progress-invariants`, `RECOVERY.invalid-utf8`, `RECOVERY.parser-phase-gate`, `FIXTURES.source-input`, `FIXTURES.entrypoints`, `FIXTURES.lexical-expectations`, `FIXTURES.location-mapping`, `FIXTURES.diagnostic-mapping`, `IMPLEMENTATION.byte-source-boundary` |
| `frontend-pilot-uninitialized-let-ast` | `frontend/pilot.json` | `GRAMMAR.program-functions`, `GRAMMAR.blocks-statements`, `GRAMMAR.declarations`, `AST-SCHEMA.source-references`, `AST-SCHEMA.source-file-functions`, `AST-SCHEMA.blocks-statements`, `AST-SCHEMA.declarations`, `AST-SCHEMA.span-composition`, `AST-SCHEMA.success-invariants`, `SOURCE-LOCATIONS.ast-spans`, `FIXTURES.parse-expectations`, `FIXTURES.ast-mapping` |
| `frontend-pilot-const-initializer-required` | `frontend/pilot.json` | `GRAMMAR.declarations`, `AST-SCHEMA.failure-boundary`, `SOURCE-LOCATIONS.missing-syntax`, `DIAGNOSTICS.absent-syntax-labels`, `DIAGNOSTICS.specialized-syntax-codes`, `RECOVERY.parser-failure`, `FIXTURES.parse-expectations`, `FIXTURES.diagnostic-mapping` |
| `parse-empty-source-ast` | `parser/ast-success.json` | `GRAMMAR.program-functions`, `GRAMMAR.blocks-statements`, `AST-SCHEMA.source-references`, `AST-SCHEMA.source-file-functions`, `AST-SCHEMA.blocks-statements`, `AST-SCHEMA.span-composition`, `AST-SCHEMA.success-invariants`, `SOURCE-LOCATIONS.ast-spans`, `FIXTURES.parse-expectations`, `FIXTURES.ast-mapping` |
| `parse-functions-parameters-declarations` | `parser/ast-success.json` | `GRAMMAR.program-functions`, `GRAMMAR.blocks-statements`, `AST-SCHEMA.source-references`, `AST-SCHEMA.source-file-functions`, `AST-SCHEMA.blocks-statements`, `AST-SCHEMA.span-composition`, `AST-SCHEMA.success-invariants`, `SOURCE-LOCATIONS.ast-spans`, `FIXTURES.parse-expectations`, `FIXTURES.ast-mapping`, `AST-SCHEMA.separated-collections`, `GRAMMAR.declarations`, `AST-SCHEMA.declarations`, `GRAMMAR.transfer-assertion`, `GRAMMAR.control-transfer-context`, `AST-SCHEMA.transfer-assertion`, `GRAMMAR.annotations`, `GRAMMAR.annotation-consistency`, `AST-SCHEMA.annotations`, `GRAMMAR.expression-precedence`, `AST-SCHEMA.expressions`, `GRAMMAR.input-syntax`, `GRAMMAR.unit-expressions`, `GRAMMAR.unit-exponents`, `GRAMMAR.unit-limits`, `AST-SCHEMA.unit-expressions` |
| `parse-assignment-update-call-io-statements` | `parser/ast-success.json` | `GRAMMAR.program-functions`, `GRAMMAR.blocks-statements`, `AST-SCHEMA.source-references`, `AST-SCHEMA.source-file-functions`, `AST-SCHEMA.blocks-statements`, `AST-SCHEMA.span-composition`, `AST-SCHEMA.success-invariants`, `SOURCE-LOCATIONS.ast-spans`, `FIXTURES.parse-expectations`, `FIXTURES.ast-mapping`, `AST-SCHEMA.separated-collections`, `GRAMMAR.assignments-updates`, `AST-SCHEMA.assignments-updates`, `GRAMMAR.output-calls`, `AST-SCHEMA.output-calls`, `GRAMMAR.transfer-assertion`, `GRAMMAR.control-transfer-context`, `AST-SCHEMA.transfer-assertion`, `GRAMMAR.expression-precedence`, `AST-SCHEMA.expressions`, `GRAMMAR.calls`, `AST-SCHEMA.grouping-calls`, `GRAMMAR.quantities`, `GRAMMAR.quantity-attachment`, `GRAMMAR.input-syntax`, `GRAMMAR.unit-expressions`, `GRAMMAR.unit-exponents`, `GRAMMAR.unit-limits`, `AST-SCHEMA.unit-expressions`, `GRAMMAR.semantic-boundary` |
| `parse-expression-and-quantity-forms` | `parser/ast-success.json` | `GRAMMAR.program-functions`, `GRAMMAR.blocks-statements`, `AST-SCHEMA.source-references`, `AST-SCHEMA.source-file-functions`, `AST-SCHEMA.blocks-statements`, `AST-SCHEMA.span-composition`, `AST-SCHEMA.success-invariants`, `SOURCE-LOCATIONS.ast-spans`, `FIXTURES.parse-expectations`, `FIXTURES.ast-mapping`, `AST-SCHEMA.separated-collections`, `GRAMMAR.declarations`, `AST-SCHEMA.declarations`, `GRAMMAR.annotations`, `GRAMMAR.annotation-consistency`, `AST-SCHEMA.annotations`, `GRAMMAR.expression-precedence`, `AST-SCHEMA.expressions`, `GRAMMAR.calls`, `AST-SCHEMA.grouping-calls`, `AST-SCHEMA.operators-conversions`, `GRAMMAR.quantities`, `GRAMMAR.quantity-attachment`, `GRAMMAR.unit-expressions`, `GRAMMAR.unit-exponents`, `GRAMMAR.unit-limits`, `AST-SCHEMA.unit-expressions` |
| `parse-conditionals-and-loops` | `parser/control-units.json` | `GRAMMAR.program-functions`, `GRAMMAR.blocks-statements`, `AST-SCHEMA.source-references`, `AST-SCHEMA.source-file-functions`, `AST-SCHEMA.blocks-statements`, `AST-SCHEMA.span-composition`, `AST-SCHEMA.success-invariants`, `SOURCE-LOCATIONS.ast-spans`, `FIXTURES.parse-expectations`, `FIXTURES.ast-mapping`, `GRAMMAR.assignments-updates`, `AST-SCHEMA.assignments-updates`, `GRAMMAR.conditionals`, `AST-SCHEMA.conditionals`, `GRAMMAR.loops`, `AST-SCHEMA.loops`, `GRAMMAR.transfer-assertion`, `GRAMMAR.control-transfer-context`, `AST-SCHEMA.transfer-assertion`, `GRAMMAR.expression-precedence`, `AST-SCHEMA.expressions`, `AST-SCHEMA.operators-conversions` |
| `parse-unit-expression-structures` | `parser/control-units.json` | `GRAMMAR.program-functions`, `GRAMMAR.blocks-statements`, `AST-SCHEMA.source-references`, `AST-SCHEMA.source-file-functions`, `AST-SCHEMA.blocks-statements`, `AST-SCHEMA.span-composition`, `AST-SCHEMA.success-invariants`, `SOURCE-LOCATIONS.ast-spans`, `FIXTURES.parse-expectations`, `FIXTURES.ast-mapping`, `GRAMMAR.declarations`, `AST-SCHEMA.declarations`, `GRAMMAR.annotations`, `GRAMMAR.annotation-consistency`, `AST-SCHEMA.annotations`, `GRAMMAR.expression-precedence`, `AST-SCHEMA.expressions`, `GRAMMAR.quantities`, `GRAMMAR.quantity-attachment`, `GRAMMAR.unit-expressions`, `GRAMMAR.unit-exponents`, `GRAMMAR.unit-limits`, `AST-SCHEMA.unit-expressions` |
| `parse-missing-closing-brace-eof` | `parser/syntax-failures.json` | `DIAGNOSTICS.general-syntax-codes`, `RECOVERY.parser-failure`, `AST-SCHEMA.failure-boundary`, `SOURCE-LOCATIONS.missing-syntax` |
| `parse-missing-unit-bracket-eof` | `parser/syntax-failures.json` | `DIAGNOSTICS.general-syntax-codes`, `RECOVERY.parser-failure`, `AST-SCHEMA.failure-boundary`, `SOURCE-LOCATIONS.missing-syntax`, `DIAGNOSTICS.expression-delimiter-labels` |
| `parse-expected-identifier` | `parser/syntax-failures.json` | `DIAGNOSTICS.general-syntax-codes`, `RECOVERY.parser-failure`, `AST-SCHEMA.failure-boundary` |
| `parse-expected-expression` | `parser/syntax-failures.json` | `DIAGNOSTICS.general-syntax-codes`, `RECOVERY.parser-failure`, `AST-SCHEMA.failure-boundary` |
| `parse-expected-statement` | `parser/syntax-failures.json` | `DIAGNOSTICS.general-syntax-codes`, `RECOVERY.parser-failure`, `AST-SCHEMA.failure-boundary` |
| `parse-expected-function` | `parser/syntax-failures.json` | `DIAGNOSTICS.general-syntax-codes`, `RECOVERY.parser-failure`, `AST-SCHEMA.failure-boundary` |
| `parse-detached-simple-quantity` | `parser/syntax-failures.json` | `DIAGNOSTICS.specialized-syntax-codes`, `RECOVERY.parser-failure`, `AST-SCHEMA.failure-boundary`, `DIAGNOSTICS.detached-quantity-labels` |
| `parse-detached-simple-quantity-comment` | `parser/syntax-failures.json` | `DIAGNOSTICS.specialized-syntax-codes`, `RECOVERY.parser-failure`, `AST-SCHEMA.failure-boundary`, `DIAGNOSTICS.detached-quantity-labels` |
| `parse-detached-compound-quantity-space` | `parser/syntax-failures.json` | `DIAGNOSTICS.specialized-syntax-codes`, `RECOVERY.parser-failure`, `AST-SCHEMA.failure-boundary`, `DIAGNOSTICS.detached-quantity-labels` |
| `parse-detached-compound-quantity` | `parser/syntax-failures.json` | `DIAGNOSTICS.specialized-syntax-codes`, `RECOVERY.parser-failure`, `AST-SCHEMA.failure-boundary`, `DIAGNOSTICS.detached-quantity-labels` |
| `parse-const-initializer-required-again` | `parser/syntax-failures.json` | `DIAGNOSTICS.specialized-syntax-codes`, `RECOVERY.parser-failure`, `AST-SCHEMA.failure-boundary` |
| `parse-invalid-declaration-annotation` | `parser/syntax-failures.json` | `DIAGNOSTICS.specialized-syntax-codes`, `RECOVERY.parser-failure`, `AST-SCHEMA.failure-boundary` |
| `parse-invalid-input-position` | `parser/syntax-failures.json` | `DIAGNOSTICS.specialized-syntax-codes`, `RECOVERY.parser-failure`, `AST-SCHEMA.failure-boundary` |
| `parse-input-arguments-not-allowed` | `parser/syntax-failures.json` | `DIAGNOSTICS.specialized-syntax-codes`, `RECOVERY.parser-failure`, `AST-SCHEMA.failure-boundary` |
| `parse-input-annotation-required` | `parser/syntax-failures.json` | `DIAGNOSTICS.specialized-syntax-codes`, `RECOVERY.parser-failure`, `AST-SCHEMA.failure-boundary` |
| `parse-assignment-not-expression` | `parser/syntax-failures.json` | `DIAGNOSTICS.specialized-syntax-codes`, `RECOVERY.parser-failure`, `AST-SCHEMA.failure-boundary` |
| `parse-update-not-expression` | `parser/syntax-failures.json` | `DIAGNOSTICS.specialized-syntax-codes`, `RECOVERY.parser-failure`, `AST-SCHEMA.failure-boundary` |
| `parse-chained-relational` | `parser/syntax-failures.json` | `DIAGNOSTICS.specialized-syntax-codes`, `RECOVERY.parser-failure`, `AST-SCHEMA.failure-boundary`, `GRAMMAR.nonchaining-comparisons` |
| `parse-chained-equality` | `parser/syntax-failures.json` | `DIAGNOSTICS.specialized-syntax-codes`, `RECOVERY.parser-failure`, `AST-SCHEMA.failure-boundary`, `GRAMMAR.nonchaining-comparisons` |
| `parse-misplaced-to` | `parser/syntax-failures.json` | `DIAGNOSTICS.specialized-syntax-codes`, `RECOVERY.parser-failure`, `AST-SCHEMA.failure-boundary` |
| `parse-misplaced-then` | `parser/syntax-failures.json` | `DIAGNOSTICS.specialized-syntax-codes`, `RECOVERY.parser-failure`, `AST-SCHEMA.failure-boundary` |
| `parse-misplaced-do` | `parser/syntax-failures.json` | `DIAGNOSTICS.specialized-syntax-codes`, `RECOVERY.parser-failure`, `AST-SCHEMA.failure-boundary` |
| `parse-break-outside-loop` | `parser/syntax-failures.json` | `DIAGNOSTICS.specialized-syntax-codes`, `RECOVERY.parser-failure`, `AST-SCHEMA.failure-boundary` |
| `parse-continue-outside-loop` | `parser/syntax-failures.json` | `DIAGNOSTICS.specialized-syntax-codes`, `RECOVERY.parser-failure`, `AST-SCHEMA.failure-boundary` |
| `parse-return-value-required` | `parser/syntax-failures.json` | `DIAGNOSTICS.specialized-syntax-codes`, `RECOVERY.parser-failure`, `AST-SCHEMA.failure-boundary` |
| `parse-return-value-forbidden` | `parser/syntax-failures.json` | `DIAGNOSTICS.specialized-syntax-codes`, `RECOVERY.parser-failure`, `AST-SCHEMA.failure-boundary` |
| `parse-empty-unit-annotation` | `parser/syntax-failures.json` | `DIAGNOSTICS.unit-syntax-codes`, `RECOVERY.parser-failure`, `AST-SCHEMA.failure-boundary` |
| `parse-expected-unit-factor` | `parser/syntax-failures.json` | `DIAGNOSTICS.unit-syntax-codes`, `RECOVERY.parser-failure`, `AST-SCHEMA.failure-boundary` |
| `parse-missing-unit-exponent` | `parser/syntax-failures.json` | `DIAGNOSTICS.unit-syntax-codes`, `RECOVERY.parser-failure`, `AST-SCHEMA.failure-boundary` |
| `parse-invalid-unit-exponent-plus` | `parser/syntax-failures.json` | `DIAGNOSTICS.unit-syntax-codes`, `RECOVERY.parser-failure`, `AST-SCHEMA.failure-boundary` |
| `parse-unit-exponent-out-of-range` | `parser/syntax-failures.json` | `DIAGNOSTICS.unit-syntax-codes`, `RECOVERY.parser-failure`, `AST-SCHEMA.failure-boundary` |
| `parse-unit-repeated-division` | `parser/syntax-failures.json` | `DIAGNOSTICS.unit-syntax-codes`, `RECOVERY.parser-failure`, `AST-SCHEMA.failure-boundary` |
| `parse-unit-nested-division` | `parser/syntax-failures.json` | `DIAGNOSTICS.unit-syntax-codes`, `RECOVERY.parser-failure`, `AST-SCHEMA.failure-boundary` |
| `parse-unit-grouped-numerator` | `parser/syntax-failures.json` | `DIAGNOSTICS.unit-syntax-codes`, `RECOVERY.parser-failure`, `AST-SCHEMA.failure-boundary` |
| `parse-unit-group-power` | `parser/syntax-failures.json` | `DIAGNOSTICS.unit-syntax-codes`, `RECOVERY.parser-failure`, `AST-SCHEMA.failure-boundary` |
| `parse-unit-implicit-multiplication` | `parser/syntax-failures.json` | `DIAGNOSTICS.unit-syntax-codes`, `RECOVERY.parser-failure`, `AST-SCHEMA.failure-boundary` |
| `parse-unit-numeric-factor` | `parser/syntax-failures.json` | `DIAGNOSTICS.unit-syntax-codes`, `RECOVERY.parser-failure`, `AST-SCHEMA.failure-boundary` |
| `parse-unit-unparenthesized-product-denominator` | `parser/syntax-failures.json` | `DIAGNOSTICS.unit-syntax-codes`, `RECOVERY.parser-failure`, `AST-SCHEMA.failure-boundary` |
| `parse-too-many-unit-factors` | `parser/syntax-failures.json` | `DIAGNOSTICS.unit-syntax-codes`, `RECOVERY.parser-failure`, `AST-SCHEMA.failure-boundary`, `DIAGNOSTICS.limit-labels` |
| `parse-unit-annotation-too-long` | `parser/syntax-failures.json` | `DIAGNOSTICS.unit-syntax-codes`, `RECOVERY.parser-failure`, `AST-SCHEMA.failure-boundary`, `DIAGNOSTICS.limit-labels` |

### Diagnostic code to fixture

Every source diagnostic code must have at least one fixture. `ICE001` is excluded from ordinary malformed-source conformance fixtures.

| Code family | Required coverage | Fixture IDs |
| --- | --- | --- |
| `LEX001` | Required code, labels, stable data, and phase result | `frontend-pilot-invalid-utf8-phase-gate` |
| `LEX002` | Required code, labels, stable data, and phase result | `lex-invalid-leading-underscore`, `lex-invalid-character-closed-string`, `lex-invalid-character-unclosed-string`, `lex-invalid-character-line-comment`, `lex-invalid-character-block-comment`, `lex-malformed-gap-preserves-spans`, `lex-diagnostic-limit-exactly-twenty`, `lex-diagnostic-limit-truncated-continues`, `location-invalid-unicode-scalar` |
| `LEX003` | Required code, labels, stable data, and phase result | `lex-leading-zero` |
| `LEX004` | Required code, labels, stable data, and phase result | `lex-malformed-leading-decimal`, `lex-malformed-trailing-decimal`, `lex-malformed-repeated-decimal`, `lex-repeated-decimal-exact-boundary` |
| `LEX005` | Required code, labels, stable data, and phase result | `lex-numeric-separator`, `lex-numeric-separator-exact-boundary` |
| `LEX006` | Required code, labels, stable data, and phase result | `lex-scientific-boundary`, `lex-scientific-notation`, `lex-scientific-incomplete-sign` |
| `LEX007` | Required code, labels, stable data, and phase result | `lex-alternate-base-empty`, `lex-hex-notation`, `lex-hex-boundary`, `lex-hex-invalid-digit-exact-boundary`, `lex-binary-notation` |
| `LEX008` | Required code, labels, stable data, and phase result | `lex-invalid-character-unclosed-string`, `lex-unclosed-string-lf`, `lex-unclosed-string-cr`, `lex-unclosed-string-crlf`, `lex-unclosed-string-eof` |
| `LEX009` | Required code, labels, stable data, and phase result | `lex-unterminated-block-comment` |
| `LEX010` | Required code, labels, stable data, and phase result | `lex-incomplete-logical-operators` |
| `SYN002` | Required code, labels, stable data, and phase result | `parse-missing-closing-brace-eof`, `parse-missing-unit-bracket-eof` |
| `SYN003` | Required code, labels, stable data, and phase result | `parse-expected-identifier` |
| `SYN004` | Required code, labels, stable data, and phase result | `parse-expected-expression` |
| `SYN005` | Required code, labels, stable data, and phase result | `parse-expected-statement` |
| `SYN006` | Required code, labels, stable data, and phase result | `parse-expected-function` |
| `SYN010` | Required code, labels, stable data, and phase result | `parse-detached-simple-quantity`, `parse-detached-simple-quantity-comment`, `parse-detached-compound-quantity-space`, `parse-detached-compound-quantity` |
| `SYN011` | Required code, labels, stable data, and phase result | `frontend-pilot-const-initializer-required`, `parse-const-initializer-required-again` |
| `SYN012` | Required code, labels, stable data, and phase result | `parse-invalid-declaration-annotation` |
| `SYN013` | Required code, labels, stable data, and phase result | `parse-invalid-input-position` |
| `SYN014` | Required code, labels, stable data, and phase result | `parse-input-arguments-not-allowed` |
| `SYN015` | Required code, labels, stable data, and phase result | `parse-input-annotation-required` |
| `SYN016` | Required code, labels, stable data, and phase result | `parse-assignment-not-expression` |
| `SYN017` | Required code, labels, stable data, and phase result | `parse-update-not-expression` |
| `SYN018` | Required code, labels, stable data, and phase result | `parse-chained-relational` |
| `SYN019` | Required code, labels, stable data, and phase result | `parse-chained-equality` |
| `SYN020` | Required code, labels, stable data, and phase result | `parse-misplaced-to`, `parse-misplaced-then`, `parse-misplaced-do` |
| `SYN021` | Required code, labels, stable data, and phase result | `parse-break-outside-loop` |
| `SYN022` | Required code, labels, stable data, and phase result | `parse-continue-outside-loop` |
| `SYN023` | Required code, labels, stable data, and phase result | `parse-return-value-required` |
| `SYN024` | Required code, labels, stable data, and phase result | `parse-return-value-forbidden` |
| `SYN030` | Required code, labels, stable data, and phase result | `parse-empty-unit-annotation` |
| `SYN031` | Required code, labels, stable data, and phase result | `parse-expected-unit-factor` |
| `SYN032` | Required code, labels, stable data, and phase result | `parse-missing-unit-exponent` |
| `SYN033` | Required code, labels, stable data, and phase result | `parse-invalid-unit-exponent-plus` |
| `SYN034` | Required code, labels, stable data, and phase result | `parse-unit-exponent-out-of-range` |
| `SYN035` | Required code, labels, stable data, and phase result | `parse-unit-repeated-division`, `parse-unit-nested-division`, `parse-unit-grouped-numerator`, `parse-unit-group-power`, `parse-unit-implicit-multiplication`, `parse-unit-numeric-factor`, `parse-unit-unparenthesized-product-denominator` |
| `SYN036` | Required code, labels, stable data, and phase result | `parse-too-many-unit-factors` |
| `SYN037` | Required code, labels, stable data, and phase result | `parse-unit-annotation-too-long` |
| `ICE001` | Process-level handling only | N/A |

### Token and AST coverage

The final mechanical coverage audit passed with 93 indexed fixtures across eight data files. The suite covers all 62 token kinds in `TOKEN-SPEC.md`, all 53 tagged AST node kinds in `AST-SCHEMA.md`, all ten lexical diagnostic codes, and all 28 active syntax diagnostic codes. `SYN001` is intentionally unused, and `ICE001` remains process-level rather than malformed-source fixture data.

The audit also verified unique fixture IDs, strict JSON without duplicate keys, indexed-file completeness, token lexemes and byte spans, physical `EOF`, required source positions, AST field sets, token-index bounds, node-span composition, diagnostic limits, reciprocal rule links, and the mandatory boundary-case fixture IDs.

## Completion gate

This registry is complete because:

- no fixture-required row contains `PENDING`;
- every fixture `covers.rules` value resolves to one row above;
- every indexed fixture appears in the fixture-to-rule reverse index;
- every token kind and AST kind has required coverage;
- every `LEX` and `SYN` code has required coverage;
- `ICE001` remains outside malformed-source fixtures;
- no fixture requires name resolution, unit checking, type checking, evaluation, or runtime behavior; and
- the final documentation audit finds no controlling rule without either fixture evidence or an explicit `N/A` process rationale.

