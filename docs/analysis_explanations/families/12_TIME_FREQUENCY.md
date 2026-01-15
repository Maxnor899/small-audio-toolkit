# Time–Frequency Analysis
## Joint Time–Frequency Structure and Stability

This document describes the **time–frequency analysis family**.
Time–frequency analyses examine how spectral content **evolves over time**, combining aspects of both temporal and spectral domains.

They are essential for understanding non-stationary signals, but also require careful interpretation due to resolution trade-offs.

---

## 1. What Time–Frequency Analyses Measure

Time–frequency analyses focus on:

- how frequency content changes over time,
- stability or variability of spectral components,
- intermittent vs. persistent structures,
- localized events in both time and frequency.

They answer questions such as:
- *When does a given frequency component appear or disappear?*
- *Is spectral content stable or transient over time?*

They do **not** directly encode intent, meaning, or causality.

---

## 2. Typical Uses in Signal Processing

In classical DSP, time–frequency analyses are used to:

- analyze non-stationary signals,
- track time-varying frequencies,
- study transient spectral events,
- visualize modulation and chirps.

They are widely applied in:
- audio and music analysis,
- speech processing,
- bioacoustics,
- radar and sonar,
- mechanical diagnostics.

---

## 3. Time–Frequency Metrics Used in This Project

This project includes several time–frequency measurements, such as:

- Short-Time Fourier Transform (STFT),
- spectrogram representations,
- frequency band stability measures,
- time-localized energy distributions.

These metrics describe **how spectral structure behaves over time**.

---

## 4. How to Read “Commonly Observed Ranges” in Time–Frequency Metrics

Time–frequency metrics are subject to explicit **resolution trade-offs**.

As in other families, three categories apply:

**A. Established numeric bounds**  
Metrics with clear mathematical limits (e.g. normalized measures).

**B. Contextual orders of magnitude**  
Metrics expressed in physical units (time, frequency) whose ranges depend on resolution choices.

**C. Distributional descriptors**  
Metrics best understood through stability, persistence, or variability rather than absolute values.

Reported values always depend on:
- window length,
- hop size,
- frequency resolution,
- preprocessing.

---

## 5. Short-Time Fourier Transform (STFT)

### What it measures

STFT computes a sequence of local spectra by applying the Fourier transform
over sliding time windows.

It provides a **time-resolved view of frequency content**.

### Typical observations

STFT representations may show:
- stable horizontal bands for steady tones,
- diagonal patterns for chirps or sweeps,
- intermittent bursts for transient events,
- broadband patterns for noise-like signals.

### Commonly observed ranges (Category B)

STFT frequency bins span:
- from 0 Hz to the Nyquist frequency.

Time resolution typically ranges from:
- a few milliseconds (short windows),
- to tens or hundreds of milliseconds (longer windows),

depending on window size and sampling rate.

These are **design choices**, not signal properties.

### Important limits

- Increasing time resolution reduces frequency resolution, and vice versa.
- STFT does not represent instantaneous frequency exactly.
- Apparent patterns may depend on windowing choices.

---

## 6. Spectrogram Representations

### What it measures

A spectrogram is a visualization of STFT magnitude (or power) over time.

### Typical observations

Spectrograms may reveal:
- stable frequency bands,
- intermittent spectral components,
- repeating spectral motifs,
- abrupt spectral transitions.

### Commonly observed ranges (Category C)

Spectrogram values are typically normalized or scaled (e.g. dB).
Absolute magnitudes depend on preprocessing and scaling choices.

Interpretation relies on:
- relative contrast,
- persistence of structures,
- comparison across time or channels.

### Important limits

- Visual contrast can exaggerate minor components.
- Color scaling affects perception.
- Visual inspection is subjective.

---

## 7. Frequency Band Stability

### What it measures

Band stability metrics quantify **how consistently energy remains within predefined frequency bands over time**.

### Typical observations

Stable bands may indicate:
- sustained tonal components,
- persistent resonances,
- steady noise bands.

Unstable bands may indicate:
- transients,
- sweeping components,
- intermittent activity.

### Commonly observed ranges (Category B/C)

Stability measures often take the form of:
- proportions of time with significant energy,
- variance of band energy over time.

Typical values depend on:
- band definitions,
- thresholding strategy,
- signal duration.

Rather than absolute values, **comparative stability across bands** is usually more informative.

### Important limits

- Stability depends on band selection.
- Narrow bands may miss drifting components.
- Broad bands may hide structure.

---

## 8. Time–Frequency Energy Distribution

### What it measures

These metrics describe **how signal energy is distributed jointly in time and frequency**.

### Typical observations

Energy distributions may show:
- concentration in specific regions,
- sparse vs. dense occupancy,
- repeating energy patterns.

### Commonly observed ranges (Category C)

Energy distributions are best interpreted via:
- relative concentration,
- sparsity vs. spread,
- comparison across segments or channels.

Absolute numeric ranges are rarely meaningful.

### Important limits

- Results depend on resolution parameters.
- Sparse patterns do not imply encoding.
- Dense patterns do not imply randomness.

---

## 9. Common Misinterpretations

Common pitfalls in time–frequency analysis include:

- treating visual patterns as intentional structures,
- assuming stability implies design,
- inferring modulation schemes from spectrogram shapes.

Time–frequency structure is descriptive, not explanatory.

---

## 10. When Time–Frequency Analyses Are Insufficient

Time–frequency analyses alone cannot:

- fully characterize modulation mechanisms,
- determine semantic structure,
- replace temporal or spectral detail.

They are most informative when combined with:
- temporal analysis,
- spectral analysis,
- modulation analysis.

---

## 11. References (selected)

Textbooks:
- Cohen, *Time-Frequency Analysis*
- Boashash, *Time-Frequency Signal Analysis*
- Lyons, *Understanding Digital Signal Processing*

Online references:
```text
STFT overview (Wikipedia)
https://en.wikipedia.org/wiki/Short-time_Fourier_transform

Spectrogram fundamentals (NI)
https://www.ni.com/en/support/documentation/supplemental/06/spectrogram.html
```

These references describe analytical tools, not interpretative frameworks.
