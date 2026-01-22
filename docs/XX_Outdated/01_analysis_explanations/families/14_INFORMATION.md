# Information Analysis
## Entropy, Redundancy, and Compressibility (Descriptive Only)

This document describes the **information analysis family**.
These analyses measure properties related to **uncertainty, redundancy, and apparent complexity** in audio signals.

Important note: information-theoretic metrics are often misunderstood.
They quantify statistical properties of representations; they do not measure semantic meaning or intent.

---

## 1. What Information Analyses Measure

Information analyses focus on:

- global and local entropy estimates,
- redundancy and predictability,
- compressibility as a proxy for repetition/structure,
- distributional balance of signal values (in chosen representations).

They answer questions such as:
- *How predictable is the signal (in a given representation)?*
- *Does it contain repeated patterns or high redundancy?*
- *Does complexity change over time?*

They do **not** answer:
- *Is there a message?*
- *Is the signal meaningful?*

---

## 2. Typical Uses in Signal Processing

In DSP practice, information metrics are used to:

- characterize texture (noise-like vs. structured),
- detect changes in statistical regime (segmentation),
- compare signals or channels quantitatively,
- evaluate coding/compression properties.

They are applied in:
- audio analysis,
- speech activity / change detection,
- anomaly detection as a generic statistical tool (context-dependent),
- compression and coding research.

---

## 3. Information Metrics Used in This Project

This project includes information-related measurements such as:

- Shannon entropy (global),
- local entropy over sliding windows,
- compression ratio (applied to a representation of the samples),
- distribution summaries that support entropy computation.

All outputs are descriptive and configuration-dependent.

---

## 4. How to Read “Commonly Observed Ranges” in Information Metrics

Information metrics depend strongly on:

- the chosen representation (raw samples, quantized samples, residuals),
- scaling and normalization,
- window size (for local metrics),
- sample count (estimation error).

As in other families:

**A. Established numeric bounds**  
E.g. entropy bounds given alphabet size; normalized measures in fixed intervals.

**B. Contextual orders of magnitude**  
E.g. entropy values in bits per sample depending on quantization/representation.

**C. Distributional descriptors**  
E.g. temporal variability of local entropy, best described via stability/contrast.

When numeric values are given, they are:
- tied to the representation and estimator,
- not used as thresholds,
- and paired with explicit caveats.

---

## 5. Shannon Entropy (Global)

### What it measures

Shannon entropy measures the expected uncertainty of a discrete random variable.
In practice, audio samples must be mapped to a discrete alphabet (e.g., via quantization or binning).

Reported entropy therefore depends on:
- bin count / quantization depth,
- amplitude scaling,
- whether dithering is present.

### Typical observations

- More concentrated value distributions tend to yield lower entropy.
- More uniformly spread distributions tend to yield higher entropy.
- Strong repetition can reduce entropy in the chosen representation.

### Commonly observed ranges (Category A/B)

**Bounds (established, given alphabet size):**
- For an alphabet of size `M`, entropy lies in **[0, log2(M)]** bits.
- For 16-bit quantized samples, the theoretical maximum is **16 bits/sample** (never reached in typical audio).

**Contextual orders of magnitude (typical audio practice):**
- Entropy estimates for real-world audio, under common binning/quantization choices, are often far below the theoretical maximum because sample distributions are not uniform.
- Reported values depend strongly on implementation details; comparisons are most meaningful **within the same tool/configuration**.

When reference values are provided, they should be tied to the exact representation (e.g., “int16 bins” or “N-bin histogram”).

### Important limits

- Entropy is not a measure of semantic information.
- Estimation bias exists for finite samples (especially with many bins).
- Changing binning/quantization changes entropy values significantly.

---

## 6. Local Entropy (Sliding Windows)

### What it measures

Local entropy measures how entropy varies over time, computed on sliding windows.

### Typical observations

Local entropy may show:
- stable regimes (consistent texture),
- abrupt changes (transitions),
- intermittent low-entropy segments (repetition or silence-like regions),
- intermittent high-entropy segments (noise-like bursts).

### Commonly observed ranges (Category B/C)

Local entropy shares the same bounds as global entropy (depending on binning),
but its most useful descriptors are often:

- contrast between minimum and maximum local entropy,
- persistence of low/high entropy regions,
- segment-wise stability.

Absolute values remain representation-dependent.

### Important limits

- Short windows increase estimation variance.
- Window overlap affects smoothness but not underlying behavior.
- Local entropy changes do not identify causes (only statistical shifts).

---

## 7. Compression Ratio

### What it measures

Compression ratio is used here as a **proxy for redundancy** in a chosen representation.
Highly repetitive or predictable data often compresses better than noise-like data.

The exact behavior depends on:
- the compressor algorithm,
- the input representation (raw bytes, quantized samples, residuals),
- preprocessing.

### Typical observations

- Random-like data tends to compress poorly.
- Repetitive patterns compress more effectively.
- Mixed signals yield intermediate behavior.

### Commonly observed ranges (Category A/B)

Compression ratio is typically bounded conceptually:
- a ratio near **1.0** means “little to no compression achieved” (context-dependent),
- higher ratios indicate more redundancy (but are not comparable across different algorithms without care).

In practice, meaningful interpretation requires:
- fixed compressor choice,
- fixed representation,
- comparative use (across segments/channels).

### Important limits

- Compression ratio is algorithm-dependent and tool-dependent.
- Good compression does not imply meaning; poor compression does not imply randomness.
- Small files/short segments may behave unpredictably due to header and block overhead.

---

## 8. Common Misinterpretations

Common pitfalls in information metrics include:

- treating entropy as “amount of meaning”,
- assuming low entropy implies “encoding”,
- assuming high entropy implies “noise”,
- treating compression ratio as proof of structure.

These metrics quantify statistical properties in a chosen representation.

---

## 9. When Information Analyses Are Insufficient

Information analyses alone cannot:

- detect steganographic payloads,
- establish semantic structure,
- distinguish between different sources with similar statistics.

They are most informative when combined with:
- time–frequency analysis (to localize regimes),
- inter-channel analysis (to compare redundancy across channels),
- modulation analysis (to understand slow structure).

---

## 10. References (selected)

Textbooks / foundations:
- Cover & Thomas — *Elements of Information Theory*
- Lyons — *Understanding Digital Signal Processing*
- Oppenheim & Schafer — *Signals and Systems*

Online technical references:
```text
Entropy definition and properties (Stanford / CCRMA context varies)
https://ccrma.stanford.edu/~jos/sasp/Entropy.html

Elements of Information Theory (book overview)
https://mitpress.mit.edu/9780471241959/elements-of-information-theory/
```

These references provide definitions and methodology, not interpretative guidance.


---

## 11. Mutual Information (Inter-Channel)

### What it measures

Mutual information quantifies **statistical dependence between channels**.
Unlike correlation, it captures both linear and non-linear dependencies.

### Typical observations

- Low values indicate weak statistical dependence.
- Higher values indicate shared structure or redundancy.

### Commonly observed ranges (Category B/C)

Mutual information:
- is non-negative,
- has no universal upper bound.

Values depend on:
- estimation method,
- binning or kernel choices,
- sample count.

### Important limits

- MI values are not directly comparable across implementations.
- High MI does not imply intentional coupling.
