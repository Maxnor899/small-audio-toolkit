# Analysis Catalog (Code-Accurate Documentation)

This document describes **all analysis functions effectively implemented in the codebase**, documented **function by function**.

For each analysis, the documentation specifies:

* the exact **registry identifier** (used in configuration files)
* the **Python function** implementing the analysis
* the **objective** of the computation
* the **parameters** actually used by the code
* the **outputs** effectively produced

This document is strictly descriptive:

* no interpretation
* no classification
* no assumptions about signal intent

---

## Temporal Analyses (`analyses/temporal.py`)

### Amplitude Envelope

**Registry identifier:** `envelope`
**Function:** `envelope_analysis`

#### Objective

Compute the amplitude envelope of the signal in the time domain to measure energy variations over time.

---

#### Parameters

| Name          | Type | Description                                               |
| ------------- | ---- | --------------------------------------------------------- |
| `method`      | str  | Envelope computation method (`hilbert` or `rms`).         |
| `window_size` | int  | Window size for RMS envelope computation (if applicable). |

---

#### Outputs

**Measurements:**

* `envelope`: amplitude envelope signal per channel

---

### Temporal Autocorrelation

**Registry identifier:** `autocorrelation`
**Function:** `autocorrelation_analysis`

#### Objective

Compute the temporal autocorrelation of the signal to measure periodic or repetitive structures.

---

#### Parameters

| Name          | Type | Description                                                     |
| ------------- | ---- | --------------------------------------------------------------- |
| `max_lag`     | int  | Maximum lag (in samples) for which autocorrelation is computed. |
| `normalize`   | bool | Normalize autocorrelation by zero-lag value.                    |
| `max_samples` | int  | Maximum number of samples used for computation.                 |

---

#### Outputs

**Measurements:**

* `lags`: array of lag values
* `autocorrelation`: autocorrelation values

---

### Pulse Detection

**Registry identifier:** `pulse_detection`
**Function:** `pulse_detection`

#### Objective

Detect discrete transient or impulsive events based on amplitude thresholding.

---

#### Parameters

| Name           | Type  | Description                                            |
| -------------- | ----- | ------------------------------------------------------ |
| `threshold`    | float | Detection threshold.                                   |
| `min_distance` | int   | Minimum distance between detected pulses (in samples). |

---

#### Outputs

**Measurements:**

* `pulse_positions`: sample indices of detected pulses

---

### Duration Ratios

**Registry identifier:** `duration_ratios`
**Function:** `duration_ratios`

#### Objective

Compute ratios between durations separating detected temporal events.

---

#### Outputs

**Measurements:**

* `ratios`: list of duration ratios

---

## Spectral Analyses (`analyses/spectral.py`)

### Global FFT

**Registry identifier:** `fft_global`
**Function:** `fft_global`

#### Objective

Compute the global frequency spectrum of the signal.

---

#### Parameters

| Name     | Type | Description                         |
| -------- | ---- | ----------------------------------- |
| `window` | str  | Window function applied before FFT. |

---

#### Outputs

**Measurements:**

* `frequencies`
* `magnitudes`

---

### Spectral Peak Detection

**Registry identifier:** `peak_detection`
**Function:** `peak_detection`

#### Objective

Identify prominent spectral peaks in the frequency domain.

---

#### Parameters

| Name         | Type  | Description                           |
| ------------ | ----- | ------------------------------------- |
| `prominence` | float | Minimum prominence of detected peaks. |
| `distance`   | int   | Minimum distance between peaks.       |
| `height`     | float | Minimum peak height (optional).       |

---

#### Outputs

**Measurements:**

* `peaks`: list of peak frequencies and magnitudes

---

### Harmonic Analysis

**Registry identifier:** `harmonic_analysis`
**Function:** `harmonic_analysis`

#### Objective

Detect harmonic relationships relative to an estimated fundamental frequency.

---

#### Parameters

| Name                | Type | Description                             |
| ------------------- | ---- | --------------------------------------- |
| `fundamental_range` | list | Frequency search range for fundamental. |
| `max_harmonics`     | int  | Maximum number of harmonics considered. |

---

#### Outputs

**Measurements:**

* `fundamental_frequency`
* `harmonics`

---

### Cepstrum Analysis

**Registry identifier:** `cepstrum`
**Function:** `cepstrum_analysis`

#### Objective

Compute the real cepstrum to detect periodic structures in the frequency domain.

---

#### Outputs

**Measurements:**

* `cepstrum`

---

### Spectral Descriptors

**Registry identifiers:** `spectral_centroid`, `spectral_bandwidth`, `spectral_flatness`

#### Objective

Compute global scalar descriptors of spectral structure.

---

#### Outputs

**Measurements:**

* centroid value
* bandwidth value
* flatness value

---

## Time–Frequency Analyses (`analyses/time_frequency.py`)

### STFT

**Registry identifier:** `stft`
**Function:** `stft_analysis`

#### Objective

Compute a short-time Fourier transform spectrogram.

---

#### Parameters

| Name         | Type | Description      |
| ------------ | ---- | ---------------- |
| `n_fft`      | int  | FFT size.        |
| `hop_length` | int  | Hop length.      |
| `window`     | str  | Window function. |

---

#### Outputs

**Measurements:**

* `spectrogram`

---

### Constant-Q Transform

**Registry identifier:** `cqt`
**Function:** `cqt_analysis`

#### Objective

Compute a constant-Q spectrogram with logarithmic frequency resolution.

---

#### Outputs

**Measurements:**

* `cqt_spectrogram`

---

### Wavelet Transform

**Registry identifier:** `wavelet`
**Function:** `wavelet_analysis`

#### Objective

Perform a multi-scale wavelet decomposition of the signal.

---

#### Parameters

| Name      | Type | Description     |
| --------- | ---- | --------------- |
| `wavelet` | str  | Wavelet type.   |
| `scales`  | list | List of scales. |

---

#### Outputs

**Measurements:**

* `coefficients`

---

### Frequency Band Stability

**Registry identifier:** `band_stability`
**Function:** `band_stability`

#### Objective

Measure temporal stability of predefined frequency bands.

---

#### Outputs

**Measurements:**

* `stability_scores`

---

## Modulation Analyses (`analyses/modulation.py`)

### Amplitude Modulation Detection

**Registry identifier:** `am_detection`
**Function:** `am_detection`

#### Objective

Extract and analyze low-frequency amplitude modulation.

---

#### Outputs

**Measurements:**

* `am_envelope`
* `modulation_index`

---

### Frequency Modulation Detection

**Registry identifier:** `fm_detection`
**Function:** `fm_detection`

#### Objective

Estimate instantaneous frequency variations.

---

#### Outputs

**Measurements:**

* `instantaneous_frequency`

---

### Phase Analysis

**Registry identifier:** `phase_analysis`
**Function:** `phase_analysis`

#### Objective

Analyze instantaneous phase evolution over time.

---

#### Outputs

**Measurements:**

* `phase`

---

### Modulation Index

**Registry identifier:** `modulation_index`
**Function:** `modulation_index`

#### Objective

Compute a scalar index describing modulation depth.

---

#### Outputs

**Measurements:**

* `modulation_index`

---

## Information Analyses (`analyses/information.py`)

### Shannon Entropy

**Registry identifier:** `shannon_entropy`
**Function:** `shannon_entropy`

#### Objective

Compute global Shannon entropy of the signal.

---

#### Outputs

**Measurements:**

* `entropy`

---

### Local Entropy

**Registry identifier:** `local_entropy`
**Function:** `local_entropy`

#### Objective

Compute windowed entropy over time.

---

#### Parameters

| Name          | Type | Description  |
| ------------- | ---- | ------------ |
| `window_size` | int  | Window size. |
| `hop_length`  | int  | Hop length.  |

---

#### Outputs

**Measurements:**

* `entropy_series`

---

### Compression Ratio

**Registry identifier:** `compression_ratio`
**Function:** `compression_ratio`

#### Objective

Estimate signal redundancy using lossless compression.

---

#### Outputs

**Measurements:**

* `compression_ratio`

---

### Approximate Complexity

**Registry identifier:** `approximate_complexity`
**Function:** `approximate_complexity`

#### Objective

Estimate algorithmic regularity using approximate complexity measures.

---

#### Outputs

**Measurements:**

* `complexity_score`

---

## Inter-Channel Analyses (`analyses/inter_channel.py`)

### L − R Difference

**Registry identifier:** `lr_difference`
**Function:** `lr_difference`

#### Objective

Compute the difference signal between left and right channels.

---

#### Outputs

**Measurements:**

* `difference_signal`

---

### Cross-Correlation

**Registry identifier:** `cross_correlation`
**Function:** `cross_correlation`

#### Objective

Compute inter-channel cross-correlation.

---

#### Parameters

| Name          | Type | Description        |
| ------------- | ---- | ------------------ |
| `max_lag`     | int  | Maximum lag.       |
| `max_samples` | int  | Sample limitation. |

---

#### Outputs

**Measurements:**

* `correlation`

---

### Phase Difference

**Registry identifier:** `phase_difference`
**Function:** `phase_difference`

#### Objective

Compute phase differences between channels across frequency bands.

---

#### Outputs

**Measurements:**

* `phase_differences`

---

### Time Delay Estimation

**Registry identifier:** `time_delay`
**Function:** `time_delay`

#### Objective

Estimate constant temporal offset between channels.

---

#### Outputs

**Measurements:**

* `delay_samples`

---

## Steganography Analyses (`analyses/steganography.py`)

### LSB Analysis

**Registry identifier:** `lsb_analysis`
**Function:** `lsb_analysis`

#### Objective

Analyze least significant bit distributions.

---

#### Outputs

**Measurements:**

* `bit_statistics`

---

### Quantization Noise Analysis

**Registry identifier:** `quantization_noise`
**Function:** `quantization_noise`

#### Objective

Analyze quantization residuals.

---

#### Outputs

**Measurements:**

* `residual_signal`

---

### Signal Residual Analysis

**Registry identifier:** `signal_residual`
**Function:** `signal_residual`

#### Objective

Compute signal residual after filtering.

---

#### Outputs

**Measurements:**

* `residual`

---

## Meta-Analyses (`analyses/meta_analysis.py`)

### Inter-Segment Comparison

**Registry identifier:** `inter_segment_comparison`
**Function:** `inter_segment_comparison`

#### Objective

Compare analysis features across temporal segments.

---

#### Outputs

**Measurements:**

* `similarity_matrix`

---

### Segment Clustering

**Registry identifier:** `segment_clustering`
**Function:** `segment_clustering`

#### Objective

Cluster segments based on measured features.

---

#### Outputs

**Measurements:**

* `cluster_labels`

---

### Stability Scores

**Registry identifier:** `stability_scores`
**Function:** `stability_scores`

#### Objective

Compute stability indicators across segments or frequency bands.

---

#### Outputs

**Measurements:**

* `stability_scores`
