# Official Context YAML — Technical Description

This document describes the **official context YAML files** used by the Small Audio Tool (SAT)
to generate the *official contextual positioning report* (report 03).

It merges:
- the formal **technical loading and matching description**,
- with the **normative structure and intent** of official context YAML files.

This is a **technical document**.
It does not justify reference values and does not interpret measurements.

For methodological rationale and reading constraints, see:
- `docs/analysis_explanations/`
- `docs/Contexts_explanations/CONTEXT_SCHEMA_GUIDE.md`

---

## Scope of This Document

This document explains:

- where official context files are located,
- how they are loaded by the report generator,
- how they are matched to analysis results,
- how reference statuses (A / B / C) affect report structure,
- what happens when contextual information is missing,
- the required structure of official context YAML files.

It does **not**:
- define reference values,
- justify reference ranges,
- describe how measurements should be interpreted.

---

## Role of an Official Context

An official context:
- defines reference information for **one analysis family**,
- is maintained by the project,
- may contain multiple reference statuses (A / B / C),
- is used only for **presentation and comparison** in reports.

It never:
- modifies measurements,
- classifies signals,
- assigns likelihoods or decisions.

---

## File Location and Naming

Official contexts are stored in a dedicated directory, typically:

```
Analysis_Workspace/02_contexts/Official/
```

The directory path is provided explicitly to the report generator.

Each context file corresponds to exactly one analysis family and must be named:

```
context_<family>.yaml
```

The `<family>` identifier must match exactly the family name used in:
- the analysis code,
- the results JSON structure.

No discovery or fallback mechanism is applied.

---

## Context File Structure (Overview)

Each official context file:

- declares exactly one analysis family,
- lists methods belonging to that family,
- lists scalar metrics produced by each method,
- assigns a reference status to each metric.

The full normative schema is defined in:

```
docs/Contexts_explanations/CONTEXT_SCHEMA_GUIDE.md
```

This document does not redefine that schema, but summarizes its structure below.

---

## High-Level YAML Structure

```yaml
family: <family_name>

methods:
  <method_name>:
    metrics:
      <metric_name>:
        reference:
          status: A | B | C
          typical_range: [min, max]   # status A only
        notes:
          - ...
```

---

## Matching Logic

Contextual references are matched using **exact identifiers**.

The matching hierarchy is:

```
family → method → metric
```

Rules:

- A context entry must match an existing metric exactly.
- No metric may be introduced by a context file.
- Metrics present in results but absent from the context are reported explicitly.
- No name normalization or inference is performed.

---

## Reference Status Handling

Each metric context entry declares a reference status:

### Status A — Reference zone available
- A numeric `typical_range` is read.
- Numeric values are positioned relative to that range
  (below / within / above).
- Positioning is descriptive only.

### Status B — Context-dependent metric
- No numeric positioning is performed.
- Metrics are listed with explanatory notes.

### Status C — Descriptive metric
- Metrics are listed as descriptive outputs.
- No numeric comparison is attempted.

---

## Missing or Incomplete Context Coverage

The report generator explicitly reports:

- missing context files for a family,
- missing method entries,
- missing metric entries,
- invalid or incomplete reference definitions.

No metric is silently ignored.
No computation is affected.

---

## Relationship With Other Documentation

- This document describes **how official contextual references are applied**.
- `analysis_explanations/` documents explain **why interpretation is constrained**.
- `Contexts_explanations/CONTEXT_SCHEMA_GUIDE.md` defines **how context files must be written**.

These documents are complementary and non-overlapping.

---

End of document.
