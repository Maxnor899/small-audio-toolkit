# Contextual References
## Using Comparative Markers Without Interpretation

This document explains **how contextual reference files are used** when generating reports.
It assumes that the reader has already read `00_README.md` and `01_METHODOLOGY.md`.

Its scope is intentionally narrow:
> it documents a **single mechanism** — contextual comparison — and nothing else.

---

## 1. Why Context Is Needed

Numerical measurements are precise but often difficult to assess in isolation.

For example:
- a correlation value,
- an entropy estimate,
- a modulation index,

has little meaning without knowing **where such values are commonly observed** in signal processing practice.

Contextual references exist to provide **orientation**, not conclusions.

In this tool, contextual references are implemented through explicit, family-scoped context files (context_<family>.yaml).
Each metric is assigned a reference status (A, B, or C), which determines whether it may be positioned relative to a numeric 
reference zone, listed as context-dependent, or presented as descriptive only.
This mechanism is used exclusively during report generation and never influences measurement or analysis execution, it is applied mechanically in the 
contextual positioning section of generated reports.

---

## 2. Why Binary Thresholds Are Explicitly Avoided

Traditional threshold-based logic (e.g. “if value > X then detected”) is avoided because it:

- collapses continuous measurements into binary outcomes,
- encodes implicit assumptions,
- increases false positives by construction,
- biases both tools and users toward confirmation.

Such logic is incompatible with a neutral measurement instrument.

---

## 3. Contextual Ranges Instead of Thresholds

This project uses **contextual ranges** rather than thresholds.

A contextual range:
- describes values commonly encountered in a given analytical context,
- is empirical, not normative,
- may vary depending on signal type and analysis scale.

Measured values are positioned relative to these ranges as:
- below typical range,
- within typical range,
- above typical range.

This positioning is **descriptive only**.

---

## 4. External Reference Files

Contextual references are stored in **external YAML files**, separate from:

- analysis implementations,
- analysis configuration,
- report-generation logic.

This separation ensures:
- transparency,
- explicit versioning,
- reproducibility,
- the ability to adapt references to different domains.

Changing a reference file changes **context**, not analytical behavior.

---

## 5. What a Reference Entry Represents

Each reference entry corresponds to:

- a specific measured metric,
- expressed in a defined unit,
- associated with a typical value range.

Reference entries do **not** correspond to:
- analyses as a whole,
- signals,
- hypotheses,
- or interpretations.

They describe measurements, not conclusions.

---

## 6. How References Are Used in Reports

During report generation, the tool may:

1. read a measured value,
2. retrieve the corresponding reference range,
3. determine the relative position of the value,
4. present this information in neutral language.

At no point does the report:
- classify the signal,
- infer intent,
- suggest meaning.

All comparisons remain explicitly non-decisional.

---

## 7. Controlled Vocabulary

To prevent interpretative drift, report text derived from contextual references
is restricted to neutral expressions such as:

- “measured value”
- “reference range”
- “relative position”
- “below / within / above typical range”

Evaluative or suggestive language is intentionally excluded.

---

## 8. Sources and Provenance

Contextual ranges should be grounded in:

- standard DSP textbooks,
- peer-reviewed publications,
- widely accepted empirical practice.

Where possible, reference files should indicate their sources.

These sources provide **context**, not authority.

---

## 9. Limits of Contextual References

Contextual references:

- are not universal,
- do not apply to all signal types,
- cannot replace expert judgment.

They are aids to reading, not analytical conclusions.

---

## 10. Relation to Other Documentation

This document should be read together with:

- `01_METHODOLOGY.md`, which defines the analytical framework,
- `03_OBSERVATION_LIMITS.md`, which explains interpretative boundaries,
- `families/*`, which document specific metrics and their typical behavior.

Understanding the role of contextual references is essential to reading reports responsibly.
