# Standard Measurement Language

Standard Measurement Language (SML) is an educational, unit-aware programming-language proposal. Its central design goal is to make measurement syntax explicit while keeping lexical structure, grammar, and later physical meaning clearly separated.

> This project is unrelated to the Standard ML programming language. The full name **Standard Measurement Language** is used in project descriptions to avoid ambiguity.

## Current status

The project is in the **front-end documentation-hardening phase**. Lexer and parser implementation has not started.

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

- [Project handoff](HANDOFF.md) — current state, finalized decisions, next task, and continuation instructions
- [Front-end development charter](docs/frontend/README.md) — scope and document authority
- [Source-location contract](docs/frontend/SOURCE-LOCATIONS.md) — accepted spans, lines, columns, and adjacency
- [Token specification](docs/frontend/TOKEN-SPEC.md) — accepted tokens and lexical behavior
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

## Next task

The next documentation-hardening artifact is `docs/frontend/GRAMMAR.ebnf`. It must consolidate the complete version 0.1 grammar and expose any genuine ambiguity before parser implementation begins.

See [`HANDOFF.md`](HANDOFF.md) before continuing work on another workstation.

## Naming migration

The current project name is **Standard Measurement Language (SML)**. Some older proposal and decision documents still use the former name **Measure**. The handoff documents the controlled migration required; avoid an indiscriminate global replacement because “measure” may also occur as an ordinary word.

## Educational-use boundary

SML is an educational language-design project. Its syntax, diagnostics, examples, and any future implementation must not be represented as suitable for professional engineering decisions, code compliance, certification, or construction safety.
