# 084: Use a colon for function return annotations

Status: ACCEPTED  
Target: function syntax and delimiter inventory  
Depends on: decisions 023, 027, and 076

## Decision

SML uses a colon after a function's parameter list to introduce an optional return annotation:

```ebnf
function_definition
    = "fn", IDENT, "(", [ parameter_list ], ")",
      [ ":", return_annotation ], block ;
```

For example:

```sml
fn speed(distance: Length, time: Time): [m/s] {
    return (distance as m) / (time as s);
}

fn main() {
    print("Ready");
}
```

A function without the optional colon and return annotation returns no value. The earlier `->` form is not part of SML.

## Rationale

The colon already introduces annotations on declarations and parameters. Reusing it for function returns keeps annotation syntax consistent, removes one delimiter and token kind, and eliminates the lexical overlap between subtraction `-` and an arrow beginning with `-`.

## Consequences

- `->` is removed from the delimiter regular expression and machine.
- The `ARROW` token is removed from the consolidated token inventory.
- Function examples and grammar use `fn name(parameters): ReturnAnnotation`.
- Explicit return contracts remain part of the proposal; only their punctuation changes.
