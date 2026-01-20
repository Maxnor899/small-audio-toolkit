# Modulation Analysis
## Amplitude, Frequency, and Phase Variations Over Time

This document describes the **modulation analysis family**.
Modulation analyses examine **slow variations imposed on a faster carrier or base signal**, such as changes in amplitude, frequency, or phase.

They are powerful tools, but also among the most frequently over-interpreted.
This document explains what modulation metrics measure, how typical values are reported in DSP practice, and where their limits lie.

---

## 1. What Modulation Analyses Measure

Modulation analyses focus on:

- slow variations of signal amplitude (AM),
- slow variations of instantaneous frequency (FM),
- evolution of phase relationships over time,
- coupling between carrier-scale and modulation-scale behavior.

They answer questions such as:
- *Does the signal exhibit slow, systematic variation?*
- *At what time scales do these variations occur?*

They do **not** identify encoding schemes, symbols, or intent.

---

## 2. Typical Uses in Signal Processing

In classical DSP, modulation analyses are used to:

- characterize amplitude and frequency modulation,
- analyze vibrato, tremolo, and beating,
- study communications signals,
- track system instabilities or drift.

They are applied in:
- audio and music analysis,
- speech processing,
- telecommunications,
- radar and sonar,
- mechanical diagnostics.

---

## 3. Modulation Metrics Used in This Project

This project implements several modulation-related measurements, including:

- amplitude modulation (AM) indicators,
- frequency modulation (FM) indicators,
- instantaneous phase analysis,
- modulation rate and stability measures.

Each metric captures **variation**, not structure at the carrier level.

---

## 4. How to Read “Commonly Observed Ranges” in Modulation Metrics

Modulation metrics are especially sensitive to **scale separation**.

As in other families, three categories apply:

**A. Established numeric bounds**  
Metrics with clear mathematical limits or normalized ranges.

**B. Contextual orders of magnitude**  
Metrics expressed in physical units (Hz, radians, seconds) whose values depend on signal class.

**C. Distributional descriptors**  
Metrics best understood through variability, stability, or spectral shape of modulation.

Reported values always depend on:
- carrier estimation method,
- filtering and smoothing,
- time resolution.

---

## 5. Amplitude Modulation (AM)

### What it measures

AM metrics describe **slow variations in signal amplitude** relative to faster carrier oscillations.

These are often computed from the amplitude envelope.

### Typical observations

AM-related measures may show:
- near-constant amplitude in steady signals,
- periodic amplitude variation (tremolo-like behavior),
- irregular amplitude fluctuations.

### Commonly observed ranges (Category B)

AM depth is often expressed as a **relative measure** (e.g. normalized variation).

In audio practice:
- weak AM corresponds to small relative envelope variation,
- strong AM corresponds to large, clearly periodic envelope swings.

Exact numeric values depend on normalization and envelope definition.
AM rates (modulation frequency) are commonly in the **sub-Hz to tens of Hz** range in audio contexts, depending on source.

### Important limits

- Envelope extraction strongly affects AM metrics.
- AM-like patterns can arise from beating between close frequencies.
- AM does not imply intentional modulation.

---

## 6. Frequency Modulation (FM)

### What it measures

FM metrics describe **variations of instantaneous frequency over time**.

They are often derived from phase derivatives or analytic signal representations.

### Typical observations

FM analysis may reveal:
- stable instantaneous frequency (no modulation),
- slow frequency drift,
- periodic frequency variation (vibrato-like behavior),
- irregular frequency fluctuations.

### Commonly observed ranges (Category B)

In many audio contexts:
- FM rates are typically in the **sub-Hz to several Hz** range for vibrato-like effects,
- larger excursions may occur in synthetic or mechanical signals.

Reported frequency deviation values depend on:
- carrier frequency,
- estimation method,
- smoothing parameters.

### Important limits

- Instantaneous frequency estimation is noise-sensitive.
- Phase unwrapping errors can dominate results.
- FM-like patterns can arise from interference or non-linearities.

---

## 7. Phase Analysis

### What it measures

Phase analysis tracks **the evolution of signal phase over time**.

This may include:
- phase continuity,
- phase drift,
- phase jumps,
- inter-channel phase relationships.

### Typical observations

Phase metrics may show:
- smooth linear phase progression for stable oscillations,
- irregular phase evolution for noise-like signals,
- abrupt changes due to transients or estimation artifacts.

### Commonly observed ranges (Category A/B)

**Bounds (established):**
- Phase values are typically wrapped to **[-π, π]** or **[0, 2π]**.

**Contextual behavior:**
- Meaningful interpretation usually concerns **phase change rates**, not absolute phase values.

### Important limits

- Absolute phase is rarely meaningful in isolation.
- Phase measures are highly sensitive to noise.
- Phase continuity does not imply synchronization or intent.

---

## 8. Modulation Stability

### What it measures

Stability metrics describe **how consistent modulation behavior is over time**.

### Typical observations

Stable modulation may show:
- narrow modulation spectra,
- consistent modulation rate,
- low variance of modulation parameters.

Unstable modulation may show:
- drifting rates,
- intermittent modulation,
- broad modulation spectra.

### Commonly observed ranges (Category C)

Stability is best interpreted through:
- variance measures,
- persistence over time,
- comparison across segments.

Absolute numeric values are rarely transferable across contexts.

### Important limits

- Stability depends on analysis window length.
- Short signals may falsely appear unstable.
- Stability does not imply deliberate control.

---

## 9. Common Misinterpretations

Common pitfalls in modulation analysis include:

- interpreting slow variation as intentional signaling,
- assuming vibrato-like patterns imply encoding,
- treating modulation presence as semantic structure.

Modulation describes **variation**, not message.

---

## 10. When Modulation Analyses Are Insufficient

Modulation analyses alone cannot:

- identify carrier identity,
- disambiguate beating from true modulation,
- establish communication schemes.

They are most informative when combined with:
- spectral analysis,
- time–frequency analysis,
- inter-channel analysis.

---

## 11. References (selected)

Textbooks:
- Lathi, *Modern Digital and Analog Communication Systems*
- Oppenheim & Schafer, *Signals and Systems*
- Lyons, *Understanding Digital Signal Processing*

Online references:
```text
Analytic signal and instantaneous frequency (Wikipedia)
https://en.wikipedia.org/wiki/Analytic_signal

AM and FM fundamentals (NI)
https://www.ni.com/en/support/documentation/supplemental/06/am-and-fm.html
```

These references provide methodological grounding, not interpretative guidance.


---

## 12. Chirp Detection (Frequency-Sweep Modulation)

### What it measures

Chirp detection examines **systematic frequency sweeps** over time,
which may be interpreted as a form of frequency modulation at a larger scale.

### Typical observations

- Continuous frequency increase or decrease.
- Localized sweep events.

### Commonly observed ranges (Category B/C)

Sweep rates and durations depend on:
- frequency range,
- time resolution,
- detection constraints.

They are not bounded to universal numeric ranges.

### Important limits

- Chirps can arise from synthesis, effects, or physical processes.
- Detection does not imply encoding or message structure.
