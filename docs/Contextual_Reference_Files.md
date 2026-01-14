# Contextual Reference Files for Report Generation
## Externalizing Comparative Markers Without Interpretation

This document describes the rationale and methodology for using an **external reference file** to support the final section of the report generation process.

Its purpose is to provide **contextual comparison markers**, not interpretations, detections, or conclusions.

---

## 1. Motivation

The analysis engine produces **objective numerical measurements**.
The report generator summarizes these measurements for human inspection.

However, without context, raw values can be difficult to assess.

At the same time, embedding thresholds directly in code or report logic introduces bias and implicit interpretation.

The adopted solution is therefore:

> **an external, versioned reference file containing contextual ranges and comparison notes**.

---

## 2. What This File Is — and Is Not

### ✅ What it *is*

- A collection of **reference ranges** drawn from DSP practice or empirical observation
- A **contextual aid** for positioning measured values
- A **fully optional** input to the report generator
- A **transparent and traceable** component of the analysis pipeline

### ❌ What it is *not*

- A detection rule set
- A classification system
- A decision engine
- A source of automated conclusions

No value in this file should ever imply:
- “signal detected”
- “artificial content present”
- “hidden message found”

---

## 3. Design Principles

### 3.1 Externalization

All comparative references are kept **outside the codebase logic**:
- no hard-coded thresholds,
- no implicit defaults,
- no invisible assumptions.

This allows:
- independent revision,
- context-specific reference sets,
- full reproducibility.

---

### 3.2 Ranges, Not Thresholds

Each reference uses **ranges or distributions**, not binary cutoffs.

Example:
- ✔️ *Typical range: 3.5–5.5 bits/sample*
- ❌ *If entropy < 3.5 → structured signal*

The report generator may describe **relative position**, but never infer meaning.

---

### 3.3 Neutral Vocabulary

The report generator must restrict itself to neutral phrasing such as:
- “measured value”
- “reference range”
- “relative position”
- “within / below / above typical range”

Interpretative terms are explicitly avoided.

---

## 4. Example Reference File Structure

Example filename:
```
configs/references/general_audio.yaml
```

```yaml
version: "1.0"
scope: "general_audio"
description: "Contextual reference ranges for report generation. No interpretation."
sources:
  - "DSP literature, empirical observations"

references:

  information.shannon_entropy:
    unit: "bits/sample"
    typical_range: [3.5, 5.5]
    notes:
      - "Lower values are often observed in more repetitive signals."
      - "Higher values are common in broadband noise."
    display:
      compare: "range"
      emphasize_if_outside: true

  temporal.autocorrelation.max_peak_excluding_zero:
    unit: "normalized"
    typical_range: [0.0, 0.2]
    notes:
      - "Non-zero peaks increase when periodic components are present."
    display:
      compare: "range"
      emphasize_if_outside: true
```

---

## 5. How the Report Generator Uses This File

For each referenced metric:

1. Read the **measured value**
2. Read the **reference range**
3. Determine **relative position** (below / within / above)
4. Generate a **purely descriptive statement**

### Example Output

> Shannon entropy: 3.2 bits/sample.  
> Reference typical range: 3.5–5.5 bits/sample.  
> Relative position: below typical range.

No further inference is produced.

---

## 6. Versioning and Traceability

The reference file must be:

- versioned,
- copied to the output directory,
- recorded alongside `config_used.json`.

This ensures that every report can be traced back to:
- the audio input,
- the analysis configuration,
- the contextual reference set used.

---

## 7. Multiple Contexts

Different reference files may coexist, for example:

- `general_audio.yaml`
- `elite_dangerous.yaml`
- `speech_recordings.yaml`

Switching reference files changes **context**, not interpretation.

---

## 8. Summary

- Analysis computes measurements.
- YAML configuration defines observation protocols.
- Reference files provide contextual ranges.
- Reports describe relative positioning.
- Interpretation remains entirely human.

This separation preserves scientific rigor while keeping reports readable and informative.
