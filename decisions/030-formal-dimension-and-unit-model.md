# 030: Formal dimension and unit model

Status: ACCEPTED  
Target: version 0.1 and later  
Depends on: SD-022, SD-026, SD-033  
Informed by: teammate proposal's unit-safe arithmetic, force quantities, and `N`/`kN` examples

Confirmed by: decision 078, which defers money and affine temperature and retains the LMT-plus-Force model
Amended by: decision 079, which adds `min` and confirms volume as unnamed `Length^3`
Amended by: decision 080, which adds `mi`
Amended by: decision 081, which adds `ft` and `in` and bounds the imperial set to those symbols plus `mi`

## Decision

Measure uses exactly three physical base dimensions in its initial model:

```text
Length = (1, 0, 0)
Mass   = (0, 1, 0)
Time   = (0, 0, 1)
```

A normalized dimension is an integer exponent vector `(L, M, T)`. Multiplication adds vectors, division subtracts them, and an allowed integer power multiplies every component. Addition, subtraction, and conversion require equal normalized vectors. The accepted normalized exponent bound remains `-32` through `32` per component.

`Force` is a named derived-dimension alias, not a fourth base dimension:

```text
Force = Mass * Length / Time^2 = (1, 1, -2)
```

The initial named physical annotations are `Length`, `Mass`, `Time`, and `Force`. Other results may have unnamed derived dimension vectors and may be constrained with an exact compound-unit annotation. The initial model does not introduce named angle, pressure, stress, moment, or energy dimensions.

## Unit registry

Every initial unit definition contains a complete case-sensitive symbol, a normalized dimension vector, and an exact rational scale relative to the canonical base units. The minimum registry is:

| Symbol | Dimension | Exact canonical scale |
| --- | --- | --- |
| `m` | `Length` | `1` |
| `cm` | `Length` | `1/100` |
| `mm` | `Length` | `1/1000` |
| `km` | `Length` | `1000` |
| `in` | `Length` | `127/5000` (`0.0254`) |
| `ft` | `Length` | `381/1250` (`0.3048`) |
| `mi` | `Length` | `201168/125` (`1609.344`) |
| `kg` | `Mass` | `1` |
| `s` | `Time` | `1` |
| `min` | `Time` | `60` relative to `s` |
| `N` | `Force` | `1` relative to `kg*m/s^2` |
| `kN` | `Force` | `1000` relative to `N` |

The canonical base units are `m`, `kg`, and `s`. The complete registered imperial Length symbols are `in`, `ft`, and `mi`, with exact scales `127/5000`, `381/1250`, and `201168/125` relative to `m`; no other imperial units are included. `min` is a complete registered Time unit with scale `60` relative to `s`. `N` is a registered derived unit whose normalized dimension and scale are equivalent to `kg*m/s^2`; it does not change the base-dimension system. All registry symbols remain complete entries rather than parser-level prefix expressions.

The accepted unit grammar permits `kg*m/s^2`: it has one numerator product, one division, one powered denominator factor, three written factors, and an in-range exponent.

## Annotation consequences

```measure
let span: Length = 5m;
let load: Force = 12kN;
let exactForce: [kg*m/s^2] = 1[kg*m/s^2];
let distributedLoad: [kN/m] = 8[kN/m];
let duration: Time = 5min;
let volume: [m^3] = 12[m^3];
```

`Force` provides a readable contract while `[N]`, `[kN]`, and `[kg*m/s^2]` remain exact-unit constraints under SD-027.

Volume remains the unnamed derived dimension `Length^3`. It is constrained with an exact annotation such as `[m^3]`; this decision does not add `Volume` as a named annotation.

## Scope boundary

This decision does not add angle, percentage, pressure/stress, temperature, currency, user-defined dimensions, or quantity-kind enforcement. Those concepts require separate justification and must not be inferred merely because the LMT algebra can represent their physical dimensions.

The exact representation of runtime magnitudes, rounding, overflow, display-unit selection, and diagnostic recovery remain separate decisions.

## Validation

Fixtures must establish vector arithmetic by hand, including `kg*m/s^2` normalizing to `Force`, `N` and `kg*m/s^2` having equal dimensions and scales, `kN/m * m` producing `Force`, cancellation to dimensionless, and rejection when additive or conversion operands have unequal vectors.
