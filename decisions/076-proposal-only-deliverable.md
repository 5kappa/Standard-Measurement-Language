# 076: Proposal-only deliverable and consolidated specification

Status: ACCEPTED  
Target: current course deliverable  
Depends on: accepted lexical, grammar, unit, declaration, and statement decisions  
Supersedes: decision 075's lexer/parser implementation boundary  
Informed by: the professor's PL-proposal outline and the teammate draft's complete lexical and statement surface

Amended by: decision 078, which defers money and affine temperature without changing the proposal-only boundary

## Decision

The current deliverable is a programming-language proposal, not a lexer, parser, checker, evaluator, or code generator.

`LANGUAGE-SPECIFICATION.md` is the normative source for the proposed language surface. `PROJECT.md`, `SPECIFICATION-ROADMAP.md`, and earlier decision records remain supporting rationale and history.

The proposal must document:

- character set and source format;
- lexical rules and machines;
- identifiers, literals, comments, keywords, reserved words, and noise words;
- operators, delimiters, expressions, and precedence;
- declaration, input/output, assignment, conditional, iterative, and function syntax;
- nested statement examples;
- the unit-expression grammar and intended LMT-plus-Force meaning; and
- the Meaning Before Math uniqueness principle.

No implementation architecture, AST, recovery algorithm, runtime numeric representation, semantic checking algorithm, evaluator, or backend is required.

## Adopted teammate-draft defaults

Where no earlier decision conflicted, the consolidated specification adopts the teammate draft's ASCII-style surface, case-sensitive identifiers, `//` and non-nesting `/* */` comments, free-field format, Boolean operators, relational operators, `%`, C-style `for`, `while`, `print`, `input`, functions, returns, assertions, `break`, and `continue`.

## Applied revisions

- Signs are parser-level operators.
- A simple quantity is `NUMBER IDENT`, not one combined token.
- `as` is a tight postfix conversion form.
- Prefix and expression-valued increment/decrement are removed.
- Assignment is a statement rather than an expression.
- Declarations contain one initialized binding.
- Annotation categories cannot be combined.
- Every conditional and loop body uses braces.
- `main` is not reserved.
- Currency, affine temperature, user-defined unit/dimension declarations, and Python generation are excluded.
- `Scalar` describes a dimensionless quantity rather than naming a dimension type.

## Revisit trigger

Revise the consolidated specification only when the team deliberately changes a proposal feature or the professor clarifies a requirement. Implementation concerns alone do not reopen proposal syntax.
