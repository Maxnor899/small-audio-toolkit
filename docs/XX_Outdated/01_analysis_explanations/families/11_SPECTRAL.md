# Spectral Analysis
## Frequency-Domain Structure and Distribution

This document describes the **spectral analysis family**.
Spectral analyses operate in the **frequency domain**, observing how signal energy is distributed across frequencies.

They are foundational in DSP and provide information that is complementary to temporal analysis.
As with all families, spectral metrics are descriptive and must not be treated as evidence of intent or meaning.

---

## 1. What Spectral Analyses Measure

Spectral analyses focus on:

- how signal energy is distributed over frequency,
- concentration vs. dispersion of spectral content,
- presence of dominant frequency components,
- harmonic vs. broadband structures.

They answer questions such as:
- *Where is the energy located in frequency?*
- *Is it concentrated or spread out?*

They do **not** describe temporal evolution directly.

---

## 2. Typical Uses in Signal Processing

In classical DSP, spectral analyses are used to:

- characterize sound timbre,
- identify dominant frequency components,
- distinguish tonal vs. noise-like signals,
- analyze resonance and filtering effects.

They are widely applied in:
- audio and music processing,
- speech analysis,
- vibration and mechanical diagnostics,
- communications and radar.

---

## 3. Spectral Metrics Used in This Project

This project includes several spectral measurements, such as:

- global Fourier spectrum (FFT),
- spectral peak detection,
- spectral centroid,
- spectral bandwidth,
- harmonic structure analysis,
- spectral flatness.

Each metric highlights a different aspect of frequency-domain structure.

---

## 4. How to Read “Commonly Observed Ranges” in Spectral Metrics

Spectral metrics fall into the same three categories used elsewhere:

**A. Established numeric bounds**  
Metrics with well-defined mathematical limits.

**B. Contextual orders of magnitude**  
Metrics whose values depend on signal type, bandwidth, and sampling rate.

**C. Distributional descriptors**  
Metrics best understood through relative comparison and shape of distributions.

When values are given, they are:
- reported with context,
- never used as thresholds,
- and accompanied by explicit limitations.

---

## 5. Global Spectrum (FFT)

### What it measures

The Fourier Transform represents the signal as a sum of sinusoidal components.
The global spectrum shows **average frequency content over the analyzed window**.

### Typical observations

FFT spectra may show:
- isolated peaks (tonal components),
- harmonic series,
- broadband or flat distributions,
- band-limited structures.

### Commonly observed ranges (Category B)

FFT magnitude values depend on:
- signal amplitude,
- windowing,
- normalization,
- FFT size.

As a result, FFT magnitudes are best interpreted through:
- relative peak prominence,
- comparison across channels or segments,
- spectral shape rather than absolute amplitude.

### Important limits

- FFT loses time localization.
- Short windows reduce frequency resolution.
- Spectral peaks do not imply oscillators or encoded carriers.

---

## 6. Spectral Peak Detection

### What it measures

Peak detection identifies **local maxima** in the frequency spectrum.

### Typical observations

Detected peaks may correspond to:
- fundamental frequencies,
- harmonics,
- resonances,
- synthesis artifacts.

### Commonly observed ranges (Category B)

Peak frequencies are expressed in hertz and span:
- from near 0 Hz up to the Nyquist frequency.

Peak counts and spacing depend on:
- peak prominence criteria,
- spectral resolution,
- noise floor.

Relative relationships between peaks (spacing, harmonicity) are often more informative than absolute counts.

### Important limits

- Peaks can arise from windowing or leakage.
- Multiple peaks do not imply modulation or encoding.
- Harmonic-looking structures may arise from non-harmonic processes.

---

## 7. Spectral Centroid

### What it measures

The spectral centroid represents the **center of mass of the spectrum**.
It is often associated with perceived “brightness” in audio.

### Typical observations

- Low centroid values indicate energy concentrated at low frequencies.
- Higher values indicate more high-frequency content.

### Commonly observed ranges (Category A/B)

**Bounds (established):**
- Centroid values lie between **0 Hz and the Nyquist frequency**.

**Contextual orders of magnitude:**
- Speech and many natural sounds tend to have centroids well below Nyquist.
- Broadband noise pushes centroids toward higher values.

Exact numeric values depend on bandwidth, sampling rate, and preprocessing.

### Important limits

- Centroid collapses complex spectra into a single number.
- Different spectra can share similar centroids.
- High centroid does not imply noise; low centroid does not imply order.

---

## 8. Spectral Bandwidth

### What it measures

Spectral bandwidth describes **how spread out** the spectral energy is around the centroid.

### Typical observations

- Narrow bandwidth for tonal or resonant signals.
- Wide bandwidth for noise-like or complex signals.

### Commonly observed ranges (Category B)

Bandwidth values depend on:
- signal bandwidth,
- sampling rate,
- centroid definition.

They are typically interpreted relative to:
- centroid value,
- full available frequency range.

### Important limits

- Bandwidth depends on centroid definition.
- It does not capture spectral shape details.
- Similar bandwidths can hide very different spectra.

---

## 9. Harmonic Structure Analysis

### What it measures

Harmonic analysis evaluates whether spectral peaks align with **integer multiples of a fundamental frequency**.

### Typical observations

- Clear harmonic series in voiced speech or musical tones.
- Weak or absent harmonicity in noise-like signals.

### Commonly observed ranges (Category B/C)

Harmonicity metrics often express:
- degree of alignment,
- strength of harmonic peaks relative to non-harmonic content.

Reported values depend strongly on:
- peak detection accuracy,
- frequency resolution,
- presence of inharmonic components.

### Important limits

- Harmonic structure does not imply musical intent.
- Some mechanical or synthetic systems produce harmonic spectra.
- Inharmonicity may arise from measurement artifacts.

---

## 10. Spectral Flatness

### What it measures

Spectral flatness quantifies how **noise-like** a spectrum is, comparing geometric and arithmetic means.

### Typical observations

- Values near 0 indicate peaky, tonal spectra.
- Values closer to 1 indicate flatter, noise-like spectra.

### Commonly observed ranges (Category A)

Spectral flatness is typically normalized to **[0, 1]**.

Contextual tendencies:
- Tonal signals: low flatness.
- Broadband noise: higher flatness.

Exact values depend on frequency resolution and preprocessing.

### Important limits

- Flatness is sensitive to noise floor estimation.
- Mixed signals may produce intermediate values.
- Flatness alone does not classify a signal.

---

## 11. Common Misinterpretations

Common pitfalls in spectral analysis include:

- assuming peaks imply carriers or encoded frequencies,
- interpreting harmonicity as intent or design,
- treating noise-like spectra as meaningless.

Spectral structure describes distribution, not purpose.

---

## 12. When Spectral Analyses Are Insufficient

Spectral analyses alone cannot:

- capture temporal variation,
- describe modulation dynamics,
- identify inter-channel relationships.

They are most informative when combined with:
- temporal analysis,
- time–frequency representations,
- modulation analysis.

---

## 13. References (selected)

Textbooks:
- Oppenheim & Schafer — *Signals and Systems*
- Lyons — *Understanding Digital Signal Processing*
- Smith, *The Scientist and Engineer’s Guide to Digital Signal Processing*

Online references:
```text
Spectral centroid and bandwidth (Librosa documentation)
https://librosa.org/doc/main/generated/librosa.feature.spectral_centroid.html

Spectral flatness definition
https://ccrma.stanford.edu/~jos/sasp/Spectral_Flatness_Measure.html

FFT fundamentals (NI)
https://www.ni.com/en/support/documentation/supplemental/06/fft-basics.html
```

These references provide methodological grounding, not interpretative guidance.


---

## 14. Spectral Rolloff

### What it measures

Spectral rolloff identifies the frequency below which a given proportion
(e.g. 85% or 95%) of the total spectral energy is contained.

It provides a compact descriptor of how energy accumulates across frequency.

### Typical observations

- Low rolloff values indicate energy concentrated at low frequencies.
- Higher rolloff values indicate significant high-frequency content.

### Commonly observed ranges (Category A/B)

**Bounds (established):**
- Rolloff frequency lies between **0 Hz and the Nyquist frequency**.

Exact values depend on:
- chosen rolloff percentage,
- spectral resolution,
- signal bandwidth.

### Important limits

- Rolloff collapses spectral shape into a single percentile-based value.
- Different spectra can share identical rolloff frequencies.
- Rolloff does not indicate noise, structure, or intent.


---

## 15. Spectral Flux

### What it measures

Spectral flux quantifies **how much the spectrum changes between successive time frames**.
It is a measure of spectral dynamics rather than static structure.

### Typical observations

- Low flux for steady, slowly varying signals.
- Higher flux for transient-rich or rapidly changing signals.

### Commonly observed ranges (Category C)

Flux values are:
- non-negative,
- highly dependent on normalization and frame parameters.

They are best interpreted via:
- relative comparison over time,
- contrast between segments or channels.

### Important limits

- Flux depends strongly on STFT parameters.
- Absolute values are rarely comparable across configurations.
- High flux does not imply modulation or encoding.
