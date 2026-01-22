# USER_DOC_Level_2 — Understanding How SAT Is Used

## Purpose

This document is for users who may have already run SAT at least once and/or want to
**understand how the different artefacts relate to each other**.

It explains workflows and outputs conceptually, without requiring technical knowledge
of configuration files or internal code.

If you are new to SAT, start with **USER_GUIDE_QUICKSTART.md** and **USER_DOC_Level_1.md**.

---

## From intent to artefacts

Using SAT always follows the same logical chain:

1. A **human intent** (explore, compare, verify)
2. A **protocol** (what aspects of the signal are observed)
3. **Measurements** (objective observations)
4. **Results** (structured record)
5. **Reports** (human-readable views)

SAT never skips steps, and never reverses this order.

---

## The role of protocols (functional view)

From a user perspective, a protocol:
- defines *what is observed*,
- limits *what can be seen*,
- does not define meaning or relevance.

Changing a protocol changes the *nature of observations*,
not their interpretation.

A protocol does **not** make results more or less “true”.
It only changes perspective.

---

## Understanding the main artefacts

### results.json

This file is the factual record of everything SAT measured.
It contains:
- raw measurements,
- scalar metrics,
- error information when a measurement failed.

It is immutable and never interpreted by itself.

---

### Reports

SAT generates several reports, each with a specific role:

- **Measurement summary**  
  High-level overview of available measurements.

- **Methodology and reading guide**  
  Explains how results should be approached.

- **Contextual positioning (official)**  
  Positions some metrics against declared reference ranges.

- **Contextual positioning (user)**  
  Same positioning logic, but with user-provided references.

Reports help reading, not deciding.

---

## Contexts: reference, not authority

Contexts provide **reference frames**, not judgments.

They:
- define ranges,
- add documentation notes,
- may be incomplete.

A value outside a range is an observation,
not a conclusion.

---

## Typical advanced workflows

After an initial run, users often:

- apply the same protocol to multiple files,
- refine protocols to focus on specific aspects,
- introduce user-defined contexts,
- compare channel-specific observations,
- inspect consistency across segments.

All these steps refine observation, not certainty.

---

## What SAT deliberately leaves to you

SAT does not:
- rank signals,
- decide anomalies,
- validate hypotheses.

Human reasoning remains central.

---

## Where to go next

- **USER_DOC_Level_3.md** — conceptual and methodological foundations
- Functional documentation — deeper understanding of scopes, families, protocols
- Technical documentation — exact formats and guarantees (advanced)

---

## Final reminder

SAT is designed to support careful analysis.

If results raise questions rather than answers,
the tool is working as intended.
