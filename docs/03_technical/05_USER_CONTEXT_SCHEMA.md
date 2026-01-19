# User Context Schema — YAML Specification

This document defines the **normative YAML schema** for *user-defined context files*
used by the Small Audio Tool (SAT).

It is a **schema reference**.
It defines what is structurally valid.
It does not describe loading mechanics or report behavior.

For context usage and report behavior, see:
- `03_USER_DEFINED_CONTEXTS.md`

---

## Scope

This schema applies to **user-defined context files** only.

User context files:
- are provided explicitly by the user,
- apply only during report generation,
- never affect analysis computation.

---

## File Naming and Location

A user context file:
- may have any filename
- must be provided explicitly via CLI
- example location:
  ```
  Analysis_Workspace/02_contexts/User_Defined/Radio_SSTV.yaml
  ```

No discovery or directory scanning is performed.

---

## Top-Level Structure

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

A single file may define **multiple families**.

---

## Field Definitions

### family (top-level key)
- Required
- Must match exactly a family present in `results.json`

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

#### reference.status
- Must be exactly: `USER`
- Any other value is invalid

#### reference.typical_user_range
- Required
- Exactly two numeric values: `[min, max]`
- Displayed as *user-provided range*

---

### notes
- Required
- List of descriptive strings
- Must contain at least one non-empty entry

---

## Validation Rules

- Unknown keys are ignored
- Missing required keys are reported
- Invalid entries never block report generation
- No fallback or inference is applied

---

## Summary

This schema defines the **structural contract** for user-defined context YAML files.
