# Specification Decision Roadmap

Status: planning reference  
Applies to: statically checked structural quantities language  
Companion document: [`PROJECT.md`](PROJECT.md)

Normative proposal specification: [`LANGUAGE-SPECIFICATION.md`](LANGUAGE-SPECIFICATION.md)

## 1. Purpose

This roadmap preserves the decision history used to produce the proposal. Decision 076 clarifies that no lexer, parser, checker, or evaluator must be implemented. `LANGUAGE-SPECIFICATION.md` is the normative proposal surface; implementation phases below are historical or optional future work.

It is organized by dependency rather than calendar date. A later decision should not be finalized while it still depends on an unresolved earlier decision. For example, parser strategy should not be selected before the grammar is understood, and numeric representation should not be selected before conversion requirements are explicit.

This roadmap does not settle the open questions. It defines:

- which decisions are required;
- why each decision matters;
- which earlier decisions it depends on;
- what evidence should be compared;
- what artifact records the result; and
- what must be true before the project proceeds.

## 2. Roadmap principles

1. **Specify source form before implementation machinery.** Decide what text tokenizes and parses before choosing how to implement the front end.
2. **Keep lexical, syntactic, and semantic decisions separate.** A parser may recognize an addition even when semantic analysis later rejects its operands.
3. **Use the same small fixtures repeatedly.** Comparing designs against different examples hides tradeoffs.
4. **Prefer reversible decisions early.** Avoid committing the project to syntax or runtime architecture before the smallest use case proves their value.
5. **Require diagnostics as evidence.** A lexical or syntactic design is incomplete until malformed inputs can be explained locally.
6. **Freeze only what the next milestone needs.** A version 0.1 decision does not automatically become a permanent language rule.
7. **Record rejected alternatives.** Future contributors should know why an apparently simple alternative was not selected.
8. **Do not fill the professor's documentation outline with invented features.** Deferred statements should be labeled deferred instead of being specified prematurely.

## 3. Decision states

Every specification decision should have one of these states:

| State | Meaning |
| --- | --- |
| `UNFRAMED` | The topic is known, but the exact question and constraints are not written. |
| `READY` | The question, alternatives, fixtures, and evaluation criteria are prepared. |
| `EVALUATING` | Alternatives are being compared through examples, grammar sketches, or experiments. |
| `PROVISIONAL` | One choice is accepted for the next milestone but may be revised. |
| `ACCEPTED` | The choice is part of the version 0.1 specification. |
| `DEFERRED` | The decision is intentionally postponed beyond version 0.1. |
| `REJECTED` | An alternative was considered and rejected with a recorded reason. |
| `SUPERSEDED` | A later decision replaces the recorded choice. |

`PROVISIONAL` is useful for choices needed to build a thin experiment. It prevents an experimental syntax from being mistaken for permanent language design.

## 4. Required decision record

Each accepted or provisional decision should eventually receive a short record. A `decisions/` directory may be introduced when the first decision is ready; this roadmap does not require creating it yet.

Suggested filename:

```text
decisions/NNN-short-decision-name.md
```

Suggested record:

```markdown
# NNN: Decision title

Status: READY | EVALUATING | PROVISIONAL | ACCEPTED | DEFERRED
Target: version 0.1 | later
Depends on: decision IDs or none

## Question

One precise question.

## Constraints

Established requirements that the choice must satisfy.

## Fixtures

The same valid, invalid, and malformed examples for every alternative.

## Alternatives

Realistic options, including the smallest option.

## Lexical and syntactic analysis

1. Which characters express it?
2. Which tokens does the lexer produce?
3. Can tokenization be deterministic and mostly context-free?
4. Which grammar productions parse it?
5. Does it introduce ambiguity or excessive lookahead?
6. What AST nodes represent it?
7. Can malformed input produce a local and useful diagnostic?
8. Can a reader understand the relevant grammar rules?
9. Is its implementation complexity justified by its domain value?

## Semantic consequences

Meaning, checking rules, conversions, and phase ownership.

## Diagnostic consequences

Expected errors, spans, recovery, and likely cascades.

## Decision

Selected alternative and scope.

## Rejected alternatives

Why each alternative was not selected.

## Validation

Tests or experiments that must pass.

## Revisit triggers

Concrete evidence that would justify reopening the decision.
```

## 5. Dependency map

```text
project boundary and fixtures
    |
    v
lexical vocabulary and quantity-literal boundary
    |
    v
expression and unit grammar
    |
    v
source AST and recovery model
    |
    v
lexical and syntax diagnostic contract
    |
    v
lexer/parser implementation choices
    |
    v
token and AST delivery milestones

Future separate project:
resolution -> checking -> conversion -> execution
```

The implementation language still appears after the grammar so one host language's conveniences do not shape the language surface accidentally.

## 6. Roadmap overview

| Phase | Main result | Exit gate |
| --- | --- | --- |
| 0. Baseline | Frozen lexer/parser boundary and shared fixtures | Everyone can state what the current project parses and what later phases are excluded. |
| 1. Lexical surface | Deterministic token vocabulary and selected quantity-literal boundary | Every fixture has one documented token stream and local lexical errors. |
| 2. Grammar and AST | Readable EBNF, precedence, AST, and parser failure contract | Every fixture has one parse or one first local syntax diagnostic. |
| 3. Semantic rationale | Existing dimension and unit decisions retained informatively | No semantic rule becomes a lexer/parser dependency. |
| 4. Deferred semantics | Conversion, numeric, kind, currency, and temperature behavior | Explicitly outside the current proposal where not already covered by physical-unit rules. |
| 5. Diagnostics and conformance | Lexical/syntax diagnostics and token/AST fixtures | The written front-end specification determines pass/fail. |
| 6. Implementation choices | Host language, lexer strategy, parser strategy, and repository tooling | Choices are justified against the frozen grammar. |
| 7. Vertical delivery | Small source-to-token/AST increments | Each milestone produces tokens, an AST, or a lexical/syntax diagnostic. |

## 7. Phase 0 - Freeze the design baseline

### SD-001: Course-project capability boundary

**Current state: ACCEPTED by decision 075; decision 001 is superseded.** The current implementation contains a lexer and parser only. The expression core is the first slice, while the final parser surface must cover the selected statements required by the course proposal. Resolution, checking, conversion, evaluation, and code generation are excluded.

Record for the current front end:

- the complete source-file grammar required by the proposal;
- the exact operator families included;
- whether unit powers are present syntactically;
- which statement and function forms are parsed;
- that successful output is a token stream and source-located AST; and
- the complete list of excluded semantic and runtime phases.

Evidence:

- at least three accepted expressions;
- at least three syntactically valid semantic-error examples that still parse;
- at least three malformed inputs; and
- one example demonstrating conversion syntax.

Exit criterion: every required proposal construct has a stated grammar status, while no fixture requires resolution, checking, evaluation, or runtime input behavior.

### SD-002: Normative terminology

**Current state: ACCEPTED.** The normative glossary is recorded in `PROJECT.md` Section 6.1. It distinguishes unit representation, dimension compatibility, quantity kind, conversion, and normalization. See `decisions/002-normative-terminology.md`.

Define the exact meanings of:

- magnitude;
- numeric value;
- unit;
- scale;
- dimension;
- quantity kind;
- quantity literal;
- compound unit;
- canonical unit;
- preferred display unit;
- compatible quantities;
- conversion; and
- compile-time diagnostic.

Exit criterion: the specification never uses `unit`, `dimension`, and `quantity kind` as synonyms.

### SD-003: Shared comparison fixture set

**Current state: ACCEPTED and reclassified by decision 075.** The 19-fixture shared expression suite contains thirteen syntactically valid expressions and six malformed inputs. Five valid expressions carry informative future semantic-error expectations but must parse successfully now. Statement and function suites extend rather than replace it. See `decisions/003-shared-core-fixtures.md`.

Maintain a small shared fixture table containing source spelling, token expectations, AST expectations, and malformed-input diagnostics. Intended meanings may remain informative.

Minimum parser fixtures:

| Source intent | Current parser outcome |
| --- | --- |
| line load times length | multiplication AST |
| area load times area | multiplication with powered unit AST |
| force divided by area | division AST |
| force times length | multiplication AST |
| length plus differently scaled length | addition/conversion syntax AST |
| length plus time | syntactically valid addition AST |
| grouped expression | grouping visibly changes AST structure |
| malformed unit exponent | local syntax diagnostic |
| unknown unit spelling | accepted identifier spelling; no registry lookup |

Exit criterion: every later syntax alternative is evaluated against the same fixture meanings.

### Phase 0 gate

Do not discuss implementation language, parser libraries, or code generation as specification decisions before this gate is complete.

## 8. Phase 1 - Decide the lexical surface

### SD-010: Source encoding and canonical character set

**Current state: ACCEPTED by decisions 076 and 088.** Source files use UTF-8; the canonical language surface is the enumerated ASCII subset in `LANGUAGE-SPECIFICATION.md`. Unicode aliases are excluded from the current proposal. At an offset where no complete well-formed UTF-8 scalar begins, the lexer diagnoses and consumes exactly one byte and advances one display column before continuing.

Alternatives to compare:

- UTF-8 source with an ASCII-only version 0.1 grammar;
- UTF-8 source with selected Unicode aliases; or
- a broader Unicode identifier policy.

Questions:

- Which characters are normative?
- How are invalid or unsupported characters diagnosed?
- Does a Unicode alias normalize before tokenization or become its own token spelling?

Likely version 0.1 direction to evaluate: UTF-8 files with canonical ASCII syntax and no required Unicode input.

### SD-011: Whitespace, line endings, and comments

**Current state: ACCEPTED by decision 076.** SML is free-field; ordinary whitespace is insignificant except for quantity attachment. It supports `//` and non-nesting `/* */` comments. Unterminated strings or block comments are lexical errors.

Decide:

- whether all ordinary whitespace is insignificant;
- whether newlines ever terminate expressions;
- whether comments are omitted, line-only, or line-plus-block;
- whether comments may occur inside a quantity literal or unit expression; and
- how unterminated comments are diagnosed.

Dependency: SD-010.

### SD-012: Numeric literal grammar

**Current state: ACCEPTED by decisions 076, 082, and 083.** `NUMBER` is `(0|[1-9][0-9]*)(\.[0-9]+)?`; signs are parser-level unary operators. Leading zeros, leading/trailing-dot forms, exponents, separators, and alternate bases are excluded.

Rejected alternatives recorded during design:

- integers and required-leading-digit decimals only: `5`, `5.0`, `0.5`;
- leading or trailing decimal-point forms: `.5`, `5.`;
- scientific notation: `2.5e3`; and
- underscore or comma numeric separators such as `1_000` or `1,000`; and
- alternate number systems such as hexadecimal and binary.

Version 0.1 accepts only unsigned decimal integer and fixed-point token spellings. Leading or trailing decimal-point forms, scientific notation, numeric separators, and alternate bases are excluded. A leading sign is a separate unary parser operator rather than part of a `NUMBER` token.

Required outputs:

- regular expression;
- deterministic finite-state machine or transition table;
- accepted and rejected examples; and
- exact malformed-number diagnostics.

### SD-013: Identifier and unit-symbol tokenization

**Current state: ACCEPTED by decision 076.** Identifiers and unit symbols share `[A-Za-z][A-Za-z0-9_]*` and are case-sensitive. Complete unit spellings are not decomposed lexically. Keywords are recognized by lookup after scanning the identifier form.

Decide:

- whether unit symbols use the ordinary identifier token;
- case sensitivity;
- whether underscores and digits are allowed;
- whether SI prefixes are parsed compositionally or included in registered unit names;
- how an unknown unit differs from a malformed identifier; and
- whether future user identifiers share the same lexical class.

The lexer must not consult the unit registry merely to decide token boundaries.

### SD-014: Quantity-literal boundary

**Current state: ACCEPTED.** Simple units use attached spelling tokenized as `NUMBER IDENT`; compound unit annotations use brackets. See `decisions/014-quantity-literal-boundary.md`.

Compare at least:

```text
100m
100 m
100[m]
quantity(100, m)
```

For each form, provide:

- exact characters;
- token stream;
- grammar production;
- AST shape;
- treatment of whitespace;
- unknown-unit behavior;
- compound-unit examples;
- malformed-input recovery; and
- effect on future identifiers, calls, indexing, and collections.

This is the first major surface-syntax decision.

Dependencies: SD-010, SD-011, SD-012, and SD-013.

### SD-015: Compound-unit notation and boundary

**Current state: ACCEPTED.** Compound units are bracketed and use the bounded ASCII `*`, `/`, and integer `^` grammar accepted by SD-022. Semantic normalization remains SD-033. See `decisions/014-quantity-literal-boundary.md` and `decisions/022-bounded-unit-expression-grammar.md`.

Compare how each quantity-literal alternative expresses:

```text
m^2
kN/m
kN/m^2
N*m
kg/m^3
```

Decide:

- product symbol;
- division structure and associativity;
- exponent spelling;
- whether negative exponents are accepted directly;
- whether parentheses are allowed inside unit expressions;
- how a unit expression ends; and
- whether repeated division is accepted or rejected for clarity.

Required ambiguity test:

```text
2 N*m * 3 m
```

The accepted grammar must not need semantic knowledge of registered units to find the boundary between a unit expression and an arithmetic expression.

Dependency: SD-014.

### SD-016: Unicode aliases

**Current state: DEFERRED by decision 076.** The proposal uses canonical ASCII syntax only.

Compare canonical ASCII with optional aliases:

```text
m^2    and m²
kN*m   and kN·m
kg/m^3 and kg/m³
```

Decide only after the ASCII grammar is stable. If adopted, aliases should normalize into the same AST and semantic model.

Dependencies: SD-010 and SD-015.

### SD-017: Optional noise words

**Current state: ACCEPTED.** SML retains the teammate proposal's optional `to`, `then`, and `do` noise words. They are reserved syntactic tokens with no semantic effect. `to` may follow postfix `as`; `then` may follow a future `if` condition; `do` may follow a future loop header. See `decisions/017-optional-noise-words.md`.

Noise words must appear only in their assigned grammar positions and must not be accepted as ordinary identifiers.

Dependencies: SD-013, SD-020, and the later control-flow grammar.

### Phase 1 gate

For every version 0.1 fixture:

- tokenization is deterministic;
- whitespace behavior is stated;
- token spans are defined;
- malformed input has a local lexical diagnostic; and
- no token boundary depends on structural-engineering meaning.

Only after this gate should the lexical state-machine diagrams for the course documentation be finalized.

## 9. Phase 2 - Specify grammar, precedence, and AST

### SD-020: Expression operator set

**Current state: ACCEPTED and completed by decisions 076 and 029.** The proposal includes unary `!`, `+`, `-`; numeric `^`; binary `*`, `/`, `%`, `+`, `-`; comparisons, equality, `&&`, `||`; postfix `as`; assignment statements; and standalone prefix and postfix update statements. See `LANGUAGE-SPECIFICATION.md`.

Confirm which of these belong in version 0.1:

- unary `+` and `-`;
- additive `+` and `-`;
- multiplicative `*` and `/`;
- numeric exponentiation;
- conversion operators; and
- comparison or Boolean operators.

The project brief currently includes the first three families and defers Boolean behavior. Numeric exponentiation must not be added merely because unit exponents use `^`.

### SD-021: Precedence and associativity

**Current state: ACCEPTED and completed by decision 076.** The full arithmetic and Boolean precedence table, associativity, examples, and equivalent EBNF are in `LANGUAGE-SPECIFICATION.md`.

Specify a complete precedence table with:

- one row per operator family;
- associativity;
- examples where precedence matters; and
- an equivalent EBNF structure.

Decide whether unary operators may repeat, as in `--5`, and whether such input is useful or confusing.

Dependency: SD-020.

### SD-022: Unit grammar

**Current state: ACCEPTED.** A compound unit is one product optionally divided by one unit power or one parenthesized product. Nested/repeated division and group powers are rejected. An annotation is limited to eight factors, 128 ASCII characters, source exponents from `-16` through `16`, and normalized exponents from `-32` through `32`. See `decisions/022-bounded-unit-expression-grammar.md`.

Write the final EBNF for:

- atomic unit names;
- products;
- quotients;
- integer powers;
- grouping, if supported; and
- the selected boundary around unit annotations.

Dependencies: SD-014 and SD-015.

### SD-023: Source-file and expression grammar

**Current state: ACCEPTED for the proposal by decisions 076 and 084.** The normative EBNF covers functions, blocks, expressions, declarations, assignment, I/O, conditionals, loops, returns, assertions, and loop-control statements. Simple statements use semicolons, every control-flow body uses braces, and a colon introduces an optional function return annotation after the parameter list.

Write the normative EBNF for the complete version 0.1 source file. Decide:

- whether a trailing semicolon is accepted, required, or rejected;
- whether empty input is legal;
- whether extra expressions are diagnosed at the first trailing token; and
- whether a final newline matters.

Dependencies: SD-011, SD-020, SD-021, and SD-022.

### SD-024: Source AST

**Current state: ACCEPTED for the current parser contract by decisions 085 and 086 and `docs/frontend/AST-SCHEMA.md`.** The parser uses a source-faithful hybrid AST. Grammar repetitions become ordered collections, alternatives become tagged variants, and expression associativity remains explicit through nesting. Parentheses and diagnostic token references are preserved. The schema covers successful parses; a syntax failure returns no AST, missing-token variant, or error node.

Confirm the node set and fields for:

- numbers;
- quantities;
- unary expressions;
- binary expressions;
- grouping;
- unit names;
- unit products;
- unit quotients; and
- unit powers.

Operators, delimiters, keywords, separators, statement terminators, and optional noise-word tokens needed for precise diagnostics survive as token references. `SourceFile` covers the complete source byte range; other nodes exclude unrelated surrounding trivia. See `decisions/085-source-ast-representation.md` and `docs/frontend/AST-SCHEMA.md`.

Dependency: SD-023.

### SD-025: Parser error recovery

**Current state: PARSER RECOVERY DEFERRED by decision 086; lexical continuation ACCEPTED.** The lexer continues after lexical failures and the parser runs only if lexing succeeds. The parser stops at its first syntax error, emits one diagnostic, returns no AST, and performs no synchronization, token synthesis, or recovered-tree construction. `docs/frontend/RECOVERY.md` fixes the lexical continuation boundaries, partial-token failure result, phase gate, and fail-fast parser policy.

Define recovery behavior for:

- missing operand;
- missing closing delimiter;
- empty unit annotation;
- missing exponent;
- repeated operator;
- trailing token; and
- malformed nested unit expression.

The previously considered semicolon, brace, list, expression, and unit-annotation synchronization boundaries are deferred guidance for a future parser-recovery proposal, not version 0.1 requirements.

Dependency: SD-023.

### SD-026: Dimensionless numbers and numeric exponentiation

**Current state: ACCEPTED for staged parser grammar.** Numeric `^` produces a right-associative power AST and permits unary-signed operands such as a negative exponent. The parser does not determine whether a base or exponent is dimensionless; all dimension-based restrictions are future semantic checks. Decimal exponents remain disallowed inside unit expressions by grammar. See `decisions/026-dimensionless-numbers-and-powers.md`.

Dependencies: SD-020, SD-021, SD-031, and SD-041.

### SD-027: Declaration annotation categories

**Current state: ACCEPTED for current parser grammar.** One annotation is either a primitive type, a dimension-name form, or an exact-unit form. Categories cannot be combined. Exact-unit constraints reuse bracketed unit expressions. Meaning and compatibility checks are deferred. See `decisions/027-declaration-annotations.md`.

Inference, initializer requirements, multiple-binding declarations, and function annotation requirements remain separate decisions.

Dependencies: SD-002, SD-014, SD-022, SD-023, and SD-043.

### SD-028: Local initializer inference

**Current state: ACCEPTED for current declaration grammar.** Every declaration has one binding and an optional annotation. A `let` may omit its initializer; a `const` must be initialized immediately. The parser records that structure but performs no inference or definite-assignment analysis. Function parameters and returns use explicit annotations. Multi-binding declarations are rejected by grammar. See `decisions/028-local-initializer-inference.md`.

Dependencies: SD-024, SD-027, SD-035, and SD-043.

### SD-029: Increment and decrement statements

**Current state: ACCEPTED for current parser grammar.** Prefix and postfix `++` and `--` are standalone identifier-target statements and do not produce expression nodes. Expression use is a syntax error. Mutability, numeric type, dimensionless-target enforcement, and update behavior are deferred. See `decisions/029-increment-decrement-statements.md`.

Dependencies: SD-023, SD-027, SD-028, and the later mutation rules.

### Phase 2 gate

- The complete selected expression and statement grammar fits in readable, cross-referenced sections.
- Every valid fixture has one intended parse.
- Every malformed fixture has one primary local diagnostic.
- AST construction does not require unit lookup or dimension checking.

## 10. Future semantic rationale - dimensions and units

**Not an implementation gate for the current project.** These accepted language-design notes may guide a future checker, but the lexer and parser treat unit spellings as syntax and do not execute this phase.

### SD-030: Base-dimension system

**Current state: ACCEPTED.** The initial physical base dimensions are `Length`, `Mass`, and `Time`. `Force` is the named derived alias `(1, 1, -2)`, not a fourth base. No named angle, pressure, stress, moment, or energy dimension is introduced by this decision. See `decisions/030-formal-dimension-and-unit-model.md`.

### SD-031: Dimension algebra

**Current state: ACCEPTED.** A normalized dimension is an integer `(L, M, T)` vector. Multiplication adds vectors, division subtracts them, and an allowed integer power multiplies every component. Addition, subtraction, and conversion require equal vectors. Normalized components remain within `-32` through `32`. See `decisions/030-formal-dimension-and-unit-model.md` and `decisions/026-dimensionless-numbers-and-powers.md`.

Accepted rules:

- multiplication as exponent addition;
- division as exponent subtraction;
- exponentiation rules;
- additive compatibility;
- behavior of the zero exponent;
- normalization and equality; and
- whether fractional dimension exponents are impossible, deferred, or supported.

Dependency: SD-030.

### SD-032: Unit registry model

**Current state: ACCEPTED for the initial registry.** Unit symbols are registered and resolved whole. The minimum symbols are `m`, `cm`, `mm`, `km`, `in`, `ft`, `mi`, `kg`, `s`, `min`, `N`, and `kN`, with exact rational scales. Imperial support is limited to `in`, `ft`, and `mi`; `min` is 60 times `s`; `N` has the dimension and scale of `kg*m/s^2`; `kN` is 1000 times `N`. Prefix tables may generate future registry entries but never alter source tokenization. Optional aliases and display names are not required initially. See decisions 030, 033, and 079 through 081.

The initial registry records:

- symbol;
- dimension;
- scale to canonical representation;
- aliases;
- preferred display spelling;
- prefix behavior; and
- optional quantity-kind hints.

`kN` is a registered complete symbol, not a parser-level application of prefix `k` to `N`.

Dependencies: SD-013 and SD-030.

### SD-033: Compound-unit normalization

**Current state: ACCEPTED.** Resolve every written symbol before normalization; expand definitions, apply exponents, negate denominator exponents, combine dimensions, remove zero exponents, check bounds, and compute scale. Preserve the source unit AST alongside normalized checking data. See `decisions/033-unit-expression-semantics.md`.

These have equal normalized dimensions and scales while retaining their source identities:

```text
N
kg*m/s^2
```

Separate these questions:

- dimensional equality;
- unit-scale equality;
- alias identity;
- quantity-kind identity; and
- preferred display form.

Dependencies: SD-031 and SD-032.

### SD-034: Dimensionless, ratio, percentage, and angle policy

**Current state: PARTIALLY ACCEPTED; angle and percentage are outside the initial model.** Plain numbers are dimensionless; `Scalar` is not a base dimension. Zero powers and cancellation may also produce dimensionless quantities. Empty and numeric unit annotations are rejected. No angle or percentage syntax, unit, annotation, or kind is introduced initially. See `decisions/030-formal-dimension-and-unit-model.md` and `decisions/033-unit-expression-semantics.md`.

Initial accepted rules and later revisit questions:

- whether a plain number is dimensionless;
- whether percentages are syntax, units, or scaled dimensionless values;
- whether radians are indistinguishable from plain ratios;
- whether degrees convert to radians internally; and
- whether angle requires a quantity kind even if it has no physical dimension.

Dependencies: SD-030 and SD-031.

### SD-035: Unit name resolution

**Current state: PARTIALLY ACCEPTED.** Resolution uses complete case-sensitive symbols and occurs before zero-power removal or cancellation. Unknown names therefore remain errors even when their algebraic contribution would disappear. Suggestions, aliases, and future duplicate-symbol rules remain open. See `decisions/033-unit-expression-semantics.md`.

Specify:

- the lookup point in the pipeline;
- unknown-unit diagnostics;
- case-sensitive suggestions;
- alias resolution;
- duplicate symbols, once user-defined units exist; and
- whether resolution produces a separate resolved unit tree.

Dependency: SD-032.

### Phase 3 gate

For every semantic fixture, a reviewer can derive the dimension result by hand from the written rules. The parser remains unchanged if a new built-in unit with an existing lexical shape is added.

## 11. Deferred future work - conversion and numeric semantics

**Outside the current lexer/parser project.** No item in this section blocks the course implementation.

### SD-040: Canonical internal units

**Current state: ACCEPTED for unit scales.** Canonical base units are `m`, `kg`, and `s`. Unit registry scales are exact rationals, including `in = 127/5000 m`, `ft = 381/1250 m`, `mi = 201168/125 m`, `min = 60 s`, `N = kg*m/s^2`, and `kN = 1000 N`. Runtime magnitude representation remains SD-041. See decisions 030 and 079 through 081.

Dependency: SD-030.

### SD-041: Numeric representation

Compare realistic alternatives:

| Alternative | Strength | Risk |
| --- | --- | --- |
| Binary floating point | Familiar, fast, available everywhere. | Decimal quantities and equality may surprise users. |
| Decimal floating point | Natural for entered decimal values. | Host-language and library support varies. |
| Rational numbers | Exact unit scales and many formulas. | Growth, performance, and non-rational results require policy. |
| Integer plus scale | Exact for controlled units and literals. | General division and formulas become complicated. |

Evaluate each with the same calculations, including `1m + (20cm as m)`, repeated conversions, and non-terminating division.

Dependency: SD-012.

### SD-042: Conversion timing

Compare:

- normalizing literals during semantic analysis;
- inserting explicit conversion nodes during lowering; and
- converting only during evaluation.

The selected strategy must preserve scale arithmetic and remain inspectable in tests.

Dependencies: SD-032, SD-040, and SD-041.

### SD-043: Implicit and explicit conversion policy

**Current state: ACCEPTED.** Operations requiring a common unit representation do not convert compatible units silently; source code must use postfix `as`. Numeric lowering and display remain SD-042 and SD-044 decisions. See `decisions/043-explicit-unit-conversion.md`.

Decide:

- whether compatible units convert implicitly for addition and subtraction;
- whether comparison, when later introduced, follows the same rule;
- whether assignment and function calls may convert implicitly later;
- whether an explicit conversion expression is needed in version 0.1; and
- what error or warning appears when conversion loses precision.

Dependencies: SD-041 and SD-042.

### SD-044: Result display-unit policy

Compare:

- always display canonical units;
- preserve the left operand's unit for addition and subtraction;
- preserve a derived symbolic unit where possible;
- choose a magnitude-friendly engineering unit; and
- require an explicit requested output unit.

The display choice must not change the physical result.

Dependencies: SD-032, SD-040, and SD-043.

### SD-045: Rounding, overflow, exceptional arithmetic, and equality

Specify:

- when rounding occurs;
- default displayed precision;
- division by zero;
- overflow and underflow;
- negative zero, if relevant;
- exact versus approximate equality for future comparisons; and
- whether numeric warnings are compile-time or runtime diagnostics.

Dependency: SD-041.

### Phase 4 gate

The result of every mixed-scale fixture is reproducible from the specification alone, including its internal value and displayed form. Required conversion arithmetic remains visible in the checked or lowered representation.

## 12. Deferred future work - quantity-kind and special-domain policy

**Outside the current proposal.** Decision 078 defers currency, affine temperature, and their associated syntax. Broader quantity-kind inference also remains future work.

### SD-049: Money and affine temperature

**Current state: DEFERRED by decision 078.** The teammate draft's visible currency rates and point-versus-difference temperature model remain possible future designs, but none of their keywords, symbols, annotations, or semantics belong to the current proposal.

### SD-050: Version 0.1 kind-checking level

Compare:

1. dimensions only;
2. dimensions plus named quantity kinds;
3. nominal wrappers; and
4. contextual kind inference.

Use these required cases:

- bending moment versus energy;
- stress versus pressure;
- length versus deflection;
- plain ratio versus angle in radians; and
- force produced from line load times length.

Decide whether version 0.1 rejects any same-dimension, different-kind operation or merely preserves kind information for diagnostics and display.

Dependencies: SD-030 through SD-035.

### SD-051: Kind representation

If kinds are included, decide whether they are:

- labels attached to checked expressions;
- nominal types;
- aliases associated with units;
- inferred tags with an `Unknown` state; or
- a separate constraint system.

Dependency: SD-050.

### SD-052: Kind inference through arithmetic

Specify result kinds for at least:

```text
LineLoad * Length
AreaLoad * Area
Force / Area
Force * Length
Length / Length
```

Define what happens when several kinds are dimensionally possible or when no rule applies.

Dependencies: SD-050 and SD-051.

### SD-053: Same-dimension interoperability

Decide whether and how a value can move between meanings such as moment and energy or stress and pressure. Possible policies include:

- freely interchangeable;
- explicit kind conversion;
- explicit annotation;
- construction through a domain operation; or
- rejection in selected contexts only.

Dependencies: SD-051 and SD-052.

### Phase 5 gate

The specification gives an unambiguous result for every required same-dimension example. If kind checking is deferred, the semantic model states exactly what metadata is retained so it can be added later without redesigning tokens or the source AST.

## 13. Freeze lexer/parser diagnostics and conformance

### SD-060: Diagnostic taxonomy

**Current state: ACCEPTED by decision 086 and `docs/frontend/DIAGNOSTICS.md`.** Stable lexical, syntactic, and internal-failure codes, phases, severity, labels, diagnostic data, ordering, and limits are fixed. The categories are:

- lexical errors;
- syntax errors; and
- internal compiler errors.

Unknown units, incompatible dimensions or kinds, invalid conversions, and runtime numeric failures are not current diagnostic categories.

### SD-061: Source-span and labeling policy

**Current state: ACCEPTED by `SOURCE-LOCATIONS.md` and decision 086.** The contract uses byte offsets, one-based diagnostic lines and display columns, four-column tab stops, one primary span, and optional secondary labels, notes, or corrections. Exact message wording is not normative.

Nested-expression highlights follow the primary and optional secondary label rules in `docs/frontend/DIAGNOSTICS.md`. Same-position lexical diagnostics are ordered by end byte and then code.

These rules are frozen before implementation data structures are introduced.

### SD-062: Error recovery and cascade control

**Current state: ACCEPTED by decision 086 and `docs/frontend/RECOVERY.md`.** The lexer continues and may collect multiple lexical errors, exposes valid partial tokens, and suppresses records after the twenty-diagnostic cap without stopping its scan. A lexical failure prevents parser invocation. The parser reports its first syntax error and returns no AST, so parser cascades, error nodes, missing-token markers, and synchronization are outside version 0.1.

Required test: one malformed unit annotation produces exactly one syntax diagnostic and no AST.

### SD-063: Normative versus explanatory text

Mark specification statements using consistent language:

- `must` for requirements;
- `must not` for prohibitions;
- `may` for permitted behavior;
- `implementation-defined` only when variation is deliberately allowed; and
- informative notes and examples as non-normative.

### SD-064: Version 0.1 conformance suite

**Current state: COMPLETE.** Decisions 087 and 089, `docs/frontend/fixtures/README.md`, and `docs/frontend/TRACEABILITY.md` define a strict versioned format and a completed 93-case suite. Static validation covers all 62 token kinds, all 53 AST node kinds, all ten lexical codes, all 28 active syntax codes, source locations, continuation, phase gating, and all 112 traceability rules through evidence or explicit process rationale.

Create fixtures for:

- token streams;
- AST shapes;
- lexical diagnostics;
- syntax diagnostics; and
- recovery results.

The accepted suite allows two independent implementations to be compared against the same expected behavior without sharing implementation-language data structures. Fixture execution remains an implementation task rather than a documentation-hardening gap.

### Phase 6 gate

Version 0.1 is specification-complete when:

- the lexical grammar is complete;
- the EBNF is complete;
- AST shapes are documented;
- lexical and syntax diagnostic requirements are testable;
- all open lexer/parser questions are accepted, provisionally accepted with a revisit trigger, or explicitly deferred; and
- the professor's required proposal sections accurately reflect the selected language rather than the sample language.

## 14. Select lexer/parser implementation approaches

These are engineering decisions, not language semantics. They come after the relevant specification gates.

### IM-070: Implementation language

**Current state: ACCEPTED by decision 089.** The initial frontend uses Python 3.11.9 as its exact reference interpreter with no runtime dependencies. Standard-library data classes, enums, JSON, tests, and CLI facilities cover the initial engineering needs.

The candidates were compared using:

- support for algebraic data types or equivalent AST modeling;
- source-span handling;
- testing ergonomics;
- parser-library availability without dependence on a parser library;
- deployment requirements;
- team familiarity; and
- suitability for coursework demonstration.

Do not choose solely because a language makes one parser technique convenient.

### IM-071: Lexer strategy

**Current state: ACCEPTED by decision 089.** The lexer is a handwritten deterministic scanner over original source bytes. It uses explicit byte classification and dedicated state functions rather than core regular expressions or generated code.

Compared alternatives:

- handwritten deterministic scanner;
- regular-expression-driven scanner; and
- lexer generator.

The chosen strategy must make the documented token machines visible and testable.

Dependencies: Phase 1 gate and IM-070.

### IM-072: Parser strategy

**Current state: ACCEPTED FOR LATER IMPLEMENTATION by decision 089.** The parser will be handwritten recursive descent, with one function per grammar or expression-precedence level. Parser implementation remains deferred until the lexer work and relevant fixtures are complete.

Compared alternatives:

- recursive descent;
- Pratt parsing;
- precedence climbing;
- parser combinators; and
- parser generator.

Evaluate against the actual version 0.1 grammar, recovery requirements, and teaching goals.

Dependencies: Phase 2 gate and IM-070.

### IM-073: Internal architecture

**Current state: ACCEPTED by decision 089 and `docs/frontend/IMPLEMENTATION.md`.** The Python module boundary preserves the specified pipeline:

```text
source -> lexer -> tokens -> parser -> source-located AST
                         \-> lexical/syntax diagnostics
```

The architecture should preserve lexer/parser separation even if both phases share one executable.

Dependencies: lexical and grammar gates.

### IM-074: Execution model

**Current state: SUPERSEDED by decision 075.** The current project has no execution model. Direct evaluation and generated code are both deferred to a separate future project. See `decisions/074-direct-checked-ast-evaluation.md` and `decisions/075-lexer-parser-project-boundary.md`.

No alternative needs selection for the current deliverable.

### IM-075: Repository and quality tooling

**Current state: ACCEPTED INITIAL BASELINE by decision 089.** Machine-readable fixtures remain under `docs/frontend/fixtures/`; implementation modules use the top-level `sml_frontend/` package; tests use `tests/`. Initial checks use Python 3.11.9 standard-library `unittest` and `compileall` without installing the package. A formatter, linter, static type checker, third-party test runner, package publisher, and CI service are not prerequisites. GitHub Actions may be added later.

The baseline covers:

- directory structure;
- formatter and linter;
- unit and snapshot test framework;
- golden-fixture layout;
- continuous-integration checks;
- reproducibility record; and
- release/versioning convention.

Dependency: IM-070.

### Phase 7 gate

**Current state: COMPLETE FOR THE INITIAL FRONTEND BASELINE.** Every selected engineering choice cites a specification need. No implementation constraint changes the accepted grammar or semantics. Additional development tools remain non-normative conveniences. The fixture-readiness gate is complete; implementation still waits only for the final repository-wide documentation audit and commit readiness review.

## 15. Deliver thin lexer/parser slices

### V-001: One expression from source to AST

Support enough source syntax, tokens, and AST structure for one line-load-times-length expression.

Proof required:

- token snapshot;
- AST snapshot;
- exact source spans; and
- no registry or semantic lookup.

### V-002: Semantic independence

Add a length-plus-time case and an unknown-unit spelling. Both must parse successfully because semantic checking is outside the project.

Proof required:

- token snapshots;
- parser accepts both shapes; and
- AST spans preserve both operands.

### V-003: Precedence and grouping

Add the full version 0.1 operator grammar and parentheses. Demonstrate one pair of expressions whose results differ because of grouping.

### V-004: Conversion syntax

Parse postfix `as` and optional `to` forms without checking compatibility or computing scale.

### V-005: Compound units and powers

Parse the compound-unit fixtures and preserve their bounded unit-expression ASTs.

### V-006: Required statement surface

Parse the selected declarations, assignments, input/output statements, conditionals, loops, blocks, functions, and returns required by the course proposal. Add token, AST, and malformed-statement fixtures without defining runtime behavior.

### V-007: Diagnostic hardening

Add malformed number, delimiter, exponent, semicolon, and brace fixtures. Verify multiple lexical diagnostics, parser phase gating after lexical failure, and exactly one syntax diagnostic for lexically valid malformed input. Unknown identifiers remain syntactically valid.

### V-008: Lexer/parser conformance run

Run the complete normative fixture set and record:

- implementation version;
- environment;
- command;
- passing and failing fixtures; and
- any implementation-defined behavior.

### Phase 8 gate

The implementation satisfies the frozen lexer/parser conformance suite without performing semantic work.

## 16. Future language and semantic growth

The current parser may recognize procedural constructs without implementing their behavior. Any future semantic feature must begin with one small use case and a separate checking, runtime, diagnostic, and test analysis.

### Suggested evaluation order

1. **Name and scope resolution** - bind declarations, parameters, and unit names.
2. **Primitive and unit-aware type checking** - validate declared constraints and operations.
3. **Conversion checking and lowering** - validate `as` and make scale operations explicit.
4. **Statement and function semantics** - define mutation, control flow, calls, and returns.
5. **Runtime input/output and evaluation** - execute checked programs.
6. **User-defined units and dimensions** - extend the registry safely.
7. **Kind-aware or dimension-polymorphic functions** - generalize reusable calculations.

This is an evaluation order, not a promise that every feature will be accepted.

### Permanent exclusions unless project scope is formally changed

- professional certification or safety guarantees;
- full building-code compliance;
- finite-element analysis;
- seismic and dynamic analysis;
- nonlinear material behavior;
- detailed connection design;
- three-dimensional structural modeling;
- CAD or BIM integration; and
- treating currency as a fixed physical dimension.

## 17. Immediate specification work queue

Decision 076 and `LANGUAGE-SPECIFICATION.md` consolidate the proposal surface. Remaining work is editorial rather than language implementation:

1. Review the consolidated specification for team agreement and professor feedback.
2. Convert the transition tables and machine descriptions into the diagrams required by the final document.
3. Lay out the final proposal in the professor's section order, adding the accepted Literals section after Identifiers under decision 082.
4. Verify that every example uses only the normative vocabulary and grammar.
5. Proofread the final proposal for consistent terminology, notation, and exclusions.

## 18. Decision-review checklist

Before changing a decision to `ACCEPTED`, verify:

- [ ] The question is narrow and answerable.
- [ ] Established constraints are listed.
- [ ] At least two realistic alternatives were compared, unless only one is technically possible.
- [ ] Valid, invalid, and malformed examples use the shared fixture set.
- [ ] Characters and tokens are explicit.
- [ ] Grammar and AST consequences are explicit.
- [ ] Phase ownership is clear.
- [ ] Any future semantic consequence is identified without making the lexer or parser enforce it.
- [ ] Diagnostic and recovery consequences are explicit.
- [ ] Test cases exist or are specified.
- [ ] Complexity is justified by a current lexer/parser use case.
- [ ] Rejected alternatives have reasons.
- [ ] A revisit trigger is recorded.
- [ ] `PROJECT.md` and the course proposal can be updated consistently.

## 19. Proposal completion checklist

The language content is ready for final proposal authoring when all boxes are checked:

- [x] Capability boundary is frozen.
- [x] Terminology is normative and consistent.
- [x] Character set and encoding are specified.
- [x] The final proposal has a dedicated Literals section for numeric, string, Boolean, and quantity-literal forms.
- [x] Numeric literal forms and sign tokenization are specified with a transition table.
- [x] Identifier and unit-symbol lexical forms are specified.
- [x] Quantity-literal syntax is selected.
- [x] Compound-unit syntax has an unambiguous source boundary.
- [x] Whitespace and comments are specified.
- [x] Complete keyword, reserved-word, noise-word, token, operator, and delimiter inventories exist.
- [x] Complete proposal EBNF exists.
- [x] Declaration, assignment, I/O, conditional, iterative, block, function, and return productions exist.
- [x] Arithmetic and Boolean precedence and associativity are documented.
- [x] Nested conditional and iterative examples exist.
- [x] The Meaning Before Math uniqueness principle is stated without excluded features.
- [ ] Required machine diagrams are rendered from the accepted transition definitions.
- [ ] The final course document is laid out and proofread in the professor's required order.
- [x] Educational-use and professional-safety limitations are visible.
- [x] Currency, affine temperature, implementation architecture, numeric runtime representation, and code generation are excluded.

## 20. Roadmap maintenance

Decision provenance and links are indexed in [`decisions/README.md`](decisions/README.md).

When a decision changes:

1. update its decision record and status;
2. identify dependent decisions using the IDs in this roadmap;
3. rerun or reconsider their fixtures;
4. update the relevant normative section of `PROJECT.md` or a later dedicated specification;
5. update conformance fixtures; and
6. record whether the change is backward compatible with earlier source examples.

The roadmap should remain a map of unresolved and completed decisions. Detailed accepted rules belong in the language specification, while the reasoning and rejected alternatives belong in decision records.
