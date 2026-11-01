# 074: Direct checked-AST evaluation

Status: SUPERSEDED by decision 075  
Target: deferred future semantic project  
Depends on: SD-024, SD-042, Phase 6 gate
Informed by: teammate proposal's Python-generation pipeline, evaluated and rejected for version 0.1

## Historical decision

This record previously selected direct evaluation of a checked AST instead of Python generation.

Decision 075 removes evaluation entirely from the current project. Neither direct evaluation nor Python generation is part of the lexer/parser deliverable.

## Reason

Direct evaluation keeps the educational implementation focused on Measure's lexer, parser, AST, unit semantics, diagnostics, and execution rules. It avoids inheriting Python's numeric and runtime behavior before Measure specifies those behaviors itself.

## Rejected for version 0.1

- Direct Python generation couples the first implementation to an external language and adds little value for a single-expression source.
- A general bytecode or multi-backend IR adds machinery not justified by the first fixtures.

## Revisit trigger

A later project may reconsider direct evaluation or Python generation only after explicitly adding semantic execution to its scope and defining numeric and conversion behavior.
