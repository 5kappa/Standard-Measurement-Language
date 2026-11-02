# Measure: A Unit-Safe Programming Language

## I. Introduction

### Description of the Proposed Programming Language

Measure is a small, statically checked procedural programming language for calculations involving physical measurements. It is intended primarily for students performing introductory structural-engineering and other scientific calculations in which confusing units can make an otherwise valid formula produce a meaningless result.

In Measure, a numerical value may carry a unit as part of its syntax. For example, `100m` represents one hundred meters, while `9.58s` represents 9.58 seconds. Units are optional rather than required for every number: a literal such as `0.5` remains a valid dimensionless value. This distinction allows the language to represent both measured quantities and ordinary numerical values without forcing artificial units onto counts, ratios, and constants.

Measure checks whether the units used in an expression are compatible. An addition such as `10m + 5s` is invalid because length and time are different dimensions. Multiplication, division, and integer powers automatically derive the dimension of their result. Thus, dividing a distance by a time produces a speed, while multiplying mass by acceleration produces force.

```measure
let distance = 100m;
let time = 9.58s;
let speed = distance / time;

let mass = 50kg;
let acceleration = 9.8[m/s^2];
let force = mass * acceleration;
```

Measure also refuses to convert compatible units silently. If two quantities use different representations of the same dimension, the programmer must state the intended conversion with the `as` operator. For example:

```measure
let total = 5km + (3mi as km);
```

This rule makes conversion decisions visible in the program instead of hiding them in an implicit operation. Measure also permits declarations with primitive, dimensional, or exact-unit annotations, while local declarations may infer their constraint from an initializer. Its syntax is intentionally bounded and familiar: it uses semicolon-terminated statements, brace-delimited blocks, and a restricted unit-expression grammar that remains manageable for lexical and syntactic analysis.

The initial proposal supports the base dimensions Length, Mass, and Time, together with the named derived dimension Force. Its initial units are `m`, `cm`, `mm`, `km`, `in`, `ft`, `mi`, `kg`, `s`, `min`, `N`, and `kN`. The imperial library is limited to inches, feet, and miles. Volume remains a derived dimension written with an exact annotation such as `[m^3]`. Currency, affine temperature, user-defined units, and automatic code generation are outside the current scope.

Measure is an educational language proposal, not a professional structural-analysis system. It is not intended to certify designs, establish compliance with engineering codes, or make construction-safety decisions.

### Inspiration for the Language

In many general-purpose programming languages, measurements are represented as ordinary integers or floating-point values. Their units exist only in comments, identifier names such as `distance_km`, or the programmer's memory. The language can detect an invalid numerical operation, such as division by zero, but it ordinarily cannot recognize that adding a length to a duration is conceptually meaningless.

Measure is inspired by dimensional analysis, where units are written with quantities and manipulated together with their magnitudes. Students already use this technique to verify formulas on paper. Measure transfers that discipline into the programming language so that measurement intent is explicit in source code and unit relationships can be checked systematically.

The loss of NASA's Mars Climate Orbiter is a motivating example. NASA's mishap investigation found that ground software supplied thruster impulse data in pound-force seconds even though the receiving interface expected newton seconds ([NASA, *Mars Climate Orbiter Mishap Investigation Board Report*, 1999](https://llis.nasa.gov/lesson/641)). The values were numerically valid, but the incompatible unit conventions were not converted correctly. Measure addresses this class of mistake by treating units as syntactic and semantic parts of quantities and by requiring conversions to be written explicitly.

The surface syntax draws on familiar elements of C-like languages, including braces, semicolons, expressions, declarations, and procedural control flow. These familiar forms reduce the amount of unrelated syntax a beginner must learn. Measure's distinguishing idea is not the shape of those statements, but the way unit information participates directly in quantities, expressions, declarations, and conversions.

### New Principle: Meaning Before Math

Measure's uniqueness principle is **Meaning Before Math**: a numerical operation is accepted only when the meanings represented by its operands are compatible. The principle is expressed through three connected design rules:

1. **Units are part of quantity syntax.** Forms such as `100m` and `9.8[m/s^2]` record measurement intent directly instead of relying on comments or naming conventions.
2. **Unit algebra is automatic but bounded.** Multiplication, division, and integer powers derive dimensions, while written compound-unit expressions follow explicit limits that keep the language lexically and syntactically manageable.
3. **Conversion is never silent.** Compatible quantities written in different units require an explicit `as` conversion whenever an operation needs a common representation.

Together, these rules allow Measure to reject nonsensical calculations early while keeping every change of unit visible to the reader.

## II. Syntactic Elements of the Language

### 3. Literals

A literal is a source form that directly represents a value. SML supports numeric, string, Boolean, and quantity literals. A leading `+` or `-` is an expression operator and is not part of a literal.

#### 3.1 Numeric Literals

Numeric literals contain decimal digits and may include one decimal point. An integer part is either the single digit `0` or a nonzero digit followed by zero or more digits. Therefore, leading zeros are not permitted. SML also does not support leading-dot forms, trailing-dot forms, exponent notation, digit separators, or alternate number bases.

```ini
Digits         = { 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 }
NonZeroDigit   = { 1, 2, 3, 4, 5, 6, 7, 8, 9 }
IntegerLiteral = 0 | NonZeroDigit Digits*
DecimalLiteral = IntegerLiteral . Digits+
NumberLiteral  = IntegerLiteral | DecimalLiteral
```

Regular expression:

```regex
(0|[1-9][0-9]*)(\.[0-9]+)?
```

Examples:

| Accepted | Rejected | Reason for rejection |
| --- | --- | --- |
| `0` | `00` | Zero must appear alone as the integer part. |
| `125` | `0123` | Leading zeros are not permitted. |
| `0.5` | `01.5` | A decimal's integer part cannot have a leading zero. |
| `9.81` | `.5` | A digit must appear before the decimal point. |
| `12.5` | `5.` | A digit must appear after the decimal point. |
| `1000` | `1e3` | Exponent notation is not supported. |
| `1000` | `1_000` | Digit separators are not supported. |
| `5` in `-5` | — | The `-` is a separate unary operator. |

Numeric-literal machine:

| State | Input | Next state | Accepting |
| --- | --- | --- | --- |
| Start | `0` | Zero | Yes |
| Start | `NonZeroDigit` | IntegerDigits | Yes |
| Start | anything else | Reject | No |
| Zero | `Digit` | Reject | No |
| Zero | `.` | DecimalPoint | No |
| Zero | anything else | Stop before input | Yes |
| IntegerDigits | `Digit` | IntegerDigits | Yes |
| IntegerDigits | `.` | DecimalPoint | No |
| IntegerDigits | anything else | Stop before input | Yes |
| DecimalPoint | `Digit` | FractionDigits | Yes |
| DecimalPoint | anything else | Reject | No |
| FractionDigits | `Digit` | FractionDigits | Yes |
| FractionDigits | anything else | Stop before input | Yes |

For example, `-5` is recognized as `MINUS NUMBER(5)`, not as one negative-number token.

#### 3.2 String and Boolean Literals

A string literal is enclosed in double quotation marks. It may contain canonical SML characters other than a double quotation mark, carriage return, or line feed. Empty strings are allowed. Escape sequences, embedded double quotation marks, and multiline strings are not supported in the current proposal.

```ini
DoubleQuote     = { " }
StringCharacter = Character - { DoubleQuote, <carriage-return>, <line-feed> }
StringLiteral   = DoubleQuote StringCharacter* DoubleQuote
```

Regular expression:

```regex
"[^"\r\n]*"
```

The quotation marks are delimiters and are part of the complete string token. Examples include:

```text
"Load applied"
"Speed: "
""
```

String-literal machine:

| State | Input | Next state | Accepting |
| --- | --- | --- | --- |
| Start | `"` | StringBody | No |
| Start | anything else | Reject | No |
| StringBody | permitted string character | StringBody | No |
| StringBody | `"` | Accept | Yes |
| StringBody | carriage return, line feed, or end of file | Reject | No |

Boolean literals have exactly two case-sensitive spellings:

```ini
BooleanLiteral = { true, false }
```

`true` and `false` are reserved and cannot be used as identifiers. Spellings such as `True` and `FALSE` remain ordinary identifiers rather than Boolean literals.

#### 3.3 Quantity Literals

A quantity literal attaches a numeric magnitude to unit syntax. A simple quantity uses one unit symbol, while a compound quantity encloses a unit expression in square brackets.

```ini
QuantityLiteral         = SimpleQuantityLiteral | CompoundQuantityLiteral
SimpleQuantityLiteral   = NumberLiteral UnitSymbol
CompoundQuantityLiteral = NumberLiteral "[" UnitExpression "]"
UnitSymbol               = Identifier
```

The magnitude must be directly adjacent to its unit symbol or opening square bracket. Whitespace and comments cannot appear between them.

| Accepted | Rejected |
| --- | --- |
| `100m` | `100 m` |
| `6ft` | `6 ft` |
| `5min` | `5 min` |
| `9.8[m/s^2]` | `9.8 [m/s^2]` |
| `12[m^3]` | `12 [m^3]` |

Quantity-recognition machine:

| State | Input | Next state | Accepting |
| --- | --- | --- | --- |
| Q0 (Start) | valid `NumberLiteral` | Q1 (Magnitude) | No |
| Q1 (Magnitude) | adjacent `UnitSymbol` | Q2 (SimpleQuantity) | Yes |
| Q1 (Magnitude) | adjacent `[` | Q3 (CompoundUnit) | No |
| Q3 (CompoundUnit) | valid `UnitExpression` followed by `]` | Q4 (CompoundQuantity) | Yes |
| Any nonaccepting state | anything else | Reject | No |

This recognition machine reuses the previously defined numeric- and identifier-recognition rules rather than duplicating their internal states. Here, *adjacent* means that no whitespace or comment may appear between the magnitude and the unit symbol or opening square bracket. A quantity still consists of multiple lexical tokens: for example, a simple quantity is emitted as `NUMBER IDENT`. After recognition, each identifier used as a unit must match a symbol in SML's predefined unit registry.

A simple quantity is not one combined lexical token. For example:

```text
100m
NUMBER(100) IDENT(m)
```

A compound quantity also consists of several tokens:

```text
9.8[m/s^2]
NUMBER(9.8) LBRACKET IDENT(m) SLASH IDENT(s)
CARET NUMBER(2) RBRACKET
```

Unit symbols share the lexical form of identifiers. The lexer does not decide whether an identifier is a registered unit; unit resolution occurs after parsing. The complete grammar and hard limits for `UnitExpression` are presented later under **Expressions**.

### 4. Operation Symbols

Operation symbols form arithmetic, comparison, logical, assignment, and update operations. SML uses maximal munch: when two valid symbols begin with the same character, the lexer selects the longest valid symbol. For example, `+=` is recognized before `+`, `!=` before `!`, and `++` before `+`.

```ini
AssignmentOperator = { =, +=, -=, *=, /= }
ArithmeticOperator = { +, -, *, /, %, ^ }
UnaryOperator      = { !, +, - }
LogicalOperator    = { !, &&, || }
RelationalOperator = { ==, !=, <, <=, >, >= }
UpdateOperator     = { ++, -- }
```

The keyword `as` is also an operator, but it is not an operation symbol. It forms a postfix unit conversion and is recognized through the keyword machine. Square brackets are delimiters rather than operators.

#### 4.1 Assignment Operators

Assignment operators occur only in assignment statements. Assignment is not an expression, so chained assignments such as `a = b = 5;` are invalid.

| Operator | Example | Description |
| --- | --- | --- |
| `=` | `length = 5m;` | Stores the right-hand value in the named variable. |
| `+=` | `length += 1m;` | Adds a value with the same exact unit representation and stores the result. |
| `-=` | `length -= 1m;` | Subtracts a value with the same exact unit representation and stores the result. |
| `*=` | `length *= 2;` | Multiplies by a dimensionless value and stores the result. |
| `/=` | `length /= 2;` | Divides by a dimensionless value and stores the result. |

Compatible values written in different units still require explicit conversion. For example, `length += 1ft;` is invalid when `length` is represented in meters; the programmer must first write `1ft as m`.

#### 4.2 Arithmetic Operators

| Operator | Example | Description |
| --- | --- | --- |
| `+` | `5m + 2m` | Adds operands with the same exact unit representation. |
| `-` | `5m - 2m` | Subtracts operands with the same exact unit representation. |
| `*` | `3m * 2m` | Multiplies magnitudes and derives the product unit. |
| `/` | `100m / 9.5s` | Divides magnitudes and derives the quotient unit. |
| `%` | `5m % 2m` | Produces the remainder for operands with the same exact unit representation. |
| `^` | `3m ^ 2` | Raises a value and its unit to a power. |

The exponent of `^` must be dimensionless. A dimensioned base requires a compile-time integer exponent, while a dimensionless base may use an integer or decimal exponent. Decimal exponents are never permitted inside a written `UnitExpression`.

#### 4.3 Unary and Logical Operators

| Operator | Example | Description |
| --- | --- | --- |
| unary `+` | `+length` | Preserves the sign of a numeric value. |
| unary `-` | `-length` | Negates a numeric value. |
| `!` | `!valid` | Produces the logical opposite of a Boolean expression. |
| `&&` | `ready && safe` | Produces `true` only when both operands are `true`. |
| `\|\|` | `ready \|\| override` | Produces `true` when at least one operand is `true`. |

The sign in `-5m` is a separate unary operator; it is not part of the numeric or quantity literal.

#### 4.4 Relational and Equality Operators

| Operator | Meaning | Example |
| --- | --- | --- |
| `<` | less than | `3m < 5m` |
| `<=` | less than or equal to | `3m <= 5m` |
| `>` | greater than | `5m > 3m` |
| `>=` | greater than or equal to | `5m >= 3m` |
| `==` | equal to | `5m == 5m` |
| `!=` | not equal to | `5m != 3m` |

These operators produce a Boolean value. Unit-bearing operands must have the same exact unit representation. Thus, `5km < 3mi` is invalid until one operand is explicitly converted, as in `5km < (3mi as km)`.

#### 4.5 Update Operators

The symbols `++` and `--` form prefix or postfix standalone update statements rather than expression-valued operators.

| Operator | Prefix form | Postfix form | Description |
| --- | --- | --- | --- |
| `++` | `++count;` | `count++;` | Adds one to a dimensionless numeric variable. |
| `--` | `--count;` | `count--;` | Subtracts one from a dimensionless numeric variable. |

Update operators cannot be used with dimensioned values. A dimensioned variable must be changed with a compound assignment whose right operand states the unit explicitly, such as `length += 1m;` or `length -= 1m;`. Update operators also cannot occur inside a larger expression, so `print(count++);` and `let next = ++count;` are invalid.

#### 4.6 Regular Expressions

```regex
AssignmentOperator = (\+=|-=|\*=|/=|=)
ArithmeticOperator = (\+|-|\*|/|%|\^)
UnaryOperator      = (!|\+|-)
LogicalOperator    = (!|&&|\|\|)
RelationalOperator = (==|!=|<=|>=|<|>)
UpdateOperator     = (\+\+|--)
```

These expressions describe each family separately. Because some symbols belong to more than one family, such as `!`, `+`, and `-`, the parser determines their role from their position in the surrounding syntax.

#### 4.7 Operation-Symbol Machine

| First character | Following character | Recognized symbol |
| --- | --- | --- |
| `+` | `+` | `++` |
| `+` | `=` | `+=` |
| `+` | anything else | `+`; stop before the following character |
| `-` | `-` | `--` |
| `-` | `=` | `-=` |
| `-` | anything else | `-`; stop before the following character |
| `*` | `=` | `*=` |
| `*` | anything else | `*`; stop before the following character |
| `/` | `=` | `/=` |
| `/` | anything else | `/`; stop before the following character |
| `%` | anything | `%`; stop before the following character |
| `^` | anything | `^`; stop before the following character |
| `<` | `=` | `<=` |
| `<` | anything else | `<`; stop before the following character |
| `>` | `=` | `>=` |
| `>` | anything else | `>`; stop before the following character |
| `=` | `=` | `==` |
| `=` | anything else | `=`; stop before the following character |
| `!` | `=` | `!=` |
| `!` | anything else | `!`; stop before the following character |
| `&` | `&` | `&&` |
| `&` | anything else | Reject |
| `\|` | `\|` | `\|\|` |
| `\|` | anything else | Reject |
| anything else | — | Reject |

The comment machine takes priority when `/` is followed by `/` or `*`. Operator precedence and associativity are specified later under **Expressions**.

### 5. Keywords and Reserved Words

Keywords and reserved words use exact, case-sensitive spellings and cannot be used as identifiers. The lexer first recognizes the complete spelling with the identifier machine and then compares it with the inventories below. A spelling that matches neither inventory remains an `IDENT` token.

```ini
Keyword = {
    let, const, fn, return,
    if, else, for, while, break, continue,
    print, input, assert, as
}

ReservedPrimitiveType = { int, float, bool, text }
ReservedBooleanLiteral = { true, false }
ReservedDimensionName  = { Length, Mass, Time, Force }

ReservedWord = {
    int, float, bool, text,
    true, false,
    Length, Mass, Time, Force
}
```

#### 5.1 Keywords

| Keyword | Purpose |
| --- | --- |
| `let` | Declares a variable binding. |
| `const` | Declares a binding that cannot be reassigned. |
| `fn` | Begins a function declaration. |
| `return` | Returns a value from a function. |
| `if` | Begins a conditional statement. |
| `else` | Introduces the alternative branch of a conditional. |
| `for` | Begins a counted or clause-controlled loop. |
| `while` | Begins a condition-controlled loop. |
| `break` | Exits the nearest enclosing loop. |
| `continue` | Skips to the next iteration of the nearest enclosing loop. |
| `print` | Writes one or more expressions to the output. |
| `input` | Reads an input value. |
| `assert` | Requires a Boolean condition to hold. |
| `as` | Forms an explicit postfix unit conversion. |

Keyword regular expression:

```regex
^(let|const|fn|return|if|else|for|while|break|continue|print|input|assert|as)$
```

#### 5.2 Reserved Words

Reserved words name primitive types, Boolean literals, and the initial named dimensions.

| Category | Reserved words | Purpose |
| --- | --- | --- |
| Primitive types | `int`, `float`, `bool`, `text` | Name the four primitive declaration types. |
| Boolean literals | `true`, `false` | Represent the two Boolean values. |
| Named dimensions | `Length`, `Mass`, `Time`, `Force` | Constrain declarations and function contracts by physical dimension. |

Reserved-word regular expression:

```regex
^(int|float|bool|text|true|false|Length|Mass|Time|Force)$
```

The language is case-sensitive. For example, `Length` is reserved, but `length` is an ordinary identifier; `true` is a Boolean literal, but `True` is an ordinary identifier.

#### 5.3 Keyword and Reserved-Word Machine

| State | Input or condition | Next state or action | Accepting |
| --- | --- | --- | --- |
| Q0 (Start) | `Alpha` | Enter the identifier machine | No |
| Identifier | `Alpha`, `Digit`, or `_` | Continue the identifier machine | Yes |
| Identifier | identifier-ending character or end of file | Compare the complete lexeme with the keyword and reserved-word tables | Yes |
| Lookup | lexeme matches a keyword | Emit its keyword token | Yes |
| Lookup | lexeme matches a reserved primitive type | Emit its primitive-type token | Yes |
| Lookup | lexeme is `true` or `false` | Emit its Boolean-literal token | Yes |
| Lookup | lexeme matches a named dimension | Emit its dimension-name token | Yes |
| Lookup | no table entry matches | Emit `IDENT` | Yes |

The scanner performs the lookup only after the whole identifier has been read. Therefore, `if` is a keyword, while `ifValue` is one identifier rather than the keyword `if` followed by `Value`.

The teammate draft's `unit`, `dimension`, and `rate` declaration keywords are deferred from this proposal. `Money`, `Temperature`, and `Scalar` are not reserved dimension names, and `main` is not reserved. Built-in unit symbols such as `m`, `km`, `kg`, `s`, `N`, and `kN` also remain identifiers and are interpreted as units only in a unit context. Optional noise words are listed separately in the next section.

### 6. Noise Words

Noise words are optional reserved words that make selected constructs read more naturally. They do not change the meaning of a program and are valid only in their designated grammatical positions.

```ini
NoiseWord = { to, then, do }
```

| Noise word | Used with | Form without the noise word | Equivalent form with the noise word |
| --- | --- | --- | --- |
| `to` | `as` conversion | `distance as km` | `distance as to km` |
| `then` | `if` conditional | `if (condition) { ... }` | `if (condition) then { ... }` |
| `do` | `while` loop | `while (condition) { ... }` | `while (condition) do { ... }` |
| `do` | `for` loop | `for (...) { ... }` | `for (...) do { ... }` |

Their grammatical positions are summarized as follows:

```ini
Conversion = Expression as [ to ] UnitTarget
ConditionalStatement = if ( Expression ) [ then ] Block [ else Block ]
WhileStatement = while ( Expression ) [ do ] Block
ForStatement = for ( ForHeader ) [ do ] Block
```

Square brackets in these productions indicate an optional element; they are grammar notation rather than literal SML brackets.

Noise-word regular expression:

```regex
^(to|then|do)$
```

#### 6.1 Noise-Word Machine

Noise words use the identifier machine followed by exact-lexeme lookup:

| State | Input or condition | Next state or action | Accepting |
| --- | --- | --- | --- |
| Q0 (Start) | `Alpha` | Enter the identifier machine | No |
| Identifier | `Alpha`, `Digit`, or `_` | Continue the identifier machine | Yes |
| Identifier | identifier-ending character or end of file | Compare the complete lexeme with the noise-word table | Yes |
| Lookup | lexeme is `to`, `then`, or `do` | Emit its noise-word token | Yes |
| Lookup | no noise-word entry matches | Continue keyword/reserved-word lookup or emit `IDENT` | Yes |

The complete lexeme must match. Therefore, `then` is a noise word, while `thenValue` is an identifier. Matching is case-sensitive, so `Then` and `DO` are also ordinary identifiers.

Because noise words are reserved, they cannot be declared as names even though their use is optional. They are not accepted in arbitrary locations: for example, `let to = 5;`, `distance to km`, and `if then (condition) { ... }` are invalid.

### 7. Comments

SML supports two forms of comments:

- **Single-line comment:** begins with `//` and ends before the next line or at the end of the file.
- **Block comment:** begins with `/*` and ends at the next `*/`. It may span multiple lines but cannot be nested.

```sml
// This is a single-line comment.
let span = 5m; // The unit is meters.

/* This block comment
   continues on another line. */
let load = 12kN;
```

Single-line comment regular expression:

```regex
//[^\r\n]*
```

Single-line comment machine:

| State | Input | Next state or action | Accepting |
| --- | --- | --- | --- |
| Start | `/` | Slash | No |
| Slash | `/` | CommentBody | Yes |
| CommentBody | carriage return, line feed, or end of file | Accept before the line ending | Yes |
| CommentBody | anything else | CommentBody | Yes |

Block comment regular expression:

```regex
/\*([^*]|\*+[^*/])*\*+/
```

Block comment machine:

| State | Input | Next state or action | Accepting |
| --- | --- | --- | --- |
| Start | `/` | Slash | No |
| Slash | `*` | CommentBody | No |
| CommentBody | `*` | PossibleClose | No |
| CommentBody | end of file | Reject as unterminated | No |
| CommentBody | anything else | CommentBody | No |
| PossibleClose | `/` | Accept | Yes |
| PossibleClose | `*` | PossibleClose | No |
| PossibleClose | end of file | Reject as unterminated | No |
| PossibleClose | anything else | CommentBody | No |

Comments are otherwise treated like whitespace. They cannot interrupt an attached quantity, so `100/* comment */m` is not a valid quantity literal. An unterminated block comment is a lexical error. Comment markers inside a string, such as `"/* text */"`, are ordinary string characters rather than comments.

### 8. Blanks

- SML recognizes spaces, horizontal tabs, carriage returns, and line feeds as whitespace.
- Whitespace separates tokens when they would otherwise run together, as in `let length`.
- Whitespace is optional around operators and delimiters. For example, `a+b` and `a + b` are equivalent.
- Whitespace cannot appear inside a multi-character operator. Thus, `+=` is one operator, while `+ =` is two separate symbols.
- A quantity's unit must be attached directly to its magnitude. Therefore, `100m` and `9.8[m/s^2]` are valid, while `100 m` and `9.8 [m/s^2]` are invalid.
- Line breaks do not terminate statements; semicolons do. Multiple statements may therefore appear on one line.
- A brace-delimited block may be written on one line or across several lines.
- Whitespace inside a string literal is part of the string and is not ignored.

### 9. Delimiters and Brackets

```ini
Delimiter = { ;, (, ), {, }, [, ], ,, : }
```

- **Semicolon (`;`):** terminates a simple statement and separates clauses in a `for` header. It terminates statements rather than physical lines.
- **Parentheses (`(` and `)`):** group expressions and enclose conditions, function parameters, function arguments, and `for` headers.
- **Curly braces (`{` and `}`):** enclose function bodies and all conditional or iterative statement bodies, including a body containing only one statement.
- **Square brackets (`[` and `]`):** enclose compound units in quantity literals, exact-unit declaration annotations, and compound conversion targets. For example, `9.8[m/s^2]` and `let force: [N] = 12kN;` use square brackets for unit syntax.
- **Comma (`,`):** separates function parameters, function arguments, and expressions passed to `print`.
- **Colon (`:`):** introduces an annotation. It separates a declared name from its annotation, as in `let span: Length = 5m;`, and introduces a function's return annotation after its parameter list.

Whitespace is generally optional around delimiters. The exception is an opening square bracket attached to a quantity magnitude: `9.8[m/s^2]` is valid, while `9.8 [m/s^2]` is not a quantity literal.

Delimiter regular expression:

```regex
(;|\(|\)|\{|\}|\[|\]|,|:)
```

Delimiter machine:

| Input | Recognized delimiter |
| --- | --- |
| `;` | Semicolon |
| `(` or `)` | Left or right parenthesis |
| `{` or `}` | Left or right curly brace |
| `[` or `]` | Left or right square bracket |
| `,` | Comma |
| `:` | Colon |
| anything else | Reject |

### 10. Free-Field and Fixed-Field Formats

SML uses a **free-field format**, so source elements do not have to begin in specific lines or columns. Spaces, tabs, line breaks, and comments may appear between tokens wherever separation is permitted. A statement may span several lines, and several statements may appear on one line because semicolons, rather than line breaks, terminate simple statements. Curly braces determine the boundaries of functions, conditionals, and loops, while indentation is used only for readability. The main exception is attached quantity syntax: no whitespace or comment may separate a magnitude from its unit symbol or opening square bracket, so `100m` and `9.8[m/s^2]` are valid while `100 m` and `9.8 [m/s^2]` are not quantity literals. Whitespace inside a string literal is preserved as part of the string. SML has no fixed-field format, required statement columns, continuation columns, or column-based interpretation.

### 11. Expressions

An expression combines literals, identifiers, calls, conversions, and operators to produce a value. SML uses one precedence hierarchy for arithmetic, relational, equality, and logical expressions.

#### 11.1 Precedence and Associativity

The levels below are ordered from highest to lowest precedence.

| Level | Form or operator | Associativity |
| --- | --- | --- |
| 1 | literals, identifiers, calls, and parenthesized expressions | Primary |
| 2 | postfix conversion `as [to] UnitTarget` | Left-to-right postfix |
| 3 | power `^` | Right-to-left |
| 4 | unary `!`, `+`, `-` | Right-to-left |
| 5 | `*`, `/`, `%` | Left-to-right |
| 6 | `+`, `-` | Left-to-right |
| 7 | `<`, `<=`, `>`, `>=` | Non-chaining |
| 8 | `==`, `!=` | Non-chaining |
| 9 | `&&` | Left-to-right |
| 10 | `\|\|` | Left-to-right |

Examples:

```sml
3m as cm + 2cm       // (3m as cm) + 2cm
-2 ^ 2              // -(2 ^ 2)
a + b * c            // a + (b * c)
a < b && b < c       // (a < b) && (b < c)
```

Assignment is a statement rather than an expression and therefore has no expression precedence. Prefix and postfix updates are also standalone statements and cannot occur inside expressions.

#### 11.2 Expression Syntax

The table summarizes the valid expression forms. Angle brackets identify a category that must be replaced by a valid SML form.

| Expression form | Syntax | Example |
| --- | --- | --- |
| Literal | `<literal>` | `9.5s` |
| Identifier | `<identifier>` | `distance` |
| Parenthesized expression | `(<expression>)` | `(distance / time)` |
| Function call | `<identifier>(<arguments>)` | `speed(distance, time)` |
| Input expression | `input()` | `input()` |
| Unit conversion | `<expression> as [to] <unit-target>` | `3mi as km` |
| Unary expression | `<unary-operator><expression>` | `-distance` |
| Power expression | `<expression> ^ <expression>` | `length ^ 2` |
| Multiplicative expression | `<expression> (* | / | %) <expression>` | `distance / time` |
| Additive expression | `<expression> (+ | -) <expression>` | `5m + 3m` |
| Relational expression | `<expression> (< | <= | > | >=) <expression>` | `distance < limit` |
| Equality expression | `<expression> (== | !=) <expression>` | `count == 5` |
| Logical expression | `<expression> (&& | \|\|) <expression>` | `valid && ready` |

The precedence table in Section 11.1 determines how expressions containing several operators are grouped. Prefix and postfix `++` and `--` are update statements, not expression forms.

Relational and equality operators are non-chaining. Expressions such as `a < b < c` and `a == b == c` are invalid; logical operators must be used to combine comparisons, as in `a < b && b < c`.

#### 11.3 Expression Rules

| Operation | Rule | Example |
| --- | --- | --- |
| `+` and `-` | Operands must have the same dimension and exact unit representation. | `5m + 2m` |
| `%` | Operands must have the same exact unit representation. | `5m % 2m` |
| `*` | Operand units are multiplied to derive the result unit. | `3m * 2m` produces `[m^2]` |
| `/` | Operand units are divided to derive the result unit. | `100m / 9.5s` produces `[m/s]` |
| `^` | A dimensioned base requires a compile-time integer exponent; a dimensionless base may use an integer or decimal exponent. | `3m ^ 2` produces `[m^2]` |
| `<`, `<=`, `>`, `>=` | Comparable operands produce a Boolean result and require an explicit common unit representation. | `5km < (3mi as km)` |
| `==` and `!=` | Comparable primitive values or quantities with the same exact unit representation produce a Boolean result. | `5m != 3m` |
| `!`, `&&`, `\|\|` | Operate on Boolean values; `&&` and `\|\|` use short-circuit evaluation. | `valid && safe` |
| `as` | Explicitly converts a quantity to a compatible unit target. | `3mi as km` |

SML does not silently convert between different unit representations. For example, `5km + 3000m` is invalid even though both operands have the dimension Length. It must be written with an explicit conversion, such as `5km + (3000m as km)`.

#### 11.4 Unit Expressions

A `UnitExpression` describes a compound unit inside square brackets. It is used by compound quantity literals, exact-unit annotations, and compound conversion targets.

```ebnf
UnitExpression
    = UnitProduct, [ "/", UnitDenominator ] ;

UnitProduct
    = UnitPower, { "*", UnitPower } ;

UnitDenominator
    = UnitPower
    | "(", UnitProduct, ")" ;

UnitPower
    = UnitSymbol, [ "^", SignedInteger ] ;

SignedInteger
    = [ "-" ], Digits+ ;
```

The following restrictions keep unit expressions manageable for lexical and syntactic analysis:

- Multiplication must be written explicitly with `*`.
- Only one top-level `/` is permitted; repeated or nested division is invalid.
- A denominator containing multiple factors must be enclosed in parentheses.
- A grouped unit expression cannot be raised to a power.
- Numeric scale factors are not allowed inside unit expressions.
- A unit expression may contain at most eight written unit-factor occurrences.
- Written unit exponents must range from `-16` through `16`.
- Normalized dimension exponents must remain from `-32` through `32`.
- The contents of one unit annotation may contain at most 128 ASCII characters, including whitespace.

Accepted unit expressions include:

```sml
9.8[m/s^2]
1[kg*m/s^2]
1[kg/(m*s^2)]
```

Rejected forms include:

```sml
1[kg/m/s^2]  // repeated division
1[m/(kg/s)]  // nested division
1[(m/s)^2]   // power applied to a group
1[N m]       // implicit multiplication
1[1000*m]    // numeric scale factor
```

The `^` inside a `UnitExpression` accepts only a signed integer exponent. This is narrower than the ordinary numeric power operator, which may accept a decimal exponent when its base is dimensionless.

### 12. Statements

Statements perform the actions of an SML program. Every simple statement ends with a semicolon, while every conditional and iterative body is enclosed in curly braces.

| Statement category | General syntax |
| --- | --- |
| Declaration | `(let \| const) <identifier> [: <annotation>] = <expression>;` |
| Assignment | `<identifier> <assignment-operator> <expression>;` |
| Update | `(++ \| --)<identifier>;` or `<identifier>(++ \| --);` |
| Output | `print(<expression>, ...);` |
| Function call | `<identifier>(<arguments>);` |
| Conditional | `if (<expression>) [then] <block> [else <block>]` |
| Iterative | `while (<expression>) [do] <block>` or `for (...) [do] <block>` |
| Return | `return [<expression>];` |
| Loop control | `break;` or `continue;` |
| Assertion | `assert <expression>;` |

Here, `<block>` means one or more statements enclosed in `{` and `}`. Square brackets indicate an optional part and are not literal SML brackets.

#### 12.1 Declaration Statements

A declaration introduces one initialized binding. The annotation is optional for a local declaration when its constraint can be inferred from the initializer.

| Syntax | Example | Declaration form |
| --- | --- | --- |
| `let <identifier> = <expression>;` | `let count = 5;` | Inferred dimensionless value |
| `let <identifier>: <primitive-type> = <expression>;` | `let count: int = 5;` | Primitive-type annotation |
| `let <identifier> = <quantity-expression>;` | `let span = 5m;` | Inferred quantity |
| `let <identifier>: <dimension> = <expression>;` | `let span: Length = 5m;` | Named-dimension annotation |
| `let <identifier>: [<unit-expression>] = <expression>;` | `let exactSpan: [m] = 5m;` | Exact-unit annotation |
| `const <identifier> [: <annotation>] = <expression>;` | `const gravity: [m/s^2] = 9.8[m/s^2];` | Constant binding |

The primitive types are `int`, `float`, `bool`, and `text`. The named dimensions are `Length`, `Mass`, `Time`, and `Force`.

Only one annotation category may be used. Combined forms such as `float[m]`, `Length(m)`, and `float Length` are invalid. Each declaration introduces one binding; comma-separated declarations are not permitted.

#### 12.2 Input and Output Statements

The `print` statement accepts one or more expressions. When a quantity is printed, its unit representation is included with its magnitude.

| Syntax | Example |
| --- | --- |
| `print(<expression>, ...);` | `print("Speed: ", speed);` |
| `let <identifier>: <annotation> = input();` | `let height: [m] = input();` |
| `<identifier> = input();` | `height = input();` |

```sml
let speed = 100m / 9.5s;
print("Speed: ", speed);
```

The input form `input()` is an expression used directly as the initializer or right-hand side of a binding whose expected primitive type or exact unit is known:

```sml
let height: [m] = input();
print("Height: ", height);

height = input();
```

An unannotated declaration such as `let value = input();` is invalid because SML cannot infer its expected type or unit from the input expression alone.

#### 12.3 Assignment Statements

An assignment stores the result of an expression in an existing mutable binding. Assignment is a statement rather than an expression.

| Syntax | Example | Meaning |
| --- | --- | --- |
| `<identifier> = <expression>;` | `a = b;` | Stores the value of an expression. |
| `<identifier> += <expression>;` | `length += 1m;` | Adds an explicitly stated value. |
| `<identifier> -= <expression>;` | `length -= 1m;` | Subtracts an explicitly stated value. |
| `<identifier> (*= \| /=) <dimensionless-expression>;` | `scale *= 2;` | Multiplies or divides without changing the binding's dimension. |
| `++<identifier>;` or `--<identifier>;` | `++count;` | Prefix update of a dimensionless numeric variable. |
| `<identifier>++;` or `<identifier>--;` | `count++;` | Postfix update of a dimensionless numeric variable. |

The following examples correspond to the required assignment forms:

```sml
let b = 5m;
let g = 2m;
let a = 0m;
let area: [m^2] = 0[m^2];

a = b;
a = b + 3m;
area = (b + 3m) * g / 24;
```

The final expression produces area rather than length because it multiplies two Length quantities. Assigning that expression to `a` would be invalid, while assigning it to `area` is valid.

Compound assignments and both update positions are supported:

```sml
a += 1m;
a *= 2;
++count;
count++;
```

The right operand of `*=` or `/=` must be dimensionless. Prefix and postfix updates apply only to dimensionless numeric variables. A dimensioned value must use `+=` or `-=` with an explicitly unit-bearing operand. Expression-valued updates and chained assignments are invalid:

```sml
length++;       // invalid: length is dimensioned
++length;       // invalid: length is dimensioned
print(count++); // invalid expression-valued update
a = b = 5m;    // invalid chained assignment
```

#### 12.4 Conditional Statements

| Form | Syntax |
| --- | --- |
| `if` | `if (<expression>) [then] <block>` |
| `if-else` | `if (<expression>) [then] <block> else <block>` |
| `if-else if-else` | `if (<expression>) [then] <block> else if (<expression>) [then] <block> else <block>` |

The condition must produce a Boolean value. Braces are required even when a branch contains only one statement.

An `if` statement:

```sml
if (load > 100kN) {
    print("High load");
}
```

An `if-else` statement:

```sml
if (load > 100kN) {
    print("High load");
} else {
    print("Normal load");
}
```

An `if-else if-else` statement:

```sml
if (load > 100kN) {
    print("High load");
} else if (load == 100kN) {
    print("At the limit");
} else {
    print("Below the limit");
}
```

A nested conditional:

```sml
if (load > 0kN) {
    if (load > 100kN) {
        print("Positive high load");
    } else {
        print("Positive normal load");
    }
} else {
    print("No positive load");
}
```

#### 12.5 Iterative Statements

SML provides `while` and C-style `for` loops. Their conditions must produce Boolean values, and their bodies always use braces.

| Form | Syntax |
| --- | --- |
| `while` loop | `while (<expression>) [do] <block>` |
| `for` loop | `for (<initialization>; <condition>; <update>) [do] <block>` |

The initialization may be a declaration or assignment. The update may be an assignment or a prefix or postfix update of a dimensionless numeric variable.

A loop containing one statement still requires braces:

```sml
for (let i: int = 0; i < 3; i++) {
    print(i);
}
```

A `while` loop:

```sml
let fuel: [kg] = 10kg;

while (fuel > 0kg) do {
    print("Fuel left: ", fuel);
    fuel -= 1kg;
}
```

Nested `for` loops:

```sml
for (let row: int = 0; row < 3; row++) {
    for (let column: int = 0; column < 3; column++) {
        print(row, ",", column);
    }
}
```

The statement `break;` exits the nearest enclosing loop, while `continue;` begins its next iteration.

#### 12.6 Other Statements

SML also provides function-call, return, assertion, and loop-control statements:

| Statement | Syntax | Example |
| --- | --- | --- |
| Function call | `<identifier>(<arguments>);` | `printResult();` |
| Return | `return [<expression>];` | `return force;` |
| Assertion | `assert <expression>;` | `assert deflection <= allowableDeflection;` |
| Break | `break;` | `break;` |
| Continue | `continue;` | `continue;` |

```sml
printResult();
return force;
assert deflection <= allowableDeflection;
break;
continue;
```

An assertion expression must produce a Boolean value. A return expression must agree with the function's declared return annotation, which is introduced with a colon after the function's parameter list.
