# Meta-Analysis
## Cross-Metric Consistency, Stability, and Comparative Structure

This document describes the **meta-analysis family**.
Meta-analyses do not introduce new signal measurements.
Instead, they examine **relationships, stability, and consistency across existing analyses**.

They operate strictly on already-computed metrics and summaries.

---

## 1. What Meta-Analyses Measure

Meta-analyses focus on:

- consistency of measurements across time segments,
- stability of metrics across channels,
- comparative behavior between analysis families,
- sensitivity of results to configuration changes.

They answer questions such as:
- *Are observed properties stable or transient?*
- *Do different metrics behave coherently over time?*
- *How sensitive are observations to analysis parameters?*

They do **not** infer causality, intent, or meaning.

---

## 2. Typical Uses in Signal Processing

In DSP practice, meta-analysis techniques are used to:

- assess robustness of measurements,
- compare alternative representations,
- validate analysis pipelines,
- detect regime changes or instabilities.

They are widely applied in:
- exploratory data analysis,
- quality control,
- system identification,
- research validation workflows.

---

## 3. Meta-Analysis Methods Used in This Project

This project includes meta-analysis methods such as:

- segment-to-segment comparison of metrics,
- variance and stability scoring of measurements over time,
- cross-channel consistency checks,
- sensitivity analysis with respect to configuration parameters.

These methods analyze **relationships between measurements**, not signals directly.

---

## 4. How to Read “Commonly Observed Ranges” in Meta-Analysis

Meta-analysis outputs often lack universal numeric ranges.

As in other families:

**A. Established numeric bounds**  
E.g. normalized similarity or stability scores in fixed intervals.

**B. Contextual orders of magnitude**  
E.g. variance or dispersion values relative to baseline variability.

**C. Distributional descriptors**  
E.g. clustering of segment-level measurements or persistence of patterns.

Interpretation is inherently comparative and context-dependent.

---

## 5. Segment Stability Analysis

### What it measures

Segment stability analysis evaluates **how much a given metric varies across time segments**.

### Typical observations

- Low variability indicates stable behavior.
- High variability indicates changing regimes or transient effects.

### Commonly observed ranges (Category B/C)

Stability is commonly described using:
- variance,
- coefficient of variation,
- relative dispersion.

Rather than absolute values, comparisons such as:
- early vs. late segments,
- channel vs. channel,
- configuration A vs. configuration B

are most informative.

### Important limits

- Stability depends on segmentation strategy.
- Short segments increase variability due to estimation noise.
- Stability does not imply simplicity or intent.

---

## 6. Cross-Metric Consistency

### What it measures

Cross-metric analysis examines whether **different metrics exhibit correlated behavior** over time or segments.

### Typical observations

- Some metrics may vary together due to shared dependencies.
- Others may vary independently.

### Commonly observed ranges (Category C)

Correlation or similarity between metric time series is best interpreted via:
- relative trends,
- persistence of relationships,
- comparison across configurations.

Absolute correlation values are rarely meaningful in isolation.

### Important limits

- Correlation does not imply causation.
- Shared preprocessing can induce artificial correlations.
- Metric dependencies may be indirect.

---

## 7. Configuration Sensitivity

### What it measures

Configuration sensitivity analysis evaluates **how strongly results change when analysis parameters change**.

### Typical observations

- Robust metrics change little with moderate parameter variation.
- Sensitive metrics vary strongly with resolution or thresholds.

### Commonly observed ranges (Category B/C)

Sensitivity is often described through:
- relative change ratios,
- stability across parameter sweeps,
- qualitative comparison of distributions.

### Important limits

- Sensitivity does not imply unreliability; some metrics are inherently scale-dependent.
- Over-interpretation of sensitivity can be misleading.

---

## 8. Aggregation and Summary Metrics

### What it measures

Some meta-analyses aggregate measurements into summaries for readability,
such as averages, medians, or stability scores.

### Typical observations

- Aggregates can highlight dominant behavior.
- Aggregates can also hide variability.

### Commonly observed ranges (Category A/B)

Aggregate metrics inherit bounds from underlying metrics (if normalized),
but their interpretation must account for information loss.

### Important limits

- Aggregation reduces detail.
- Summary metrics should always be read alongside distributions or segment-level data.

---

## 9. Common Misinterpretations

Common pitfalls in meta-analysis include:

- treating stability as significance,
- assuming cross-metric agreement implies truth,
- interpreting aggregated scores as conclusions.

Meta-analysis supports reasoning; it does not replace it.

---

## 10. When Meta-Analyses Are Insufficient

Meta-analyses alone cannot:

- validate hypotheses,
- establish meaning,
- replace detailed inspection of raw measurements.

They are most informative when used to:
- guide further exploration,
- identify robust vs. fragile observations,
- structure human analysis.

---

## 11. References (selected)

Textbooks / methodological context:
- Tukey — *Exploratory Data Analysis*
- Montgomery — *Design and Analysis of Experiments*
- Lyons — *Understanding Digital Signal Processing*

Online references:
```text
Exploratory data analysis (Wikipedia)
https://en.wikipedia.org/wiki/Exploratory_data_analysis
```

These references provide methodological grounding, not interpretative guidance.
