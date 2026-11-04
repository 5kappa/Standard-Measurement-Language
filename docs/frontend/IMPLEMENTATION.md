# Standard Measurement Language Frontend Implementation Plan

Status: accepted engineering baseline  
Applies to: initial SML version 0.1 lexer and later parser implementation  
Depends on: all accepted frontend contracts and [decision 089](../../decisions/089-python-frontend-implementation.md)

## Boundary

This document selects implementation technology. It is not a language specification and must not change observable tokens, ASTs, diagnostics, failure behavior, or fixtures.

## Technology baseline

| Concern | Accepted choice |
| --- | --- |
| Host language | Python 3.11.9 reference interpreter |
| Runtime dependencies | None |
| Lexer | Handwritten deterministic scanner over original `bytes` |
| Token recognition | Explicit byte classification and loops; no core regex |
| Frontend records | Standard-library `dataclasses` and `enum` |
| Fixture input | Trusted version-controlled JSON decoded by test-only helpers |
| Tests | Standard-library `unittest` |
| CLI | Standard-library `argparse` |
| Initial checks | `python -m unittest discover`; `python -m compileall sml_frontend tests` |
| Parser later | Handwritten recursive descent, one function per grammar or precedence level |
| Generated code | None |

An optional virtual environment may isolate the interpreter, but the initial implementation installs no runtime or test packages.

## Source boundary

The public lexer accepts original source bytes:

```text
lex(source: bytes) -> LexSuccess | LexFailure
```

The complete source must not be decoded before lexing. The lexer decodes only spans already established as well-formed UTF-8. It retains the original bytes through scanning so token lexemes, byte spans, malformed ranges, and diagnostic data remain exact.

## Core Python records

The implementation uses immutable returned records conceptually equivalent to:

```python
from dataclasses import dataclass, field

@dataclass(frozen=True)
class SourceSpan:
    start_byte: int
    end_byte: int

class TokenKind(Enum):
    ...

@dataclass(frozen=True)
class Token:
    kind: TokenKind
    lexeme: str
    span: SourceSpan

class DiagnosticCode(Enum):
    LEX001 = "LEX001"
    # ... through LEX010 and later parser codes

DiagnosticValue = str | int | bool

@dataclass(frozen=True)
class Diagnostic:
    code: DiagnosticCode
    phase: DiagnosticPhase
    severity: Severity
    primary: DiagnosticLabel
    secondary: tuple[DiagnosticLabel, ...]
    notes: tuple[DiagnosticNote, ...]
    data: dict[str, DiagnosticValue] = field(default_factory=dict)

@dataclass(frozen=True)
class LexSuccess:
    tokens: tuple[Token, ...]

@dataclass(frozen=True)
class LexFailure:
    partial_tokens: tuple[Token, ...]
    diagnostics: tuple[Diagnostic, ...]
    diagnostics_truncated: bool
```

The pseudocode fixes responsibilities rather than exact Python spelling. The implementation may split shared records among modules, but it must preserve the documented observable fields.

## Failure classification

`LexFailure` means that at least one malformed-source condition occurred during the scan. It is not specialized into classes such as `InvalidUtf8Failure` or `MalformedNumberFailure` because one source can contain several different failures.

The specific failure types are the ordered diagnostic codes:

```text
LexFailure
    diagnostics:
        LEX006 SCIENTIFIC_NOTATION
        LEX002 INVALID_SOURCE_CHARACTER
```

Required invariants:

- `LexFailure.diagnostics` contains from one through twenty diagnostics;
- every contained diagnostic has phase `LEXER` and code `LEX001` through `LEX010`;
- different codes may coexist in one result;
- the direct `Diagnostic.data` mapping carries the stable fields required by `DIAGNOSTICS.md`;
- `partial_tokens` ends with physical `EOF`;
- malformed source does not raise a Python exception; and
- the parser is never called with `LexFailure`.

File access errors are reported by the CLI before calling `lex`. Unexpected invariant violations are internal implementation failures; they are not converted into lexical source diagnostics. The application boundary may report them as `ICE001` while preserving debugging information.

## Command-line boundary

The completed command-line entry point is intentionally smaller than the lexer:

```powershell
.venv\Scripts\python.exe -m sml_frontend INPUT [--output PATH]
```

It reads `INPUT` with `Path.read_bytes()`, passes the unchanged bytes to `lex`, and writes a deterministic human-readable report to standard output unless `--output` names a file. It does not pre-decode the complete source. Existing explicitly named output files may be overwritten; a resolved input/output path collision is rejected before reading or writing so the source cannot be overwritten.

Every token line contains the token kind, zero-based half-open byte span, and JSON-quoted lexeme. A failure report contains the valid partial token collection followed by each diagnostic code, primary span, stable JSON diagnostic data, any secondary label roles and spans, and the lowercase `diagnostics_truncated` state. JSON quoting uses ASCII escapes and sorted object keys so report text is stable across output environments. English diagnostic prose remains non-normative and is not synthesized by this boundary.

Process exit statuses are:

| Status | Meaning |
| --- | --- |
| `0` | Lexical success; the complete token collection was reported |
| `1` | Lexical failure; valid partial tokens and diagnostics were reported |
| `2` | Argument parsing, path resolution, input read, or output write failure |
| `3` | Unexpected internal frontend failure, reported as `ICE001` |

The boundary never calls a parser. `tests/test_cli.py` covers direct `main(argv)` behavior and a real `python -m sml_frontend` subprocess invocation using only the standard library.

## Lexer architecture

One scanner instance owns:

```text
source: bytes
offset: byte index
line: one-based logical line
column: one-based display column
state: ordinary | string | line-comment | block-comment
tokens
diagnostics
diagnostics_truncated
```

The main loop dispatches to small functions such as:

```text
scan_identifier_or_keyword
scan_numeric_candidate
scan_string
scan_slash_or_comment
scan_operator_or_delimiter
report_invalid_utf8_byte
```

Every successful scanner function consumes at least one byte. Every failure path follows `RECOVERY.md` and also consumes a nonempty range. Bytewise invalid UTF-8 consumes exactly one byte.

The lexer does not consult declarations, units, functions, types, dimensions, or runtime values.

## Fixture and test architecture

Fixtures are trusted, version-controlled conformance data. The test loader validates only enough structure to decode and execute the indexed fixture cases. Exhaustive validation of the fixture format is not part of the lexer implementation.

Test-only helpers use the standard-library `json` module to read the fixture records needed by the current milestone, construct source bytes and expected frontend records, and compare those expectations with actual results. Support for a new fixture result variant is added only when the corresponding lexer or parser milestone begins.

Test layers are:

1. focused unit tests for byte classification, UTF-8 validation, positions, and scanner functions;
2. machine-readable lexer-success and lexical-failure conformance fixtures decoded by small test-only helpers; and
3. later source-to-AST frontend fixtures after parser implementation.

Rendered English diagnostic messages may have implementation-specific tests but are not conformance snapshots.

## Repository layout

```text
sml_frontend/
    __init__.py
    __main__.py
    source.py
    token.py
    diagnostic.py
    lexer.py
tests/
    fixture_loader.py
    test_cli.py
    test_source.py
    test_lexer.py
    test_fixtures.py
docs/frontend/fixtures/
    README.md
    index.json
    ... categorized fixture files ...
```

The top-level package makes `python -m unittest discover` and `python -m sml_frontend` work from the repository without installation or path configuration. Parser modules are intentionally absent until parser work begins. At that point, `syntax.py` and `parser.py` are added without changing the lexer API.

## Later parser strategy

The parser will be handwritten recursive descent. Expression parsing follows the accepted precedence hierarchy with one function per level rather than a Pratt binding-power table. Grammar-specific functions handle source files, functions, blocks, statements, declarations, calls, and unit expressions.

This strategy is compatible with the accepted first-error policy: a parse function returns a node or propagates the first structured syntax diagnostic. It uses no parser generator, parser combinator framework, or external AST library.

## Deferred tools

The baseline does not require a formatter, linter, static type checker, third-party test runner, package publisher, or CI service. These may be added later as development conveniences. Any addition must remain non-normative and must not alter fixture interpretation or frontend behavior.

GitHub Actions may run the two accepted check commands with Python 3.11.9 after a workflow is added.

## Readiness rule

The technology decision, trusted-fixture policy, and complete static conformance suite are accepted. The R0–R10 byte-oriented lexer is implemented and passes the lexer-only conformance gate under Python 3.11.9. Parser work may begin from the accepted grammar, AST, diagnostic, recovery, and fixture contracts without changing the lexer API.

