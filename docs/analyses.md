# Analysis Catalog

This document describes **all envisioned analyses**, grouped by **scientific analysis class**. It serves as a methodological reference and configuration base for the audio analysis pipeline.

No analysis listed here performs semantic or narrative interpretation. All produce only **objective measurements**.

## 1. Preprocessing

### Objective

Stabilize the signal, reduce recording or mixing biases, and prepare analytically exploitable segments.

### Methods

**RMS / LUFS Normalization**
Global level adjustment for inter-file comparability.

**Silence Detection**
Identification of low-energy ranges based on threshold and duration.

**Temporal Segmentation**
Signal splitting into homogeneous segments (energy, spectral stability).

**Background Noise Estimation**
Stationary noise calculation for differential analysis.

## 2. Temporal Analysis

### Objective

Identify **rhythmic structures**, repetitions, or temporal encodings.

### Methods

**Amplitude Envelope (Hilbert)**
Measurement of energy evolution over time.

**Temporal Autocorrelation**
Detection of periodicities and cycles.

**Pulse / Impulse Detection**
Identification of non-natural discrete events.

**Duration Ratios**
Relative comparison of intervals between events.

## 3. Frequency Analysis

### Objective

Highlight **carriers**, dominant frequencies, or artificial harmonic structures.

### Methods

**Global FFT**
Average signal spectrum.

**Spectral Peak Detection**
Identification of dominant frequencies and their stability.

**Harmonic Analysis**
Search for non-natural harmonic relationships.

**Cepstrum**
Detection of frequency repetitions and modulation structures.

**Spectral Centroid / Bandwidth / Flatness**
Global spectral structure indicators.

## 4. Time-Frequency Analysis

### Objective

Observe the evolution of frequency components over time and detect **persistent visual or structural patterns**.

### Methods

**STFT (Short-Time Fourier Transform)**
Standard time-frequency analysis.

**CQT (Constant-Q Transform)**
Logarithmic analysis adapted to musical or designed signals.

**Wavelet Transforms**
Multi-scale structure detection.

**Frequency Band Stability**
Measurement of temporal constancy of certain bands.

## 5. Modulation Analysis

### Objective

Detect **information carried indirectly** through amplitude, frequency, or phase modulation.

### Methods

**Amplitude Modulation Detection (AM)**
Low-frequency envelope extraction.

**Frequency Modulation Analysis (FM)**
Instantaneous frequency calculation.

**Instantaneous Phase Analysis**
Study of continuous phase variations.

**Modulation Index**
Measurement of modulation depth.

## 6. Information Analysis

### Objective

Measure the **informational complexity** of the signal and detect compressible structures.

### Methods

**Global Shannon Entropy**
Measurement of informational disorder.

**Local Entropy (Windowed)**
Detection of structured zones.

**Compression Ratio**
Redundancy estimation (gzip, LZ).

**Approximate Complexity**
Algorithmic regularity measurement.

## 7. Inter-Channel Analysis

### Objective

Identify **information distributed between channels**, invisible in mono.

### Methods

**Inter-Channel Cross-Correlation**
Measurement of similarity and synchronization.

**L - R Difference**
Highlighting signals hidden by phase opposition.

**Inter-Channel Phase Analysis**
Phase stability and coherence per band.

**Inter-Channel Delays (ITD)**
Detection of constant temporal offsets.

## 8. Steganography Analysis (Exploratory)

### Objective

Test for **intentional discrete encodings**, without presuming their existence.

### Methods

**Least Significant Bit Analysis (LSB)**
Applicable to uncompressed PCM formats.

**Structured Quantization Noise**
Search for non-random patterns.

**Signal / Residual Comparison**
Differential analysis after filtering.

## 9. Meta-Analysis

### Objective

Provide global indicators to guide human analysis.

### Methods

**Inter-Segment Comparison**
Detection of repetitions or anomalies.

**Segment Clustering**
Grouping by measured similarity.

**Stability Scores**
Temporal or frequency constancy indicators.

## Method Identification

Each method has:

- A unique identifier used in configuration
- Clear input parameters
- Well-defined output format
- Scientific references where applicable

## Implementation Notes

### Parameter Ranges

All methods define reasonable parameter ranges based on:

- Signal sample rate
- Expected signal characteristics
- Computational constraints

### Output Format

Each method returns a structured result containing:

- Primary measurements
- Derived metrics
- Anomaly scores (where applicable)
- Visualization data (optional)

### Validation

Methods include internal validation to:

- Check parameter validity
- Detect edge cases
- Report warnings for unusual inputs

## Final Note

This catalog defines **the field of possible analyses**, not their default activation.
Actual method selection is entirely driven by the configuration file.

This document constitutes a **methodological reference**, not an interpretive manifesto.
