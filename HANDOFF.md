# Standard Measurement Language Project Handoff

Handoff date: 2026-11-01  
Project name: Standard Measurement Language (SML)  
Current phase: front-end documentation hardening  
Implementation status: not started

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
4. [Normative language specification](LANGUAGE-SPECIFICATION.md)
5. [Specification roadmap](SPECIFICATION-ROADMAP.md)
6. [Project rationale and historical design](PROJECT.md)
7. [Decision index](decisions/README.md)

The first three files are the new implementation-facing hardening layer. `LANGUAGE-SPECIFICATION.md` remains the normative authority for the language surface until it is deliberately amended.

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
- syntactic diagnostics and documented recovery.

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
- zero-width `EOF` and missing-token locations; and
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

## Next hardening task

Create `docs/frontend/GRAMMAR.ebnf` by extracting the complete version 0.1 grammar from `LANGUAGE-SPECIFICATION.md`.

Before marking it accepted:

1. Include the complete source-file, function, statement, declaration, expression, and unit-expression grammar.
2. Remove historical alternatives and explanatory pseudogrammars.
3. Preserve the accepted precedence and associativity.
4. Check shared-prefix productions such as `NUMBER` versus quantity literals, `IDENT` versus calls, and assignment/update statements.
5. Check every terminal against `TOKEN-SPEC.md`.
6. Surface genuine ambiguities for discussion rather than silently choosing a parse.
7. Add a short mapping from grammar sections to the normative specification.

After the grammar, the planned order is:

1. `AST-SCHEMA.md`
2. `DIAGNOSTICS.md`
3. `RECOVERY.md`
4. machine-readable `fixtures/`
5. `TRACEABILITY.md`
6. implementation-language, parser-strategy, and repository-tooling decisions

No implementation should begin until the contracts required by the relevant readiness gate are accepted.

## Language-name migration

The current name is **Standard Measurement Language (SML)**. The newly hardened front-end documents use this name.

The older proposal, roadmap, and decision records still contain the former name **Measure**. This is intentional at handoff time: a broad search-and-replace was not performed while pausing work.

On resumption, perform a controlled terminology migration:

1. Rename the title and current-language references in `LANGUAGE-SPECIFICATION.md`.
2. Update active references in `PROJECT.md` and `SPECIFICATION-ROADMAP.md`.
3. Decide whether historical decision records should preserve the former name as history or receive a note explaining the rename.
4. Search case-sensitively for the proper noun `Measure`; do not replace ordinary uses of the verb or noun “measure.”
5. Recheck headings, examples, repository description, and future implementation package names.

Because “SML” is also widely associated with Standard ML, the GitHub repository description should spell out **Standard Measurement Language** and identify it as a unit-aware educational language.

## GitHub repository setup

This folder is not currently a Git repository. No commits have been created.

A suitable repository name is `standard-measurement-language`. Before the first commit:

1. Create a root `README.md` that introduces Standard Measurement Language and links to this handoff and the normative specification.
2. Add a `.gitignore` appropriate for the eventual implementation language.
3. At minimum, ignore generated working material:

   ~~~gitignore
   graphify-out/
   tmp/
   __pycache__/
   *.py[cod]
   .venv/
   ~~~

4. Review whether `test.py` should be removed or retained; it is currently empty.
5. Keep the professor-provided PDF and proposal source documents unless the team intentionally relocates them.
6. Initialize Git only after reviewing the initial file set so generated caches are not committed accidentally.
7. Make the first commit a documentation-baseline commit; do not imply that lexer or parser implementation exists.

No remote repository, branch, commit, or GitHub configuration was created during this handoff.

## Known unfinished work

- The complete grammar has not been consolidated into `GRAMMAR.ebnf`.
- The full statement and function AST schema is not defined.
- Diagnostic codes and message requirements are not frozen.
- Parser recovery and cascade control are not frozen.
- Fixtures exist mainly as prose rather than machine-readable data.
- No implementation language, lexer approach, parser approach, testing framework, or directory structure has been selected.
- The normative specification still uses the former language name.
- `test.py` is empty.

## Safe continuation rule

Keep each hardening change small and reviewable. If a new implementation-facing document conflicts with `LANGUAGE-SPECIFICATION.md`, stop at the conflict. Either follow the normative specification or deliberately amend it; do not let an implementation convenience silently redefine SML.
