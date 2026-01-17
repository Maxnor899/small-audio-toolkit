# Contextual References — Technical Description

This document describes the **technical mechanism** by which contextual references
are loaded and applied during report generation in the Small Audio Tool (SAT).

It is a **technical document**.
It does not justify the existence of contextual references, nor does it explain how results
should be interpreted.

For methodological rationale and reading constraints, see:
- `docs/analysis_explanations/`
- `docs/Contexts_explanations/CONTEXT_SCHEMA_GUIDE.md`

---

## Scope of This Document

This document explains:

- where contextual reference files are located,
- how they are loaded by the report generator,
- how they are matched to analysis results,
- how reference statuses (A / B / C) affect report structure,
- what happens when contextual information is missing.

It does **not**:
- define reference values,
- justify reference ranges,
- describe how measurements should be interpreted.

---

## Context Files

Contextual references are provided as **family-scoped YAML files**.

### File Location

Context files are expected to be located in a dedicated directory,
typically:

```
Analysis_examples/02_contexts/
```

The directory path is provided to the report generator as a parameter.

### File Naming

Each context file corresponds to exactly one analysis family and must follow
this naming convention:

```
context_<family>.yaml
```

The `<family>` identifier must match the family name used in:
- the analysis code,
- the results JSON structure.

---

## Context File Structure (Overview)

Each context file:

- declares exactly one analysis family,
- lists methods belonging to that family,
- lists scalar metrics produced by each method,
- assigns a reference status to each metric.

The full normative schema is defined in:

```
docs/Contexts_explanations/CONTEXT_SCHEMA_GUIDE.md
```

This document does not redefine that schema.

---

## Loading Mechanism

During report generation:

1. The report generator inspects `results.json`.
2. It extracts the list of analysis families present.
3. For each family:
   - it attempts to load `context_<family>.yaml` from the contexts directory,
   - failures are reported explicitly in the generated report.

No default or fallback context is applied.

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
- Metrics present in results but absent from the context are reported as such.

The generator performs no inference or name normalization.

---

## Reference Status Handling

Each metric context entry declares a reference status:

- **A** — metric admits a numeric reference zone,
- **B** — metric is context-dependent and non-zonable,
- **C** — metric is descriptive only.

The report generator uses this status mechanically:

### Status A
- A numeric `typical_range` is read.
- Numeric values are positioned relative to that range
  (below / within / above).
- Positioning is descriptive only.

### Status B
- No numeric positioning is performed.
- Metrics are listed with explanatory notes.

### Status C
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

---

## Relationship With Other Documentation

- This document describes **how** contextual references are applied.
- `analysis_explanations/` documents explain **why** interpretation is constrained.
- `Contexts_explanations/CONTEXT_SCHEMA_GUIDE.md` defines **how context files must be written**.

These documents are complementary and non-overlapping.

---

End of document.
