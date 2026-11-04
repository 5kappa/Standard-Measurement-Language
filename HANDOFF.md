# Standard Measurement Language Project Handoff

Handoff date: 2026-11-04
Project name: Standard Measurement Language (SML)  
Current phase: lexer complete through R10; parser planning is next
Implementation status: lexer-only conformance gate passes under Python 3.11.9; parser not started

## Resume here

The project is converting an existing programming-language proposal into a precise implementation contract. The final implementation scope is:

~~~text
UTF-8 source
    -> lexer
    -> tokens with original lexemes and source spans
    -> parser
    -> source-located AST or lexical/syntax diagnostics
~~~

Do not expand the project into semantic analysis, unit resolution, dimensional checking, unit normalization, evaluation, code generation, or runtime implementation.

Read these documents in order:

1. [Front-end development charter](docs/frontend/README.md)
2. [Accepted source-location contract](docs/frontend/SOURCE-LOCATIONS.md)
3. [Accepted token specification](docs/frontend/TOKEN-SPEC.md)
4. [Accepted grammar](docs/frontend/GRAMMAR.ebnf)
5. [Accepted source AST schema](docs/frontend/AST-SCHEMA.md)
6. [Accepted diagnostic contract](docs/frontend/DIAGNOSTICS.md)
7. [Accepted lexical continuation and parser failure contract](docs/frontend/RECOVERY.md)
8. [Accepted machine-readable fixture format](docs/frontend/fixtures/README.md)
9. [Accepted traceability registry](docs/frontend/TRACEABILITY.md)
10. [Accepted frontend implementation plan](docs/frontend/IMPLEMENTATION.md)
11. [Normative language specification](LANGUAGE-SPECIFICATION.md)
12. [Specification roadmap](SPECIFICATION-ROADMAP.md)
13. [Project rationale and historical design](PROJECT.md)
14. [Decision index](decisions/README.md)

The accepted files under `docs/frontend/` are the implementation-facing hardening layer. `LANGUAGE-SPECIFICATION.md` remains the normative authority for the language surface until it is deliberately amended.

## Finalized project boundary

The lexer owns:

- UTF-8 and canonical-character validation;
- token boundaries and token kinds;
- original lexemes and source locations;
- whitespace and comment scanning;
- maximal-munch operator recognition; and
- lexical diagnostics.

The parser owns:

- grammar recognition;
- precedence, associativity, and grouping;
- quantity-attachment validation;
- structural unit-expression limits;
- source-located AST construction; and
- one fail-fast syntactic diagnostic after lexically successful input.

The lexer and parser do not determine:

- whether a unit name is registered;
- whether dimensions or quantity kinds are compatible;
- whether a conversion is meaningful;
- whether a unit expression simplifies to another unit;
- whether an operation is physically meaningful; or
- how any program executes.

## Important phase-boundary examples

| Source | Required front-end result |
| --- | --- |
| `10foo` | Accept as `NUMBER IDENT` and build a quantity-literal AST. Unknown-unit detection is outside scope. |
| `10 foo` | Reject during parsing because the magnitude and simple unit are detached. |
| `10m + 5s` | Accept as an addition AST; dimension compatibility is outside scope. |
| `5m as s` | Accept as a conversion AST; compatibility is outside scope. |
| `1[m^2/m]` | Preserve the unit-expression AST; do not simplify it to `m`. |
| `1[kg/m/m/m/m]` | Reject during parsing because repeated top-level division violates the unit grammar. |
| `1[kg/(m*m*m*m)]` | Accept structurally; usefulness of the resulting dimension is outside scope. |

If asked why `10foo` parses:

> The lexer validates that `foo` has the shape of an identifier, and the parser validates that an identifier may occur in a unit position. Determining whether that name denotes a registered unit is name resolution, not tokenization or grammar recognition.

## Completed hardening work

### Front-end charter

[`docs/frontend/README.md`](docs/frontend/README.md) is accepted as the scope and authority map. It freezes the lexer/parser-only boundary and lists the remaining hardening artifacts.

### Source locations

[`docs/frontend/SOURCE-LOCATIONS.md`](docs/frontend/SOURCE-LOCATIONS.md) is accepted. It fixes:

- half-open UTF-8 byte spans `[start_byte, end_byte)`;
- zero-based byte offsets;
- one-based diagnostic lines and display columns;
- four-column tab stops;
- `CR`, `LF`, and `CRLF` newline behavior;
- original-source preservation;
- adjacency derived from byte spans;
- zero-width `EOF` and absent-syntax diagnostic locations; and
- AST span-composition principles.

### Token specification

[`docs/frontend/TOKEN-SPEC.md`](docs/frontend/TOKEN-SPEC.md) is accepted. It fixes:

- all 62 token kinds;
- exact case-sensitive reserved spellings;
- identifier, number, string, comment, operator, and delimiter rules;
- maximal-munch behavior;
- quantity adjacency;
- unit spellings as ordinary `IDENT` tokens; and
- required token fixture coverage.

The following numeric ambiguity was deliberately resolved:

~~~text
2.5e3  -> lexical error
0x10   -> lexical error
0b1010 -> lexical error
10foo  -> NUMBER("10") IDENT("foo") EOF
5e     -> NUMBER("5") IDENT("e") EOF
~~~

Recognizable exponent, hexadecimal, and binary notations are malformed numeric candidates. They are not reinterpreted as quantities. The narrower `5e` spelling remains a quantity boundary because it lacks the digit or sign that makes an exponent continuation recognizable.

### Grammar

[`docs/frontend/GRAMMAR.ebnf`](docs/frontend/GRAMMAR.ebnf) is accepted. It consolidates the complete token-level grammar and fixes:

- source files, functions, blocks, and every statement form;
- optional `let` initialization and mandatory immediate `const` initialization;
- prefix and postfix `++` and `--` as standalone statements;
- optional `for` clauses, including `for (;;) {}`;
- direct-only `input()` initializer and simple-assignment placement;
- the complete precedence hierarchy, including right-associative negative numeric exponents;
- bounded unit-expression syntax and parser-enforced structural limits;
- parser-visible context checks for `return`, `break`, and `continue`; and
- the boundary between syntactic call recognition and later function/argument resolution.

The grammar records that the proposal example `let distance: m = 100m;` conflicts with the accepted bracketed exact-unit category. The canonical spelling is `let distance: [m] = 100m;`.

### Source AST schema

[`docs/frontend/AST-SCHEMA.md`](docs/frontend/AST-SCHEMA.md) is accepted for successful parses. It fixes:

- a source-faithful hybrid AST without changing the lexer contract;
- explicit `GroupExpr` nodes and retained source tokens needed for diagnostics;
- ordered collections for repetitions, optional fields for EBNF options, tagged variants for alternatives, and nested nodes for expression associativity;
- first-branch plus ordered `else if` representation and an optional final `else`;
- dedicated `for` initializer and update variants without synthetic semicolons;
- first-factor plus star-and-factor unit products and one optional quotient;
- complete-file and per-node source-span composition; and
- a successful-parse-only boundary; syntax failure returns no AST and creates no missing tokens or error nodes.

The representation requires only ordinary records, tagged variants, optional values, and basic ordered collections. It does not require a parser generator or specialized AST library.

### Diagnostic and failure policy

[`decisions/086-diagnostic-and-failure-policy.md`](decisions/086-diagnostic-and-failure-policy.md) fixes the phase-level policy:

- all current frontend diagnostics have severity `error`;
- codes, categories, and source labels are stable while exact English wording may evolve;
- every diagnostic has one primary span and may have secondary labels, notes, or corrections;
- detached quantities and misplaced noise words receive specialized local diagnostics;
- the lexer continues after lexical failures, may collect multiple independent errors in source order, and still emits physical-end `EOF`;
- the parser runs only after lexing succeeds;
- the parser stops at its first syntax error and returns no AST; and
- version 0.1 has no parser synchronization, token synthesis, skipped-token representation, or recovered AST.

Parser recovery starting points previously discussed are deferred guidance only. `DIAGNOSTICS.md` later fixed the maximum at twenty lexical diagnostic records with an explicit truncation flag.

### Diagnostic contract

[`docs/frontend/DIAGNOSTICS.md`](docs/frontend/DIAGNOSTICS.md) is accepted. It fixes:

- the complete `LEX`, `SYN`, and internal-failure code inventory;
- `error` as the only current severity;
- stable primary and secondary label roles plus code-specific diagnostic data;
- non-normative English rendering;
- source-order and same-position tie-breaking;
- a maximum of twenty lexical diagnostic records and an explicit truncation flag;
- deterministic malformed-number spans;
- parser phase gating after lexical failure; and
- exactly one syntax diagnostic and no AST after parser failure.

### Lexical continuation and parser failure contract

[`docs/frontend/RECOVERY.md`](docs/frontend/RECOVERY.md) is accepted. It fixes:

- a tagged lexer result with complete tokens on success and valid partial tokens on failure;
- one real physical-end `EOF` in either token collection;
- nonempty malformed-range consumption and the continuation point for every lexical diagnostic family;
- unchanged scanning after the twenty-diagnostic reporting cap is reached;
- the rule that failed lexical results never reach the parser; and
- the parser's first-error, no-recovery, no-AST failure behavior.

[Decision 088](decisions/088-bytewise-invalid-utf8.md) resolves the remaining invalid-UTF-8 boundary and position question with the simpler bytewise policy: each invalid byte produces one `LEX001`, consumes one byte, advances one display column, emits no token, and leaves every following valid byte for ordinary scanning.

### Machine-readable fixture format

[`docs/frontend/fixtures/README.md`](docs/frontend/fixtures/README.md) and [decision 087](decisions/087-machine-readable-fixture-format.md) are accepted. They fix:

- strict JSON format version 1, separate from SML language version 0.1;
- categorized files listed in a deterministic `index.json`;
- globally unique descriptive fixture IDs;
- tagged UTF-8 text or lowercase hexadecimal source bytes;
- explicit `lexer` and `frontend` entry points and tagged phase results;
- complete token arrays and zero-based AST token indices;
- explicit AST variants, null optionals, ordered arrays, and node spans;
- structured diagnostics without normative English rendering;
- required byte spans and location-sensitive line/column assertions;
- non-behavioral coverage metadata; and
- trusted, version-controlled fixture data, with lexer variants decoded by small test-only helpers and parser/AST decoding deferred until parser implementation.

### Implementation technologies

[`docs/frontend/IMPLEMENTATION.md`](docs/frontend/IMPLEMENTATION.md) and [decision 089](decisions/089-python-frontend-implementation.md) are accepted. The initial frontend uses Python 3.11.9 as its exact reference interpreter, no runtime dependencies, a handwritten deterministic lexer over original bytes, immutable returned records, standard-library JSON and `unittest`, and a small `argparse` CLI. The later parser will use handwritten recursive descent without a parser generator or external parsing library.

`LexFailure` is one failed-scan result rather than a hierarchy of error subclasses. Its ordered structured diagnostics, each carrying a code from `LEX001` through `LEX010`, identify the possibly heterogeneous source-failure causes. In Python, each diagnostic stores its code-specific stable data in a small dictionary whose required keys are determined by the diagnostic code. File I/O errors remain outside the lexer; internal defects are not lexical source failures.

### Traceability registry

[`docs/frontend/TRACEABILITY.md`](docs/frontend/TRACEABILITY.md) is complete. It assigns 112 unique stable rule IDs across the token, source-location, grammar, AST, diagnostic, recovery, fixture-format, and implementation contracts. Every fixture-required row links to evidence, every process-only row has an explicit `N/A` rationale, and all 93 indexed fixtures appear in the reverse index.

The mechanical coverage audit found no pending rule rows or reciprocal-link failures.

### Pilot fixtures

[`docs/frontend/fixtures/index.json`](docs/frontend/fixtures/index.json) indexes four structurally validated pilot cases across `lexer/pilot.json` and `frontend/pilot.json`. Together they demonstrate lexer success, lexical failure with valid partial tokens, bytewise invalid UTF-8 and exact positions, parser phase gating, successful source AST serialization, and first-error parser failure without an AST. The `10m` lexer pilot and invalid-UTF-8 lexical phase gate pass; successful-parse and syntax-failure pilot assertions remain pending until parser implementation.

### Complete fixture suite

The completed suite contains 93 fixtures across eight indexed JSON files. Static validation covers all 62 token kinds, all 53 AST node kinds, all ten lexical codes, all 28 active syntax codes, source positions, continuation boundaries, diagnostic limits, phase gating, token references, node spans, strict JSON, unique IDs, and traceability metadata. `SYN001` is intentionally unused; `ICE001` remains process-level. Runtime lexer conformance now covers all 44 indexed lexer and source-location records plus the frontend invalid-UTF-8 phase-gate case. Parser and AST fixture execution remains pending.

## Hardening completion

The final repository-wide documentation consistency audit, fixture population, traceability completion, and mechanical coverage audit are complete. The hardened contracts govern the completed R0–R10 lexer implementation.

The next implementation phase is parser planning against the accepted grammar, AST, diagnostic, recovery, and fixture contracts. Do not expand into semantics or change the completed lexer contract merely for parser convenience.

## Language-name migration

Status: completed after handoff

The current name is **Standard Measurement Language (SML)**. Current normative, planning, and implementation-facing documents use this name.

The teammate draft, legacy proposal, filenames derived from them, and historical decision records may retain the former name **Measure**. These occurrences preserve provenance rather than naming the current language. The decision index records this naming history.

The migration was deliberately case-sensitive; ordinary uses of the verb or noun “measure” were not changed.

Because “SML” is also widely associated with Standard ML, the GitHub repository description should spell out **Standard Measurement Language** and identify it as a unit-aware educational language.

## Repository status

The canonical branch is `main`, with `origin` at `5kappa/Standard-Measurement-Language`. Generated working material remains excluded by `.gitignore`, including `graphify-out/`, `tmp/`, `__pycache__/`, `*.py[cod]`, and `.venv/`. Keep the professor-provided PDF and proposal source documents unless the team intentionally relocates them.

## Known unfinished work

- Parser and AST fixture records are accepted but have not yet been executed against a parser implementation.
- Parser modules, source AST construction, and syntax-diagnostic execution do not exist yet.
- Semantic analysis, unit resolution, dimensional checking, evaluation, and runtime behavior remain outside the project boundary.

## Safe continuation rule

Keep each parser change small and reviewable. If a new implementation-facing document or parser decision conflicts with `LANGUAGE-SPECIFICATION.md` or the accepted lexer contract, stop at the conflict. Either follow the normative specification or deliberately amend it; do not let an implementation convenience silently redefine SML.
