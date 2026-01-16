# Example Analysis Protocols

This directory contains **reference analysis protocols** for the Small Audio Tool (SAT).

In SAT, a protocol is not a preset, not a scenario, and not a hypothesis.
It is a **formal observation contract** that defines *what is measured*,
*how it is measured*, and *on which analytical axes*.

All protocols in this directory are:
- explicit
- reproducible
- interpretation-free

They differ only by **scope and intent of observation**.

---

## Directory Structure

```
examples/protocols/
├── Baseline/
├── Focused/
├── Experimental/
└── README.md
```

Each subdirectory corresponds to a **distinct methodological role**.

---

## Baseline/

The `Baseline/` directory contains **reference protocols** designed to provide
**maximal analytical coverage with minimal assumptions**.

Baseline protocols aim to:
- observe all major degrees of freedom of an audio signal,
- cover all analysis families at least once,
- provide a neutral starting point when no hypothesis exists.

They are typically used:
- for first-pass exploration of unknown signals,
- as a shared reference for comparison,
- to validate or calibrate more specialized protocols.

Baseline protocols are **not defaults** and are **not optimized**.
They are intentionally exhaustive rather than selective.

Each baseline protocol is usually paired with:
- a dedicated README explaining its intent,
- an optional contextual reference file.

---

## Focused/

The `Focused/` directory contains **specialized observation protocols**.

Focused protocols deliberately:
- restrict analytical scope,
- emphasize specific families, scales, or relationships,
- leave certain degrees of freedom unobserved on purpose.

They are used when:
- a hypothesis has been formulated,
- a structure was suggested by a baseline pass,
- computational cost must be reduced,
- a specific analytical question is being explored.

A focused protocol should always be readable as:
> “This protocol observes *this* and explicitly ignores *that*.”

---

## Experimental/

The `Experimental/` directory contains **exploratory or provisional protocols**.

These protocols may:
- test unusual parameter ranges,
- explore edge cases,
- support development or visualization validation,
- experiment with new analysis combinations.

They are not guaranteed to be:
- stable,
- optimal,
- or methodologically complete.

Experimental protocols may evolve, be replaced, or be removed.
They should not be used as references without critical review.

---

## What a Protocol Is (and Is Not)

A protocol in SAT:

- defines *what to observe*, not *what to conclude*
- never embeds thresholds or decisions
- never implies intent, meaning, or anomaly
- does not classify signals
- does not validate hypotheses

Changing a protocol changes the **question asked of the signal**,
not the interpretation of the results.

---

## Relationship With Context Files

Protocols define **measurements**.

Context files (when used) define **comparative reference ranges**
that help position numerical values during report generation.

- Protocols affect computation.
- Contexts affect presentation only.
- The two are strictly independent.

---

## Usage

Example using a baseline protocol **with its associated context file**:

```bash
python run_analysis.py input_audio.wav \
  --config examples/protocols/Baseline/protocol_baseline_full.yaml \
  --context examples/protocols/Baseline/context_baseline_general_audio.yaml \
  --output output_dir/
```

Each execution produces:
- raw numerical measurements,
- optional visualizations,
- an exact copy of the protocol used,
- an optional context-aware report (when report generation is applied).

Interpretation always occurs **outside the tool**.

---

## Final Note

These protocols are provided as **methodological references**.

They are meant to be:
- read,
- questioned,
- adapted,
- and extended.

They are not authoritative answers — only carefully defined ways of looking.
