# Standard Measurement Language

Standard Measurement Language (SML) is an educational, unit-aware programming-language proposal. Its central design goal is to make measurement syntax explicit while keeping lexical structure, grammar, and later physical meaning clearly separated.

> This project is unrelated to the Standard ML programming language. The full name **Standard Measurement Language** is used in project descriptions to avoid ambiguity.

## Current status

The **front-end documentation-hardening phase is complete**, and lexer implementation is active. Roadmap milestones R0 through R3 are complete; parser implementation has not started.

The final implementation boundary is:

~~~text
UTF-8 source
    -> lexer
    -> tokens with original lexemes and source spans
    -> parser
    -> source-located AST or lexical/syntax diagnostics
~~~

Semantic analysis, unit-name resolution, dimensional checking, unit normalization, evaluation, code generation, and runtime behavior are outside the project scope.

## Start here

- [Project handoff](HANDOFF.md) — current state, finalized decisions, and continuation instructions
- [Front-end development charter](docs/frontend/README.md) — scope and document authority
- [Source-location contract](docs/frontend/SOURCE-LOCATIONS.md) — accepted spans, lines, columns, and adjacency
- [Token specification](docs/frontend/TOKEN-SPEC.md) — accepted tokens and lexical behavior
- [Grammar](docs/frontend/GRAMMAR.ebnf) — accepted token-level syntax and parser context constraints
- [Source AST schema](docs/frontend/AST-SCHEMA.md) — accepted successful-parse nodes, source preservation, collections, and spans
- [Diagnostic contract](docs/frontend/DIAGNOSTICS.md) — accepted lexical and syntactic codes, labels, ordering, and failure behavior
- [Lexer development roadmap](docs/frontend/LEXER-ROADMAP.md) — active lexer-only milestones and progress
- [Language specification](LANGUAGE-SPECIFICATION.md) — normative language surface
- [Decision index](decisions/README.md) — design history and rationale

## Important front-end boundary

The lexer and parser recognize spelling and structure; they do not determine whether a unit name exists or whether an operation is physically meaningful.

For example:

~~~text
10foo          accepted as NUMBER IDENT
10 foo         rejected because the unit is detached
1[m^2/m]       parsed without simplifying it to m
1[kg/m/m]      rejected because repeated division violates the unit grammar
~~~

Unknown-unit detection would require name resolution, which is not part of the lexer/parser-only implementation.

## Implementation readiness

The machine-readable fixture format and complete 93-case conformance suite are accepted in [`docs/frontend/fixtures/README.md`](docs/frontend/fixtures/README.md), and [`docs/frontend/TRACEABILITY.md`](docs/frontend/TRACEABILITY.md) contains the completed coverage registry. Lexer implementation now proceeds incrementally against those accepted contracts and fixtures; R0 through R3, including ordinary names, accepted decimal numbers, separate signs, EOF, and basic adjacency, are complete.

The initial engineering stack is accepted in [`docs/frontend/IMPLEMENTATION.md`](docs/frontend/IMPLEMENTATION.md): Python 3.11.9, a handwritten byte-oriented lexer, standard-library fixtures and tests, and a handwritten recursive-descent parser later.

See [`HANDOFF.md`](HANDOFF.md) before continuing work on another workstation.

## Naming history

The current project name is **Standard Measurement Language (SML)**. The teammate draft, legacy proposal, and historical decision records may retain the former name **Measure** when recording earlier work. Current normative, planning, and implementation-facing documents use the new name.

## Educational-use boundary

SML is an educational language-design project. Its syntax, diagnostics, examples, and any future implementation must not be represented as suitable for professional engineering decisions, code compliance, certification, or construction safety.
