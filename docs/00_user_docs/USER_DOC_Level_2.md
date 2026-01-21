# USER DOC — Level 2: How Your Choices Map to the System

This section explains **what really happens behind the scenes**, using simple words,
and how each step of the user journey maps to concrete artifacts produced by the system.

You do **not** need to understand or modify these artifacts to use the tool,
but knowing they exist helps you understand *why* we sometimes ask questions
and *why* results are reliable.

---

## 1. “You want to analyze an audio file”

**What you do**
- You select an audio file.

**What the system creates**
- The audio file itself is the single source of truth.
- Nothing is analyzed yet.

**Artifact**
- `audio.wav` (or any supported audio format)

---

## 2. “You describe what you want to look for”

**What you do**
- You explain, in simple terms, what kind of thing you suspect:
  - rhythms, pulses, silences
  - tones, frequencies, shifts
  - repetitions or anomalies

You are *not* choosing algorithms.
You are expressing an **intention**.

**What the system creates**
- A first, human-oriented description of your analysis idea.

**Artifact**
- `user_protocol.yaml`  
  (a declarative description of *what* you want to do, not *how* to do it)

---

## 3. “The system proposes a recipe”

**What you see**
- The tool proposes a coherent type of analysis.
- Some options appear mandatory, others optional.

**What the system does**
- It matches your intention against known analysis families.
- It selects which analyses are relevant and which are not.

**Artifact**
- `user_protocol.yaml` (updated or validated)

At this stage, the protocol can still be incomplete.
That is normal.

---

## 4. “We prepare everything that can be done automatically”

**What you don’t see**
- The system runs a *preflight* pass on the audio.
- Only neutral, objective properties are computed.

Examples:
- duration
- sample rate
- basic amplitude statistics
- robust noise or envelope statistics

No interpretation happens here.

**Artifacts**
- `audio_context.json`  
  (objective properties of the audio file)

Optionally:
- `derived_values.json`  
  (values that can be safely computed from the audio alone)

---

## 5. “We follow the known recipes”

**What this means**
- For every analysis parameter, the system knows whether it:
  - can be computed automatically,
  - follows a known convention,
  - or requires a decision from you.

These rules are fixed and documented.

**Artifact**
- `threshold_catalog.json`  
  (the global catalog of defensible rules)

This catalog is **not specific to your file**.
It is part of the system’s knowledge.

---

## 6. “The protocol is compiled for your audio”

**What happens**
- Your protocol is combined with:
  - the audio context,
  - the rule catalog,
  - and your explicit choices.

The system:
- fills in what can be computed,
- applies conventions,
- and clearly marks what is missing.

**Possible outcomes**
- fully ready protocol
- partially ready protocol (with clear questions)

**Artifacts**
- `compiled_protocol.yaml`
- `compile_report.md` or `compile_report.json`

Nothing is hidden.
Nothing is guessed.

---

## 7. “You answer questions, if needed”

**Why this happens**
- Some parameters cannot be deduced honestly from the audio alone.
- Only you can provide that information.

Examples:
- expected rhythm speed
- maximum pulse rate
- relevant frequency range

**What you do**
- You answer explicit, well-scoped questions.

**Artifact**
- `compiled_protocol.yaml` (updated and now complete)

---

## 8. “The analysis is executed”

**What happens**
- The compiled protocol is executed exactly as written.
- No parameters are changed during execution.

**Artifact**
- `results.json`

This file contains only **measurements**, not interpretations.

---

## 9. “The results are checked for structural validity”

**What happens**
- The system checks whether the results are structurally usable.
- It may conclude:
  - applicable
  - under-constrained
  - not applicable

This step does not assign meaning.

**Artifacts**
- `sap2_report.md`
- `applicability.json`

---

## 10. Why this structure matters

Because of this pipeline:

- parameters are never tuned to make something appear,
- missing assumptions are made explicit,
- and “there is nothing” is a trustworthy result.

You don’t need to understand all artifacts.
But they ensure that **the tool never lies to you**.

---

## Summary Table

| User concept | System artifact |
|-------------|-----------------|
| Audio file | `audio.wav` |
| What you want to do | `user_protocol.yaml` |
| Audio properties | `audio_context.json` |
| Known rules | `threshold_catalog.json` |
| Ready-to-run protocol | `compiled_protocol.yaml` |
| What was computed / missing | `compile_report.md` |
| Raw measurements | `results.json` |
| Structural validation | `sap2_report.md` |

---

If you want to go deeper, the technical documentation explains each artifact in detail.
This section exists so you never have to wonder *why* the system behaves the way it does.
