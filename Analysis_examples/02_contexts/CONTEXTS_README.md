# Contextual Reference Files

This directory contains **contextual reference files** used by the Small Audio Tool (SAT)
during report generation.

In SAT, a context is **not an interpretation**, **not a decision rule**, and **not a normalization scheme**.
It is a **documentary reference layer** that helps position numerical measurements
*when such positioning is methodologically justified*.

Contexts affect **presentation only**.
They never influence computation.

---

## Purpose of Context Files

Context files exist to:

- document when a numeric measurement can be meaningfully compared to a reference zone,
- explicitly state when such comparison is **not** justified,
- make methodological limits visible in generated reports,
- prevent silent or implicit interpretation.

A context never adds new information.
It only constrains how existing measurements may be read.

---

## Directory Structure

```
Analysis_examples/02_contexts/
├── context_temporal.yaml
├── context_spectral.yaml
├── context_time_frequency.yaml
├── context_modulation.yaml
├── context_information.yaml
├── context_inter_channel.yaml
├── context_steganography.yaml
├── context_meta_analysis.yaml
└── README.md
```

Each file corresponds to **one analysis family**.
File names and family identifiers must match the analysis code exactly.

---

## What a Context Is (and Is Not)

A context in SAT:

- defines **reference status** for measured metrics,
- may define numeric reference zones *only when justified by the literature*,
- documents why some metrics cannot be zoned,
- is static and declarative.

A context does **not**:

- change or filter measurements,
- introduce thresholds or decisions,
- normalize values,
- classify signals,
- infer intent, meaning, or anomaly.

Contexts are reference tables, not reasoning engines.

---

## Reference Status Categories (A / B / C)

Each metric listed in a context file is assigned exactly one reference status.

### Status A — Zoned Metrics

- The literature defines a stable numeric reference zone.
- A `typical_range` may be provided.
- These metrics can be positioned relative to a reference interval.

Examples:
- normalized correlation measures
- normalized entropy
- bounded flatness metrics

### Status B — Context-Dependent Metrics

- No universal numeric reference zone exists.
- Values depend on signal class, configuration, or scale.
- Numeric comparison is not meaningful in isolation.

Metrics in this category are listed and documented,
but never positioned relative to a zone.

### Status C — Descriptive Metrics

- Values are scale-dependent or distributional.
- Absolute numeric interpretation is not meaningful.
- Metrics are provided for inspection only.

The absence of a reference zone is intentional and informative.

---

## Relationship With Analysis Protocols

Protocols and contexts are strictly independent.

- **Protocols** define *what is measured*.
- **Contexts** define *how measurements may be positioned, if at all*.

Changing a protocol changes the observation space.
Changing a context changes only the presentation of results.

No protocol requires a specific context.
No context alters protocol execution.

---

## Use During Report Generation

During report generation:

- contexts are loaded automatically from this directory,
- one context file is applied per analysis family,
- missing context files are reported explicitly,
- all measured metrics remain visible.

Contexts influence only how metrics are organized and described
in the contextual positioning section of the report.

---

## Design Intent

Context files are designed to:

- make methodological assumptions explicit,
- preserve scientific restraint,
- avoid over-interpretation,
- expose limits rather than hide them.

They support human reasoning.
They do not replace it.

