# YAML Configuration Methodology
## Observation Protocols for Audio Signal Analysis

This document describes the **central role of YAML configurations** in the *Small Audio Tool* project and introduces a **first reference observation protocol** specifically suited to the analysis of audio signals from the game *Elite Dangerous*.

---

## 1. Fundamental Principle

The analysis engine is deliberately **neutral**:

- it computes objective measurements only,
- it never interprets results,
- it produces no automatic conclusions.

As a result, the **scientific subtlety** of the analysis lies almost entirely in the YAML configuration.

A YAML configuration is **not** a simple parameter file:
> it is an **experimental observation protocol**, fully explicit and reproducible.

---

## 2. Role of YAML in the Architecture

A YAML configuration defines:

- **which channels** are observed (left, right, difference, etc.),
- **which analysis families** are enabled,
- **which specific methods** are applied,
- **at what temporal and spectral scales**,
- **with which resolution trade-offs**.

Changing the YAML means:
> observing the same signal **from a different analytical angle**, without changing the instrument.

---

## 3. Why Multiple Configurations Are Necessary

An audio signal may simultaneously contain:

- temporal structures,
- spectral structures,
- modulations,
- inter-channel relationships,
- informational signatures.

A single configuration cannot explore all these dimensions effectively without:

- increasing noise,
- masking certain structures,
- introducing implicit compromises.

The adopted solution is therefore:
> **multiple YAML configurations, each corresponding to a clearly defined observation objective.**

---

## 4. Reference Protocol:
## “Artificial Structures and Regularities”

### Objective

Reveal **stable temporal, spectral, and inter-channel structures** that may indicate intentional or algorithmic construction, **without any interpretation of content**.

This protocol is particularly suited to audio signals from *Elite Dangerous*, which often exhibit:

- non-musical repetitions,
- regular pulsations,
- deliberate left/right asymmetries,
- strong spectral stability.

---

### Corresponding YAML Configuration

```yaml
version: "1.0"

channels:
  analyze:
    - left
    - right
    - difference

analyses:

  temporal:
    enabled: true
    methods:
      - name: envelope
        params:
          method: hilbert

      - name: autocorrelation
        params:
          max_lag: 5000
          normalize: true
          max_samples: 100000

  spectral:
    enabled: true
    methods:
      - name: fft_global
        params:
          window: hann

      - name: peak_detection
        params:
          prominence: 0.05
          distance: 50

      - name: harmonic_analysis
        params:
          fundamental_range: [20, 2000]
          max_harmonics: 10

  time_frequency:
    enabled: true
    methods:
      - name: stft
        params:
          n_fft: 4096
          hop_length: 256
          window: hann

      - name: band_stability
        params:
          bands:
            - [20, 100]
            - [100, 300]
            - [300, 800]
            - [800, 2000]
            - [2000, 6000]

  modulation:
    enabled: true
    methods:
      - name: am_detection
      - name: fm_detection
      - name: phase_analysis

  information:
    enabled: true
    methods:
      - name: shannon_entropy
      - name: local_entropy
        params:
          window_size: 2048
          hop_length: 512
      - name: compression_ratio

  inter_channel:
    enabled: true
    methods:
      - name: lr_difference
      - name: cross_correlation
        params:
          max_lag: 2000
          max_samples: 50000
      - name: phase_difference
      - name: time_delay

visualization:
  enabled: true
  formats: ["png"]
  dpi: 150
  figsize: [12, 8]

output:
  save_raw_data: true
  save_config: true
```

---

## 5. What This Protocol Allows One to Observe

Without drawing conclusions, this protocol makes it possible to measure:

- global and local periodicities,
- repetitive structures in time and frequency,
- frequency-band stability,
- slow or structured modulations,
- inter-channel coherence or asymmetry,
- levels of order, redundancy, or complexity.

All interpretations remain **outside the tool** and are the responsibility of the human analyst.

---

## 6. General Philosophy

- The **code** is the instrument.
- The **YAML file** is the experimental protocol.
- The **results** are observations.
- **Interpretation** belongs to the user.

This separation is a deliberate methodological choice, ensuring rigor, reproducibility, and the absence of automatic bias.
