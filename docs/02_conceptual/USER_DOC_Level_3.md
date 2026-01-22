# USER_DOC_Level_3 — Conceptual and Methodological Foundations of SAT

## Purpose

This document explains **why SAT is designed the way it is**.
It is not a usage guide and not required to operate the tool.

Its role is to:
- make the design choices explicit,
- document methodological constraints,
- prevent misinterpretation of SAT’s scope and intent.

This document is intended for advanced users, reviewers, and contributors.

---

## 1. The problem SAT addresses

Audio analysis tools are often expected to:
- detect,
- classify,
- decide,
- or infer intent.

In many real-world situations, these expectations are **unjustified**.

Signals may be:
- complex,
- multi-causal,
- ambiguous,
- or deliberately structured.

SAT is designed for contexts where **observation must precede interpretation**.

---

## 2. Observation versus interpretation

SAT enforces a strict separation between:
- **measurement** (what is observed),
- **interpretation** (what meaning is assigned).

Measurements are:
- objective,
- repeatable,
- documented.

Interpretation is:
- contextual,
- hypothesis-driven,
- human.

SAT deliberately refuses to collapse these two layers.

---

## 3. Why SAT avoids automated conclusions

Automated conclusions require:
- strong priors,
- training data,
- implicit assumptions.

SAT avoids these because:
- priors may not apply,
- training data may be incomplete,
- assumptions may be hidden.

By refusing to conclude, SAT remains:
- auditable,
- falsifiable,
- adaptable.

---

## 4. Multiplicity of measurements

No single measurement can characterize a signal.

SAT therefore:
- uses many independent analyses,
- across multiple families,
- across multiple scopes.

Agreement across measurements is **informative**.
Disagreement is **also informative**.

SAT treats both as data.

---

## 5. Contexts as documentation, not authority

Contexts in SAT are:
- declarative,
- external,
- optional.

They provide:
- reference ranges,
- documentation notes.

They do not:
- validate signals,
- invalidate signals,
- impose meaning.

Contexts support reading, not judgment.

---

## 6. Protocols as observation strategies

Protocols define:
- what is observed,
- at which resolution,
- under which constraints.

They do not define:
- relevance,
- importance,
- truth.

Changing a protocol changes perspective,
not reality.

---

## 7. Uncertainty as a design outcome

SAT does not attempt to remove uncertainty.

Instead, it:
- makes uncertainty explicit,
- structures it,
- documents it.

Uncertainty is treated as a signal property,
not a failure.

---

## 8. Common misinterpretations SAT prevents

SAT is explicitly designed to prevent:
- threshold-driven verdicts,
- single-metric reasoning,
- black-box scoring,
- hidden heuristics.

If a question cannot be answered from measurements alone,
SAT will not pretend otherwise.

---

## 9. Scientific posture

SAT adopts a conservative scientific posture:
- measurements over models,
- transparency over performance,
- reproducibility over prediction.

This posture limits automation,
but maximizes trust and auditability.

---

## 10. Intended and unintended uses

SAT is intended for:
- exploratory analysis,
- comparative studies,
- hypothesis generation.

SAT is not intended for:
- certification,
- forensic proof,
- automated detection.

Using SAT outside its design intent
invalidates its guarantees.

---

## 11. Relationship to other documentation

- USER_GUIDE_QUICKSTART.md: practical usage
- USER_DOC_Level_1.md: user mindset
- USER_DOC_Level_2.md: workflows and artefacts
- Functional documentation: conceptual mechanics
- Technical documentation: exact guarantees

This document provides the **philosophical and methodological frame**
for all others.

---

## Final note

SAT does not aim to be clever.
It aims to be honest.

If this document feels restrictive,
that restriction is intentional.
