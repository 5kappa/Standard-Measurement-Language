# Decision record index

This directory records accepted and provisional language decisions. `PROJECT.md` contains the consolidated design; `SPECIFICATION-ROADMAP.md` retains dependency order and unresolved work.

The teammate-authored *Measure: A Unit-Safe Programming Language* proposal is a major design input. A record marked **adopted** preserves its choice, **revised** preserves the intent while changing the technical rule, and **rejected for version 0.1** records a deliberate departure.

| Record | Status | Relationship to teammate proposal |
| --- | --- | --- |
| [001: Version 0.1 scope](001-version-0.1-scope.md) | Superseded by 075 | **Historical.** Its expression-only semantic implementation boundary is replaced by the lexer/parser boundary. |
| [002: Normative terminology](002-normative-terminology.md) | Accepted | **Revised.** Preserves unit-aware numeric meaning while separating magnitude, unit, dimension, kind, and type. |
| [003: Shared core fixtures](003-shared-core-fixtures.md) | Accepted | **Adopted and expanded.** Reuses the proposal's calculations, errors, and conversions as phase-owned fixtures. |
| [012: Numeric sign tokenization](012-numeric-sign-tokenization.md) | Accepted | **Revised.** A sign is a parser operator rather than part of the numeric token. |
| [014: Quantity-literal boundary](014-quantity-literal-boundary.md) | Accepted | **Adopted with lexical refinement.** Keeps `100m` and `9.8[m/s^2]`; tokenizes the simple form as `NUMBER IDENT`. |
| [017: Optional noise words](017-optional-noise-words.md) | Accepted | **Adopted.** Retains optional `to`, `then`, and `do` in fixed grammar positions without semantic effect. |
| [020: Staged operators](020-staged-operator-set.md) | Accepted | **Revised.** Adopts the operator direction, stages the broader set, and makes `as` a tight postfix operator. |
| [022: Bounded unit-expression grammar](022-bounded-unit-expression-grammar.md) | Accepted | **Revised.** Preserves the proposal's `*`, `/`, and integer `^` notation while imposing one-division and resource limits. |
| [023: Statements and blocks](023-statement-and-block-syntax.md) | Accepted for current parser grammar | **Revised.** Keeps semicolons and braces, requires braces for all control flow, and does not reserve `main`. |
| [026: Dimensionless numbers and powers](026-dimensionless-numbers-and-powers.md) | Accepted for staged parser grammar | **Adopted and refined.** Keeps numeric `^`; dimension-based exponent restrictions are future semantic checks. |
| [027: Declaration annotations](027-declaration-annotations.md) | Accepted for current parser grammar | **Revised.** Replaces mixed forms such as `Length(m)` with one primitive, dimension, or exact-unit annotation category. |
| [028: Local initializer inference](028-local-initializer-inference.md) | Accepted declaration grammar; inference deferred | **Adopted and bounded.** Keeps one initialized binding per declaration; actual inference is outside the parser. |
| [029: Increment/decrement statements](029-increment-decrement-statements.md) | Accepted for current parser grammar | **Revised.** Keeps postfix `++` and `--` as standalone statements; mutation checks are deferred. |
| [030: Formal dimension and unit model](030-formal-dimension-and-unit-model.md) | Accepted | **Adopted and narrowed.** Uses physical LMT bases, derives `Force`, and limits the initial named dimensions and unit registry to the draft's required surface. |
| [033: Unit-expression semantics](033-unit-expression-semantics.md) | Accepted | **Adopted and bounded.** Uses complete registered symbols, exact normalization and cancellation, source-spelling preservation, and local limit diagnostics. |
| [043: Explicit conversion](043-explicit-unit-conversion.md) | Accepted | **Adopted.** Preserves the No Silent Conversion principle and `as`. |
| [074: Direct evaluation](074-direct-checked-ast-evaluation.md) | Superseded by 075 | **Deferred.** The current project has no execution phase, whether direct or generated. |
| [075: Lexer/parser project boundary](075-lexer-parser-project-boundary.md) | Superseded by 076 | **Historical.** The deliverable was later clarified as proposal-only. |
| [076: Proposal-only deliverable](076-proposal-only-deliverable.md) | Accepted | **Revised and consolidated.** Uses the professor's outline as the coverage contract, adopts compatible teammate defaults, and makes `LANGUAGE-SPECIFICATION.md` normative. |
| [077: Money and affine temperature](077-money-and-affine-temperature.md) | Superseded by 078 | **Historical.** This briefly accepted visible currency rates and affine temperature before the team narrowed the proposal. |
| [078: Defer money and affine temperature](078-defer-money-and-affine-temperature.md) | Accepted | **Deferred.** Removes currency and affine temperature from the current proposal while preserving them as possible future extensions. |
| [079: Minutes and derived volume](079-minutes-and-derived-volume.md) | Accepted | **Expanded and clarified.** Adds `min = 60s` to the initial registry while retaining volume as unnamed `Length^3` expressed with `[m^3]`. |
| [080: Add the mile unit](080-add-mile-unit.md) | Expanded by 081 | **Expanded and bounded.** Introduced exact `mi` support and explicit conversion between `mi` and metric Length units. |
| [081: Add feet and inches](081-add-feet-and-inches.md) | Accepted | **Expanded and bounded.** Adds exact `ft` and `in` support while limiting the imperial library to `in`, `ft`, and `mi`. |
| [082: Dedicated Literals section](082-dedicated-literals-section.md) | Accepted | **Documentation structure.** Adds Literals after Identifiers, keeps quantity boundaries there, and leaves detailed unit-expression grammar under Expressions. |
| [083: Disallow leading zeros](083-disallow-leading-zeros.md) | Accepted | **Canonical numeric syntax.** Restricts an integer part to `0` or a nonzero-leading digit sequence and updates the combined number pattern. |
| [084: Use colon for function returns](084-colon-function-return-annotation.md) | Accepted | **Simplified function syntax.** Reuses `:` for function return annotations and removes the `->` delimiter and `ARROW` token. |

## Proposal choices not yet accepted

Decision 076 settled the proposal's remaining lexical and statement surface. Decision 078 defers money and affine temperature. General quantity-kind enforcement, runtime input semantics, output formatting details, and numeric representation remain outside the required proposal semantics.

## Maintenance rule

When a proposal-derived choice is accepted, revised, rejected, or superseded:

1. update its decision record and provenance line;
2. update this index;
3. update the corresponding roadmap state;
4. update normative wording and examples in `PROJECT.md`; and
5. update affected fixtures.
