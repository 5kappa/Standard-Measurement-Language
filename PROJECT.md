# Measure Programming-Language Proposal Workspace

Status: supporting design history and rationale  
Target: course programming-language proposal  
Project type: educational language-design proposal

Normative proposal specification: [`LANGUAGE-SPECIFICATION.md`](LANGUAGE-SPECIFICATION.md)  
Companion planning reference: [`SPECIFICATION-ROADMAP.md`](SPECIFICATION-ROADMAP.md)

## 1. Document purpose and decision status

This document records design history, alternatives, test ideas, and rationale for a clean-slate programming language centered on quantities and units of measurement. The current deliverable is the written proposal. `LANGUAGE-SPECIFICATION.md` is normative when this historical workspace conflicts with the consolidated proposal.

This is a living design document, not a claim that every example is accepted syntax.

The following labels distinguish requirements from proposals:

- **Established**: required by the project brief unless deliberately revised later.
- **Candidate**: concrete enough to evaluate, but not yet accepted.
- **Open**: requires comparison or experimentation before a decision.
- **Deferred**: intentionally outside version 0.1.

The professor-provided documentation outline is treated as a reporting guide. The Tinapay proposal is treated only as an example of the expected level of lexical and syntactic documentation. Neither document defines this language's syntax, architecture, terminology, or feature set.

The teammate-authored draft, *Measure: A Unit-Safe Programming Language*, is a design input rather than a normative specification. Its concrete choices are mapped to the decision roadmap in Section 19. A choice appearing in that draft remains a candidate, deferred feature, or conflict until the corresponding decision record reaches `PROVISIONAL` or `ACCEPTED`.

## 2. Project charter

### 2.1 Purpose

**Established.** Design and document a small unit-aware language proposal. The first domain is scalar structural load analysis. The deliverable explains the language's lexical, syntactic, and intended unit-safety rules without requiring an implementation.

The proposal coverage is:

```text
introduction and uniqueness
    -> character set and lexical machines
    -> operators, delimiters, and expression hierarchy
    -> declaration, I/O, assignment, conditional, and iterative examples
    -> unit-aware language rules and exclusions
```

### 2.2 Intended users

- Students learning programming-language design and lexical/syntactic specification.
- Students exploring how domain-specific notation can prevent unit confusion.
- Readers evaluating whether Measure is coherent and sufficiently distinct from its inspirations.

### 2.3 Success criteria

The project succeeds when it can:

1. describe the language, its inspiration, audience, and uniqueness;
2. enumerate its source character set;
3. specify identifiers, literals, comments, keywords, noise words, operators, and delimiters with regular expressions or machines;
4. state its free-field and whitespace rules;
5. define arithmetic and Boolean expressions with a complete precedence hierarchy;
6. provide declaration, input/output, assignment, nested conditional, and nested iterative examples;
7. explain the bounded unit syntax and intended unit-safety rules; and
8. use one internally consistent vocabulary and example set throughout the final proposal.

### 2.4 Safety and professional-use boundary

**Established.** This is an educational language. It must not claim that its calculations, diagnostics, or generated reports are suitable for professional engineering decisions, code compliance, certification, or construction safety.

## 3. Origin and narrowing record

### 3.1 Original idea

The original concept was a general-purpose language in which units such as meters, seconds, kilograms, and currencies were built into numeric types. Expressions would infer derived units:

```text
distance / time        -> velocity
force * distance       -> moment or energy
line_load * length     -> force
force / area           -> stress
```

The motivation was to prevent ordinary numeric values with different meanings from being confused silently.

### 3.2 Why the first domain is narrower

The first version narrows the idea to simple structural load analysis because that domain supplies small, concrete examples with meaningful unit algebra:

- a line load multiplied by a length produces a force;
- an area load multiplied by an area produces a force;
- a force divided by an area produces stress or pressure;
- a force multiplied by a distance produces a bending moment dimensionally;
- stiffness and geometry formulas introduce useful derived dimensions and conversions.

This boundary lets the project study lexical and syntactic design without also implementing a type checker, evaluator, or complete general-purpose runtime.

### 3.3 Explicitly deferred origin concepts

**Deferred by decision 078.** Currency is not part of the initial dimensional model. A currency conversion depends on an exchange rate, source, and time, so it is not equivalent to a fixed physical-unit conversion. Affine temperature likewise requires distinct point and difference rules beyond the current physical-unit algebra.

## 4. Current proposal boundary

The boundary below describes what the proposal documents. It does not promise an implementation.

### 4.1 Included

**Established for the proposal:**

- a complete documented language surface containing expressions, declarations, assignment, input/output, conditionals, iteration, and functions;
- dimensionless integer and decimal numeric literals with no leading zeros except the literal `0`; numerical values and future numerical variables do not require units;
- attached simple quantity literals such as `100m`, tokenized as `NUMBER IDENT`;
- bracketed compound quantity literals such as `9.8[m/s^2]`;
- unary `+` and `-`;
- binary `+`, `-`, `*`, and `/`;
- parentheses and conventional arithmetic precedence;
- unit spellings sharing the identifier lexical form;
- compound unit expressions using multiplication, division, and integer exponents;
- postfix conversion syntax with `as`, such as `3mi as km`, without checking compatibility;
- lexical machines and statement examples required by the professor's outline; and
- ASCII as the canonical documented form.

### 4.2 Informative initial unit vocabulary

**Accepted as future semantic rationale, not as a parser dependency.** These spellings support examples and future checking, but the lexer emits `IDENT` and the parser does not consult a registry:

| Family | Candidate units | Notes |
| --- | --- | --- |
| Length and deflection | `mm`, `cm`, `m`, `km`, `in`, `ft`, `mi` | Imperial support is limited to inches, feet, and miles with exact scales. |
| Time | `s`, `min` | `min` is a complete symbol with exact scale `60` relative to `s`. |
| Mass | `kg` | Needed if force is represented from base physical dimensions. |
| Force | `N`, `kN` | `kN` scales from `N`. |

Compound forms such as `m^2`, `m^3`, `kN/m`, and `kg*m/s^2` are produced by unit algebra rather than registered as unrelated primitive dimensions. Volume remains `Length^3`, expressed with an exact annotation such as `[m^3]`; it does not introduce a named `Volume` annotation. Supporting a physical dimension algebraically does not automatically introduce a named annotation or quantity kind for it.

### 4.3 Excluded from the current proposal

**Deferred:**

- implementation algorithms for unit resolution or checking;
- a runtime numeric representation and rounding/overflow specification;
- interpretation, compilation, code generation, and implementation architecture;
- reusable beam, column, slab, material, or section objects;
- load combinations and load propagation;
- runtime input carrying units;
- assertions and engineering constraints;
- structured reports;
- user-defined units;
- polymorphic unit-aware functions;
- detailed runtime implementation of declarations, functions, control flow, or input/output;
- currency and exchange-rate declarations;
- affine temperature points and differences;
- finite-element analysis;
- seismic, dynamic, nonlinear, or three-dimensional analysis;
- detailed connection design;
- CAD or BIM integration; and
- building-code compliance or professional certification.

### 4.4 Not selected by this document

No implementation language, parser strategy, AST representation, recovery algorithm, numeric runtime, evaluator, or backend is required by the course deliverable.

## 5. Representative programs and expressions

All examples in this section communicate intended capability. Their spelling is illustrative unless a later decision record accepts it.

### 5.1 Version 0.1 expression fixtures

```text
8[kN/m] * 4m
```

Parser requirement: accept the expression and preserve its binary and unit-expression structure. Informative future semantic intent: force equivalent to `32 kN`.

```text
2.5[kN/m^2] * 24[m^2]
```

Parser requirement: accept the expression and preserve its binary and unit-expression structure. Informative future semantic intent: force equivalent to `60 kN`.

```text
10m + 5s
```

Parser requirement: accept this syntactically valid addition. A future semantic checker may reject the incompatible dimensions.

```text
1m + (20cm as m)
```

Parser requirement: accept an `as` conversion expression with the grouped right operand. Conversion behavior is outside the current project.

```text
(8[kN/m] * 4m) / 2
```

Parser requirement: accept the expression and represent its grouping and precedence. Its computed result is outside the current project.

### 5.2 Later structural-program examples

These examples motivate later language features and are not version 0.1 syntax.

```text
let wallLoad = 8[kN/m] * 4m;
let floorLoad = 2.5[kN/m^2] * 24[m^2];
let totalLoad = wallLoad + floorLoad
```

```text
let reactionA = uniformLoad * span / 2
let reactionB = uniformLoad * span / 2
```

```text
let axialStress = axialLoad / sectionArea
let bendingMoment = force * leverArm
```

```text
let deflection = 5 * uniformLoad * span^4 / (384 * elasticModulus * inertia)
assert deflection <= allowableDeflection
```

```text
for load in loads {
    total = total + load
}
```

The final example only records the future need for collections and iteration. It does not approve braces, the `for` keyword, assignment behavior, or mutable state.

## 6. Quantity, dimension, unit, and kind model

**Informative for the current project.** This section records intended language meaning and vocabulary so the syntax remains extensible. The lexer and parser do not resolve units, normalize dimensions, check operations, or construct checked quantities. Nothing in this section is an implementation gate unless a rule is explicitly restated as a lexical, grammar, AST, or syntax-diagnostic requirement.

### 6.1 Normative terminology

**Accepted.** The specification uses the following terms consistently:

| Term | Normative meaning |
| --- | --- |
| **Magnitude** | The numeric component of a quantity, excluding its unit. In `5km`, the source magnitude is `5`. |
| **Numeric value** | The internal number used to represent or evaluate a magnitude. Its representation is selected separately by SD-041. |
| **Quantity** | A magnitude interpreted using a unit. |
| **Unit symbol** | The case-sensitive source spelling that refers to a unit definition, such as `m`, `km`, or `N`. |
| **Unit definition** | A registry entry containing at least a symbol, dimension, and scale, plus optional display information. |
| **Unit expression** | A syntactic combination of unit symbols using multiplication, division, or integer powers. |
| **Simple unit** | A unit expression consisting of one unit symbol. |
| **Compound unit** | A unit expression containing multiplication, division, or an exponent, such as `m/s` or `m^2`. |
| **Quantity literal** | Source syntax that directly combines a numeric literal with a unit annotation, such as `5m` or `9.8[m/s^2]`. |
| **Dimension** | The normalized algebraic compatibility class of a quantity, independent of unit scale. |
| **Base dimension** | A dimension selected as a primitive axis of the dimension system. |
| **Derived dimension** | A dimension produced algebraically from base dimensions. |
| **Quantity kind** | The domain meaning of a quantity beyond its dimension, such as moment versus energy or stress versus pressure. |
| **Dimensionless quantity** | A quantity whose normalized dimension exponents are all zero. |
| **Scalar** | Shorthand for a dimensionless quantity, not a separate base dimension. |
| **Scale** | The multiplicative factor relating a linear unit to its canonical unit. Affine and contextual conversions are outside this definition. |
| **Canonical unit** | The internal reference unit selected for a dimension. The initial canonical base units are `m`, `kg`, and `s`. |
| **Preferred display unit** | Unit metadata requested or retained for formatting a result; it does not change the represented quantity. |
| **Dimension-compatible** | Having equal normalized dimensions. `m` and `km` are dimension-compatible even though their scales differ. |
| **Operation-compatible** | Satisfying every rule required by a particular operation, including dimension, explicit-unit, and any applicable quantity-kind rules. |
| **Conversion** | Changing a quantity's unit representation while preserving the represented quantity. Source-level conversion uses `as`. |
| **Normalization** | Internal rewriting into canonical dimension, unit, or magnitude form. Normalization is not necessarily a source-language operation. |
| **Evaluation** | Computing the numeric result of a successfully resolved and checked expression. |
| **Compile-time diagnostic** | A message produced before evaluation because source text cannot be tokenized, parsed, resolved, or checked successfully. |

The specification must not use `unit`, `dimension`, `quantity kind`, or `type` as synonyms. Until the later type system is designed, prefer: "a quantity expression has a dimension, unit representation, and optional quantity kind."

Quantity kinds are defined terminology but their enforcement remains an SD-050 decision. The concrete canonical base units are selected by decision 030.

A numeric literal without a unit is a valid dimensionless quantity. Future declarations may therefore bind ordinary numerical variables without attaching a unit, for example `let coefficient = 0.5;`. Measure requires units only when the value is intended to carry a unit-bearing quantity.

### 6.2 Formal dimension representation

**Accepted.** Measure has exactly three initial physical base dimensions and represents a normalized dimension as their integer exponent vector:

```text
Dimension = Length^L * Mass^M * Time^T
```

Examples:

| Quantity | Exponent vector `(L, M, T)` |
| --- | --- |
| Dimensionless | `(0, 0, 0)` |
| Length | `(1, 0, 0)` |
| Mass | `(0, 1, 0)` |
| Time | `(0, 0, 1)` |
| Force | `(1, 1, -2)` |

`Force` is the named derived-dimension alias `Mass * Length / Time^2`, not a fourth base dimension. The initial named physical annotations are `Length`, `Mass`, `Time`, and `Force`. Other algebraic results may retain unnamed vectors and may use exact compound-unit annotations where a declaration constraint is needed.

Multiplication adds exponent vectors. Division subtracts them. An allowed integer power multiplies every component by its exponent. Addition, subtraction, and conversion require equal normalized vectors, followed by any quantity-kind rule selected later. Each normalized component must remain in the accepted range `-32` through `32`.

This initial model does not introduce named angle, pressure, stress, moment, or energy dimensions merely because LMT algebra could represent them.

### 6.3 Unit record and initial registry

**Accepted.** A built-in unit has the following semantic information:

```text
UnitDefinition
    symbol
    dimension
    exact_rational_scale_to_canonical
    optional_display_name
    optional_aliases
```

The canonical base units are `m`, `kg`, and `s`. Initial entries are:

```text
m   -> dimension Length, scale 1
cm  -> dimension Length, scale 1/100
mm  -> dimension Length, scale 1/1000
km  -> dimension Length, scale 1000
in  -> dimension Length, scale 127/5000 relative to m
ft  -> dimension Length, scale 381/1250 relative to m
mi  -> dimension Length, scale 201168/125 relative to m
kg  -> dimension Mass, scale 1
s   -> dimension Time, scale 1
min -> dimension Time, scale 60 relative to s
N   -> dimension Force, scale 1 relative to kg*m/s^2
kN  -> dimension Force, scale 1000
```

Unit scales are exact rational factors, independently of the still-open representation of evaluated magnitudes. Thus `in`, `ft`, and `mi` have scales `127/5000`, `381/1250`, and `201168/125` relative to `m`; no other imperial units are registered. `cm`, `mm`, `km`, and `min` retain scales `1/100`, `1/1000`, `1000`, and `60` relative to their canonical units. `N` normalizes to the same dimension and scale as `kg*m/s^2`, and `kN` has scale `1000` relative to `N`.

`kg*m/s^2` satisfies the bounded unit grammar: one numerator product, one division, one powered denominator factor, three written factors, and an in-range exponent.

**Accepted symbol policy.** Every supported unit spelling is registered and resolved as one complete, case-sensitive symbol. `km` and `kN` are each one `IDENT`; the parser and resolver do not decompose them into a prefix and another symbol. A later registry-construction tool may generate prefixed entries, but source tokenization and lookup remain whole-symbol operations.

### 6.4 Candidate checked quantity

```text
CheckedQuantity
    canonical_magnitude
    dimension
    optional_quantity_kind
    optional_preferred_display_unit
    source_span
```

This is a semantic model, not necessarily the final runtime representation.

### 6.5 Quantity-kind alternatives to investigate

| Alternative | Benefit | Cost or risk |
| --- | --- | --- |
| Dimensions only | Smallest checker; direct algebra. | Cannot distinguish moment from energy or stress from pressure. |
| Dimensions plus named kinds | Represents domain meaning while retaining dimensional algebra. | Needs rules for inferring, preserving, and combining kinds. |
| Nominal wrapper types | Strong explicit separation of domain concepts. | Future semantic machinery with no role in the current parser. |
| Contextual kind inference | Concise source programs. | Can be difficult to predict and diagnose; context may leak across phases. |

**Candidate direction, not a decision:** implement dimensional checking first while keeping an explicit optional kind field in the semantic design. Evaluate named kinds with concrete moment-versus-energy and stress-versus-pressure cases before enabling kind-based rejection.

## 7. Conversion and representation

### 7.1 Conversion requirement

**Established.** Static unit labels may eventually be erased, but scale conversion arithmetic may not be erased.

For example, `1m + (20cm as m)` cannot be lowered to `1 + 20`. The compiler or evaluator must preserve the requested scale conversion or insert an explicit conversion operation.

### 7.2 Candidate conversion strategies

| Strategy | Description | Tradeoff |
| --- | --- | --- |
| Normalize literals immediately | Convert every literal to a canonical unit during semantic analysis. | Simple evaluation; may lose preferred display information unless stored separately. |
| Insert conversion nodes | Preserve source units and add explicit `Convert` nodes before compatible operations. | Clear lowering and diagnostics; larger typed tree. |
| Convert during evaluation | Keep unit metadata until the evaluator combines values. | Easy prototype; weakens separation between checking and execution. |

### 7.3 Open representation questions

**Accepted conversion policy.** Operations that require a common unit representation do not convert silently. Differently scaled compatible operands must be made explicit with postfix `as`, which binds more tightly than multiplication, division, addition, and subtraction. For example, `5km + (3mi as km)` is accepted while `5km + 3mi` is rejected with a conversion-oriented diagnostic.

- Which canonical units are used internally?
- Are physical base dimensions `Length`, `Mass`, and `Time`, or are engineering dimensions such as `Force` primitive?
- Are values represented as integers, decimal floating point, binary floating point, or rationals?
- When and how is rounding permitted?
- Does addition preserve the left operand's display unit, choose a canonical unit, or infer a convenient unit?
- Do derived quantities retain preferred display units?

## 8. Quantity-literal lexical decision

**Accepted.** Simple quantity literals use attached spelling such as `100m`; compound unit annotations use brackets such as `9.8[m/s^2]`. Attachment is a syntactic condition recorded through token spans or leading-trivia metadata, not a combined semantic token.

### 8.1 Comparison

| Form | Likely token sequence | Strengths | Risks |
| --- | --- | --- | --- |
| `100m` | `NUMBER(100) IDENT(m)` if a digit-to-letter boundary is recognized | Compact and familiar in informal engineering notation. | Easy to confuse with identifier rules; errors such as `100foo` may look valid; attached compound units need careful boundaries. |
| `100 m` | `NUMBER(100) IDENT(m)` with discarded whitespace | Readable and familiar. | The parser cannot normally see whether whitespace was present; `100 m` and `100m` may become indistinguishable unless trivia is retained or lexical rules differ. |
| `100[m]` | `NUMBER LBRACKET IDENT RBRACKET` | Explicit boundary; local recovery; compound units are contained. | More punctuation; square brackets may be wanted for collections later. |
| `quantity(100, m)` | `IDENT LPAREN NUMBER COMMA IDENT RPAREN` | Reuses an ordinary call-like grammar and is unambiguous. | Verbose; requires call or special-form syntax before the language otherwise needs functions. |

The first form is accepted for simple units. The bracketed form is accepted for compound units. Spaced suffixes and constructor syntax are rejected for version 0.1.

### 8.2 Compound-unit pressure points

The unbracketed form `8 kN/m * 4 m` exposes an important grammar boundary and is not accepted syntax. Because `*` is allowed both inside a unit expression and between numeric expressions, the parser would otherwise need to infer where the unit suffix ends.

For example:

```text
2 N*m * 3 m
```

Possible readings include:

```text
(2 [N*m]) * (3 [m])
((2 [N]) * m) * (3 [m])
```

The accepted spelling is `8[kN/m] * 4m`. Resolving its boundary does not require the lexer or parser to know which identifiers are registered unit symbols.

### 8.3 ASCII and Unicode

| Canonical ASCII | Possible Unicode alias | Planning position |
| --- | --- | --- |
| `m^2` | `m²` | ASCII should remain canonical; Unicode may later normalize to the same tokens or AST. |
| `kN*m` | `kN·m` | ASCII should remain canonical; middle dot may later be an alias. |
| `kg/m^3` | `kg/m³` | ASCII should remain canonical; superscripts require a small explicit mapping. |

Unicode alternatives must not require a separate semantic model. Their normalization and diagnostics would need dedicated lexer tests.

## 9. Minimal lexical specification

This specification defines the lexical core for attached simple units and bracketed compound units.

### 9.1 Character set

**Candidate for version 0.1:** canonical source uses ASCII characters.

```text
LETTER      = "A".."Z" | "a".."z"
DIGIT       = "0".."9"
WHITESPACE  = space | tab | carriage-return | line-feed
SYMBOL      = "." | "+" | "-" | "*" | "/" | "^"
            | "(" | ")" | "[" | "]" | "," | "_"
```

Source encoding should be UTF-8 even if version 0.1 accepts only an ASCII lexical subset. This leaves a controlled path for Unicode unit aliases.

### 9.2 Token classes

| Token | Candidate lexical rule | Example |
| --- | --- | --- |
| `NUMBER` | `DIGIT+ ("." DIGIT+)?` | `8`, `2.5`, `100` |
| `IDENT` | `LETTER (LETTER | DIGIT | "_")*` | `m`, `kN`, `quantity` |
| `PLUS` | `+` | `+` |
| `MINUS` | `-` | `-` |
| `STAR` | `*` | `*` |
| `SLASH` | `/` | `/` |
| `CARET` | `^` | `^` |
| `LPAREN`, `RPAREN` | `(`, `)` | `(x)` |
| `LBRACKET`, `RBRACKET` | `[`, `]` | `[m]` |
| `COMMA` | `,` | `quantity(1, m)` |
| `AS` | keyword `as` | `3mi as km` |
| `TO` | optional noise word `to` | `3mi as to km` |
| `THEN` | optional noise word `then` | `if (condition) then { ... }` |
| `DO` | optional noise word `do` | `while (condition) do { ... }` |
| `EOF` | end of source | - |

The lexer records at least a token kind, original lexeme, byte or character offsets, and line/column positions. It does not resolve unit names or dimensions.

`100m` is tokenized as `NUMBER("100") IDENT("m")`, not as a combined quantity token. The tokens' adjacent spans establish the attached simple-unit form. Unit lookup occurs after parsing.

### 9.3 Number machine

```text
START --digit--> INTEGER
INTEGER --digit--> INTEGER
INTEGER --'.'--> DOT_AFTER_INTEGER
DOT_AFTER_INTEGER --digit--> FRACTION
FRACTION --digit--> FRACTION
```

Accepting states: `INTEGER`, `FRACTION`.

The current candidate boundary deliberately rejects `.5`, `5.`, exponent notation, numeric separators, and hexadecimal forms. Signs inside the token are already rejected by SD-012: unary signs are parser-level operators.

### 9.4 Identifier machine

```text
START --letter--> IDENTIFIER
IDENTIFIER --letter-or-digit-or-underscore--> IDENTIFIER
```

Accepting state: `IDENTIFIER`.

Unit symbols remain case-sensitive, so `N` and `n` are different lexemes. Recognition as a known unit occurs after parsing.

### 9.5 Operators and delimiters

All version 0.1 operators in the common core are single-character tokens, so maximal-munch conflicts do not arise among them. If comments later use `//` or `/*`, the lexer must prefer those longer prefixes over the single `/` token.

### 9.6 Whitespace, comments, and field format

- **Candidate:** whitespace separates tokens where necessary and is otherwise insignificant.
- **Established:** the language is free-field, not column-sensitive or indentation-sensitive.
- **Open:** whether version 0.1 includes comments at all.
- **Candidate for later:** `//` line comments and `/* ... */` block comments.
- **Established:** the optional noise words are `to`, `then`, and `do`. They are reserved syntactic tokens and do not affect semantics.
- **Established:** the expression core recognizes `as` and its optional noise word `to`; `then` and `do` become active when the required control-flow grammar is completed.

### 9.7 Lexical diagnostics

The lexer should report errors at the smallest local span:

- unknown character;
- decimal point not followed by a digit;
- unsupported Unicode unit spelling;
- unterminated block comment, if block comments are adopted; and
- invalid token boundary required by the selected quantity-literal syntax.

## 10. Minimal draft grammar

The grammar is split into the expression core, postfix conversion, and the accepted simple and compound quantity-literal productions.

### 10.1 Stable expression core

```ebnf
source              = expression, EOF ;

expression          = additive_expression ;
additive_expression = multiplicative_expression,
                      { ("+" | "-"), multiplicative_expression } ;
multiplicative_expression
                    = unary_expression,
                      { ("*" | "/"), unary_expression } ;
unary_expression    = [ "+" | "-" ], conversion_expression ;
conversion_expression
                    = primary_expression,
                      { "as", [ "to" ], unit_target } ;
primary_expression  = quantity_literal
                    | number_literal
                    | "(", expression, ")" ;
number_literal      = NUMBER ;
unit_target         = IDENT
                    | "[", unit_expression, "]" ;
```

This grammar gives primary expressions highest precedence, followed by postfix conversion, unary signs, multiplication and division, then addition and subtraction. Binary operators associate left-to-right. `to` is optional noise, so `3mi as km` and `3mi as to km` have the same AST meaning. A sign is always a parser operator: `-5m` tokenizes as `MINUS NUMBER IDENT`.

### 10.2 Unit-expression core

```ebnf
unit_expression     = unit_product, [ "/", unit_denominator ] ;
unit_denominator    = unit_power
                    | "(", unit_product, ")" ;
unit_product        = unit_power, { "*", unit_power } ;
unit_power          = IDENT, [ "^", signed_integer ] ;
signed_integer      = [ "-" ], integer_number ;
integer_number      = NUMBER ;
```

The parser accepts `integer_number` only when the `NUMBER` lexeme contains digits and no decimal point. The unit grammar has these normative bounds:

- at most one `/` per annotation;
- no nested division;
- parentheses may wrap only a multi-factor denominator;
- at most eight written unit-factor occurrences across numerator and denominator;
- source exponents range from `-16` through `16`;
- normalized dimension exponents range from `-32` through `32`;
- unit annotations contain at most 128 ASCII characters, including whitespace; and
- numeric scale factors are not permitted inside unit expressions.

A single-factor denominator needs no parentheses: `N/m^2`. A multi-factor denominator requires them: `kg/(m*s^2)`. Repeated division such as `kg/m/s^2`, nested division such as `m/(kg/s)`, group powers such as `(m/s)^2`, and implicit multiplication such as `N m` are rejected. Equivalent forms must be rewritten using one product over at most one product.

The opening `[` of a compound quantity must be adjacent to its number. Whitespace inside the brackets is insignificant and counts toward the 128-character content limit. Factor occurrences are counted before normalization; an exponent does not multiply the factor count.

All unit symbols resolve before algebraic normalization, including symbols raised to zero or later cancelled. Normalization then expands registered definitions, applies exponents, negates denominator exponents, combines equal base dimensions, removes zero exponents, checks the normalized exponent range, and computes the combined scale. The source unit AST is retained for diagnostics and display while a normalized exponent map and scale are used for checking.

Zero and negative exponents are syntactically valid. An explicit positive sign is not. Thus `m^0`, `m^-2`, and `N*m^-2` parse; `m^+2` and decimal unit exponents are syntax errors. `unknown^0` also parses successfully; only a future resolver could diagnose the spelling as unknown.

Plain numbers, `m^0`, and cancelling units such as `m/m` may be dimensionless. Empty annotations and numeric pseudo-units are invalid: `5[]` and `5[1]` are rejected. Numeric scale factors are also invalid inside units; use a registered complete symbol such as `km` or ordinary arithmetic instead of `1000*m` inside an annotation.

Named and expanded units with equal normalized dimensions and scales are equivalent for checking, while their source identities remain available for display and later quantity-kind rules. For example, `N` and `kg*m/s^2` check equivalently without requiring identical preferred display spelling.

### 10.3 Accepted quantity-literal productions

```ebnf
quantity_literal        = simple_quantity_literal
                        | compound_quantity_literal ;
simple_quantity_literal = NUMBER, IDENT ;
compound_quantity_literal
                        = NUMBER, "[", unit_expression, "]" ;
```

`NUMBER` and `IDENT` must be adjacent in a simple quantity literal. The parser checks their recorded spans or leading-trivia metadata. Compound units are always bracketed, so arithmetic operators outside the brackets cannot be consumed as unit operators.

### 10.4 Parsing versus semantics

The parser establishes syntactic structure only. It may parse `10m + 5s` as an addition without deciding whether the operation is valid. Unit-name resolution, dimension compatibility, scale conversion, and quantity-kind rules belong to later phases.

### 10.5 Parser recovery goals

Recovery should be local around delimiters and operators. Candidate messages include:

- `Expected an expression after '*'.`
- `Expected ')' to close the expression started here.`
- `Expected a unit expression before ']'.`
- `Expected an integer exponent after '^'.`
- `Unexpected token after the complete source expression.`

### 10.6 Accepted staged numeric-power syntax

Numeric exponentiation with `^` is accepted for the staged parser grammar. The parser constructs a power AST without determining whether either operand is dimensionless.

- A future checker may require the exponent to be dimensionless.
- A future checker may allow decimal exponents for dimensionless bases while requiring compile-time integer exponents for dimensioned bases.
- Decimal exponents are not allowed inside unit expressions.
- Exact root operations such as `sqrt` and `cbrt` may later accept dimensioned arguments only when every dimension exponent divides evenly by the root degree.

Examples:

```text
16 ^ 0.5          -> dimensionless 4
10 ^ 2.5          -> dimensionless approximate result
3m ^ 2            -> 9[m^2]
3m ^ 0.5          -> valid power AST; possible future semantic rejection
sqrt(9[m^2])      -> future exact-root case producing 3m
```

Numeric-domain behavior for negative bases, overflow, and approximate results remains part of SD-041 and SD-045.

### 10.7 Accepted declaration-annotation grammar

A parsed declaration may contain at most one annotation category:

```ebnf
declaration_annotation
    = primitive_type
    | dimension_name
    | exact_unit_constraint ;

primitive_type
    = "int"
    | "float"
    | "bool"
    | "text" ;

dimension_name
    = "Length"
    | "Mass"
    | "Time"
    | "Force" ;

exact_unit_constraint
    = "[", unit_expression, "]" ;
```

The grammar records whether the source used a primitive, dimension-name, or exact-unit annotation. The intended checking behavior is normative in `LANGUAGE-SPECIFICATION.md`.

```text
let count: int = 5;
let distance: Length = 5m;
let exactDistance: [m] = 5m;
let area: [m^2] = 10[m^2];
```

Annotation categories cannot be combined syntactically. Forms such as `float[m]`, `Length(m)`, and `float Length` do not match the declaration grammar.

### 10.8 Accepted initialized-declaration grammar

Every declaration has exactly one initializer. Its annotation is optional:

```ebnf
declaration
    = ( "let" | "const" ), IDENT,
      [ ":", declaration_annotation ],
      "=", expression, ";" ;
```

The parser records the optional annotation and required initializer. It performs no inference and does not check the initializer.

```text
let count = 5;              // inferred int
let ratio = 0.5;            // inferred float
let span = 5m;              // inferred exact-unit constraint [m]
let area = 6[m^2];          // inferred exact-unit constraint [m^2]
let flexible: Length = 5m;  // explicit dimension constraint
```

Future semantics may infer a binding constraint from an unannotated initializer. Function parameters use `name: annotation`, and a function return annotation follows its parameter list using the same colon, as in `fn speed(distance: Length, time: Time): [m/s]`. Uninitialized and multi-binding declarations are rejected by the current grammar.

Scope, mutation, assignment, and the exact numeric promotion rules remain separate decisions.

### 10.9 Accepted increment and decrement statements

`++` and `--` are postfix standalone mutation statements, not expression operators:

```ebnf
increment_statement
    = IDENT, ( "++" | "--" ), ";" ;
```

The parser records the target identifier and postfix operator. The statement does not form an expression, so it cannot be nested. Mutability, numeric type, and update behavior are future semantic/runtime concerns.

```text
let count = 5;
count++;              // 6

let length = 5m;
length++;             // 6m

let flexible: Length = 20cm;
flexible++;           // 21cm
```

Prefix and expression-valued forms are syntax errors: `++count` and `print(count++)` are invalid. `constValue++` and `flag++` are syntactically valid and could only be rejected later for constness or nonnumeric type.

## 11. Initial source AST

### 11.1 Expression-core AST

```text
SourceFile
    expression: Expr
    span: SourceSpan

Expr
    NumberLiteral
        lexeme
        span

    QuantityLiteral
        magnitude: NumberLiteral
        unit: UnitExpr
        span

    UnaryExpr
        operator
        operand
        operator_span
        span

    BinaryExpr
        left
        operator
        right
        operator_span
        span

    GroupExpr
        inner
        open_span
        close_span
        span

UnitExpr
    UnitName
        name
        span

    UnitMultiply
        left
        right
        span

    UnitDivide
        numerator
        denominator
        span

    UnitPower
        base
        integer_exponent
        span
```

`GroupExpr` could be erased because parentheses do not change semantics, but preserving it initially improves diagnostics and source reconstruction.

### 11.2 Statement AST extension

The final parser AST must add nodes for the accepted declaration, assignment, input/output, conditional, iterative, block, function, and return forms. Their exact fields follow the final EBNF and are still to be completed. No checked or lowered AST belongs to the current project.

## 12. Lexer/parser pipeline

```text
UTF-8 source text
    -> lexical analysis
       tokens with lexemes and source spans
    -> syntactic analysis
       source AST
    -> lexical or syntactic diagnostics when malformed
```

### Phase ownership

| Concern | Owning phase |
| --- | --- |
| Character validity and token boundaries | Lexer |
| Operator precedence and grouping | Parser |
| Whether a bracketed unit expression is grammatically well formed | Parser |
| Whether `kN` is a known unit | Outside the current project |
| Whether `m + s` is semantically legal | Outside the current project |
| Numeric conversion and calculation | Outside the current project |
| Runtime behavior of statements | Outside the current project |

The lexer and parser must not need structural-engineering knowledge or a unit registry. Syntactically valid expressions such as `10m + 5s`, `5m as s`, and `10foo` must still produce ASTs.

## 13. Diagnostics as a language feature

### 13.1 Required diagnostic information

The current implementation reports only lexical and syntactic failures. Where practical, a diagnostic should identify the unexpected character or token, the expected token family or delimiter, the narrowest relevant source span, and a concise correction or recovery point.

### 13.2 Example syntax diagnostic

```text
Expected `]` to close the unit annotation.

  9.8[m/s^2
     ^^^^^^
```

### 13.3 Diagnostic design implications

- Tokens and AST nodes retain exact spans.
- Unit AST nodes retain the spelling the user wrote.
- Grouping information should remain available until diagnostics are produced.
- Unknown identifiers and unknown unit spellings are not lexer or parser errors.
- Recovery must not manufacture cascades of unrelated syntax errors.
- Exact wording may evolve, but diagnostic categories, spans, and recovery boundaries must be testable.

## 14. Test strategy

### 14.1 Lexer tests

Test exact token kinds, lexemes, and spans for:

- integers and decimals;
- adjacent digit-to-letter boundaries;
- unit symbols with uppercase letters;
- operators and delimiters;
- whitespace variations;
- line and column tracking;
- malformed decimals;
- unknown characters;
- longest-match behavior if comments or multi-character operators are added; and
- Unicode aliases, if later accepted.

Representative assertion:

```text
input:  2.5[kN/m^2] * 24[m^2]
tokens: NUMBER LBRACKET IDENT SLASH IDENT CARET NUMBER RBRACKET
        STAR NUMBER LBRACKET IDENT CARET NUMBER RBRACKET EOF
```

The parser validates that each unit exponent's `NUMBER` lexeme is an integer.

### 14.2 Parser tests

Test:

- precedence: `a + b * c`;
- associativity: `a / b / c`;
- grouping: `(a + b) * c`;
- unary operators;
- compound-unit multiplication, division, and powers;
- missing operands;
- missing closing delimiters;
- missing exponents;
- trailing tokens; and
- recovery that produces one useful primary error where possible.

Parser tests should use syntactically valid but dimensionally invalid expressions to confirm that semantic work is not leaking into parsing.

### 14.3 Semantic and evaluator tests

Deferred to a future project. Semantic examples remain useful parser fixtures precisely because a lexer and parser must accept them without attempting unit resolution, dimension checking, conversion, or evaluation.

### 14.5 Diagnostic tests

Use snapshot or golden tests for:

- message wording;
- source labels and carets;
- error ordering; and
- suppression of cascaded lexical and syntax errors.

### 14.6 Test layers

1. Unit tests for lexer states and grammar productions.
2. Phase-boundary tests from source to tokens and from tokens to AST.
3. End-to-end fixtures from source to AST or lexical/syntax diagnostic.
4. Recovery tests at delimiters, semicolons, and closing braces once statement grammar is present.
5. Regression tests for every corrected lexer or parser bug.

### 14.7 Accepted shared core fixture set

**Accepted under SD-003 and revised by decision 075.** These fixtures are the reusable expression-parser foundation. Each later grammar suite must continue to pass them. They do not replace the declaration, I/O, assignment, conditional, and iteration examples required in the final course proposal; those require extension token, AST, malformed-input, and recovery fixtures.

#### Accepted expressions

| ID | Source | Required parser result | Informative future meaning |
| --- | --- | --- | --- |
| A01 | `8[kN/m] * 4m` | Binary multiplication with two quantity operands | Line load times length |
| A02 | `2[kN/m^2] * 3[m^2]` | Binary multiplication with powered compound units | Area load times area |
| A03 | `12kN / 3[m^2]` | Binary division AST | Derived quotient |
| A04 | `3kN * 2m` | Binary multiplication AST | Force times length |
| A05 | `5m / 2m` | Binary division AST retaining both source units | Unit cancellation |
| A06 | `1m + (20cm as m)` | Addition whose right group contains postfix conversion | Explicit conversion intent |
| A07 | `12kN / 3m * 2m` | Left-associated multiplicative AST | Left associativity |
| A08 | `12kN / (3m * 2m)` | Division whose right operand is a grouped multiplication | Grouping changes structure |

#### Syntactically valid future semantic fixtures

| ID | Source | Current parser requirement | Possible future semantic owner |
| --- | --- | --- | --- |
| R01 | `10m + 5s` | Accept and produce an addition AST | Dimension checker |
| R02 | `1m + 20cm` | Accept and produce an addition AST | Conversion checker |
| R03 | `5m as s` | Accept and produce a conversion AST | Conversion checker |
| R04 | `10foo` | Accept `foo` as an attached `IDENT` unit spelling | Unit resolver |
| R05 | `2[N*m] + 3[N/m]` | Accept both compound units and the addition | Dimension checker |

#### Malformed source

| ID | Source | Rejecting phase | Required local problem |
| --- | --- | --- | --- |
| M01 | `100 m` | Parser adjacency validation | A simple unit must touch its number. |
| M02 | `5.` | Lexer | A decimal point requires a following digit. |
| M03 | `9.8[m/s^]` | Parser | The integer exponent is missing. |
| M04 | `9.8[m/s^2` | Parser | The closing `]` is missing. |
| M05 | `9.8[]` | Parser | The unit annotation is empty. |
| M06 | `2[N*m] *` | Parser | The right operand is missing. |

Two fixtures have normative token streams:

```text
100m
-> NUMBER("100") IDENT("m", adjacent-to-previous) EOF
```

```text
9.8[m/s^2]
-> NUMBER("9.8") LBRACKET IDENT("m") SLASH IDENT("s")
   CARET NUMBER("2") RBRACKET EOF
```

The current suite records token streams, AST shapes, and lexical or syntax diagnostics. Semantic expectations may be retained as informative notes for a future checker, but they are not current pass/fail criteria.

## 15. Thin vertical milestones

Each milestone ends at tokens, an AST, or a lexical/syntax diagnostic.

### Milestone 0: documented fixtures

- Use the accepted quantity-literal syntax and the SD-003 fixture set.
- Record token streams, AST shapes, and malformed-input diagnostics.
- Treat every unit spelling as syntax rather than consulting a registry.

### Milestone 1: expression tokens and AST

```text
source -> tokens -> source-located AST
```

Target one multiplication such as `8[kN/m] * 4m`. Verify tokens, precedence, unit-expression structure, and spans.

### Milestone 2: semantic independence

Parse syntactically valid inputs such as `10m + 5s`, `5m as s`, and `10foo`. Verify that the parser does not attempt semantic rejection.

### Milestone 3: complete expression grammar

Add unary operators, the selected binary operators, precedence, grouping, conversion syntax, and compound units.

### Milestone 4: statement grammar

Add declarations, assignment, input/output, conditionals, loops, blocks, functions, and returns in dependency-sized slices. Produce AST nodes without executing statements.

### Milestone 5: syntax diagnostics and recovery

Add malformed numbers, missing operands, delimiters, semicolons, and braces. Recover only at documented boundaries and verify that error cascades remain bounded.

### Milestone 6: lexer/parser conformance run

Run the complete token, AST, malformed-input, and recovery fixture set. Record the implementation version, environment, command, and results.

### Future project boundary

Unit resolution, semantic checking, conversion, evaluation, and code generation require a separate formally approved project boundary.

## 16. Syntax acceptance and rejection criteria

A proposed syntax should be rejected or redesigned when one or more of the following remain true after simplification:

1. Its characters cannot be enumerated clearly.
2. Its token boundaries depend on whether an identifier is semantically a known unit.
3. Tokenization requires broad context or irregular whitespace rules.
4. Its grammar requires excessive lookahead or backtracking for ordinary cases.
5. It creates unresolved ambiguity between unit operators and expression operators.
6. It cannot be represented by a small, comprehensible AST.
7. A malformed construct cannot produce a local diagnostic.
8. Its grammar rule is difficult for a reader to explain.
9. It reserves punctuation or keywords without enough domain value.
10. It makes future user-defined units substantially harder without helping version 0.1.
11. It makes source formatting significant without a compelling reason.
12. It pushes dimension or structural meaning into the lexer or parser.
13. It requires substantially more implementation machinery than its first motivating use case justifies.
14. Its ASCII form is awkward to type, test, or document.

Every accepted syntax proposal must document:

- characters used;
- token sequence;
- grammar production;
- AST shape;
- post-parse semantic checks;
- ambiguities and required lookahead;
- malformed-input behavior; and
- domain value relative to implementation cost.

## 17. Major unresolved design questions

### Syntax and lexical analysis

- Are comments needed in version 0.1?
- Should integer unit exponents have a distinct token or be validated by the parser?
- Which Unicode aliases, if any, are accepted?
- What notation should future collections use now that square brackets delimit compound unit annotations?

### Future semantic model—not required by this project

- What concrete requirement would justify adding a new named dimension or quantity kind beyond the accepted LMT-plus-Force model?
- Does version 0.1 enforce dimensions only, or any named quantity kinds?
- If kinds exist, how are they inferred through arithmetic?
- Can two same-dimension, different-kind quantities be converted explicitly?
- If a future extension introduces same-dimension named meanings, what metadata and operations would distinguish them?

### Future conversion and numbers—not required by this project

- What numeric representation is used?
- What internal canonical units are used?
- When are conversions inserted?
- What unit is chosen for displayed results?
- What are the rounding and overflow rules?
- How are percentages represented?

Explicit `as` syntax is settled. Its numeric lowering, precision, and result-display behavior are deferred to a separate semantic project rather than open blockers for this one.

### Execution

**Outside the current project.** Decision 075 supersedes the former direct-evaluation plan. The current implementation neither interprets the AST nor generates code.

### Later language growth

- How are units written in variable and function signatures?
- Does inference cross function boundaries?
- How are user-defined units declared safely?
- How do runtime inputs carry units?
- Which structural object first justifies records, functions, or collections?
- How are domain constraints distinguished from general assertions?

## 18. Professor documentation-outline crosswalk

| Requested topic | Location or current status |
| --- | --- |
| Introduction and inspiration | Sections 2 and 3 |
| Character set | Section 9.1 |
| Identifiers and regular expression | Sections 9.2 and 9.4; general variables deferred |
| Literals (added proposal section) | Numeric, string, Boolean, and quantity-literal forms follow Identifiers; detailed unit-expression grammar remains under Expressions. See decision 082. |
| Arithmetic operations and machines | Sections 9.5 and 10 |
| Boolean relational/logical operations | Required if used by the selected conditional and iterative grammar; exact syntax remains to be completed |
| Keywords and reserved words | Complete inventory is normative in `LANGUAGE-SPECIFICATION.md`; `as` is required for explicit conversion, and `to`, `then`, and `do` are reserved noise words. `rate`, `Money`, and `Temperature` are deferred. |
| Noise words | Optional `to`, `then`, and `do`, matching the teammate proposal; Section 9.6 |
| Comments and machine | Open; candidate forms in Section 9.6 |
| Blanks/spaces | Section 9.6 |
| Delimiters/brackets and machines | Sections 9.5 and 10 |
| Free- or fixed-field format | Free-field; Section 9.6 |
| Expression rules and precedence | Section 10.1 |
| Declaration statement | Required in the final proposal and parser grammar; annotation and inference syntax already bounded |
| Input/output statements | Required in the final proposal and parser grammar; exact productions remain open |
| Assignment statement | Required in the final proposal and parser grammar |
| Conditional statements | Required in the final proposal and parser grammar with mandatory braces |
| Iterative statements | Required in the final proposal and parser grammar with mandatory braces |

The final course proposal may need state-machine diagrams for every required token family. Those diagrams should be generated only after the corresponding syntax is selected; drawing machines for undecided tokens would present candidates as commitments.

## 19. Teammate draft to decision-log mapping

### 19.1 Mapping policy

The teammate draft is valuable because it supplies concrete syntax, semantic examples, diagnostics, and an implementation sketch. It does not by itself change the version 0.1 boundary or settle a roadmap decision. This crosswalk uses five classifications:

- **Accepted**: selected as part of the language design, with its implementation milestone stated separately.
- **Aligned**: supports an already established project requirement, without necessarily settling its exact design.
- **Candidate**: supplies an alternative that must be compared under the cited decision record.
- **Deferred**: describes a feature intentionally outside version 0.1.
- **Conflict**: contradicts or overstates a current boundary, phase separation, or safety requirement and must be resolved explicitly.

### 19.2 Design-specification crosswalk

| Teammate-draft specification | Decision-log mapping | Current project treatment |
| --- | --- | --- |
| The language is named `Measure` and follows the principle "Meaning Before Math." | SD-001, SD-002 | **Candidate.** The name and slogan may be adopted separately from the technical design. Terms such as unit, dimension, type, and meaning must first be normalized under SD-002. |
| Units participate in static checking; multiplication and division derive result units; incompatible dimensions are rejected before execution. | SD-001, SD-003, SD-030, SD-031 | **Accepted and formalized.** The LMT vector model, derived `Force`, normalization rules, bounds, and initial conformance cases are recorded. |
| The target audience includes students and beginner programmers. | SD-001 | **Aligned.** These users fit the educational charter. |
| Small businesses, currencies, and engineers prototyping real calculations are initial targets. | SD-001; decision 078 | **Conflict / Deferred.** Currency is excluded from the current proposal, and professional engineering use remains subject to the educational-use disclaimer. |
| Source characters are an ASCII-style set; identifiers begin with a letter and then contain letters, digits, or underscores; names are case-sensitive. | SD-010, SD-013 | **Candidate.** This is evidence for UTF-8 source with canonical ASCII syntax and the existing identifier machine. Whether unit names share `IDENT` and whether keywords are reserved require separate decisions. |
| Integer syntax includes an optional leading minus. | SD-012, SD-020, SD-021 | **Accepted with revision.** Signs are parser-level unary operators, so `-5` is `MINUS NUMBER`, not one numeric token. |
| Simple quantities use attached spelling such as `100m`; the draft describes the number and unit as one value token. | SD-012, SD-013, SD-014, SD-024 | **Accepted with revision.** The spelling is adopted, but the token stream is `NUMBER IDENT`; adjacency is checked from token metadata and unit lookup remains post-parse. |
| Compound quantity literals use brackets, such as `9.8[m/s^2]`. | SD-014, SD-015, SD-022 | **Accepted.** Brackets provide the compound-unit boundary. Square brackets are therefore committed to unit annotations in the current language design. |
| Units must touch numbers; ordinary whitespace is otherwise optional or separating; the language is free-field. | SD-011, SD-014, SD-023 | **Partly aligned, partly candidate.** Free-field format and required quantity attachment are established. Statement/newline behavior must be completed for the current parser grammar. |
| Both `//` line comments and `/* ... */` block comments are supported. | SD-011, decision 076 | **Accepted with refinement.** Block comments do not nest, unterminated block comments are lexical errors, and comments cannot interrupt quantity attachment. |
| Arithmetic includes `+`, `-`, `*`, `/`, `%`, and numeric `^`; unary operators include prefix/postfix `++` and `--`. | SD-020, SD-021, SD-026, SD-029 | **Accepted as a staged design.** Version 0.1 contains unary signs and `+`, `-`, `*`, `/`. Numeric `^` is accepted for a later layer. Postfix `++` and `--` are accepted only as standalone mutation statements. `%` remains open. |
| Boolean, relational, logical, and assignment operators are part of the language. | SD-020, SD-021; required statement surface | **Required where used by the selected parser grammar.** Exact token inventory, precedence, and productions remain to be completed; their semantics are outside this project. |
| `as` performs explicit conversion, and differently scaled compatible units cannot be added or compared without it. | SD-020, SD-021, SD-043, SD-044 | **Accepted.** Compatible-unit conversion is explicit. Postfix `as` binds more tightly than arithmetic; numeric lowering and display policy remain separate decisions. |
| Unit products, quotients, and integer powers form derived units; division of a unit by itself yields a scalar. | SD-015, SD-022, SD-031, SD-033, SD-034 | **Accepted with bounded syntax.** Dimension algebra, grouping, signed integer powers, resource limits, normalization, and named-versus-expanded equality are fixed. Preferred display remains separate. |
| User declarations may define `dimension`, `unit`, and currency `rate` bindings. | SD-032, SD-035, SD-043; decision 078 | **Deferred.** User-defined dimensions and units, currency, and `rate` declarations are outside the current proposal. |
| Temperature points and differences are separate types. | SD-050 through SD-053; decision 078 | **Deferred.** The distinction remains useful future design input but is not part of the current proposal. |
| Functions carry dimension contracts such as `fn speed(distance: Length, time: Time): [m/s]`. | SD-023, SD-027, decision 084; future SD-050 through SD-053 | **Accepted syntax.** A colon introduces the explicit return annotation; contract checking, conversion at boundaries, and polymorphism are outside this project. |
| Declarations, mutable assignment, input/output, conditionals, loops, assertions, strings, functions, and a required `main` entry point are included. | SD-001, SD-023, SD-027; required statement surface | **Partly accepted for the current parser target.** The professor-required statement categories must receive grammar and AST nodes. Additional assertions and entry-point conventions remain subject to syntax decisions; `main` is not reserved. Runtime behavior is excluded. |
| Every statement ends with `;`, blocks use braces, and square brackets are reserved for compound units. | SD-014, SD-023; required statement surface | **Accepted for the current parser grammar.** Simple statements require semicolons and control-flow bodies require braces. |
| Diagnostics identify incompatible dimensions or units and sometimes suggest an explicit conversion. | SD-035, SD-060 through SD-064 | **Aligned direction.** The examples are candidate diagnostic fixtures. They do not yet define span labels, taxonomy, cascade control, or stable wording. |
| The compiler pipeline is lexer -> parser -> unit checker -> Python code generator. | SD-024, IM-073, IM-074, decision 075 | **Narrowed to the course boundary.** The current pipeline is source -> lexer -> parser -> source-located AST. Checking and generation are outside the project. |
| Unit labels are erased and generated Python uses ordinary floating-point arithmetic with zero runtime cost. | SD-041, SD-042, SD-045, IM-074 | **Outside the current project.** No numeric runtime or generated Python exists in the lexer/parser deliverable. |

### 19.3 Decisions adopted from or materially informed by the draft

The draft should be cited as an input when preparing these decision records:

1. **SD-014 and SD-015:** attached simple literals plus bracketed compound literals are accepted, using `NUMBER IDENT` tokenization for the simple form.
2. **SD-020 and SD-021:** the minimal version 0.1 operator set is accepted; the broader operators are staged behind their semantic dependencies.
3. **SD-043:** explicit-only `as` conversion is accepted and binds more tightly than arithmetic.
4. **Required statement surface:** use the draft's declarations, I/O, assignment, control-flow, and function forms as design input for lexer/parser decisions.
5. **SD-060 through SD-064:** define lexical/syntax diagnostics and recovery; retain the draft's semantic messages only as future examples.
6. **Decision 076:** the deliverable is proposal-only, and `LANGUAGE-SPECIFICATION.md` is normative; no implementation or backend is required.
7. **Decision 078:** money and affine temperature are deliberately deferred from the current proposal.

### 19.4 Items excluded from the current proposal

The proposal documents declarations, mutation, control flow, functions, and input/output at the language-design level. Currency, affine temperature, user-defined-unit declarations, implementation architecture, evaluation, and code generation remain excluded.

## 20. Reference documents

Decision record index: [`decisions/README.md`](decisions/README.md)

- `Outline - Documentation-for-PL-Proposal-2024.pdf`: professor-provided checklist for proposal documentation.
- `PPL_Mini-Programming-Language-Proposal.pdf`: professor-provided sample showing one prior proposal's presentation depth and use of lexical machines, regular expressions, precedence tables, and statement examples.
- `Measure_A_Unit-Safe_Programming_Language_PL_Proposal.md`: teammate-authored working draft containing proposed surface syntax, unit semantics, statement forms, diagnostics, and a Python code-generation sketch; mapped in Section 19 and treated as non-normative.

These references inform document coverage only. They are not specifications for this project.

## 21. Next planning step

The next design activity should complete the remaining lexical details around the accepted literal syntax—comment policy, numeric forms, identifier rules, malformed adjacency diagnostics, and Unicode policy—then finish the expression and statement EBNF, AST shapes, and bounded parser recovery. Numeric representation, semantic checking, conversion lowering, result display, and execution are not decisions required by this project.
