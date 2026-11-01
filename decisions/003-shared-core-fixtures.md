# 003: Shared core expression fixtures

Status: ACCEPTED  
Target: parser core and later semantic regression suites  
Depends on: SD-001, SD-002, SD-012, SD-014, SD-015, SD-020, SD-043
Informed by: teammate proposal's valid calculations, unit-error examples, and explicit-conversion examples

## Decision

The shared fixture set is maintained in `PROJECT.md` Section 14.7. It contains eight ordinary expressions, five syntactically valid expressions reserved for future semantic or resolution tests, and six malformed inputs.

The current lexer/parser must produce tokens and ASTs for all thirteen syntactically valid expressions and lexical or syntax diagnostics for the six malformed inputs. A future semantic project may add resolved units, normalized dimensions, conversions, evaluated magnitudes, formatting, and semantic diagnostics.

## Scope boundary

This core set does not remove declarations, I/O, assignment, conditionals, iteration, or functions from Measure or from the final course proposal. Those features require lexer/parser extension fixtures. The professor's documentation outline requires statement examples, so the final proposal is incomplete until their grammar, AST shapes, and malformed cases exist.


## Validation policy

- Every syntactically valid expression has a token stream and AST expectation.
- Malformed source identifies the lexer or parser as its owning phase.
- Semantic expectations remain informative and must not cause parser rejection.

## Revisit trigger

Revise the core only if an accepted foundational rule changes. New language features should normally add extension fixtures instead of broadening the core set.
