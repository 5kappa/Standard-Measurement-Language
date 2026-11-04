# Standard Measurement Language

Standard Measurement Language (SML) is an educational, unit-aware programming-language proposal. Its central design goal is to make measurement syntax explicit while keeping lexical structure, grammar, and later physical meaning clearly separated.

> This project is unrelated to the Standard ML programming language. The full name **Standard Measurement Language** is used in project descriptions to avoid ambiguity.

## Current status

The **front-end documentation-hardening phase and version 0.1 lexer are complete**. Lexer roadmap milestones R0 through R10, the lexer-only conformance gate, and the lexer command-line interface pass under Python 3.11.9; parser implementation has not started.

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
- [Lexer development roadmap](docs/frontend/LEXER-ROADMAP.md) — completed lexer milestones and conformance gate
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

The machine-readable fixture format and complete 93-case conformance suite are accepted in [`docs/frontend/fixtures/README.md`](docs/frontend/fixtures/README.md), and [`docs/frontend/TRACEABILITY.md`](docs/frontend/TRACEABILITY.md) contains the completed coverage registry. The byte-oriented lexer now passes its complete lexer-only fixture scope: all 44 indexed lexer and source-location records plus the frontend invalid-UTF-8 phase-gate case. Parser and AST fixtures remain pending until parser implementation begins.

The initial engineering stack is accepted in [`docs/frontend/IMPLEMENTATION.md`](docs/frontend/IMPLEMENTATION.md): Python 3.11.9, a handwritten byte-oriented lexer, standard-library fixtures and tests, and a handwritten recursive-descent parser later.

Run the lexer on a source file and write its deterministic text report to standard output:

~~~powershell
.venv\Scripts\python.exe -m sml_frontend input.sml
~~~

Use `--output` to write the report to a file instead:

~~~powershell
.venv\Scripts\python.exe -m sml_frontend input.sml --output output.txt
~~~

The report includes every valid token, its half-open byte span, and a JSON-quoted lexeme. Lexical failures additionally include valid partial tokens, structured diagnostics, secondary labels, and the diagnostic-truncation flag. The command exits with status `0` for lexical success, `1` for lexical failure, `2` for argument or file-I/O failure, and `3` for an unexpected internal frontend failure. An input/output path collision is rejected so the source file cannot be overwritten.

Run the completed lexer gate from the repository root with the exact project interpreter:

~~~powershell
.venv\Scripts\python.exe --version
.venv\Scripts\python.exe -m unittest tests.test_cli
.venv\Scripts\python.exe -m unittest tests.test_source tests.test_lexer tests.test_fixtures
.venv\Scripts\python.exe -m unittest discover
.venv\Scripts\python.exe -m compileall sml_frontend tests
~~~

See [`HANDOFF.md`](HANDOFF.md) before continuing work on another workstation.

## Naming history

The current project name is **Standard Measurement Language (SML)**. The teammate draft, legacy proposal, and historical decision records may retain the former name **Measure** when recording earlier work. Current normative, planning, and implementation-facing documents use the new name.

## Educational-use boundary

SML is an educational language-design project. Its syntax, diagnostics, examples, and any future implementation must not be represented as suitable for professional engineering decisions, code compliance, certification, or construction safety.
