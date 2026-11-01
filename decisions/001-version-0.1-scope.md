# 001: Version 0.1 scope and long-term language target

Status: SUPERSEDED by decision 075  
Target: historical expression-core plan  
Depends on: none
Informed by: teammate proposal's complete procedural Measure design

Current note: decision 078 confirms that money and affine temperature are deferred from the proposal.

## Historical decision

The teammate's procedural Measure design remains the long-term language target. This record previously treated a single expression plus semantic checking and evaluation as the complete version 0.1 implementation.

Under this superseded plan, declarations, mutation, output, comparisons, control flow, functions, and user-defined units entered through later dependency-ordered milestones. It excluded currency and treated affine temperature only as a candidate; decision 078 retains their deferral for the current proposal.

## Reason

Decision 075 replaces that implementation boundary. The current course project implements a lexer and parser, using the expression core as its first slice while extending the grammar to the statement forms required by the final proposal. Semantic checking and execution are outside the project.

## Revisit trigger

See decision 075. A future project may define a new semantic implementation boundary explicitly.
