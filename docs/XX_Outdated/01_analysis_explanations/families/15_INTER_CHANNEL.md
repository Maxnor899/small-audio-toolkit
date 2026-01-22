# Inter-Channel Analysis
## Similarity, Delay, and Phase Relationships Between Channels

This document describes the **inter-channel analysis family**.
These analyses examine relationships between channels (typically Left/Right) and derived channels (such as the difference channel `L−R`).

Inter-channel measurements are often extremely informative in stereo recordings,
but also require careful interpretation because many production and rendering processes create channel differences without any hidden intent.

---

## 1. What Inter-Channel Analyses Measure

Inter-channel analyses focus on:

- similarity between channels (correlation),
- relative delay or time offset,
- phase relationships and phase consistency,
- properties of derived channels (especially the difference channel).

They answer questions such as:
- *How similar are the two channels?*
- *Is one channel delayed relative to the other?*
- *Are phase relationships stable or drifting?*

They do **not** determine why a relationship exists.

---

## 2. Typical Uses in Signal Processing

In DSP practice, inter-channel analysis is used to:

- assess stereo coherence,
- detect misalignment or polarity inversion,
- estimate time delay of arrival (TDOA),
- study spatial audio rendering artifacts,
- analyze microphone array recordings.

They are widely applied in:
- audio engineering,
- acoustics and localization,
- communications (multi-channel signals),
- system diagnostics.

---

## 3. Inter-Channel Metrics Used in This Project

This project includes inter-channel measurements such as:

- difference channel analysis (`L−R`),
- cross-correlation and lag estimation,
- phase difference and phase consistency,
- coherence-like similarity measures (depending on implementation).

These metrics quantify relationships between channels and do not interpret their origin.

---

## 4. How to Read “Commonly Observed Ranges” in Inter-Channel Metrics

Inter-channel metrics often have well-known bounds, but their interpretation is context-dependent.

As in other families:

**A. Established numeric bounds**  
E.g. correlation values in `[-1, 1]`, phase in `[-π, π]`.

**B. Contextual orders of magnitude**  
E.g. delays in milliseconds or samples, depending on recording setup and sampling rate.

**C. Distributional descriptors**  
E.g. stability of phase difference over time, best described via variance/persistence.

---

## 5. Difference Channel (`L−R`)

### What it measures

The difference channel is computed as:
- `D = L − R`

It emphasizes content that is **not shared** between left and right channels.

### Typical observations

A strong difference channel may indicate:
- stereo widening effects,
- spatialization or panning,
- reverb differences,
- phase differences or partial cancellations,
- independent content in one channel.

A weak difference channel may indicate:
- highly correlated channels,
- mono or near-mono content.

### Commonly observed ranges (Category B/C)

There is no universal “correct” amplitude for `L−R`.
Typical practice is comparative:

- compare RMS/energy of `L−R` to RMS/energy of `L` and `R`,
- compare spectral shape of `L−R` to `L`/`R`,
- compare stability across time segments.

Useful derived descriptors include:
- `ratio = RMS(L−R) / RMS((L+R)/2)`
- segment-wise variance of this ratio

These are descriptive and should not be treated as thresholds.

### Important limits

- Many legitimate stereo processes create large `L−R` energy.
- A strong `L−R` does not imply hidden content.
- A weak `L−R` does not imply absence of structure.

---

## 6. Cross-Correlation and Time Delay

### What it measures

Cross-correlation measures similarity between two signals as a function of time shift.
It can be used to estimate a relative delay (lag).

### Typical observations

- Peak near zero lag: aligned channels.
- Peak at non-zero lag: one channel appears delayed relative to the other.
- Broad peaks: similarity is weak or spread across time shifts.

### Commonly observed ranges (Category A/B)

**Bounds (established):**
- Normalized cross-correlation lies in **`[-1, +1]`**.

**Delay magnitudes (contextual):**
- In stereo microphone recordings, delays are often in the **sub-millisecond to few-millisecond** range.
- In post-processed audio (rendering, spatial effects), larger apparent lags can occur depending on effect design.

Always interpret delay in relation to:
- sampling rate (samples ↔ seconds),
- window length and segmentation,
- signal bandwidth (narrowband signals can yield ambiguous delays).

### Important limits

- Narrowband signals can produce multiple plausible correlation peaks (ambiguity).
- Delays can be produced by processing, not propagation.
- Correlation does not establish causality or intent.

---

## 7. Phase Difference

### What it measures

Phase difference describes how the phase of one channel relates to the other.
It may be estimated in the time domain (analytic signal) or frequency domain (phase spectrum).

### Typical observations

- Stable phase difference: consistent relationship between channels.
- Phase flips or instability: possible polarity changes, transients, or processing artifacts.
- Frequency-dependent phase difference: common in stereo filtering or spatialization.

### Commonly observed ranges (Category A/C)

**Bounds (established):**
- Phase is typically expressed in **`[-π, π]`** or **`[0, 2π]`**.

**Behavioral ranges:**
- The informative quantity is often phase difference **variance over time** or **consistency across frequency bins**, rather than absolute phase.

### Important limits

- Absolute phase is rarely meaningful without a defined reference.
- Phase estimates are noise-sensitive and parameter-dependent.
- Stable phase difference does not imply synchronization intent.

---

## 8. Coherence and Similarity Over Frequency (if applicable)

### What it measures

Some inter-channel metrics evaluate similarity as a function of frequency,
often referred to as coherence-like behavior.

### Typical observations

- High similarity at low frequencies, lower similarity at high frequencies (common in natural stereo recordings).
- Frequency bands with strong differences due to effects or independent content.

### Commonly observed ranges (Category A/B)

Coherence-like metrics are commonly bounded in **[0, 1]** when normalized,
but exact definitions vary by implementation.

Interpretation is most reliable through:
- comparison across frequency bands,
- stability across segments,
- cross-channel symmetry.

### Important limits

- Different definitions exist; numeric values may not be comparable across tools.
- Coherence can be biased by noise floors and windowing.

---

## 9. Common Misinterpretations

Common pitfalls in inter-channel analysis include:

- treating strong `L−R` content as “hidden signal” evidence,
- assuming a detected lag implies physical propagation delay,
- interpreting phase stability as synchronization intent,
- interpreting phase inversion as purposeful encoding.

Inter-channel relationships are descriptive properties that can result from many benign causes.

---

## 10. When Inter-Channel Analyses Are Insufficient

Inter-channel analyses alone cannot:

- determine whether channel differences are intentional,
- distinguish production effects from physical recording geometry,
- infer meaning from spatial structure.

They are most informative when combined with:
- time–frequency analysis (to localize differences in frequency),
- modulation analysis (to examine slow variation),
- temporal segmentation (to compare stability across time).

---

## 11. References (selected)

Textbooks / foundational concepts:
- Oppenheim & Schafer — *Signals and Systems*
- Lyons — *Understanding Digital Signal Processing*
- Kuttruff — *Room Acoustics* (for time delay / spatial context)

Online technical references:
```text
Cross-correlation (SciPy)
https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.correlate.html

Phase and analytic signal (CCRMA / Julius O. Smith)
https://ccrma.stanford.edu/~jos/sasp/Analytic_Signals_Hilbert_Transform.html
```

These references provide methodological grounding, not interpretative guidance.
