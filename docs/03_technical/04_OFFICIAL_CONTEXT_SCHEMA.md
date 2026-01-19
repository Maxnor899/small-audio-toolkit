# Official Context Schema — YAML Specification

This document defines the **normative YAML schema** for *official context files*
used by the Small Audio Tool (SAT).

It is a **schema reference**.
It defines what is structurally valid.
It does not describe loading mechanics or report behavior.

For context usage and mechanics, see:
- `02_OFFICIAL_CONTEXTS.md`

---

## Scope

This schema applies to **official context files** only.

Official context files:
- are maintained by the project,
- apply to exactly one analysis family,
- may define multiple reference statuses (A / B / C),
- never affect analysis computation.

---

## File Naming and Location

Each official context file:

- must be named:
  ```
  context_<family>.yaml
  ```
- must be stored in:
  ```
  Analysis_Workspace/02_contexts/Official/
  ```

The `<family>` identifier must match the analysis family name exactly.

---

## Top-Level Structure

```yaml
family: <family_name>

methods:
  <method_name>:
    metrics:
      <metric_name>:
        reference:
          status: A | B | C
          typical_range: [min, max]   # required for status A
        notes:
          - ...
```

---

## Field Definitions

### family
- Required
- String
- Must match exactly one analysis family

---

### methods
- Required
- Mapping of method identifiers

---

### metrics
- Required
- Mapping of metric identifiers

---

### reference
- Required
- Defines how the metric is contextualized

#### reference.status
Allowed values:
- `A` — metric has a stable numeric reference zone
- `B` — metric is context-dependent
- `C` — metric is descriptive only

#### reference.typical_range
- Required if `status: A`
- Forbidden for `status: B` and `status: C`
- Exactly two numeric values: `[min, max]`

---

### notes
- Optional
- List of descriptive strings
- No semantic interpretation is applied

---

## Validation Rules

- Unknown keys are ignored
- Missing required keys invalidate the entry
- Invalid entries are reported during report generation
- No fallback or inference is applied

---

## Summary

This schema defines the **structural contract** for official context YAML files.
