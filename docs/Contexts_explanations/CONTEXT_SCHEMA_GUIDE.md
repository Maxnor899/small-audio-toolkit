# Context Reference Schema & Authoring Guide

This document defines the **official schema and authoring rules** for all
`context_<family>.yaml` files used by the report generator.

Its purpose is to ensure that contextual references:
- remain scientifically defensible,
- strictly match the analysis code outputs,
- never introduce interpretation or hidden logic.

This document is normative.
It complements the methodological documents in docs/analysis_explanations by translating their 
constraints into a concrete, machine-readable context schema.

---

## 1. Core Principle (Non-Negotiable)

**A context entry MUST correspond exactly to a metric produced by the analysis code.**

- No metric may be introduced based on documentation alone.
- Documentation only authorizes or forbids the use of numeric reference zones.
- If a metric is not produced by the code, it does not exist for the context.

The code defines the vocabulary.  
The documentation defines the legitimacy of reference zones.

---

## 2. Two-Pass Construction Process

### Pass 1 — Technical Inventory (Code-Driven)

For each analysis family:

1. Inspect the analysis functions.
2. Extract all scalar numeric metrics actually produced.
3. Record their exact identifiers:

```
family.method.metric
```

This guarantees that every contextual entry maps to a real result.

### Pass 2 — Scientific Filtering (Documentation-Driven)

For each metric in the inventory:

- Consult the corresponding methodological document (`10_*.md` → `17_*.md`).
- Determine whether the literature:
  - defines a stable numeric reference,
  - allows only contextual / order-of-magnitude reasoning,
  - or explicitly forbids numeric zoning.

The metric identifier always remains the one defined by the code.

---

## 3. Reference Status Categories

Each metric MUST be assigned exactly one reference status.

### Status A — Zoned / Reference-Based

- A stable numeric reference zone is justified by the literature.
- A `typical_range` MAY be defined.
- These metrics are eligible for detailed contextual positioning.

Examples:
- normalized correlation
- normalized entropy
- bounded flatness measures

### Status B — Contextual / Order-of-Magnitude

- No stable universal reference zone exists.
- Values depend on signal class, configuration, or scale.
- Numeric comparison is not meaningful in isolation.

Examples:
- event counts
- temporal intervals
- delays
- energy ratios

### Status C — Descriptive Only

- Values are scale-dependent or distributional.
- Absolute numeric interpretation is not meaningful.
- Metrics are provided for inspection only.

Examples:
- envelope magnitudes
- FFT/STFT magnitudes
- list-based or distributional outputs

---

## 4. Context File Schema

```yaml
version: "1.0"
family: "<family_name>"
description: "<short description>"

methods:
  <method_name>:
    scope: "per_channel | pair | single"
    metrics:
      <metric_name>:
        unit: "<string>"
        reference:
          status: "A | B | C"
          typical_range: [min, max]   # present only if status == A
        notes:
          - "<mandatory explanation for B and C>"
```

---

## 5. Authoring Rules

- Metric identifiers MUST match code outputs exactly.
- `typical_range` MUST exist only for status A.
- Metrics with status B or C MUST include an explanatory note.
- Absence of `typical_range` is meaningful and intentional.
- Context files contain no logic and no inference rules.

---

## 6. Impact on Report Generation

The report generator MUST behave mechanically:

- Section 3.A:
  - metrics with `reference.status == A`
  - detailed comparison to reference zones

- Section 3.B:
  - metrics with `reference.status == B or C`
  - grouped listing with explanatory notes
  - no numeric positioning

No metric is skipped silently.
This behavior is implemented in the contextual positioning section of generated reports and 
reflects exactly the constraints described in 02_LINK_WITH_CONTEXTUAL_REFERENCES.md.

---

## 7. Design Intent

This schema enforces:

- separation of measurement and interpretation,
- traceability between code, context, and documentation,
- transparency of methodological limits,
- resistance to over-interpretation.

Context files are reference tables, not decision engines.

---

End of document.
