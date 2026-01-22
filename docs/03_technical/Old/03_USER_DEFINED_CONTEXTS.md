# User Context YAML — Technical Description

This document describes the **user-defined context YAML file** used by the Small Audio Tool (SAT)
to generate the *user contextual positioning report* (report 04).

It is a **technical document**.
It explains how user contexts are structured, loaded, and applied during report generation.
It does not justify reference values and does not interpret measurements.

---

## Scope of This Document

This document explains:

- the role of a user context,
- how a user context file is provided to the report generator,
- how it is matched against analysis results,
- how user reference ranges are applied,
- how missing or invalid entries are reported.

It does **not**:
- affect analysis computation,
- classify or validate signals,
- introduce reference values automatically.

---

## Role of a User Context

A user context:

- is explicitly provided by the user,
- applies only at report generation time,
- defines **user-provided reference ranges**,
- allows comparison of measured values against domain-specific knowledge.

It never:
- modifies measurements,
- influences analysis execution,
- assigns meaning or likelihood to results.

---

## File Usage and Invocation

A user context is provided explicitly via the command line:

```
--user-context PATH.yaml
```

Example:

```
Analysis_Workspace/02_contexts/User_Defined/Radio_SSTV.yaml
```

Only one user context file is used per report generation.
There is no discovery, scanning, or fallback mechanism.

---

## Context File Structure (Overview)

A user context file may cover **one or more analysis families**.
It mirrors the result hierarchy and uses exact identifiers.

High-level structure:

```yaml
<family_name>:
  methods:
    <method_name>:
      metrics:
        <metric_name>:
          reference:
            status: USER
            typical_user_range: [min, max]
          notes:
            - ...
```

---

## Matching Logic

User contexts are matched using **exact identifiers**.

The matching hierarchy is:

```
family → method → metric
```

Rules:

- Identifiers must match `results.json` exactly.
- No normalization or inference is performed.
- User contexts may not introduce new metrics.
- Metrics present in results but absent from the user context are explicitly reported.

---

## Reference Definition Rules

Each metric entry must define a `reference` section.

### reference.status

- Must be exactly: `USER`
- Any other value is considered invalid and reported as such.

### reference.typical_user_range

- Mandatory
- Exactly two numeric values: `[min, max]`
- Used for positional comparison:
  - below
  - within
  - above
- Displayed as **"user-provided range"** in the report.

---

## Notes Field

Each metric entry must define a `notes` field.

Rules:
- Must be a list
- Must contain at least one non-empty entry
- Free-text, descriptive only

Notes are displayed verbatim in the report.

---

## Behavior in Report 04

For each measured metric:

- If a valid user reference is present:
  - the measured value is positioned against `typical_user_range`,
  - the positioning is descriptive only.
- If the user context entry is missing or invalid:
  - the measured value is still displayed,
  - the report explicitly explains why no positioning was applied.

No metric is silently ignored.
No error prevents report generation.

---

## Invalid or Incomplete Context Entries

The report generator explicitly signals:

- missing family entries,
- missing method entries,
- missing metric entries,
- invalid reference definitions,
- missing required fields.

These situations are reported inline in report 04.
They never stop report generation.

---

## Relationship With Other Documentation

- This document describes **how user contexts are applied**.
- `01_official_context_yaml_merged.md` describes official contexts.
- `analysis_explanations/` documents explain interpretation constraints.

These documents are complementary and non-overlapping.

---

## Summary

A user context YAML file is a **strict, explicit, user-supplied reference description**
used solely to contextualize existing measurements.

It is:
- explicit,
- non-blocking,
- interpretation-free,
- and fully traceable.

---

End of document.
