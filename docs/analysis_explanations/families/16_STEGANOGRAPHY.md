# Steganography-Oriented Analysis
## Residuals, Quantization Structure, and LSB Statistics (Non-Interpretative)

This document describes the **steganography-oriented analysis family** implemented in the tool.

Important note up front: these analyses are **not steganography detectors**.
They measure signal properties that are *sometimes* examined in steganography research and in forensic DSP,
but they do not establish intent, payload existence, or method.

---

## 1. What This Family Measures

These analyses focus on properties that often become visible when:

- a signal has undergone quantization or re-quantization,
- low-level bit patterns exhibit non-random behavior,
- filtering separates “main content” from “residual” components.

They answer questions such as:

- *Do the least significant bits (LSBs) look statistically balanced?*
- *Does quantization error behave like random noise or show structure?*
- *How much energy remains after removing a frequency band (residual analysis)?*

They do **not** answer:

- *Is there hidden data?*
- *What is the message?*
- *Was this intentionally encoded?*

---

## 2. Typical Uses in Signal Processing / Forensics

In DSP practice, related measurements are used to:

- characterize quantization and coding artifacts,
- inspect residual noise floors,
- evaluate randomness of low-level representations,
- compare channels or segments for consistency.

In steganography research, similar statistics may be used as *features*,
but they are rarely sufficient on their own and are highly context-dependent.

---

## 3. Methods Implemented in This Project

This project currently implements the following methods in this family:

- `lsb_analysis` — least significant bit statistics on a 16-bit quantized view of the samples
- `quantization_noise` — structure of quantization error (difference between float samples and re-quantized samples)
- `signal_residual` — energy/SNR comparison between signal and residual after filtering

These outputs are **measurements and descriptive summaries**.

---

## 4. How to Read “Commonly Observed Ranges” Here

As with other families, “ranges” fall into three categories:

**A. Established numeric bounds**  
E.g. probabilities in `[0, 1]`, correlation in `[-1, 1]`, flatness in `[0, 1]`.

**B. Contextual orders of magnitude**  
E.g. residual energy ratios or SNR values that depend on signal class and filtering parameters.

**C. Distributional descriptors**  
E.g. run-length distributions, which are best interpreted via shape and stability rather than a single number.

When numeric values are given, they are:
- tied to a model/context,
- not used as decision thresholds,
- paired with explicit caveats.

---

## 5. LSB Analysis (`lsb_analysis`)

### What it measures

This analysis converts samples to an `int16` representation and extracts the **least significant bit** (LSB) of each sample.
It reports, per channel:

- `lsb_mean`: proportion of 1s in the LSB stream
- `lsb_std`: standard deviation of the LSB stream
- `transition_rate`: fraction of adjacent samples whose LSB differs (0→1 or 1→0)
- `mean_zero_run`, `mean_one_run`: mean run lengths of consecutive 0s / 1s
- `samples_analyzed`: number of samples used

### Typical observations

- Balanced LSBs: roughly equal numbers of 0 and 1
- Biased LSBs: skew toward 0 or 1
- Transition patterns: fast alternation vs. long runs

### Commonly observed ranges (Category A/C)

**For a Bernoulli(0.5) “random” bitstream model (contextual baseline):**
- `lsb_mean` is expected near **0.5** (with finite-sample fluctuations)
- `lsb_std` is expected near **0.5** for a 0/1 variable with p=0.5
- `transition_rate` is expected near **0.5**
- mean run length (either bit) is expected near **2** samples (geometric distribution with p=0.5)

These are **baseline expectations** for an i.i.d. model. Real audio is not i.i.d.,
and LSB behavior depends on quantization, dithering, compression, and signal content.
Deviations from these baselines are therefore descriptive observations, not evidence of payloads.

### Important limits

- LSBs are affected by quantization method, dithering, and post-processing.
- Many legitimate processing chains change LSB statistics.
- “Random-looking” LSBs do not imply hidden data; “non-random” LSBs do not prove it either.

---

## 6. Quantization Noise Structure (`quantization_noise`)

### What it measures

This analysis computes quantization error by comparing:

- the original float samples, and
- the same samples after conversion to `int16` and back to float.

It reports, per channel:

- `noise_mean`: mean quantization error
- `noise_std`: standard deviation of quantization error
- `autocorr_peak`: a non-zero-lag autocorrelation peak measure on the quantization error
- `spectral_flatness`: flatness of the quantization-error spectrum
- `samples_analyzed`: number of samples used

### Typical observations

- Ideally, quantization error is approximately zero-mean and weakly correlated.
- Structured error may appear with:
  - deterministic rounding without dither,
  - strong tonal content,
  - low-amplitude signals near quantization steps,
  - repeated processing/encoding.

### Commonly observed ranges (Category A/B)

**Established bounds:**
- spectral flatness is in **[0, 1]**.
- normalized correlation measures are in **[-1, 1]** (when normalized).

**A common textbook model (uniform quantization error, no overload, sufficiently “busy” signal):**
- error is approximately uniform in **[-0.5, +0.5]** LSB units
- standard deviation is approximately **1/√12 ≈ 0.289 LSB**

Caveat: the tool’s reported `noise_std` depends on the chosen amplitude scaling and representation.
If you convert between “LSB units” and float units, you must account for the scaling factor used by the implementation.

### Important limits

- Quantization error models depend on assumptions (e.g., signal independence).
- Real codecs and processing pipelines can introduce correlated residuals unrelated to steganography.
- Flatness and autocorrelation are sensitive to analysis windowing and sample count.

---

## 7. Signal vs Residual Comparison (`signal_residual`)

### What it measures

This method filters the signal and compares the “main” component to a residual component,
reporting (per channel) quantities such as:

- `residual_rms`: RMS of the residual
- `signal_rms`: RMS of the filtered/remaining component (definition depends on implementation parameters)
- `residual_energy_ratio`: ratio of residual energy to signal energy
- `snr_db`: an SNR-like quantity derived from the ratio
- `samples_analyzed` and filter metadata (e.g., cutoff frequency)

### Typical observations

Residual analysis can reveal:
- whether a large fraction of energy sits outside a chosen band,
- whether residual energy is stable across channels or segments,
- whether filtering exposes structured artifacts (in conjunction with time–frequency plots).

### Commonly observed ranges (Category B)

Residual ratios and SNR values are inherently **context-dependent**:
- a lowpass cutoff at 1 kHz will behave very differently for speech vs. broadband noise vs. game audio effects.
- different filter types and orders change residual energy significantly.

Because of this, typical ranges are best defined:
- per signal family (speech, music, effects),
- and per filter configuration.

In practice, the most robust use is comparative:
- left vs right vs difference channel,
- segment-to-segment consistency,
- configuration-to-configuration sensitivity.

### Important limits

- Residual metrics are highly dependent on the filter design and cutoff frequency.
- A “high residual” is not inherently suspicious; it may be expected for wideband or noisy content.
- These metrics do not isolate “hidden” components; they isolate frequency regions defined by the filter.

---

## 8. Common Misinterpretations

Common pitfalls include:

- assuming biased LSBs imply embedded data,
- treating “structured” quantization noise as proof of steganography,
- assuming residual energy corresponds to “the hidden signal”.

These analyses provide measurements that may motivate further manual inspection
(e.g., plots, segmentation, cross-channel comparison), but do not justify conclusions.

---

## 9. When This Family Is Insufficient

These analyses alone cannot:

- detect or decode steganographic payloads,
- distinguish intentional embedding from normal processing artifacts,
- prove intent or communication.

They are most informative when combined with:
- time–frequency visualizations,
- inter-channel analysis,
- information-theoretic metrics,
- careful comparison across segments and configurations.

---

## 10. References (selected)

Textbooks / foundational DSP context:
- Lyons — *Understanding Digital Signal Processing*
- Oppenheim & Schafer — *Signals and Systems*
- Gray & Stockham — work on quantization/noise models (classical references)

Steganography / LSB context (intro-level but widely cited starting points):
- Fridrich — *Steganography in Digital Media: Principles, Algorithms, and Applications*

Online technical references (definitions and background):
```text
Spectral flatness measure (CCRMA / Julius O. Smith)
https://ccrma.stanford.edu/~jos/sasp/Spectral_Flatness_Measure.html

Quantization noise (intro, conceptual)
https://en.wikipedia.org/wiki/Quantization_(signal_processing)

LSB (conceptual)
https://en.wikipedia.org/wiki/Least_significant_bit
```

These references provide methodological grounding, not interpretative guidance.
