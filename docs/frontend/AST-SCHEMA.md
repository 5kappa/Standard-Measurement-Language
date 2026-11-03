# Standard Measurement Language Source AST Schema

Status: accepted  
Applies to: Standard Measurement Language (SML) version 0.1 parser and successful-parse AST fixtures  
Depends on: [`GRAMMAR.ebnf`](GRAMMAR.ebnf), [`SOURCE-LOCATIONS.md`](SOURCE-LOCATIONS.md), and [decision 085](../../decisions/085-source-ast-representation.md)

## Purpose

This document defines the source abstract syntax tree produced by a successful parse. It fixes every node kind, field, retained token reference, and span-composition rule required before parser implementation begins.

The AST preserves source syntax needed for diagnostics and fixtures. It does not contain resolved declarations, registered units, inferred types, normalized dimensions, checked conversions, computed numeric values, or runtime behavior.

## Notation and common types

The schema uses language-independent pseudotypes:

```text
T?              optional T
List<T>         ordered collection, possibly empty
NonEmpty<T>     ordered collection containing at least one T
A | B           tagged variant containing exactly one alternative
```

An implementation may use arrays, vectors, slices, or a simple linked representation. The observable order and fields must remain the same. No specialized AST library is required.

### Source references

```text
SourceSpan
    start_byte: integer
    end_byte: integer

TokenRef
    kind: TokenKind
    lexeme: string
    span: SourceSpan
```

Every `TokenRef` in a successful AST refers to one real token emitted by the lexer. Its kind, lexeme, and span are unchanged. The parser never recreates a token by rescanning source text.

Every AST node has a `span: SourceSpan`, even where the field is omitted from an inline variant for brevity.

### Separated collections

```text
SeparatedList<T>
    first: T
    rest: List<SeparatedItem<T>>

SeparatedItem<T>
    separator: TokenRef
    item: T
```

`SeparatedList` is always nonempty. For the current grammar, its separator is `COMMA`. Implementations without generic types may define equivalent concrete records for parameters, arguments, and print arguments.

## Source file and functions

```text
SourceFile
    functions: List<FunctionDef>
    eof_token: TokenRef                  // EOF
    span: SourceSpan                     // [0, source_byte_length)

FunctionDef
    fn_keyword: TokenRef                 // FN
    name: TokenRef                       // IDENT
    left_paren: TokenRef                 // LPAREN
    parameters: SeparatedList<Parameter>?
    right_paren: TokenRef                // RPAREN
    return_contract: ReturnContract?
    body: Block
    span: SourceSpan

Parameter
    name: TokenRef                       // IDENT
    annotation_clause: AnnotationClause
    span: SourceSpan

ReturnContract
    colon: TokenRef                      // COLON
    annotation: DeclarationAnnotation
    span: SourceSpan
```

An empty file has no functions, one zero-width `EOF` token, and `SourceFile.span == [0, 0)`. For nonempty source, `SourceFile.span` still covers the complete byte range, including leading and trailing trivia.

## Blocks and statements

```text
Block
    left_brace: TokenRef                 // LBRACE
    statements: List<Stmt>
    right_brace: TokenRef                // RBRACE
    span: SourceSpan

Stmt
    LetDecl
    | ConstDecl
    | AssignmentStmt
    | UpdateStmt
    | PrintStmt
    | CallStmt
    | IfStmt
    | WhileStmt
    | ForStmt
    | ReturnStmt
    | BreakStmt
    | ContinueStmt
    | AssertStmt
```

### Declarations

```text
LetDecl
    let_keyword: TokenRef                // LET
    name: TokenRef                       // IDENT
    annotation_clause: AnnotationClause?
    initializer: InitializerClause?
    semicolon: TokenRef                  // SEMICOLON
    span: SourceSpan

ConstDecl
    const_keyword: TokenRef              // CONST
    name: TokenRef                       // IDENT
    annotation_clause: AnnotationClause?
    initializer: InitializerClause       // required
    semicolon: TokenRef                  // SEMICOLON
    span: SourceSpan

AnnotationClause
    colon: TokenRef                      // COLON
    annotation: DeclarationAnnotation
    span: SourceSpan

InitializerClause
    assign: TokenRef                     // ASSIGN
    value: InitializerValue
    span: SourceSpan

InitializerValue
    Expr
    | InputExpr
```

If `InitializerValue` is `InputExpr`, the declaration must have a primitive or exact-unit annotation as required by `GRAMMAR.ebnf` constraint C5.

### Assignments and updates

```text
AssignmentStmt
    assignment: AssignmentCore
    semicolon: TokenRef                  // SEMICOLON
    span: SourceSpan

AssignmentCore
    target: TokenRef                     // IDENT
    operation: AssignmentOperation
    span: SourceSpan

AssignmentOperation
    SimpleAssignment
    | CompoundAssignment

SimpleAssignment
    operator: TokenRef                   // ASSIGN
    value: AssignmentValue
    span: SourceSpan

CompoundAssignment
    operator: TokenRef                   // PLUS_ASSIGN, MINUS_ASSIGN,
                                         // STAR_ASSIGN, or SLASH_ASSIGN
    value: Expr
    span: SourceSpan

AssignmentValue
    Expr
    | InputExpr

UpdateStmt
    update: UpdateCore
    semicolon: TokenRef                  // SEMICOLON
    span: SourceSpan

UpdateCore
    target: TokenRef                     // IDENT
    operator: TokenRef                   // PLUS_PLUS or MINUS_MINUS
    position: UpdatePosition
    span: SourceSpan

UpdatePosition
    PREFIX
    | POSTFIX
```

For a prefix update, `UpdateCore.span` begins at `operator`; for a postfix update, it begins at `target`. Whether the target is mutable, numeric, or dimensionless is not represented in this AST.

### Output and call statements

```text
PrintStmt
    print_keyword: TokenRef              // PRINT
    left_paren: TokenRef                 // LPAREN
    arguments: SeparatedList<Expr>       // nonempty
    right_paren: TokenRef                // RPAREN
    semicolon: TokenRef                  // SEMICOLON
    span: SourceSpan

CallStmt
    call: CallExpr
    semicolon: TokenRef                  // SEMICOLON
    span: SourceSpan
```

The AST does not record whether a called function exists or whether its arguments match a declaration.

### Conditional statements

```text
IfStmt
    first_branch: IfBranch
    else_if_branches: List<ElseIfBranch>
    else_clause: ElseClause?
    span: SourceSpan

IfBranch
    if_keyword: TokenRef                 // IF
    left_paren: TokenRef                 // LPAREN
    condition: Expr
    right_paren: TokenRef                // RPAREN
    then_keyword: TokenRef?              // THEN noise word
    body: Block
    span: SourceSpan

ElseIfBranch
    else_keyword: TokenRef               // ELSE
    if_keyword: TokenRef                 // IF
    left_paren: TokenRef                 // LPAREN
    condition: Expr
    right_paren: TokenRef                // RPAREN
    then_keyword: TokenRef?              // THEN noise word
    body: Block
    span: SourceSpan

ElseClause
    else_keyword: TokenRef               // ELSE
    body: Block
    span: SourceSpan
```

A source-written `else if` is one `ElseIfBranch`. An `if` written inside an `else` block is a separate `IfStmt` in that block's `statements` collection.

### Loops

```text
WhileStmt
    while_keyword: TokenRef              // WHILE
    left_paren: TokenRef                 // LPAREN
    condition: Expr
    right_paren: TokenRef                // RPAREN
    do_keyword: TokenRef?                // DO noise word
    body: Block
    span: SourceSpan

ForStmt
    for_keyword: TokenRef                // FOR
    left_paren: TokenRef                 // LPAREN
    initializer: ForInitializer?
    first_semicolon: TokenRef             // SEMICOLON
    condition: Expr?
    second_semicolon: TokenRef            // SEMICOLON
    update: ForUpdate?
    right_paren: TokenRef                 // RPAREN
    do_keyword: TokenRef?                 // DO noise word
    body: Block
    span: SourceSpan

ForInitializer
    ForLetInitializer
    | AssignmentCore

ForLetInitializer
    let_keyword: TokenRef                // LET
    name: TokenRef                       // IDENT
    annotation_clause: AnnotationClause?
    assign: TokenRef                     // ASSIGN
    value: InitializerValue
    span: SourceSpan

ForUpdate
    AssignmentCore
    | UpdateCore
```

`for (;;) {}` has absent initializer, condition, and update fields while retaining both semicolon tokens.

### Transfer and assertion statements

```text
ReturnStmt
    return_keyword: TokenRef             // RETURN
    value: Expr?
    semicolon: TokenRef                  // SEMICOLON
    span: SourceSpan

BreakStmt
    break_keyword: TokenRef              // BREAK
    semicolon: TokenRef                  // SEMICOLON
    span: SourceSpan

ContinueStmt
    continue_keyword: TokenRef           // CONTINUE
    semicolon: TokenRef                  // SEMICOLON
    span: SourceSpan

AssertStmt
    assert_keyword: TokenRef             // ASSERT
    condition: Expr
    semicolon: TokenRef                  // SEMICOLON
    span: SourceSpan
```

Successful AST construction follows the parser context rules: `break` and `continue` occur only inside loops, and the `ReturnStmt.value` presence agrees with the enclosing function's return contract.

## Declaration annotations

```text
DeclarationAnnotation
    PrimitiveTypeAnnotation
    | DimensionAnnotation
    | ExactUnitAnnotation

PrimitiveTypeAnnotation
    keyword: TokenRef                    // INT, FLOAT, BOOL, or TEXT
    span: SourceSpan

DimensionAnnotation
    keyword: TokenRef                    // LENGTH, MASS, TIME, or FORCE
    span: SourceSpan

ExactUnitAnnotation
    left_bracket: TokenRef               // LBRACKET
    unit: UnitExpr
    right_bracket: TokenRef              // RBRACKET
    span: SourceSpan
```

Bare unit identifiers are not declaration annotations. For example, `[m]` produces `ExactUnitAnnotation`; bare `m` does not match `DeclarationAnnotation`.

## Expressions

```text
Expr
    NumberLiteral
    | StringLiteral
    | BoolLiteral
    | IdentifierExpr
    | SimpleQuantityLiteral
    | CompoundQuantityLiteral
    | GroupExpr
    | CallExpr
    | UnaryExpr
    | PowerExpr
    | BinaryExpr
    | ConversionExpr
```

### Leaves and quantities

```text
NumberLiteral
    token: TokenRef                      // NUMBER
    span: SourceSpan

StringLiteral
    token: TokenRef                      // STRING, including quotes
    span: SourceSpan

BoolLiteral
    token: TokenRef                      // TRUE or FALSE
    span: SourceSpan

IdentifierExpr
    name: TokenRef                       // IDENT
    span: SourceSpan

SimpleQuantityLiteral
    magnitude: NumberLiteral
    unit_name: UnitName
    span: SourceSpan

CompoundQuantityLiteral
    magnitude: NumberLiteral
    unit_annotation: ExactUnitAnnotation
    span: SourceSpan
```

The magnitude and following unit token or left bracket must be byte-adjacent. Literal nodes retain source spellings only; they do not store parsed numeric, decoded string, Boolean runtime, or resolved unit values.

### Grouping and calls

```text
GroupExpr
    left_paren: TokenRef                 // LPAREN
    inner: Expr
    right_paren: TokenRef                // RPAREN
    span: SourceSpan

CallExpr
    callee: TokenRef                     // IDENT
    left_paren: TokenRef                 // LPAREN
    arguments: SeparatedList<Expr>?
    right_paren: TokenRef                // RPAREN
    span: SourceSpan

InputExpr
    input_keyword: TokenRef              // INPUT
    left_paren: TokenRef                 // LPAREN
    right_paren: TokenRef                // RPAREN
    span: SourceSpan
```

`InputExpr` is intentionally not an `Expr` variant. It appears only through `InitializerValue` or `AssignmentValue`.

### Operators and conversions

```text
UnaryExpr
    operator: TokenRef                   // BANG, PLUS, or MINUS
    operand: Expr
    span: SourceSpan

PowerExpr
    base: Expr
    caret: TokenRef                      // CARET
    exponent: Expr
    span: SourceSpan

BinaryExpr
    left: Expr
    operator: TokenRef                   // STAR, SLASH, PERCENT, PLUS, MINUS,
                                         // LESS, LESS_EQUAL, GREATER,
                                         // GREATER_EQUAL, EQUAL_EQUAL,
                                         // BANG_EQUAL, AND_AND, or OR_OR
    right: Expr
    span: SourceSpan

ConversionExpr
    operand: Expr
    as_keyword: TokenRef                 // AS
    to_keyword: TokenRef?                // TO noise word
    target: UnitTarget
    span: SourceSpan

UnitTarget
    SimpleUnitTarget
    | ExactUnitAnnotation

SimpleUnitTarget
    name: UnitName
    span: SourceSpan
```

Associativity is represented by nesting:

- left-associative operators nest through `BinaryExpr.left`;
- numeric power nests through `PowerExpr.exponent` according to the accepted right-associative grammar;
- repeated conversions nest through `ConversionExpr.operand` from left to right; and
- unary signs in negative exponents remain `UnaryExpr` nodes.

The parser does not determine whether operands or exponents carry units or whether a conversion target is compatible.

## Unit expressions

```text
UnitExpr
    numerator: UnitProduct
    quotient: UnitQuotient?
    span: SourceSpan

UnitProduct
    first: UnitPower
    rest: List<UnitProductPart>
    span: SourceSpan

UnitProductPart
    star: TokenRef                       // STAR
    factor: UnitPower
    span: SourceSpan

UnitQuotient
    slash: TokenRef                      // SLASH
    denominator: UnitDenominator
    span: SourceSpan

UnitDenominator
    UnitPower
    | GroupedUnitProduct

GroupedUnitProduct
    left_paren: TokenRef                 // LPAREN
    product: UnitProduct
    right_paren: TokenRef                // RPAREN
    span: SourceSpan

UnitPower
    base: UnitName
    exponent: UnitExponent?
    span: SourceSpan

UnitName
    token: TokenRef                      // IDENT
    span: SourceSpan

UnitExponent
    caret: TokenRef                      // CARET
    minus: TokenRef?                     // MINUS
    magnitude: TokenRef                  // integer-spelling NUMBER
    span: SourceSpan
```

The AST preserves written unit names, factor order, stars, division, denominator grouping, exponent signs, and exponent lexemes. It does not store a normalized dimension, combined exponent map, scale, or resolved unit identity.

`UnitProduct.rest.length + 1` contributes that product's written factor count. The parser applies the accepted annotation-wide eight-factor and exponent-range limits before returning a successful AST.

## Span composition

All spans are half-open UTF-8 byte ranges governed by `SOURCE-LOCATIONS.md`.

### General rules

- A leaf node uses its token's span.
- A clause or helper record spans from its first retained token or child to its last retained token or child.
- A declaration or simple statement ends after its semicolon.
- A block includes both braces.
- A function begins at `fn` and ends after its body.
- An `if`, `while`, or `for` statement begins at its keyword and ends after its final body block.
- An optional noise word lies inside its containing node's span but does not change the node's semantic variant.

### Expression rules

- `SimpleQuantityLiteral` spans from its magnitude through its unit name.
- `CompoundQuantityLiteral` spans from its magnitude through its closing bracket.
- `GroupExpr` and `CallExpr` include both parentheses.
- `UnaryExpr` spans from its operator through its operand.
- `PowerExpr` and `BinaryExpr` span from their left/base child through their right/exponent child.
- `ConversionExpr` spans from its operand through its target.

### Unit rules

- `ExactUnitAnnotation` includes both brackets.
- `UnitProduct` spans from its first factor through its last factor.
- `UnitProductPart` spans from its star through its factor.
- `UnitQuotient` spans from its slash through its denominator.
- `GroupedUnitProduct` includes both parentheses.
- `UnitExponent` spans from its caret through its magnitude.

## Successful-AST invariants

A successful AST satisfies all of the following:

1. Every retained token is a real lexer token with unchanged kind, lexeme, and span.
2. Every node span contains all retained tokens and child spans belonging to that node.
3. Ordered collections preserve source order.
4. A `SeparatedList` has exactly one fewer separators than items.
5. `ConstDecl.initializer` is always present.
6. `PrintStmt.arguments` is nonempty.
7. An `IfStmt` has one first branch, zero or more `else if` branches, and at most one final `else`.
8. A `ForStmt` retains exactly two header semicolons even when every clause is absent.
9. `InputExpr` occurs only in the direct declaration or simple-assignment positions permitted by grammar constraint C5.
10. Unit-expression structure and limits already conform to grammar constraints C2 through C4.
11. Control-transfer placement conforms to grammar constraint C6.
12. No semantic-resolution or runtime field is present.

## Failure boundary

This accepted schema covers successful parses only. It contains no missing-token, error-expression, error-statement, skipped-token, or recovered-node variants.

The parser runs only after lexing succeeds. On its first syntax error, it emits one diagnostic, stops, and returns no AST. It does not synthesize tokens or expose a recovered tree. Any future parser-recovery proposal must deliberately amend this boundary while preserving every successful node kind, field, and fixture defined here.

## Grammar-to-AST mapping

| Grammar area | AST representation |
| --- | --- |
| `source_file`, `function_definition` | `SourceFile`, `FunctionDef` |
| `parameter_list`, `argument_list` | `SeparatedList<T>` |
| `block`, `statement` | `Block`, `Stmt` variants |
| declarations | `LetDecl`, `ConstDecl`, annotation and initializer clauses |
| assignment/update forms | `AssignmentCore`, `AssignmentOperation`, `UpdateCore` |
| `if_statement` | first branch, ordered `ElseIfBranch` list, optional `ElseClause` |
| loop grammar | `WhileStmt`, `ForStmt`, dedicated header variants |
| literal and identifier primaries | literal, quantity, identifier, group, and call nodes |
| precedence hierarchy | nested unary, power, binary, and conversion nodes |
| `input_expression` | context-only `InputExpr` |
| declaration annotations and unit targets | tagged annotation and target variants |
| unit grammar | product parts plus one optional quotient |

## Minimum AST fixture coverage

Fixtures added later must cover at least:

- an empty source file and a multi-function source file;
- functions with empty and nonempty parameter lists and optional return contracts;
- initialized and uninitialized `let`, initialized `const`, and every annotation category;
- simple and compound assignment, prefix and postfix update, and standalone call statements;
- direct `input()` declaration and assignment values;
- empty and nonempty blocks;
- `if`, multiple `else if` branches, final `else`, and a genuinely nested conditional;
- `while`, `for (;;)`, and every `for` initializer/update variant;
- bare and value returns, loop control, assertion, and multi-argument print;
- every expression precedence level and associativity boundary;
- explicit grouping, optional noise words, and conversion chains;
- simple and compound quantities with exact adjacency;
- unit products, simple and grouped denominators, and signed exponents; and
- exact byte spans for every node in at least one complete function.

## Acceptance rule

An implementation does not conform if it changes node variants, field optionality, collection order, retained token references, successful-node spans, or the parser/semantic boundary without deliberately amending this document and its dependent fixtures.
