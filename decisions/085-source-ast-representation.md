# 085: Source AST representation

Status: ACCEPTED FOR CURRENT PARSER CONTRACT  
Target: Standard Measurement Language version 0.1 parser  
Depends on: SD-017, SD-023, SD-024, `docs/frontend/GRAMMAR.ebnf`, and `docs/frontend/SOURCE-LOCATIONS.md`  
Informed by: the accepted grammar, source-location requirements, diagnostic needs, and a handwritten-parser implementation boundary

## Decision

The parser constructs a source-faithful abstract syntax tree. This decision does not change the lexer: the lexer continues to emit only token kinds, original lexemes, and source spans. The parser consumes those tokens, determines their grammatical roles, and composes them into AST nodes.

The AST uses a hybrid representation:

- an EBNF repetition `{ item }` becomes an ordered collection;
- an EBNF option `[ item ]` becomes an optional field;
- an EBNF alternative becomes a tagged node variant;
- operator associativity remains explicit through nested expression nodes; and
- source separators and delimiters needed for diagnostics are retained as token references.

The representation must be implementable with ordinary records, tagged variants, optional values, and a basic ordered collection. It must not require a parser generator, reflection framework, visitor library, or specialized AST package.

## Source-syntax preservation

- Parenthesized expressions produce explicit `GroupExpr` nodes.
- Literals retain their original tokens rather than storing computed runtime values.
- Operators, delimiters, declaration and control-flow keywords, and statement terminators needed for precise diagnostics remain available as token references.
- Optional noise words `to`, `then`, and `do` do not create semantic nodes, but their optional token references are retained on the containing conversion or control-flow node.
- `SourceFile.span` is `[0, source_byte_length)` and therefore includes leading and trailing trivia.
- Every other AST node spans exactly its represented source construct and excludes unrelated surrounding trivia.

## Repeated structures

### Conditionals

An `if` statement stores its required first branch, an ordered collection of zero or more `else if` branches, and an optional final `else` clause. An `else if` branch is not represented as an artificially nested `IfStmt`. A genuinely nested `if` inside an `else` block remains a separate `IfStmt` in that block's statement collection.

### For headers

`for` initializers and updates use dedicated tagged variants rather than complete statement nodes. Header clauses therefore do not contain synthetic statement terminators or admit statement forms that the grammar excludes.

### Unit products

A unit product stores its first `UnitPower` followed by an ordered collection of star-and-factor parts. A quotient stores one numerator product and one optional slash-and-denominator part. This shape preserves written order and structurally prevents repeated or nested division.

### Separated lists

Parameters, call arguments, and print arguments use a first item followed by ordered separator-and-item parts. Implementations without generic types may define equivalent concrete list records for each element category.

### Expressions

Unary, binary, power, and conversion expressions remain nested nodes. Their tree shape records precedence and associativity so later consumers do not need to reconstruct parser rules.

## Failure boundary

`docs/frontend/AST-SCHEMA.md` defines the AST produced by a successful parse. Decision 086 later selected a fail-fast parser: its first syntax error produces one diagnostic and no AST. The current parser therefore has no synthetic missing-token references or explicit error or recovered-node variants.

Any future recovery design must not change the meaning or fields of successful AST nodes.

## Reason

This hybrid shape follows the accepted EBNF directly and is simple to construct with handwritten recursive-descent functions and loops. It preserves the syntax needed for diagnostics without carrying every grammar wrapper as a concrete-syntax-tree node. It also avoids fake semicolons, invalid nullable-field combinations, artificial `else if` nesting, and overly deep unit-product trees.

## Validation

AST fixtures must demonstrate:

- complete-file and nested-node spans;
- retained grouping and noise-word token references;
- ordered function, statement, branch, parameter, argument, and print-argument collections;
- dedicated `for` initializer and update variants;
- flat written unit products and one optional quotient;
- nested expression nodes with accepted associativity; and
- no AST result after a syntax diagnostic.

