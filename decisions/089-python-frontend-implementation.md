# 089: Python frontend implementation technologies

Status: ACCEPTED FOR THE INITIAL FRONT-END IMPLEMENTATION  
Target: Standard Measurement Language version 0.1 lexer and later parser  
Depends on: the accepted frontend contracts, decision 087, and decision 088

## Decision

The initial SML frontend is implemented and tested with Python 3.11.9 as its exact reference interpreter. Changing the reference version requires a deliberate documentation update and a complete conformance run; implementations may later demonstrate compatibility with newer Python releases without changing SML behavior.

The implementation has no runtime dependencies. It uses the Python standard library for data classes, enumerations, JSON, command-line handling, filesystem access, and tests.

### Lexer

The lexer is a handwritten deterministic scanner over the original `bytes`. It does not decode the complete file before scanning. It uses explicit byte classification and dedicated scanner functions rather than a regular-expression-driven lexer or lexer generator.

The scanner owns the current byte offset, logical line, display column, lexical state, tokens, diagnostics, and truncation flag. Returned tokens, spans, diagnostics, and result records are immutable data classes.

### Results and failures

The Python API exposes explicit `LexSuccess` and `LexFailure` record types. `LexFailure` is one overall failed-scan result, not a hierarchy of source-failure subclasses. Its ordered `diagnostics` collection contains one or more `Diagnostic` records whose `DiagnosticCode` values `LEX001` through `LEX010` identify the individual failure types. One result may contain different lexical codes.

Malformed source is ordinary result data and must not raise an exception. File-open and file-read failures occur before lexing and belong to the CLI boundary. Internal invariant failures are implementation defects, not `LexFailure`; they may raise an internal exception that the application boundary reports as `ICE001`.

### Fixtures and tests

The implementation loads the accepted strict JSON fixtures using the standard-library `json` module and performs the additional structural checks required by `docs/frontend/fixtures/README.md`. Tests use standard-library `unittest`. Exact rendered diagnostic English is not snapshot-tested as conformance behavior.

### Command line and repository tools

The initial CLI uses standard-library `argparse`. The initial quality commands are `python -m unittest discover` and `python -m compileall sml_frontend tests`. No formatter, linter, type checker, packaging service, editable installation, or code generator is required to begin. Such development tools may be added later without changing frontend behavior.

### Parser

When parser implementation begins, it will use handwritten recursive descent in the same Python project. Expression precedence is represented by one function per accepted grammar level. Statements, functions, and unit expressions use grammar-specific recursive-descent functions. The parser will not use a parser generator, parser combinator framework, or external parsing library.

## Initial module layout

```text
sml_frontend/
    __init__.py
    __main__.py
    source.py
    token.py
    diagnostic.py
    lexer.py
    fixture_loader.py
tests/
    test_source.py
    test_lexer.py
    test_fixtures.py
```

The top-level package permits direct test discovery and module execution without an editable install or `PYTHONPATH` configuration. Parser and AST modules are added only when parser implementation starts. Machine-readable conformance data remains under `docs/frontend/fixtures/`.

## Reason

Python provides the shortest path to a readable byte-oriented academic lexer while supplying JSON, immutable-style data records, enums, testing, and CLI support in its standard library. A handwritten scanner provides exact control over malformed numeric boundaries, bytewise UTF-8 failure, source positions, continuation, partial tokens, and the diagnostic limit. Handwritten recursive descent later maps directly to the accepted EBNF, source AST, specialized diagnostics, and fail-fast parser policy.

## Rejected alternatives

- Go, C#, and TypeScript remain technically viable, but their static or ecosystem advantages do not outweigh Python's shorter implementation path under the current deadline.
- Rust, Java, and C++ add avoidable implementation, dependency, or boilerplate cost for this academic prototype.
- A regex-driven lexer and lexer generator provide less direct control over byte-invalid source and malformed-candidate continuation.
- A Pratt parser or parser generator is unnecessary because the accepted expression grammar already exposes fixed precedence levels and specialized fail-fast diagnostics.
- Third-party JSON, test, formatting, linting, and type-checking packages are not required for the first implementation baseline.

## Revisit triggers

The team may deliberately amend this engineering decision if the course requires another host language, all implementers are substantially more proficient in another candidate, Python byte-level performance is measured to be inadequate, or a later project introduces deployment requirements that Python cannot meet. Host-language changes must not alter the accepted token, AST, diagnostic, recovery, or fixture contracts.

