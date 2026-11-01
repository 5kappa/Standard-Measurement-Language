# 082: Add a dedicated Literals section to the final proposal

Status: ACCEPTED  
Target: final course proposal organization  
Depends on: decisions 012, 014, 022, and 076  
Informed by: the professor's documentation outline and the need to place numeric and quantity-literal rules at the correct lexical/syntactic level

Amended by: decision 083, which excludes leading zeros and revises the number pattern

## Decision

Add **Literals** as a dedicated section immediately after **Identifiers** in Part II, *Syntactic Elements of the Language*. Renumber the professor's later topics accordingly:

1. Character Set
2. Identifiers
3. Literals
4. Operation Symbols
5. Keywords and Reserved Words
6. Noise Words
7. Comments
8. Blanks
9. Delimiters and Brackets
10. Free-and-fixed-field Formats
11. Expressions
12. Statements

The Literals section contains:

- integer, decimal, and combined number-literal productions;
- the number regular expression and lexical machine;
- string and Boolean literal forms;
- simple and compound quantity-literal productions; and
- the source-adjacency rule between a magnitude and its attached unit syntax.

The general number token, as amended by decision 083, is:

```regex
(0|[1-9][0-9]*)(\.[0-9]+)?
```

A leading `+` or `-` remains an expression operator rather than part of a numeric literal.

The Literals section introduces the quantity boundary:

```ebnf
quantity_literal
    = simple_quantity_literal
    | compound_quantity_literal ;

simple_quantity_literal
    = number_literal, unit_symbol ;

compound_quantity_literal
    = number_literal, "[", unit_expression, "]" ;
```

Because BNF/EBNF does not encode trivia, prose states that `NUMBER` must be adjacent to the following unit symbol or `[`.

The complete `unit_expression` grammar and its hard limits remain under **Expressions**, where unit operators, precedence, grouping, and powers are explained. The Expressions section lists quantity literals among primary expressions and cross-references the Literals section.

## Rationale

The professor's outline requires a character set and identifier rules but does not provide a suitable location for literal patterns. A literal is neither a character nor an identifier. Adding one clearly named section keeps character enumeration, lexical recognition, and expression composition distinct without removing any required outline topic.

## Consequences

- `Integer` is removed from the Character Set enumeration.
- Integer and decimal forms are documented under Literals.
- The sign decision remains unchanged: `-5` is `MINUS NUMBER(5)`.
- Simple quantities remain `NUMBER IDENT`, not one combined token.
- Compound quantities remain bounded by brackets.
- This is a presentation decision; it does not alter the accepted token inventory or language grammar.

## Revisit trigger

Revisit only if the professor requires the original numbering to remain unchanged. In that case, Literals may become an unnumbered subsection between Identifiers and Operation Symbols while retaining the same content split.
