# Methodology
## How Measurements Are Produced and How They Should Be Read

This document describes the methodological foundations of the analysis tool.
It explains **how observations are produced**, **what they represent**, and **how they should (and should not) be interpreted**.

The tone is intentionally conservative and slightly pedagogical.
No prior expertise in digital signal processing (DSP) is required, but no scientific shortcuts are taken.

---

## 1. Purpose of This Document

The purpose of this document is to explain the **method**, not the results.

It is intended to:
- clarify the design choices behind the tool,
- explain the separation between measurement and interpretation,
- provide a stable conceptual framework for reading analysis outputs.

This document should be read **before** consulting detailed analysis descriptions or generated reports.

---

## 2. Fundamental Design Principles

The tool is built around a small number of explicit principles:

- **Measurements only**: the tool produces numerical observations.
- **No automated interpretation**: no labels, scores, or conclusions are generated.
- **Explicit choices**: all analytical behavior is driven by configuration.
- **Reproducibility**: the same input and configuration always produce the same output.

These principles are not technical constraints; they are **methodological choices**.

---

## 3. Measurements as the Only Output

All outputs produced by the tool are measurements.

A measurement is understood here as:
- a numerical value,
- computed from the signal,
- using a documented and deterministic method.

Examples include:
- amplitudes,
- frequencies,
- correlation values,
- entropy measures.

No measurement is ever promoted to:
- a classification,
- a detection,
- or an interpretation.

The tool does not answer questions such as:
- “Is this signal meaningful?”
- “Is this signal artificial?”

It only answers:
- “What was measured, and how?”

---

## 4. Independence of Analyses

Each analysis method represents an **independent point of view** on the signal.

There is:
- no ordering between analyses,
- no hierarchy,
- no logical chain connecting their outputs.

Analyses do **not** reinforce or validate each other automatically.

Any perceived convergence between multiple observations is a **human analytical construct**, not a property of the tool.

This design avoids hidden decision paths or implicit reasoning.

---

## 5. Role of protocol Files (YAML)

The behavior of the tool is defined by protocol files.

These files specify:
- which channels are analyzed,
- which analysis families are enabled,
- which methods are applied,
- at which temporal or spectral scales.

The configuration file acts as a **protocol of observation**.

Changing the configuration does not change the tool itself;
it changes the *questions being asked of the signal*.

---

## 6. Contextual References vs Thresholds

Raw measurements can be difficult to assess without context.

Rather than embedding decision thresholds, the tool relies on **external contextual references**.

These references:
- describe commonly observed value ranges,
- provide comparative context,
- do not encode decisions.

They are used to position measurements as:
- below,
- within,
- or above typical ranges.

They are **not** used to infer meaning or significance.

---

## 7. Interpretation Is Out of Scope

Interpretation begins when meaning, intent, or relevance is assigned to measurements.

This step is deliberately excluded from the tool.

The responsibility for interpretation lies entirely with the user,
who may bring domain knowledge, external information, or alternative hypotheses.

This separation preserves:
- objectivity,
- transparency,
- and analytical freedom.

---

## 8. Validity of Null Results

A common analytical bias is the expectation that “something must be found”.

This tool explicitly rejects that assumption.

A result where:
- measurements fall within common ranges,
- no strong structures appear,
- no notable deviations are observed,

is a **valid and meaningful outcome**.

---

## 9. Methodological Limits

The tool operates strictly at the signal level.

It cannot:
- infer semantics,
- validate hypotheses,
- prove intent,
- replace expert judgment.

No single measurement, and no combination of measurements,
can serve as definitive evidence of meaning or design.

These limits are structural and intentional.

---

## 10. How This Methodology Shapes the Documentation

All subsequent documentation follows from this methodology.

Documents describing analysis families:
- explain what is measured,
- describe typical uses in DSP,
- outline common value ranges,
- and state known limitations.

They do not prescribe interpretations.

Reading this document first is essential to avoid misusing or misreading the tool’s outputs.
