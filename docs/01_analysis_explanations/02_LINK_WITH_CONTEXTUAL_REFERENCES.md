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

## 4. External context Reference Files

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

### 4a. Official Contextual References

Official contextual references are **maintained by the project** and are intended to provide a  
**generic analytical frame of reference**.

They describe value ranges and qualitative statuses that are commonly observed in signal
processing practice, as documented in standard literature or widely accepted empirical use.
Their purpose is to offer **orientation grounded in shared knowledge**, not to define norms
or decision criteria.

Official contextual references are:
- scoped to specific analytical families and metrics,
- independent from any particular signal instance,
- intended to remain valid across a broad range of signal types and acquisition conditions.

They are used to support **neutral positioning of measured values** relative to commonly
encountered ranges, without asserting correctness, abnormality, or intent.

Their presence in a report does not imply validation, detection, or classification.

---

### 4b. User-Provided Contextual References

User-provided contextual references are **explicitly supplied by the user** and reflect a  
**situated or experiential frame of reference**.

They may be based on prior observations, domain-specific knowledge, experimental conditions,
or assumptions about the nature of the analyzed signal. The tool does not verify, validate,
or assess the correctness of these references.

A user-provided context represents a **hypothesis of reading**, not an authority.

User-provided contextual references:
- apply only within the user-defined analytical frame,
- may differ from, complement, or contradict official contextual references,
- carry no intrinsic priority or validation status.

When both official and user-provided contexts are present, they are presented **side by side**
as descriptive information. The tool does not resolve discrepancies, assign preference, or
derive conclusions from their agreement or divergence.

Responsibility for interpreting user-provided contextual references rests entirely with the
user.


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
