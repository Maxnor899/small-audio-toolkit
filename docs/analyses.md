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

## Performance Optimizations

### Critical: Correlation-Based Methods

Several analysis methods use NumPy's `correlate()` function, which has **O(n²) computational complexity**. On long audio files, this can lead to extremely long processing times.

#### Affected Methods

The following methods have been optimized with sample limitation to maintain reasonable execution times:

**1. Temporal Autocorrelation** (`temporal.autocorrelation`)
- **Without optimization:** 4h 24min on 5.2M samples (110s audio @ 48kHz)
- **With optimization:** ~5 seconds using first 50,000 samples
- **Parameter:** `max_samples` (default: 50000)

**2. Inter-Channel Cross-Correlation** (`inter_channel.cross_correlation`)
- **Without optimization:** ~2 hours per channel pair on long files
- **With optimization:** ~10 seconds total using first 50,000 samples
- **Parameter:** `max_samples` (default: 50000)

**3. Inter-Channel Time Delay** (`inter_channel.time_delay`)
- **Without optimization:** ~2 hours per channel pair on long files
- **With optimization:** ~10 seconds total using first 50,000 samples
- **Parameter:** `max_samples` (default: 50000)

**4. Quantization Noise Autocorrelation** (`steganography.quantization_noise`)
- **Without optimization:** ~5 minutes on 100k samples
- **With optimization:** ~1 second using first 50,000 samples
- **Fixed limit:** 50,000 samples (internal)

#### Why 50,000 Samples?

At 48kHz sample rate, 50,000 samples represents approximately **1 second of audio**. This is sufficient to:

- Detect periodic patterns and repetitions
- Measure inter-channel correlations
- Identify temporal delays
- Capture signal characteristics

For signals with consistent characteristics throughout their duration, analyzing the first second provides representative results while dramatically reducing computation time.

#### Performance Impact Summary

| Method | Before | After | Speedup |
|--------|--------|-------|---------|
| autocorrelation | 4h 24m | 5s | 3168x |
| cross_correlation | ~2h | 10s | 720x |
| time_delay | ~2h | 10s | 720x |
| quantization_noise | ~5m | 1s | 300x |
| **Complete Analysis** | **~8h 30m** | **~15m** | **34x** |

#### Configuration

To enable these optimizations, specify `max_samples` in your configuration:

```yaml
analyses:
  temporal:
    methods:
      - name: "autocorrelation"
        params:
          max_samples: 50000  # Use first 50k samples
          max_lag: 1000
          normalize: true
  
  inter_channel:
    methods:
      - name: "cross_correlation"
        params:
          max_samples: 50000  # Use first 50k samples
          max_lag: 1000
      
      - name: "time_delay"
        params:
          max_samples: 50000  # Use first 50k samples
          max_delay: 100
```

#### Adjusting the Limit

You can adjust `max_samples` based on your needs:

| Samples | Duration @ 48kHz | Computation Time | Use Case |
|---------|------------------|------------------|----------|
| 10,000 | 0.2s | <1s | Very quick preview |
| 50,000 | 1.0s | ~5s | **Recommended default** |
| 100,000 | 2.1s | ~20s | More representative |
| 200,000 | 4.2s | ~90s | Very thorough |
| Unlimited | Full file | Hours | Research/validation only |

**Recommendation:** Keep the default 50,000 samples for production use. Only increase if you specifically need to analyze longer signal portions.

### Other Optimizations

Several other computationally intensive methods also include sample limitations:

- **Local Entropy:** Limited to 200,000 samples
- **Compression Ratio:** Limited to 100,000 samples
- **Approximate Complexity:** Limited to 50,000 samples
- **Wavelet Analysis:** Limited to 100,000 samples
- **Cepstrum:** Limited to 100,000 samples
- **LSB Analysis:** Limited to 100,000 samples
- **Signal Residual:** Limited to 100,000 samples
- **Stability Scores:** Limited to 200,000 samples

These limits are applied internally and do not require configuration parameters.

## Final Note

This catalog defines **the field of possible analyses**, not their default activation.
Actual method selection is entirely driven by the configuration file.

This document constitutes a **methodological reference**, not an interpretive manifesto.