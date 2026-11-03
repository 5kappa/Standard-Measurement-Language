# Standard Measurement Language Lexer Development Roadmap

Status: active; R0 through R2 complete

Applies to: initial SML version 0.1 lexer implementation only

Engineering baseline: Python 3.11.9, standard library only

Depends on: [`README.md`](README.md), [`IMPLEMENTATION.md`](IMPLEMENTATION.md), [`TOKEN-SPEC.md`](TOKEN-SPEC.md), [`SOURCE-LOCATIONS.md`](SOURCE-LOCATIONS.md), [`DIAGNOSTICS.md`](DIAGNOSTICS.md), [`RECOVERY.md`](RECOVERY.md), and [`fixtures/README.md`](fixtures/README.md)

## Purpose

This roadmap turns the accepted lexer contracts and fixtures into small implementation slices. Each milestone has one main responsibility, names the files it may change, identifies the fixtures it unlocks, and defines an observable completion gate.

The accepted contracts and indexed fixtures remain authoritative. This document sequences the work; it does not change tokenization, locations, diagnostics, recovery, or fixture meaning.

## Progress

- [x] R0 — Confirm repository and contract baseline
- [x] R1 — Establish lexer records, source cursor, and focused test harness
- [x] R2 — Pass the `10m` lexer pilot
- [ ] R3 — Complete ordinary names, numbers, signs, EOF, and basic adjacency
- [ ] R4 — Complete token inventory, delimiters, and maximal-munch operators
- [ ] R5 — Complete strings, trivia, newlines, tabs, and comment adjacency
- [ ] R6 — Complete UTF-8 and canonical-character diagnostics
- [ ] R7 — Complete malformed-number diagnostics and continuation
- [ ] R8 — Complete unclosed strings and unterminated block comments
- [ ] R9 — Complete logical-operator recovery, diagnostic ordering, and the reporting cap
- [ ] R10 — Run the lexer-only conformance gate

Mark a milestone complete only after its tests pass under the exact Python 3.11.9 reference interpreter and its completion criteria are met.

## Lexer/parser boundary

The public lexer boundary is:

```text
lex(source: bytes) -> LexSuccess | LexFailure
```

The lexer owns original-byte scanning, UTF-8 and canonical-character validation, token kinds and boundaries, original lexemes, byte spans and positions, trivia handling, maximal munch, lexical diagnostics, continuation, and one physical-end `EOF`.

The parser may later receive only `LexSuccess.tokens`. `LexFailure.partial_tokens` are test/debug data and must never be parser input. This roadmap tests that gate as a result invariant but does not design or implement parsing.

## Planned module boundaries

| File | Lexer-only responsibility | Must not own |
| --- | --- | --- |
| `sml_frontend/source.py` | Immutable source spans and positions; a byte cursor that advances through ASCII, UTF-8 scalars, `LF`, `CR`, `CRLF`, tabs, and invalid bytes according to the accepted location rules | Token recognition, diagnostic selection, file I/O |
| `sml_frontend/token.py` | Complete `TokenKind` enum and immutable `Token` record | Keyword scanning logic, unit lookup, parser categories |
| `sml_frontend/diagnostic.py` | Lexical diagnostic codes `LEX001`–`LEX010`, phase/severity/label records, one direct stable-data mapping, and immutable diagnostic records | English rendering as conformance data, syntax diagnostics beyond shared enum placeholders |
| `sml_frontend/lexer.py` | `LexSuccess`, `LexFailure`, scanner state, token scanners, trivia scanning, diagnostic accumulation, recovery, and public `lex(bytes)` | File access, parser calls, AST construction, semantic/unit lookup |
| `sml_frontend/__init__.py` | Stable exports for the lexer API and returned records | Eager CLI work or parser exports |
| `sml_frontend/__main__.py` | Small `argparse` boundary that reads files as bytes, invokes the lexer, and distinguishes file-I/O/internal failures from lexical failures | Decoding the complete file before lexing, parser behavior |
| `tests/fixture_loader.py` | Small test-only decoder for the trusted fixture variants required by the current milestone | Exhaustive format validation, parser/AST decoding before its milestone |
| `tests/test_source.py` | Cursor, byte-span, newline, tab, Unicode-scalar, and invalid-byte unit tests | Scanner integration assertions |
| `tests/test_lexer.py` | Focused scanner and recovery unit tests, including contract cases not exposed through a lexer-entrypoint fixture | Fixture decoding |
| `tests/test_fixtures.py` | Fixture-driven lexer conformance classes | Parser/AST conformance |

`sml_frontend/parser.py`, `sml_frontend/syntax.py`, and parser test modules are intentionally absent during this roadmap.

Fixtures are trusted, version-controlled conformance data. The test loader validates only enough structure to decode and execute the indexed fixture cases. Exhaustive validation of the fixture format is not part of the lexer implementation.

## Verification commands

Use an interpreter whose `--version` is exactly `Python 3.11.9`; do not silently substitute the workstation's default `python` if it differs.

```powershell
python3.11 --version
python3.11 -m unittest tests.test_source
python3.11 -m unittest tests.test_lexer
python3.11 -m unittest tests.test_fixtures
python3.11 -m unittest discover
python3.11 -m compileall sml_frontend tests
```

The command name may be an explicit absolute path instead of `python3.11`, but the reported version remains part of the evidence. Milestone-specific fixture classes named below allow narrow runs such as:

```powershell
python3.11 -m unittest tests.test_fixtures.PilotLexerFixtureTests
```

## Milestones

### R0 — Confirm repository and contract baseline

Status: complete for roadmap preparation.

Purpose: establish that implementation starts from the accepted contracts rather than reconstructing behavior from examples.

Evidence:

- the clean `main` worktree matches `origin/main` at `1c4ffeb`;
- the implementation package and tests do not yet exist;
- `docs/frontend/fixtures/index.json` lists the authoritative fixture files; and
- all lexer/location fixture IDs and the invalid-UTF-8 frontend pilot were inventoried before sequencing the work.

Completion criteria:

- no local changes were overwritten;
- no lexer or parser implementation exists yet; and
- this roadmap is reviewed before R1 begins.

### R1 — Establish lexer records, source cursor, and focused test harness

Status: complete; passing under the exact Python 3.11.9 reference interpreter.

Purpose: create the smallest reusable foundation so later scanner functions share one byte and position model.

Primary files:

- `sml_frontend/source.py`
- `sml_frontend/token.py`
- `sml_frontend/diagnostic.py`
- `sml_frontend/lexer.py` for result records and a scanner shell only
- `tests/test_source.py`
- `tests/test_lexer.py`

Work:

- add immutable dataclasses/enums for spans, positions, tokens, lexical diagnostics, `LexSuccess`, and `LexFailure`;
- keep source as `bytes` and expose only validated token spans as decoded lexemes;
- implement cursor advancement for ordinary ASCII, `LF`, `CR`, `CRLF`, four-column tabs, well-formed UTF-8 scalars, and one-byte invalid-UTF-8 recovery;
- establish scanner progress assertions: every success or failure path consumes a nonempty range unless already at EOF; and
- add focused tests for half-open spans and position advancement without recognizing the full language.

Fixture group unlocked: none yet; this is an internal prerequisite.

Verification:

```powershell
python3.11 -m unittest tests.test_source tests.test_lexer.SourceFoundationTests
python3.11 -m compileall sml_frontend tests
```

Completion criteria:

- source bytes are never normalized or completely pre-decoded;
- cursor tests cover the accepted newline/tab/UTF-8 rules;
- returned public records are immutable; and
- no parser or semantic concept appears in the foundation API.

### R2 — Pass the `10m` lexer pilot

Status: complete; the authoritative pilot and all R1 regressions pass under Python 3.11.9.

Purpose: prove the end-to-end byte-scanner shape with the smallest accepted fixture before widening token coverage.

Primary files:

- `sml_frontend/lexer.py`
- `tests/fixture_loader.py`
- `tests/test_fixtures.py`

Work:

- recognize the minimum decimal-integer, ASCII-identifier, and EOF paths;
- retain exact lexemes and half-open byte spans;
- derive adjacency only from `NUMBER.end_byte == IDENT.start_byte`;
- decode the trusted indexed pilot with a small test-only helper; and
- compare the structured result rather than rendered text.

Fixture group unlocked:

- `lexer/pilot.json`
  - `lex-pilot-attached-quantity-tokens`

Verification:

```powershell
python3.11 -m unittest tests.test_fixtures.PilotLexerFixtureTests
```

Completion criteria:

- `b"10m"` produces `NUMBER("10") [0,2)`, `IDENT("m") [2,3)`, and `EOF [3,3)`;
- the lexer performs no unit lookup and no parsing; and
- the pilot passes through the fixture loader, not only a hand-authored unit test.

### R3 — Complete ordinary names, numbers, signs, EOF, and basic adjacency

Purpose: finish the successful token families that do not require multi-byte operator or comment lookahead.

Primary files: `token.py`, `lexer.py`, `test_lexer.py`, and `test_fixtures.py`.

Work:

- scan complete ASCII identifiers before exact case-sensitive reserved-word classification;
- accept integers and fixed-point decimals while leaving leading signs as separate tokens;
- preserve the explicit `5e -> NUMBER IDENT` boundary; and
- handle empty input, whitespace gaps, and zero-width physical EOF.

Fixture group unlocked:

- `lexer/tokens.json`
  - `lex-keyword-near-misses-identifiers`
  - `lex-accepted-numbers-and-signs`
  - `lex-ordinary-attached-e-identifier`
- `locations/source-locations.json`
  - `location-empty-source`
  - `location-adjacent-quantity-boundary`
  - `location-space-detached-quantity-boundary`

Verification:

```powershell
python3.11 -m unittest tests.test_fixtures.OrdinaryTokenFixtureTests
python3.11 -m unittest tests.test_fixtures.BasicLocationFixtureTests
```

Completion criteria:

- case variants and nonreserved names remain `IDENT`;
- signs never become part of a `NUMBER`;
- whitespace affects span-derived adjacency without becoming a token; and
- every success token collection ends with exactly one physical-end `EOF`.

### R4 — Complete token inventory, delimiters, and maximal-munch operators

Purpose: make every version 0.1 token kind constructible on successful input.

Primary files: `token.py`, `lexer.py`, `test_lexer.py`, and `test_fixtures.py`.

Work:

- add the complete 62-kind enum and exact reserved-spelling table;
- implement delimiter recognition;
- implement longest-valid-operator matching; and
- enforce slash-prefix ordering as `//`, `/*`, `/=`, then `/` while leaving comment bodies for R5.

Fixture group unlocked:

- `lexer/tokens.json`
  - `lex-all-token-kinds`
  - `lex-maximal-munch-boundaries`

Verification:

```powershell
python3.11 -m unittest tests.test_fixtures.TokenInventoryFixtureTests
```

Completion criteria:

- all 62 token kinds appear with their exact original lexemes and spans;
- `--`, `++`, comparison, equality, and assignment operators use maximal munch; and
- context-sensitive validity remains a later parser concern.

### R5 — Complete strings, trivia, newlines, tabs, and comment adjacency

Purpose: finish successful scanning while proving that skipped bytes still control positions and attachment.

Primary files: `source.py`, `lexer.py`, `test_source.py`, `test_lexer.py`, and `test_fixtures.py`.

Work:

- scan complete single-line double-quoted strings with quotes retained in the lexeme;
- skip line comments and first-closer, non-nesting block comments;
- process `LF`, `CR`, and `CRLF` without source normalization;
- apply four-column tab stops; and
- ensure comments create physical span gaps just like whitespace.

Fixture group unlocked:

- `lexer/tokens.json`
  - `lex-complete-strings`
  - `lex-comments-adjacency-and-nonnesting`
- `locations/source-locations.json`
  - `location-comment-detached-quantity-boundary`
  - `location-newline-and-tab-forms`
  - `location-multiline-block-comment`

Verification:

```powershell
python3.11 -m unittest tests.test_source
python3.11 -m unittest tests.test_fixtures.TriviaAndPositionFixtureTests
```

Completion criteria:

- all indexed successful lexer/location fixtures pass;
- `CRLF` advances one logical line while retaining both bytes;
- comments emit no tokens and do not preserve quantity adjacency; and
- nested `/*` inside a block comment is ordinary content.

### R6 — Complete UTF-8 and canonical-character diagnostics

Purpose: introduce lexical failure as structured result data while preserving scanner state and later valid tokens.

Primary files: `source.py`, `diagnostic.py`, `lexer.py`, `test_lexer.py`, and `test_fixtures.py`.

Work:

- implement `LEX001` bytewise invalid-UTF-8 detection and one-byte continuation;
- implement `LEX002` for complete well-formed but noncanonical characters;
- preserve ordinary/string/line-comment/block-comment state across a bad byte or character;
- suppress a `STRING` token when that string contains a lexical failure; and
- return `LexFailure` with ordered diagnostics, valid partial tokens, and physical-end EOF.

Fixture group unlocked:

- `locations/source-locations.json`
  - `location-invalid-unicode-scalar`
- `lexer/lexical-failures.json`
  - `lex-invalid-leading-underscore`
  - `lex-invalid-character-closed-string`
  - `lex-invalid-character-line-comment`
  - `lex-invalid-character-block-comment`
  - `lex-malformed-gap-preserves-spans`
- lexer-owned portion of `frontend/pilot.json`
  - `frontend-pilot-invalid-utf8-phase-gate`

The frontend pilot is included only to verify its lexical result and the fixed `LexFailure -> parse not_run` boundary. It does not authorize a parser implementation.

Verification:

```powershell
python3.11 -m unittest tests.test_lexer.InvalidUtf8Tests
python3.11 -m unittest tests.test_fixtures.SourceCharacterFixtureTests
```

Completion criteria:

- each invalid UTF-8 byte owns one `LEX001`, one byte, and one display column;
- each invalid Unicode scalar owns one `LEX002` spanning its full UTF-8 encoding;
- no replacement/error token is emitted;
- later valid tokens retain original byte spans; and
- no parser callback is reachable from `LexFailure`.

### R7 — Complete malformed-number diagnostics and continuation

Purpose: implement numeric candidate ownership as one deliberate subsystem so malformed forms are never reinterpreted as convenient shorter tokens.

Primary files: `lexer.py`, `diagnostic.py`, `test_lexer.py`, and `test_fixtures.py`.

Work:

- classify and consume `LEX003` leading-zero candidates;
- classify and consume `LEX004` leading, trailing, and repeated decimal-point candidates;
- classify and consume `LEX005` underscore-containing numeric candidates;
- classify and consume `LEX006` recognizable scientific notation; and
- classify and consume `LEX007` hexadecimal/binary-looking candidates, including the accepted ambiguous boundaries.

Fixture group unlocked: the first fifteen cases in `lexer/lexical-failures.json`:

- `lex-leading-zero`
- `lex-malformed-leading-decimal`
- `lex-malformed-trailing-decimal`
- `lex-malformed-repeated-decimal`
- `lex-numeric-separator`
- `lex-numeric-separator-exact-boundary`
- `lex-scientific-boundary`
- `lex-scientific-notation`
- `lex-scientific-incomplete-sign`
- `lex-alternate-base-empty`
- `lex-hex-notation`
- `lex-hex-boundary`
- `lex-hex-invalid-digit-exact-boundary`
- `lex-binary-notation`
- `lex-repeated-decimal-exact-boundary`

Verification:

```powershell
python3.11 -m unittest tests.test_lexer.NumericCandidateTests
python3.11 -m unittest tests.test_fixtures.MalformedNumberFixtureTests
```

Completion criteria:

- each complete candidate has the accepted primary span and `candidate_lexeme`;
- malformed candidates emit no token for any owned byte;
- `2.5e3foo` resumes at `foo`, `0xG` owns the accepted full candidate, and `5e` remains successful; and
- commas are never absorbed into numeric candidates.

### R8 — Complete unclosed strings and unterminated block comments

Purpose: make stateful end conditions deterministic across every newline form and physical EOF.

Primary files: `lexer.py`, `diagnostic.py`, `test_lexer.py`, and `test_fixtures.py`.

Work:

- implement `LEX008` at `LF`, `CR`, `CRLF`, and EOF;
- leave a terminating newline for ordinary whitespace handling;
- independently report an invalid character and an unclosed string when both apply; and
- implement `LEX009` with the opening `/*` primary label and zero-width `reached_eof` secondary label.

Fixture group unlocked in `lexer/lexical-failures.json`:

- `lex-invalid-character-unclosed-string`
- `lex-unclosed-string-lf`
- `lex-unclosed-string-cr`
- `lex-unclosed-string-crlf`
- `lex-unclosed-string-eof`
- `lex-unterminated-block-comment`

Verification:

```powershell
python3.11 -m unittest tests.test_fixtures.StringCommentFailureFixtureTests
```

Completion criteria:

- an unclosed string span excludes its terminating newline;
- no failed string emits a `STRING` token;
- independent diagnostics use the accepted source ordering; and
- unterminated block comments consume through EOF and still produce physical-end EOF.

### R9 — Complete logical-operator recovery, diagnostic ordering, and the reporting cap

Purpose: close the remaining recovery behavior and prove that output limits do not change scanning.

Primary files: `diagnostic.py`, `lexer.py`, `test_lexer.py`, and `test_fixtures.py`.

Work:

- implement `LEX010` for lone `&` and `|` with one-byte continuation;
- sort/accumulate diagnostics by accepted primary start, primary end, and code order;
- retain at most twenty diagnostic records;
- set truncation only when a twenty-first failure is detected; and
- continue scanning, locating, and emitting later valid partial tokens after the cap.

Fixture group unlocked in `lexer/lexical-failures.json`:

- `lex-incomplete-logical-operators`
- `lex-diagnostic-limit-exactly-twenty`
- `lex-diagnostic-limit-truncated-continues`

Verification:

```powershell
python3.11 -m unittest tests.test_fixtures.DiagnosticLimitFixtureTests
```

Completion criteria:

- exactly twenty failures return twenty diagnostics with truncation false;
- a twenty-first failure returns twenty diagnostics with truncation true;
- the later `ok` token and physical-end EOF survive truncation; and
- all failure paths consume a nonempty range and terminate.

### R10 — Run the lexer-only conformance gate

Purpose: verify the assembled lexer rather than treating isolated milestone passes as proof of conformance.

Fixture scope:

- all 44 indexed records in:
  - `lexer/pilot.json`;
  - `lexer/tokens.json`;
  - `lexer/lexical-failures.json`; and
  - `locations/source-locations.json`;
- plus the lexical result and parser-not-run boundary of `frontend-pilot-invalid-utf8-phase-gate`;
- excluding the two parser-behavior records in `frontend/pilot.json` and every file under `fixtures/parser/`.

Verification:

```powershell
python3.11 --version
python3.11 -m unittest tests.test_source tests.test_lexer tests.test_fixtures
python3.11 -m unittest discover
python3.11 -m compileall sml_frontend tests
```

Completion criteria:

- the interpreter reports exactly Python 3.11.9;
- all lexer-only unit and fixture tests pass without expected-failure markers or fixture weakening;
- all ten lexical codes have focused evidence, and all lexer/location fixture expectations match exactly;
- every success/failure token collection ends with one real physical-end EOF;
- no implementation runtime/test dependency has been added;
- no parser module, AST, semantic lookup, or runtime behavior has been introduced; and
- the public `lex(bytes)` result remains the only handoff point to future parser work.

## Review discipline

Implement one milestone at a time. Before moving forward:

1. review the small diff and its fixture IDs;
2. explain why each accepted source range belongs to either a token, trivia, or one malformed candidate;
3. run the milestone command and the previously passing regression commands;
4. record measured failures separately from assumptions; and
5. do not stage, commit, or push unless explicitly requested.

If code behavior and an accepted contract or fixture disagree, stop and resolve the contract conflict rather than changing expected results to fit the implementation.

## Explicitly not in scope

- parser architecture or implementation beyond enforcing that `LexFailure` is never parser input;
- grammar recognition, precedence, associativity, grouping, detached-quantity rejection, or unit-expression structure;
- AST records, AST spans, token references, recovery nodes, or parser fixtures;
- parser diagnostics `SYN001`–`SYN037`, synchronization, token synthesis, or recovered trees;
- unit/name resolution, dimensional checking, unit normalization, conversions, evaluation, code generation, or runtime behavior;
- formatter, linter, static type checker, parser generator, regex-driven core scanner, or third-party packages;
- changes to accepted fixtures, token kinds, diagnostic meanings, source-location rules, or recovery boundaries; and
- staging, committing, pushing, publishing, or CI setup without a separate explicit request.
