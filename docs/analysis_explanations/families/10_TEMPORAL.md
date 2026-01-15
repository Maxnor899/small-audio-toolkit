# Temporal Analysis
## Time-Domain Structure and Regularity

This document describes the **temporal analysis family**.
Temporal analyses operate directly in the **time domain**, observing how a signal evolves sample by sample.

They are often the most intuitive analyses for non-specialists, but also among the easiest to over-interpret.
This document explains what these analyses measure, how “typical ranges” should be understood, and where the limits are.

---

## 1. What Temporal Analyses Measure

Temporal analyses focus on **time-domain structure**, including:

- amplitude variations over time,
- repetition and periodicity,
- impulsive or transient events,
- temporal regularity or irregularity.

They do not analyze frequency content explicitly.
They observe *when* things happen, not *at which frequency*.

---

## 2. Typical Uses in Signal Processing

In classical DSP, temporal analyses are used to:

- detect periodic patterns,
- identify transient events and onsets,
- measure event timing and regularity,
- characterize signal stationarity in time.

They are commonly applied in:
- audio and speech processing,
- vibration/condition monitoring,
- communications signals,
- system diagnostics.

---

## 3. Temporal Metrics Used in This Project

This project implements several temporal measurements, including:

- amplitude envelope,
- autocorrelation,
- pulse/transient detection,
- duration ratios between detected events.

Each metric captures a different aspect of temporal structure.

---

## 4. How to Read “Commonly Observed Ranges” in Temporal Metrics

Not all temporal metrics have stable, universal numeric ranges.

This document uses three levels of “range” information:

**A. Established numeric bounds / well-known magnitudes**  
Examples: normalized correlation values are in `[-1, 1]`; some typical peak magnitudes are widely discussed.

**B. Contextual orders of magnitude**  
Examples: event spacing in milliseconds, onset densities in events/second. These depend on signal class and detector parameters.

**C. Distribution/behavior descriptions (no stable numeric ranges)**  
Examples: envelope shapes or relative variability when absolute scales are dominated by normalization and preprocessing.

When numeric values are given, they are always:
- tied to a context,
- not used as decision thresholds,
- and paired with explicit caveats.

---

## 5. Amplitude Envelope

### What it measures

The amplitude envelope represents the **slow variation of signal amplitude (or energy proxy) over time**.
In many DSP settings, this is computed from the analytic signal (e.g., via a Hilbert transform) and then optionally smoothed.

### Typical observations

Envelopes commonly show:
- steady levels for sustained sounds,
- periodic rises and falls for amplitude-modulated signals,
- abrupt changes around transients/onsets.

### Commonly observed ranges (Category C)

Envelope values are typically **scale-dependent**:
- they change with normalization, gain, and preprocessing,
- absolute magnitudes are not comparable across unrelated recordings unless scaling is strictly controlled.

Because of that, envelope “ranges” are most reliably described through:
- relative variation over time,
- stability vs. sudden changes,
- comparison across channels or segments *within the same run*.

### Important limits

- Envelope shape does not directly encode frequency content.
- Similar envelopes can arise from very different signals.
- Envelope regularity does not imply intentional modulation.

---

## 6. Autocorrelation

### What it measures

Autocorrelation measures **similarity between a signal and a time-shifted version of itself**.
It is a standard tool to reveal periodicity and repeated patterns.

When normalized (common practice), autocorrelation values are bounded.

### Typical observations

Autocorrelation often shows:
- strong peaks at regular delays for periodic or quasi-periodic signals,
- low, rapidly decaying values for irregular/noise-like signals,
- multiple peaks when more than one periodic component exists.

### Commonly observed ranges (Category A + context)

**Numeric bounds (established):**
- Normalized autocorrelation values are in **`[-1, +1]`**.

**Common magnitudes (contextual, not universal):**
- For many noise-like or weakly correlated signals, non-zero-lag peaks tend to be small (often visually near 0 in normalized plots).
- For periodic components, non-zero-lag peaks can become clearly visible and may approach larger fractions of the zero-lag value, depending on periodic strength and windowing.

If you need a principled “noise baseline” framing: for ideal white noise, the theoretical autocorrelation is an impulse (all non-zero lags are zero in expectation), but finite samples will always show some non-zero fluctuation. In practice, this is one reason why autocorrelation should be read alongside configuration choices and sample length.

### Important limits

- Periodicity does not imply encoding, intent, or meaning.
- Physical systems, game audio loops, and synthesis engines often produce periodic patterns.
- Autocorrelation depends strongly on:
  - window size / segment length,
  - detrending and DC removal,
  - normalization choice,
  - preprocessing (e.g., clipping, compression).

---

## 7. Pulse and Transient Detection

### What it measures

Pulse/transient detection identifies **abrupt changes** (peaks, onsets, impacts) in the signal.
Depending on parameters, it may track:
- the number of detected events,
- their time positions,
- their spacing (inter-event intervals).

### Typical observations

Detected events may correspond to:
- percussive onsets,
- impacts or clicks,
- switching artifacts,
- repeated “tick-like” structures,
- sudden envelope changes.

### Commonly observed ranges (Category B: orders of magnitude)

Pulse metrics do not have universal ranges, but widely used DSP literature on onset/transient detection provides common **time scales** and **event-rate concepts**.

**Time scale (typical order of magnitude):**
- Inter-event intervals frequently fall in the **tens of milliseconds** (fast sequences) up to **hundreds of milliseconds** or more (slower event structures), depending on the signal class.

**Event density framing (conceptual):**
- Many analyses report *event density* in “events per second” as a useful descriptor (especially in music/audio onset research), but the absolute values depend on detector design and thresholding.

In this tool, pulse-related “ranges” should therefore be understood through:
- event density over time (sparse vs. dense),
- spacing stability (regular vs. variable),
- clustering (isolated vs. grouped events),
- comparisons across segments/channels using identical parameters.

### Important limits

- Pulse detection output depends strongly on parameter choices:
  - thresholding strategy,
  - minimum separation between events,
  - smoothing/windowing,
  - dynamic range handling.
- Not all detected pulses correspond to meaningful “events” in any semantic sense.
- Absence of detected pulses does not imply the signal is smooth (it may simply not match the detector’s sensitivity settings).

---

## 8. Duration Ratios

### What it measures

Duration ratios describe **relative timing relationships** between detected events.
Instead of absolute timing, ratios focus on proportional spacing patterns.

### Typical observations

Ratios may reveal:
- stable spacing (ratios clustering around 1),
- integer-like relationships (e.g., 2×, 3×) in rhythmic or cyclic structures,
- drifting ratios in irregular or changing patterns.

### Commonly observed ranges (Category B/C)

Duration ratios are not bounded to a small universal numeric interval (they depend on how ratios are defined and which events are included). However, typical behaviors include:

- **near-1 clustering** when events occur at roughly regular intervals,
- **multi-cluster patterns** when multiple time scales coexist (e.g., “fast” and “slow” event layers),
- **broad distributions** when timing is irregular or detection is unstable.

Where ratios are computed from inter-event intervals, their reliability depends directly on the quality and stability of the underlying event detection.

### Important limits

- Ratios inherit uncertainty from event detection and segmentation.
- Apparent simple ratios can arise by coincidence in short samples.
- Ratios alone do not define structure; they are descriptive summaries.

---

## 9. Common Misinterpretations

Common pitfalls when reading temporal analyses include:

- assuming periodicity implies design or encoding,
- treating envelope regularity as a modulation scheme,
- reading pulse detection as “semantic event detection” rather than a parameterized detector output,
- assuming that multiple temporal indicators automatically “confirm” a hypothesis.

Temporal structure is descriptive, not explanatory.

---

## 10. When Temporal Analyses Are Insufficient

Temporal analyses alone cannot:

- describe spectral content,
- identify modulation frequencies robustly,
- distinguish between different sources that share similar time-domain patterns.

They are most informative when combined with:
- spectral or time–frequency analyses,
- inter-channel analysis,
- information metrics.

---

## 11. References (selected)

Below are representative, widely used references and reputable technical resources for temporal analysis concepts.

Textbooks (general DSP foundations):
- Oppenheim & Schafer — *Signals and Systems*
- Rabiner & Schafer — *Theory and Applications of Digital Signal Processing*
- Lyons — *Understanding Digital Signal Processing*

Online / openly accessible technical resources (definitions and context):
```text
SciPy: signal envelope definition
https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.envelope.html

Onset/transient detection tutorial (IEEE)
https://iro.umontreal.ca/~pift6080/H09/documents/papers/bello_onset_tutorial.pdf

Normalized autocorrelation range [-1, 1] (technical reference)
https://www.ni.com/docs/en-US/bundle/diadem/page/genmaths/genmaths/calc_correlation.htm
```

These references provide methodological grounding, not decision rules.
