# 023: Statement terminators and control-flow blocks

Status: ACCEPTED FOR CURRENT PARSER GRAMMAR  
Target: current course lexer/parser  
Depends on: SD-020 through SD-022
Informed by: teammate proposal's semicolon and brace syntax; revised to disallow unbraced control-flow bodies and to make `main` an ordinary identifier

## Decision

When statements are introduced, simple statements require trailing semicolons and every conditional or loop body requires braces. Unbraced control-flow bodies are not supported. `main` remains an ordinary identifier with a possible entry-point role, not a reserved word.

The parser also enforces context visible from surrounding syntax: `break;` and `continue;` require an enclosing loop; a bare `return;` requires a function without a return annotation; and `return expression;` requires a function with a return annotation. Name resolution, call-argument matching, Boolean condition typing, and unit-sensitive checks remain later semantic work.

## Reason

Mandatory braces avoid dangling-`else` ambiguity and simplify parsing, formatting, and recovery. Required semicolons give statement sequences an explicit boundary in a free-field language.

## Revisit trigger

Revisit only if a later expression-oriented block design provides equally local boundaries and diagnostics with less syntax.
