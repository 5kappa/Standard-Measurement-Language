# Measure Language Specification

Status: consolidated proposal specification  
Scope: programming-language proposal; no implementation is required  
Canonical source form: UTF-8 files using the ASCII syntax defined below

This file is the normative source for the Measure proposal. `PROJECT.md` records design history and rationale, `SPECIFICATION-ROADMAP.md` records how decisions were reached, and `decisions/` preserves individual decision records. If those documents conflict with this specification, this file governs the proposal.

## 1. Introduction

### 1.1 Description

Measure is a small procedural language for calculations whose numerical values may carry physical units. It is designed first for educational structural-engineering calculations. A quantity such as `100m` contains a magnitude and a unit, while a plain value such as `0.5` remains a valid dimensionless number.

Measure's intended static semantics prevent incompatible operations such as adding length to time. Multiplication, division, and integer powers derive compound dimensions. Conversions between compatible units are written explicitly with `as` rather than occurring silently.

Examples:

```measure
let distance = 100m;
let time = 9.58s;
let speed = distance / time;

let trip = 5km + (3mi as km);
```

Measure is an educational proposal. It does not claim suitability for professional engineering design, code compliance, certification, or construction-safety decisions.

### 1.2 Inspiration

Mainstream languages usually represent measurements as ordinary numbers. Their units survive only in variable names, comments, or programmer memory. Measure applies the discipline of dimensional analysis directly to language design so that unit intent is visible in source code.

The Mars Climate Orbiter loss is a motivating example of why numerically valid values with incompatible unit conventions should not be silently interchangeable. Measure therefore makes quantity syntax and conversion decisions explicit.

### 1.3 New principle: Meaning Before Math

Measure's uniqueness principle is **Meaning Before Math**: a numerical operation is acceptable only when the meanings represented by its operands are compatible.

The principle appears in three language features:

1. **Units are part of quantity syntax.** `100m` and `9.8[m/s^2]` state measurement intent directly rather than through comments or identifier names.
2. **Unit algebra is automatic.** Multiplication, division, and powers derive result dimensions; programmers may also write bounded compound-unit annotations when stating an exact unit.
3. **Conversion is never silent.** Compatible but differently represented values require explicit postfix `as` conversion before operations that require a common unit representation.

Currency, affine temperature, generated Python, and claims of zero runtime cost are not part of this proposal.

## 2. Character set and source format

### 2.1 Encoding and canonical characters

Source files use UTF-8 encoding. The canonical grammar uses only this ASCII subset:

```text
UPPER  = { A, B, C, ..., Z }
LOWER  = { a, b, c, ..., z }
DIGIT  = { 0, 1, 2, ..., 9 }
LETTER = UPPER union LOWER

WHITESPACE = { space, horizontal tab, carriage return, line feed }

SYMBOL = {
  .  +  -  *  /  %  ^  <  >  =  !  &  |
  (  )  {  }  [  ]  ;  :  ,  "  _
}
```

Non-ASCII source characters are outside the canonical grammar. Unicode aliases may be proposed later but are not required by this proposal.

### 2.2 Free-field format

Measure is free-field. A statement is not tied to a line or column. Line breaks ordinarily behave like other whitespace. Semicolons terminate simple statements, and braces delimit blocks.

The attachment rules for quantity literals are exceptions to ordinary whitespace freedom:

```measure
100m          // valid simple quantity
100 m         // invalid: the unit is detached
9.8[m/s^2]    // valid compound quantity
9.8 [m/s^2]   // invalid: `[` is detached
```

## 3. Lexical elements

### 3.1 Identifiers

Identifiers are case-sensitive.

```regex
[A-Za-z][A-Za-z0-9_]*
```

Rules:

- The first character must be an ASCII letter.
- Later characters may be ASCII letters, digits, or underscores.
- Consecutive and trailing underscores are allowed.
- A keyword, reserved word, noise word, or registered unit symbol cannot be redeclared as a value identifier.
- `main` is an ordinary identifier, not a reserved word. A function named `main` may serve as an entry point by convention.

Identifier machine:

| State | Input | Next state | Accepting |
| --- | --- | --- | --- |
| Start | `LETTER` | Identifier | No |
| Start | anything else | Reject | No |
| Identifier | `LETTER`, `DIGIT`, or `_` | Identifier | Yes |
| Identifier | anything else | Stop before input | Yes |

### 3.2 Numeric literals

Measure accepts decimal integers and fixed-point decimal literals. The integer part is either `0` or begins with a nonzero digit; leading zeros are not permitted.

```regex
(0|[1-9][0-9]*)(\.[0-9]+)?
```

Accepted examples:

```text
0  5  125  5.0  0.5  123.456
```

Rejected examples:

```text
00  0123  01.5  .5  5.  2.5e3  1_000  0x10  0b1010
```

A leading `+` or `-` is a unary operator token, not part of the numeric token. Thus `-5m` begins with `MINUS NUMBER IDENT`.

Number machine:

| State | Input | Next state | Accepting |
| --- | --- | --- | --- |
| Start | `0` | Zero | Yes |
| Start | `NON_ZERO_DIGIT` | IntegerDigits | Yes |
| Zero | `DIGIT` | Reject | No |
| Zero | `.` | DecimalPoint | No |
| Zero | other input | Stop before input | Yes |
| IntegerDigits | `DIGIT` | IntegerDigits | Yes |
| IntegerDigits | `.` | DecimalPoint | No |
| DecimalPoint | `DIGIT` | FractionDigits | Yes |
| FractionDigits | `DIGIT` | FractionDigits | Yes |
| Any accepting state | other input | Stop before input | Yes |

Ending in `DecimalPoint` is a lexical error because a digit must follow `.`.

### 3.3 String literals

Text literals use double quotes. They may contain canonical ASCII characters other than a double quote, carriage return, or line feed. Escape sequences and multiline strings are not part of this proposal.

```measure
"Speed: "
"Within the limit"
```

An unclosed string before the end of the line is a lexical error.

### 3.4 Comments

Measure supports line comments and non-nesting block comments:

```measure
// continues through the end of the line

/* may cross line boundaries */
```

Comments behave like whitespace between tokens. They cannot satisfy or interrupt the adjacency required between a magnitude and its attached unit syntax. An unterminated block comment is a lexical error.

Comment machines:

- After `/`, a second `/` enters a line comment, which ends before CR, LF, or EOF.
- After `/`, `*` enters a block comment.
- Inside a block comment, `*/` returns to ordinary scanning.
- Reaching EOF before `*/` is an error.
- A nested `/*` has no special meaning inside a block comment.

### 3.5 Keywords, reserved words, and noise words

Keywords:

```text
let const fn return
if else for while break continue
print input assert
as
```

Reserved primitive types and literals:

```text
int float bool text
true false
```

Reserved named dimensions:

```text
Length Mass Time Force
```

Optional noise words:

```text
to then do
```

Noise words are reserved but semantically inert. They are valid only in these positions:

```measure
distance as to km
if (condition) then { ... }
while (condition) do { ... }
for (...) do { ... }
```

Keyword machine: scan the complete identifier machine first, then compare the accepted lexeme with the keyword, reserved-word, and noise-word tables. A nonmatching lexeme remains `IDENT`.

The following teammate-draft words are deliberately absent: `rate`, `Money`, `Temperature`, and `Scalar` as a type or dimension. `unit` and `dimension` declarations are deferred. `main` is not reserved.

### 3.6 Unit symbols and quantity literals

Unit symbols have the lexical form `IDENT`. The lexer does not consult a unit registry. Each supported spelling, such as `km` or `kN`, is treated as one complete symbol rather than prefix multiplication.

A simple quantity is a number immediately followed by an identifier:

```text
simple_quantity = NUMBER IDENT-with-no-leading-space
```

A compound quantity is a number immediately followed by a bracketed unit expression:

```text
compound_quantity = NUMBER "[" unit_expression "]"
```

Examples:

```measure
100m
12kN
9.8[m/s^2]
1[kg*m/s^2]
```

## 4. Operators and delimiters

### 4.1 Operator inventory

| Family | Operators |
| --- | --- |
| Postfix conversion | `as`, optionally followed by noise word `to` |
| Numeric power | `^` |
| Unary | `!`, unary `+`, unary `-` |
| Multiplicative | `*`, `/`, `%` |
| Additive | `+`, `-` |
| Relational | `<`, `<=`, `>`, `>=` |
| Equality | `==`, `!=` |
| Logical | `&&`, `||` |
| Assignment statements | `=`, `+=`, `-=`, `*=`, `/=` |
| Postfix update statements | `++`, `--` |

The scanner uses maximal munch. For example, `++`, `+=`, `<=`, `==`, `!=`, `&&`, and `||` are recognized before their one-character prefixes.

Operator machine:

| First character | Optional second character | Tokens |
| --- | --- | --- |
| `+` | `+` or `=` | `+`, `++`, `+=` |
| `-` | `-` or `=` | `-`, `--`, `-=` |
| `*` | `=` | `*`, `*=` |
| `/` | `/`, `*`, or `=` | `/`, line comment, block comment, `/=` |
| `%` | none | `%` |
| `^` | none | `^` |
| `<` or `>` | `=` | `<`, `<=`, `>`, `>=` |
| `=` | `=` | `=`, `==` |
| `!` | `=` | `!`, `!=` |
| `&` | required `&` | `&&`; a lone `&` is invalid |
| `|` | required `|` | `||`; a lone `|` is invalid |

### 4.2 Delimiters

| Delimiter | Function |
| --- | --- |
| `;` | Terminates a simple statement or separates clauses in a `for` header. |
| `(` `)` | Groups expressions and encloses conditions, arguments, and parameter lists. |
| `{` `}` | Encloses every control-flow or function body. |
| `[` `]` | Encloses compound-unit syntax and exact-unit annotations. |
| `,` | Separates function arguments, parameters, and output arguments. |
| `:` | Introduces a declaration, parameter, or function-return annotation. |

Every conditional and loop body uses braces, including a body containing only one statement. Semicolons terminate statements, not physical lines.

## 5. Unit-expression syntax

```ebnf
unit_expression
    = unit_product, [ "/", unit_denominator ] ;

unit_product
    = unit_power, { "*", unit_power } ;

unit_denominator
    = unit_power
    | "(", unit_product, ")" ;

unit_power
    = IDENT, [ "^", signed_integer ] ;

signed_integer
    = [ "-" ], DIGIT, { DIGIT } ;
```

Rules:

- Multiplication is explicit with `*`; adjacent unit names do not imply multiplication.
- At most one top-level `/` is allowed.
- Repeated or nested division is rejected.
- A multi-factor denominator requires parentheses.
- A grouped unit expression cannot itself be raised to a power.
- Numeric scale factors are not allowed inside unit expressions.
- A unit annotation contains at most eight written unit-factor occurrences.
- Source unit exponents range from `-16` through `16`.
- Normalized dimension exponents range from `-32` through `32`.
- Bracket contents contain at most 128 ASCII characters, including whitespace.

Accepted:

```measure
9.8[m/s^2]
1[kg*m/s^2]
1[kg/(m*s^2)]
```

Rejected:

```measure
1[kg/m/s^2]
1[m/(kg/s)]
1[(m/s)^2]
1[N m]
1[1000*m]
```

## 6. Expressions

### 6.1 Precedence and associativity

Highest precedence appears first:

| Level | Forms | Associativity |
| --- | --- | --- |
| 1 | literals, identifiers, calls, parenthesized expressions | Primary |
| 2 | postfix conversion `as [to] unit-target` | Left-to-right postfix |
| 3 | numeric power `^` | Right-to-left |
| 4 | unary `!`, `+`, `-` | Right-to-left |
| 5 | `*`, `/`, `%` | Left-to-right |
| 6 | `+`, `-` | Left-to-right |
| 7 | `<`, `<=`, `>`, `>=` | Non-chaining |
| 8 | `==`, `!=` | Non-chaining |
| 9 | `&&` | Left-to-right |
| 10 | `||` | Left-to-right |

Assignment is a statement, not an expression, and therefore has no expression precedence. Postfix `++` and `--` are also standalone statements.

Examples:

```measure
3m as cm + 2cm        // (3m as cm) + 2cm
-2 ^ 2               // -(2 ^ 2)
a + b * c             // a + (b * c)
a < b && b < c        // (a < b) && (b < c)
```

### 6.2 Expression grammar

```ebnf
expression       = logical_or ;
logical_or       = logical_and, { "||", logical_and } ;
logical_and      = equality, { "&&", equality } ;
equality         = relational, [ ( "==" | "!=" ), relational ] ;
relational       = additive, [ ( "<" | "<=" | ">" | ">=" ), additive ] ;
additive         = multiplicative, { ( "+" | "-" ), multiplicative } ;
multiplicative   = unary, { ( "*" | "/" | "%" ), unary } ;
unary            = ( "!" | "+" | "-" ), unary | power ;
power            = postfix, [ "^", power ] ;
postfix          = primary, { "as", [ "to" ], unit_target } ;
unit_target      = IDENT | "[", unit_expression, "]" ;

primary
    = NUMBER
    | simple_quantity
    | compound_quantity
    | STRING
    | "true"
    | "false"
    | IDENT
    | call_expression
    | input_expression
    | "(", expression, ")" ;

call_expression  = IDENT, "(", [ argument_list ], ")" ;
argument_list    = expression, { ",", expression } ;
input_expression = "input", "(", ")" ;

simple_quantity
    = NUMBER, IDENT ;

compound_quantity
    = NUMBER, "[", unit_expression, "]" ;
```

The `NUMBER` and following `IDENT` in `simple_quantity`, or `NUMBER` and `[` in `compound_quantity`, must be adjacent in source text.

### 6.3 Intended expression rules

- `+` and `-` require compatible dimensions and a common explicit unit representation.
- `%` requires operands with the same exact unit representation and produces that representation.
- `*` and `/` derive result dimensions automatically.
- A dimensioned base requires a compile-time integer numeric exponent.
- A dimensionless base may use an integer or decimal exponent.
- Relational operators require compatible operands and produce `bool`.
- Equality requires comparable primitive values or compatible quantities and produces `bool`.
- `!`, `&&`, and `||` operate on `bool` values.
- Logical `&&` and `||` use short-circuit evaluation.
- `as` requires a dimension-compatible target and makes conversion explicit.

## 7. Dimensions, units, and declarations

### 7.1 Dimension model

Measure initially uses three base dimensions:

```text
Length = (1, 0, 0)
Mass   = (0, 1, 0)
Time   = (0, 0, 1)
```

`Force` is a named derived dimension:

```text
Force = Mass * Length / Time^2 = (1, 1, -2)
```

The initial named physical dimension annotations are `Length`, `Mass`, `Time`, and `Force`. Other algebraic results may remain unnamed and may be constrained using an exact compound-unit annotation. Volume remains the derived dimension `Length^3` and is written with an exact annotation such as `[m^3]`; `Volume` is not a named annotation.

The initial built-in unit registry is:

```text
m cm mm km in ft mi
kg
s min
N kN
```

The imperial Length symbols are `in`, `ft`, and `mi`, with exact scales `127/5000`, `381/1250`, and `201168/125` relative to `m` (`0.0254m`, `0.3048m`, and `1609.344m`). No other imperial units are built in. `min` is a complete Time-unit symbol with exact scale `60` relative to `s`. `N` is dimensionally and scalarly equivalent to `kg*m/s^2`. Every supported spelling remains a complete, case-sensitive symbol rather than a parser-level prefix expression.

### 7.2 Declaration annotations

A declaration annotation is exactly one of:

1. a primitive type: `int`, `float`, `bool`, or `text`;
2. a named dimension: `Length`, `Mass`, `Time`, or `Force`; or
3. an exact-unit annotation such as `[m]` or `[kg*m/s^2]`.

Categories cannot be combined. Forms such as `float[m]`, `Length(m)`, and `float Length` are invalid.

Primitive `int` and `float` values are dimensionless. A dimension annotation accepts any representation of that dimension. An exact-unit annotation fixes the representation and requires explicit conversion from a different compatible representation.

### 7.3 Declaration grammar

Every declaration introduces one binding and has an initializer:

```ebnf
declaration
    = ( "let" | "const" ), IDENT,
      [ ":", declaration_annotation ],
      "=", expression, ";" ;

declaration_annotation
    = primitive_type
    | dimension_name
    | "[", unit_expression, "]" ;

primitive_type = "int" | "float" | "bool" | "text" ;
dimension_name = "Length" | "Mass" | "Time" | "Force" ;
```

Examples:

```measure
let count: int = 5;
let ratio = 0.5;
let span: Length = 5m;
let exactSpan: [m] = 5m;
const gravity: [m/s^2] = 9.8[m/s^2];
let duration: Time = 5min;
let volume: [m^3] = 12[m^3];
```

If the annotation is omitted, the intended static semantics infer the binding constraint only from the initializer. Parameters and function return values require explicit annotations.

## 8. Statements

### 8.1 Statement grammar

```ebnf
statement
    = declaration
    | assignment_statement
    | update_statement
    | print_statement
    | call_statement
    | if_statement
    | while_statement
    | for_statement
    | return_statement
    | break_statement
    | continue_statement
    | assert_statement ;

block = "{", { statement }, "}" ;
```

All simple statements end with `;`. Every conditional and iterative body is a block.

### 8.2 Assignment and update

```ebnf
assignment_statement
    = IDENT, assignment_operator, expression, ";" ;

assignment_operator
    = "=" | "+=" | "-=" | "*=" | "/=" ;

update_statement
    = IDENT, ( "++" | "--" ), ";" ;
```

Examples:

```measure
length = 5m;
length += 1m;
length *= 2;
length++;
```

Assignment is not an expression. `++length`, `print(length++)`, and chained assignment are invalid. Postfix update adds or subtracts one in the target's current unit representation. `*=` and `/=` require a dimensionless right operand so the binding's dimension does not change.

### 8.3 Input and output

`print` accepts one or more expressions and writes them in order. Intended unit-aware output includes a quantity's unit representation.

```ebnf
print_statement
    = "print", "(", expression, { ",", expression }, ")", ";" ;
```

Examples:

```measure
print("Speed: ", speed);
print(height);
```

`input()` is a context-sensitive input expression. It is valid only as the direct initializer or right-hand side of a binding whose expected primitive or exact-unit annotation is known. Unit-bearing runtime input therefore uses an exact-unit target:

```measure
let height: [m] = input();
height = input();
```

An unannotated declaration such as `let value = input();` is invalid because no type or unit can be inferred from the source expression.

### 8.4 Conditional statements

```ebnf
if_statement
    = "if", "(", expression, ")", [ "then" ], block,
      { "else", "if", "(", expression, ")", [ "then" ], block },
      [ "else", block ] ;
```

Conditions must have type `bool`.

```measure
if (speed > limit) then {
    print("Over the limit");
} else if (speed == limit) {
    print("At the limit");
} else {
    print("Within the limit");
}
```

Nested conditionals use the same mandatory-brace rule:

```measure
if (load > 0kN) {
    if (load > 100kN) {
        print("High load");
    } else {
        print("Positive load");
    }
}
```

### 8.5 Iterative statements

```ebnf
while_statement
    = "while", "(", expression, ")", [ "do" ], block ;

for_statement
    = "for", "(", [ for_initializer ], ";",
      [ expression ], ";", [ for_update ], ")",
      [ "do" ], block ;

for_initializer
    = "let", IDENT,
      [ ":", declaration_annotation ], "=", expression
    | assignment_core ;

for_update
    = assignment_core
    | IDENT, ( "++" | "--" ) ;

assignment_core
    = IDENT, assignment_operator, expression ;
```

Loop conditions must have type `bool`.

```measure
for (let t: [s] = 0s; t < 5s; t += 1s) do {
    print("Time: ", t);
}

let fuel: [kg] = 10kg;
while (fuel > 0kg) {
    print("Fuel left: ", fuel);
    fuel -= 1kg;
}
```

Nested loops are ordinary blocks containing another loop:

```measure
for (let row: int = 0; row < 3; row++) {
    for (let column: int = 0; column < 3; column++) {
        print(row, ",", column);
    }
}
```

`break;` exits the nearest loop. `continue;` begins its next iteration.

### 8.6 Assertions

```ebnf
assert_statement = "assert", expression, ";" ;
```

The expression must be `bool`.

```measure
assert deflection <= allowableDeflection;
```

## 9. Functions and programs

```ebnf
source_file
    = { function_definition } ;

function_definition
    = "fn", IDENT, "(", [ parameter_list ], ")",
      [ ":", return_annotation ], block ;

parameter_list
    = parameter, { ",", parameter } ;

parameter
    = IDENT, ":", declaration_annotation ;

return_annotation
    = declaration_annotation ;

return_statement
    = "return", [ expression ], ";" ;

call_statement
    = call_expression, ";" ;

break_statement    = "break", ";" ;
continue_statement = "continue", ";" ;
```

Function parameters and return values use explicit contracts. A function without a return annotation after `:` returns no value. A `return` with an expression is valid only in a value-returning function.

```measure
fn speed(distance: Length, time: Time): [m/s] {
    return (distance as m) / (time as s);
}

fn main() {
    let result = speed(100m, 9.58s);
    print("Speed: ", result);
}
```

`main` is lexically an ordinary `IDENT`. The proposal uses `fn main()` as the conventional program entry point rather than reserving the spelling as a keyword.

## 10. Consolidated token inventory

### 10.1 Value and name tokens

```text
NUMBER STRING IDENT
TRUE FALSE
```

### 10.2 Keyword and type tokens

```text
LET CONST FN RETURN
IF ELSE FOR WHILE BREAK CONTINUE
PRINT INPUT ASSERT AS
INT FLOAT BOOL TEXT
LENGTH MASS TIME FORCE
TO THEN DO
```

### 10.3 Operator and delimiter tokens

```text
PLUS MINUS STAR SLASH PERCENT CARET BANG
PLUS_PLUS MINUS_MINUS
ASSIGN PLUS_ASSIGN MINUS_ASSIGN STAR_ASSIGN SLASH_ASSIGN
LESS LESS_EQUAL GREATER GREATER_EQUAL EQUAL_EQUAL BANG_EQUAL
AND_AND OR_OR
LPAREN RPAREN LBRACE RBRACE LBRACKET RBRACKET
SEMICOLON COLON COMMA EOF
```

## 11. Explicit exclusions

The following are outside this proposal:

- currency and exchange-rate declarations;
- affine temperature points or differences;
- percentages and angle units;
- user-defined dimensions or units;
- collections, records, classes, and object-oriented features;
- exceptions and concurrency;
- generated Python or another required backend;
- a required runtime numeric representation;
- professional engineering certification or safety guarantees.

These exclusions do not prevent later extensions, but no excluded feature may be assumed by the proposal's grammar, examples, or uniqueness claims.

## 12. Proposal conformance checklist

The final written proposal should contain:

- the introduction, inspiration, audience, safety boundary, and uniqueness principle;
- the enumerated character set;
- identifier, number, string, comment, keyword, operator, and delimiter machines;
- a dedicated final-proposal Literals section containing numeric, string, Boolean, and quantity-literal forms and the quantity-adjacency rule;
- the complete keyword, reserved-word, noise-word, operator, and delimiter inventories;
- free-field and whitespace rules;
- the expression grammar and precedence table;
- examples of declaration, input/output, assignment, nested conditional, and nested iterative statements;
- the unit-expression grammar and its hard limits;
- the LMT-plus-Force model as intended meaning; and
- a complete sample program that uses only syntax accepted by this specification.
