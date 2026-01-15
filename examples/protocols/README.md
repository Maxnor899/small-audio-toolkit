# Example Analysis Protocols

This directory contains **example analysis protocols** for the Small Audio Tool.

Each YAML file defines a **self-contained observation protocol**:
it specifies *what is measured*, *on which channels*, and *with which parameters*.

These files are intended for:
- testing analysis coverage by category,
- validating visualizations,
- demonstrating reproducible observation setups,
- onboarding and experimentation.

They are **not hypotheses**, **not scenarios**, and **not interpretations**.

---

## What Is a Protocol?

In this project, a protocol is:

- a declarative description of **what to observe**,
- fully explicit and reproducible,
- independent from interpretation,
- external to the analysis code.

Changing a protocol changes the **question asked of the signal**,
not the meaning of the results.

---

## Structure

Each protocol typically defines:

- analyzed channels (`channels.analyze`),
- enabled analysis families and methods,
- method-specific parameters,
- visualization settings,
- output options.

Protocols are expected to be versioned and shareable.

---

## Usage

Example:

```bash
python run_analysis.py input_audio.wav output_directory/ examples/protocols/03_time_frequency.yaml
```

Each run produces:
- raw measurement results (`results.json`),
- optional visualizations,
- optional reports (when post-processing is applied).

---

## Relationship With Contexts

Protocols define **what is measured**.

Context files (see `examples/contexts/`) define **how measurements may be positioned**
relative to external reference ranges.

The two are intentionally separate.

---

## Important Notes

- Protocols never contain thresholds or decisions.
- Protocols never imply intent or meaning.
- Results are valid regardless of whether a context is applied.

Interpretation always happens **outside the tool**.

---

These example protocols are provided as **reference implementations**.
They may be adapted, combined, or extended as needed.
