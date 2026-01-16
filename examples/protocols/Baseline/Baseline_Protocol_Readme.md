# Baseline Protocol

## Purpose

The **Baseline Protocol** defines a **reference observation setup** for the
Small Audio Tool (SAT).

Its role is deliberately limited and explicit:

> **Ensure that all major degrees of freedom of an audio signal are observed at least once, without prior assumptions.**

This protocol is intended for **initial exploration**, when:
- the signal is unknown or poorly characterized,
- no hypothesis has yet been formulated,
- a neutral and exhaustive first analytical pass is required.

It is not designed to be optimal, fast, or selective.

---

## What This Protocol Is

The Baseline Protocol is:

- a **coverage protocol**, not a detection protocol
- a **starting point**, not a conclusion
- a **shared reference**, not a universal solution
- a **neutral observation grid**, not an analytical opinion

It defines *what is measured*, never *what should be found*.

---

## What This Protocol Is Not

The Baseline Protocol does **not**:

- detect messages, codes, or structures
- infer intent, meaning, or artificiality
- classify signals (natural, artificial, encoded, etc.)
- optimize parameters for a specific signal type
- privilege one analytical family over another

Running this protocol does **not** imply that
“something interesting must appear”.

A result showing no notable structure is a **valid and expected outcome**.

---

## Design Principles

### 1. Orthogonality of Analyses

Each analysis family observes the signal from an **independent projection**:

- temporal analyses observe repetition and event structure
- spectral analyses observe global frequency constraints
- time–frequency analyses provide exploratory localization
- modulation analyses observe hidden dynamics
- information analyses measure freedom vs redundancy
- inter-channel analyses observe relational structure

No analysis depends on the output of another.
No hierarchy exists between families.

Any perceived convergence is a **human interpretative act**, not a property of the protocol.

---

### 2. Explicit Coverage of Degrees of Freedom

For each analytical family, the protocol explicitly covers its essential axes:

- **Temporal**: multiple time scales (slow / intermediate / event-level)
- **Spectral**: global structure, discrete components, and descriptors
- **Time–Frequency**: localization and stability across predefined bands
- **Modulation**: amplitude, frequency, and phase dynamics
- **Information**: global and local measures of order and redundancy
- **Inter-channel**: similarity, opposition, delay, and phase relations

Nothing is left implicit or assumed.

---

### 3. No Embedded Interpretation

The protocol contains:

- no thresholds implying detection
- no semantic labels
- no decision rules
- no weighting of results

All numerical outputs are **measurements only**.

Interpretation, hypothesis building, and relevance assessment
are entirely outside the scope of SAT.

---

## Role of Time–Frequency Analysis

Time–frequency representations (STFT, band stability) play a **cartographic role**.

They:
- help locate when and where structures may exist,
- guide human attention,
- do not serve as a computational foundation for other analyses.

They are **exploratory**, not central or authoritative.

---

## Relationship to Contextual Reference Files

This protocol is typically paired with a **contextual reference file**.

- The protocol defines *what is measured*.
- The context defines *how values may be positioned relative to typical ranges*.

Contextual references:
- are external to the analysis,
- never influence computation,
- provide comparative orientation only,
- never imply interpretation or anomaly.

Changing the context changes **perspective**, not results.

---

## When to Use the Baseline Protocol

Use this protocol when:

- starting analysis on a new or unknown signal
- establishing a neutral analytical baseline
- comparing multiple signals under identical conditions
- validating or calibrating more specialized protocols

It is often followed by:
- narrower, hypothesis-driven protocols
- zoomed analyses at specific scales
- targeted explorations informed by human inspection

---

## When *Not* to Use It

Avoid using the Baseline Protocol when:

- computational efficiency is critical
- the signal type is already well-characterized
- a precise analytical question is already defined

In those cases, a **specialized protocol** is more appropriate.

---

## Summary

The Baseline Protocol is an **instrument calibration step**.

It does not answer questions.
It ensures that meaningful questions can be asked later,
with confidence that major analytical dimensions were not ignored.

> Measurement first.  
> Interpretation later.  
> Never the other way around.
