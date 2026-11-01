# 075: Lexer-and-parser project boundary

Status: SUPERSEDED by decision 076  
Target: historical lexer/parser implementation plan  
Depends on: SD-010 through SD-025  
Supersedes: decisions 001's expression-only implementation boundary and 074's execution model  
Informed by: the course deliverable being a lexer and parser, the professor's required lexical and syntactic documentation, and the teammate proposal's broader surface syntax

## Decision

Decision 076 later clarified that the course deliverable is the proposal itself. The lexer/parser boundary below is retained only as historical planning context and is not a current implementation requirement.

The current implementation ends after parsing:

```text
UTF-8 source
    -> lexer
    -> tokens with source spans
    -> parser
    -> source-located AST
    -> lexical or syntactic diagnostics
```

The implementation does not resolve unit names, check dimensions, insert conversions, evaluate expressions, generate Python, or format numeric results.

The expression fixture set remains the first implementation slice, not the entire language surface required by the final proposal. The lexer and parser specification must eventually cover the selected declaration, assignment, input/output, conditional, iterative, and function syntax required by the course documentation. These constructs may be added in small grammar slices.

## Semantic material

Accepted descriptions of dimensions, units, conversions, inference, and mutation remain language-design rationale. They explain intended meaning and constrain future work, but they are not acceptance criteria for the current lexer/parser implementation.

Syntactically valid but semantically invalid input must still tokenize and parse. For example, `10m + 5s`, `5m as s`, and `10foo` are not lexer or parser errors merely because a future resolver or checker would reject them.

## Required deliverables

- character and source-encoding policy;
- complete token inventory and lexical machines or regular expressions;
- keyword, identifier, number, comment, whitespace, and delimiter rules;
- complete EBNF for the selected proposal surface;
- precedence and associativity;
- source-located AST or parse-tree shapes;
- lexical and syntactic diagnostic categories;
- bounded parser recovery rules; and
- token-stream, AST, malformed-input, and recovery fixtures.

## Explicitly outside the current implementation

- unit-name resolution and registries as executable components;
- dimensional or quantity-kind checking;
- numeric representation, rounding, overflow, and equality;
- conversion lowering and result-display policy;
- temperature and currency semantics;
- interpretation, compilation, code generation, and runtime behavior; and
- semantic diagnostics and semantic cascade recovery.

## Revisit trigger

Add a semantic phase only if a later course deliverable explicitly requires it and the project boundary is formally revised. Do not infer that requirement from semantic examples in the proposal.
