# A1 – Catalog of Analysis Methods and Outputs

## 1. Purpose and organization

**⚠️ CRITICAL DISCLAIMER:** This catalog is **informative, not normative**. It documents observed implementations in the codebase at a given time. It **MUST NOT** be used as a stability or compatibility contract.

This catalog documents all 39 analysis methods available in SAT, organized by category. For each method, the catalog specifies:

- **Description**: What the method computes
- **Parameters**: Configuration options with defaults (as currently implemented)
- **Measurements**: Structure of output data (as currently observed)  
- **Metrics**: Method-level metadata
- **Visualization**: Whether visualization is currently supported (non-contractual)

**Non-contractual aspects:**
- Measurement structures may evolve
- Field names may change between versions
- New methods may be added
- Parameters and defaults may be modified
- Visualization support is non-contractual

**Field names are method-specific and MUST NOT be assumed comparable across methods.** For example, `periodicity_score`, `anomaly_score`, or `confidence` may use different algorithms and scales in different methods.

For stability guarantees and breaking change policies, see `01_TECHNICAL_OVERVIEW.md` section 6 and `05_EXTENDING_SAT.md` section 6.

**Status:** This catalog reflects the codebase as of 2025-01-22. Methods and parameters may evolve in future versions.

**Usage:** This catalog is a reference for:
- Protocol authors (choosing methods and setting parameters)
- Context authors (defining reference ranges for measurements)
- Developers (understanding existing methods before adding new ones)

---

## 2. Reading guide

### 2.1 Measurement scope notation

Methods produce measurements at different scopes:

| Scope | Notation | Example |
|-------|----------|---------|
| **Per-channel** | `{channel: {...}}` | `{"left": {"mean": 0.5}, "right": {"mean": 0.6}}` |
| **Global** | `{"global": {...}}` | `{"global": {"correlation": 0.85}}` |
| **Per-segment** | `{channel: {segment: {...}}}` | `{"left": {"segment_0": {...}}}` (currently unused) |

### 2.2 Parameter notation

- **Required**: Must be specified in protocol
- **Optional**: Has a default value
- **Type**: Expected data type (int, float, str, list, etc.)

### 2.3 Measurement types

- **Scalar**: Single numeric value (int, float)
- **Array**: List of values (limited to ~20 elements in measurements)
- **Object**: Nested structure

**IMPORTANT:** Field names are method-specific and MUST NOT be assumed comparable across methods. For example:
- `periodicity_score` from `autocorrelation` vs `phase_linearity` from `phase_analysis` use different algorithms and scales
- `confidence` fields from different methods are not comparable
- `anomaly_score` implementations vary by method
- Always check method-specific documentation for interpretation

---

## 3. Temporal analysis (4 methods)

### 3.1 `envelope`

**Description:** Compute amplitude envelope using Hilbert transform or RMS windowing.

**Parameters:**
- `method` (str, default: `"hilbert"`): Envelope extraction method
  - `"hilbert"`: Analytic signal via Hilbert transform
  - `"rms"`: Root mean square in sliding windows
- `window_size` (int, default: `1024`): Window size for RMS method (ignored for Hilbert)

**Measurements (per-channel):**
```python
{
  "channel_name": {
    "envelope_mean": float,      # Mean envelope amplitude
    "envelope_max": float,        # Maximum envelope amplitude
    "envelope_std": float,        # Standard deviation of envelope
    "envelope_length": int        # Number of envelope samples
  }
}
```

**Metrics:**
```python
{
  "method": str  # "hilbert" or "rms"
}
```

**Visualization:** Supported (non-contractual) (envelope waveform over time)

---

### 3.2 `autocorrelation`

**Description:** Compute temporal autocorrelation to detect periodicity and self-similarity.

**Parameters:**
- `max_lag` (int, default: `5000`): Maximum lag in samples
- `normalize` (bool, default: `true`): Normalize autocorrelation to [0, 1]
- `max_samples` (int, default: `50000`): **Performance limit** - maximum samples to analyze

**Measurements (per-channel):**
```python
{
  "channel_name": {
    "autocorr_max": float,         # Maximum autocorrelation (excluding lag 0)
    "first_peak_lag": int,         # Lag of first significant peak
    "num_peaks": int,              # Number of detected peaks
    "periodicity_score": float,    # Proxy for temporal periodicity strength
    "samples_analyzed": int        # Number of samples actually analyzed
  }
}
```

**Metrics:**
```python
{
  "max_lag": int,
  "normalize": bool,
  "max_samples": int
}
```

**Visualization:** Supported (non-contractual) (autocorrelation function vs lag)

**Performance notes:** O(n²) complexity. Always uses `max_samples` limit. 50k samples → ~10 seconds. 2.88M samples (60s @ 48kHz) would take hours without limit.

---

### 3.3 `pulse_detection`

**Description:** Detect pulses or impulses in the envelope.

**Parameters:**
- `threshold` (float, default: `0.6`): Detection threshold (relative to max envelope)
- `min_distance` (int, default: `2000`): Minimum distance between pulses in samples

**Measurements (per-channel):**
```python
{
  "channel_name": {
    "num_pulses": int,                    # Number of detected pulses
    "pulse_positions": list[int],         # Sample positions (limited to first 20)
    "mean_pulse_interval": float,         # Mean interval between pulses
    "pulse_regularity": float            # Coefficient of variation
  }
}
```

**Metrics:**
```python
{
  "threshold": float,
  "min_distance": int
}
```

**Visualization:** Supported (non-contractual) (waveform + envelope + pulse markers)

---

### 3.4 `duration_ratios`

**Description:** Compute ratios between consecutive event intervals (for pattern detection).

**Parameters:**
- `threshold` (float, default: `0.5`): Event detection threshold
- `min_duration` (int, default: `1000`): Minimum event duration in samples

**Measurements (per-channel):**
```python
{
  "channel_name": {
    "num_events": int,                # Number of detected events
    "duration_ratios": list[float],   # Ratios between consecutive intervals
    "mean_ratio": float,              # Mean of ratios
    "ratio_std": float               # Standard deviation of ratios
  }
}
```

**Metrics:**
```python
{
  "threshold": float,
  "min_duration": int
}
```

**Visualization:** Not supported

---

## 4. Spectral analysis (9 methods)

### 4.1 `fft_global`

**Description:** Compute global FFT spectrum.

**Parameters:**
- `window` (str, default: `"hann"`): Window function (`"hann"`, `"hamming"`, `"blackman"`, `"bartlett"`)

**Measurements (per-channel):**
```python
{
  "channel_name": {
    "n_fft": int,                     # FFT size (= audio length)
    "frequency_resolution": float,    # Frequency bin width (Hz)
    "peak_frequency": float,          # Frequency of maximum magnitude
    "peak_magnitude": float,          # Maximum magnitude
    "spectral_energy": float         # Sum of squared magnitudes
  }
}
```

**Metrics:**
```python
{
  "window": str,
  "sample_rate": int
}
```

**Visualization:** Supported (non-contractual) (magnitude spectrum)

---

### 4.2 `peak_detection`

**Description:** Detect spectral peaks in FFT spectrum.

**Parameters:**
- `prominence` (float, default: `0.05`): Minimum peak prominence
- `distance` (int, default: `50`): Minimum distance between peaks (in bins)
- `height` (float, optional): Minimum peak height

**Measurements (per-channel):**
```python
{
  "channel_name": {
    "num_peaks": int,                     # Total number of peaks
    "peak_frequencies": list[float],      # Peak frequencies (first 20)
    "peak_magnitudes": list[float],       # Peak magnitudes (first 20)
    "dominant_frequency": float,          # Frequency of highest peak
    "frequency_spread": float            # Std dev of peak frequencies
  }
}
```

**Metrics:**
```python
{
  "prominence": float,
  "distance": int
}
```

**Visualization:** Supported (non-contractual) (spectrum with peak markers)

---

### 4.3 `harmonic_analysis`

**Description:** Analyze harmonic structure (fundamental + harmonics).

**Parameters:**
- `fundamental_range` (list[int], default: `[20, 2000]`): Frequency range to search for fundamental (Hz)
- `max_harmonics` (int, default: `10`): Maximum number of harmonics to detect

**Measurements (per-channel):**
```python
{
  "channel_name": {
    "fundamental_frequency": float,       # Detected fundamental (Hz)
    "fundamental_magnitude": float,       # Fundamental magnitude
    "num_harmonics": int,                 # Number of detected harmonics
    "harmonic_frequencies": list[float],  # Harmonic frequencies
    "harmonic_magnitudes": list[float],   # Harmonic magnitudes
    "harmonic_ratio": float              # Energy in harmonics / total energy
  }
}
```

**Metrics:**
```python
{
  "fundamental_range": list[int],
  "max_harmonics": int
}
```

**Visualization:** Supported (non-contractual) (spectrum with fundamental + harmonics marked)

---

### 4.4 `spectral_centroid`

**Description:** Compute spectral centroid (brightness measure).

**Parameters:** None

**Measurements (per-channel):**
```python
{
  "channel_name": {
    "spectral_centroid": float  # Frequency-weighted mean (Hz)
  }
}
```

**Metrics:** `{}`

**Visualization:** Not supported

---

### 4.5 `spectral_bandwidth`

**Description:** Compute spectral bandwidth (spread around centroid).

**Parameters:** None

**Measurements (per-channel):**
```python
{
  "channel_name": {
    "spectral_bandwidth": float  # Bandwidth in Hz
  }
}
```

**Metrics:** `{}`

**Visualization:** Not supported

---

### 4.6 `spectral_flatness`

**Description:** Compute spectral flatness (noisiness measure).

**Parameters:** None

**Measurements (per-channel):**
```python
{
  "channel_name": {
    "spectral_flatness": float  # 0 = tonal, 1 = noise-like
  }
}
```

**Metrics:** `{}`

**Visualization:** Not supported

---

### 4.7 `spectral_flux`

**Description:** Compute spectral flux (rate of spectral change).

**Parameters:**
- `hop_length` (int, default: `512`): Hop size for consecutive spectra

**Measurements (per-channel):**
```python
{
  "channel_name": {
    "mean_flux": float,    # Mean spectral flux
    "max_flux": float,     # Maximum flux
    "flux_std": float     # Standard deviation
  }
}
```

**Metrics:**
```python
{
  "hop_length": int
}
```

**Visualization:** Not supported

---

### 4.8 `spectral_rolloff`

**Description:** Compute spectral rolloff frequency (frequency below which X% of energy lies).

**Parameters:**
- `rolloff_threshold` (float, default: `0.85`): Energy threshold (0.85 = 85%)

**Measurements (per-channel):**
```python
{
  "channel_name": {
    "spectral_rolloff": float  # Rolloff frequency (Hz)
  }
}
```

**Metrics:**
```python
{
  "rolloff_threshold": float
}
```

**Visualization:** Not supported

---

### 4.9 `cepstrum`

**Description:** Compute cepstrum (spectrum of log spectrum).

**Parameters:** None

**Measurements (per-channel):**
```python
{
  "channel_name": {
    "peak_quefrency": float,    # Quefrency of maximum cepstral peak
    "cepstral_peak": float,     # Magnitude of peak
    "fundamental_estimate": float  # Estimated fundamental (if detected)
  }
}
```

**Metrics:** `{}`

**Visualization:** Supported (non-contractual) (cepstrum vs quefrency)

---

## 5. Time-frequency analysis (3 methods)

### 5.1 `stft`

**Description:** Short-Time Fourier Transform (spectrogram).

**Parameters:**
- `n_fft` (int, default: `2048`): FFT size
- `hop_length` (int, default: `512`): Hop size between frames
- `window` (str, default: `"hann"`): Window function

**Measurements (per-channel):**
```python
{
  "channel_name": {
    "num_frames": int,          # Number of time frames
    "num_freq_bins": int,       # Number of frequency bins
    "time_resolution": float,   # Time resolution (seconds)
    "freq_resolution": float,   # Frequency resolution (Hz)
    "mean_energy": float,       # Mean spectrogram energy
    "peak_time": float,         # Time of peak energy
    "peak_freq": float         # Frequency of peak energy
  }
}
```

**Metrics:**
```python
{
  "n_fft": int,
  "hop_length": int,
  "window": str,
  "sample_rate": int
}
```

**Visualization:** Supported (non-contractual) (spectrogram heatmap)

**Performance notes:** Can be memory-intensive for long files. Spectrogram stored in `visualization_data` only (not in measurements).

---

### 5.2 `wavelet`

**Description:** Continuous wavelet transform.

**Parameters:**
- `wavelet` (str, default: `"morl"`): Wavelet type (`"morl"`, `"mexh"`, `"gaus1"`, etc.)
- `scales` (list[int], default: `[1, 2, 4, ..., 128]`): Scales to analyze

**Measurements (per-channel):**
```python
{
  "channel_name": {
    "num_scales": int,           # Number of scales analyzed
    "dominant_scale": int,       # Scale with maximum energy
    "scale_energy": list[float], # Energy per scale
    "mean_energy": float        # Mean across scales
  }
}
```

**Metrics:**
```python
{
  "wavelet": str,
  "num_scales": int
}
```

**Visualization:** Supported (non-contractual) (scalogram heatmap)

**Dependencies:** Requires `pywt` (PyWavelets library) - optional dependency, not required by SAT core

---

### 5.3 `band_stability`

**Description:** Measure energy stability in frequency bands over time.

**Parameters:**
- `bands` (list[list[int]], required): Frequency bands as `[[low, high], ...]`
  - Example: `[[20, 80], [80, 200], [200, 800]]`

**Measurements (per-channel):**
```python
{
  "channel_name": {
    "band_0_mean": float,      # Mean energy in band 0
    "band_0_std": float,       # Std dev of energy in band 0
    "band_0_cv": float,        # Coefficient of variation
    # ... repeated for each band ...
    "num_bands": int          # Total number of bands
  }
}
```

**Metrics:**
```python
{
  "bands": list[list[int]],
  "num_bands": int
}
```

**Visualization:** Supported (non-contractual) (energy evolution per band)

---

## 6. Modulation analysis (5 methods)

### 6.1 `am_detection`

**Description:** Detect amplitude modulation.

**Parameters:** None

**Measurements (per-channel):**
```python
{
  "channel_name": {
    "am_detected": bool,            # Whether AM is detected
    "modulation_rate": float,       # Modulation rate (Hz)
    "modulation_depth": float,      # Modulation depth (0-1)
    "carrier_frequency": float     # Estimated carrier (Hz)
  }
}
```

**Metrics:** `{}`

**Visualization:** Supported (non-contractual) (envelope + modulation spectrum)

---

### 6.2 `fm_detection`

**Description:** Detect frequency modulation.

**Parameters:**
- `carrier_estimate` (float, optional): Estimated carrier frequency (Hz)

**Measurements (per-channel):**
```python
{
  "channel_name": {
    "fm_detected": bool,            # Whether FM is detected
    "modulation_rate": float,       # Modulation rate (Hz)
    "frequency_deviation": float,   # Max deviation from carrier (Hz)
    "carrier_frequency": float     # Detected/estimated carrier (Hz)
  }
}
```

**Metrics:**
```python
{
  "carrier_estimate": float  # or null
}
```

**Visualization:** Supported (non-contractual) (instantaneous frequency over time)

---

### 6.3 `phase_analysis`

**Description:** Analyze phase continuity and detect phase jumps.

**Parameters:**
- `jump_threshold` (float, default: `1.0`): Phase jump detection threshold (radians)

**Measurements (per-channel):**
```python
{
  "channel_name": {
    "num_phase_jumps": int,        # Number of detected jumps
    "mean_phase": float,           # Mean unwrapped phase
    "phase_std": float,            # Phase standard deviation
    "phase_linearity": float      # Measure of phase linearity
  }
}
```

**Metrics:**
```python
{
  "jump_threshold": float
}
```

**Visualization:** Supported (non-contractual) (unwrapped phase + jump markers)

---

### 6.4 `modulation_index`

**Description:** Compute modulation index for AM/FM signals.

**Parameters:**
- `carrier_frequency` (float, required): Carrier frequency (Hz)

**Measurements (per-channel):**
```python
{
  "channel_name": {
    "modulation_index": float,     # Modulation index
    "modulation_type": str        # "AM" or "FM" or "unknown"
  }
}
```

**Metrics:**
```python
{
  "carrier_frequency": float
}
```

**Visualization:** Not supported

---

### 6.5 `chirp_detection`

**Description:** Detect linear frequency modulation (chirp).

**Parameters:**
- `min_duration` (float, default: `0.1`): Minimum chirp duration (seconds)

**Measurements (per-channel):**
```python
{
  "channel_name": {
    "chirp_detected": bool,          # Whether chirp is detected
    "chirp_rate": float,             # Frequency sweep rate (Hz/s)
    "start_frequency": float,        # Starting frequency (Hz)
    "end_frequency": float,          # Ending frequency (Hz)
    "chirp_duration": float         # Duration (seconds)
  }
}
```

**Metrics:**
```python
{
  "min_duration": float
}
```

**Visualization:** Not supported

---

## 7. Information theory (5 methods)

### 7.1 `shannon_entropy`

**Description:** Compute Shannon entropy (information content).

**Parameters:**
- `num_bins` (int, default: `256`): Number of histogram bins

**Measurements (per-channel):**
```python
{
  "channel_name": {
    "shannon_entropy": float,        # Shannon entropy (bits)
    "normalized_entropy": float,     # Normalized to [0, 1]
    "num_bins": int                 # Bins used
  }
}
```

**Metrics:**
```python
{
  "num_bins": int
}
```

**Visualization:** Not supported

---

### 7.2 `local_entropy`

**Description:** Compute entropy in sliding windows.

**Parameters:**
- `window_size` (int, default: `2048`): Window size in samples
- `hop_length` (int, default: `512`): Hop size between windows
- `num_bins` (int, default: `64`): Histogram bins

**Measurements (per-channel):**
```python
{
  "channel_name": {
    "mean_entropy": float,           # Mean windowed entropy
    "std_entropy": float,            # Standard deviation
    "min_entropy": float,            # Minimum entropy
    "max_entropy": float,            # Maximum entropy
    "num_windows": int,              # Number of windows
    "entropy_variation": float      # Coefficient of variation
  }
}
```

**Metrics:**
```python
{
  "window_size": int,
  "hop_length": int,
  "num_bins": int
}
```

**Visualization:** Supported (non-contractual) (entropy evolution over time)

---

### 7.3 `compression_ratio`

**Description:** Estimate compressibility using gzip.

**Parameters:** None

**Measurements (per-channel):**
```python
{
  "channel_name": {
    "original_size": int,          # Original size (bytes)
    "compressed_size": int,        # Compressed size (bytes)
    "compression_ratio": float,    # Ratio (>1 = compressible)
    "samples_analyzed": int       # Samples used (max 100k)
  }
}
```

**Metrics:** `{}`

**Visualization:** Not supported

**Performance notes:** Limited to first 100k samples for performance.

---

### 7.4 `approximate_complexity`

**Description:** Approximate sample entropy (complexity measure).

**Parameters:**
- `m` (int, default: `2`): Pattern length
- `r_factor` (float, default: `0.2`): Tolerance factor (fraction of std dev)

**Measurements (per-channel):**
```python
{
  "channel_name": {
    "approximate_complexity": float,  # Sample entropy approximation
    "pattern_length": int,            # m parameter
    "tolerance": float,               # r parameter (computed)
    "samples_analyzed": int          # Samples used (max 5k)
  }
}
```

**Metrics:**
```python
{
  "m": int,
  "r_factor": float
}
```

**Visualization:** Not supported

**Performance notes:** **CRITICAL O(n²) algorithm**. Limited to 5000 samples (→ ~5 seconds). 50k samples would take ~8 minutes.

---

### 7.5 `mutual_information`

**Description:** Compute mutual information between channels.

**Parameters:**
- `num_bins` (int, default: `64`): Histogram bins for MI estimation

**Measurements (global scope):**
```python
{
  "global": {
    "num_channels": int,                    # Number of channels analyzed
    "channel_names": list[str],             # Channel names
    "mi_pairs": {                           # MI for each pair
      "left_vs_right": float,
      "left_vs_difference": float,
      ...
    },
    "mean_mi": float,                       # Mean MI across pairs
    "max_mi": float,                        # Maximum MI
    "samples_analyzed": int                # Samples used (max 50k)
  }
}
```

**Metrics:**
```python
{
  "num_bins": int
}
```

**Visualization:** Supported (non-contractual) (MI matrix heatmap)

**Performance notes:** Limited to 50k samples per channel.

---

## 8. Inter-channel analysis (4 methods)

### 8.1 `lr_difference`

**Description:** Analyze L-R difference channel properties.

**Parameters:** None

**Measurements (global scope):**
```python
{
  "global": {
    "lr_correlation": float,         # Correlation between L and R
    "lr_difference_energy": float,   # Energy in L-R channel
    "lr_sum_energy": float,          # Energy in L+R channel
    "stereo_width": float           # Measure of stereo spread
  }
}
```

**Metrics:** `{}`

**Visualization:** Not supported

**Requirements:** Stereo audio (left and right channels)

---

### 8.2 `cross_correlation`

**Description:** Compute cross-correlation between channel pairs.

**Parameters:**
- `max_lag` (int, default: `2000`): Maximum lag in samples
- `max_samples` (int, default: `50000`): Performance limit

**Measurements (global scope):**
```python
{
  "global": {
    "num_pairs": int,                    # Number of channel pairs
    "pairs": {                           # Results per pair
      "left_vs_right": {
        "max_correlation": float,
        "lag_at_max": int,
        "correlation_strength": float
      },
      ...
    },
    "samples_analyzed": int
  }
}
```

**Metrics:**
```python
{
  "max_lag": int,
  "max_samples": int
}
```

**Visualization:** Supported (non-contractual) (cross-correlation function for each pair)

---

### 8.3 `phase_difference`

**Description:** Compute phase difference between channels.

**Parameters:** None

**Measurements (global scope):**
```python
{
  "global": {
    "num_pairs": int,
    "pairs": {
      "left_vs_right": {
        "mean_phase_diff": float,      # Mean phase difference (radians)
        "phase_diff_std": float,       # Standard deviation
        "phase_coherence": float      # Phase stability measure
      },
      ...
    }
  }
}
```

**Metrics:** `{}`

**Visualization:** Not supported

---

### 8.4 `time_delay`

**Description:** Estimate inter-channel time delay (ITD - Interaural Time Difference).

**Parameters:**
- `max_delay` (int, default: `1000`): Maximum delay in samples

**Measurements (global scope):**
```python
{
  "global": {
    "num_pairs": int,
    "pairs": {
      "left_vs_right": {
        "time_delay_samples": int,     # Delay in samples
        "time_delay_ms": float,        # Delay in milliseconds
        "confidence": float           # Delay estimate confidence
      },
      ...
    }
  }
}
```

**Metrics:**
```python
{
  "max_delay": int,
  "sample_rate": int
}
```

**Visualization:** Not supported

---

## 9. Steganography detection (5 methods)

### 9.1 `lsb_analysis`

**Description:** Analyze least significant bit patterns.

**Parameters:**
- `bit_depth` (int, default: `16`): Audio bit depth

**Measurements (per-channel):**
```python
{
  "channel_name": {
    "lsb_entropy": float,            # Entropy of LSBs
    "lsb_randomness": float,         # Randomness score (0-1)
    "lsb_pattern_score": float      # Pattern detection score
  }
}
```

**Metrics:**
```python
{
  "bit_depth": int
}
```

**Visualization:** Not supported

---

### 9.2 `parity_analysis`

**Description:** Analyze parity bit patterns.

**Parameters:** None

**Measurements (per-channel):**
```python
{
  "channel_name": {
    "parity_entropy": float,         # Entropy of parity bits
    "parity_balance": float,         # Balance of 0s and 1s
    "parity_anomaly": float         # Anomaly score
  }
}
```

**Metrics:** `{}`

**Visualization:** Not supported

---

### 9.3 `quantization_noise`

**Description:** Analyze quantization noise structure.

**Parameters:**
- `quantization_bits` (int, default: `16`): Assumed quantization bit depth

**Measurements (per-channel):**
```python
{
  "channel_name": {
    "noise_floor": float,            # Estimated noise floor
    "noise_distribution": float,     # Distribution uniformity
    "noise_anomaly": float          # Anomaly score
  }
}
```

**Metrics:**
```python
{
  "quantization_bits": int
}
```

**Visualization:** Not supported

---

### 9.4 `signal_residual`

**Description:** Compare signal to prediction residual.

**Parameters:**
- `predictor_order` (int, default: `10`): Linear prediction order

**Measurements (per-channel):**
```python
{
  "channel_name": {
    "residual_energy": float,        # Energy in residual
    "prediction_gain": float,        # Signal/residual ratio (dB)
    "residual_structure": float     # Structure in residual (anomaly indicator)
  }
}
```

**Metrics:**
```python
{
  "predictor_order": int
}
```

**Visualization:** Not supported

---

### 9.5 `statistical_anomalies`

**Description:** Detect statistical anomalies in audio data.

**Parameters:**
- `window_size` (int, default: `2048`): Analysis window size

**Measurements (per-channel):**
```python
{
  "channel_name": {
    "anomaly_count": int,            # Number of anomalous windows
    "anomaly_ratio": float,          # Fraction of anomalous windows
    "max_anomaly_score": float,      # Maximum anomaly score
    "mean_anomaly_score": float     # Mean anomaly score
  }
}
```

**Metrics:**
```python
{
  "window_size": int
}
```

**Visualization:** Not supported

---

## 10. Meta-analysis (4 methods)

### 10.1 `high_order_statistics`

**Description:** Compute high-order statistical moments (skewness, kurtosis).

**Parameters:** None

**Measurements (per-channel):**
```python
{
  "channel_name": {
    "mean": float,              # First moment
    "variance": float,          # Second moment
    "skewness": float,          # Third moment (asymmetry)
    "kurtosis": float          # Fourth moment (tailedness)
  }
}
```

**Metrics:** `{}`

**Visualization:** Not supported

---

### 10.2 `stability_scores`

**Description:** Measure temporal and spectral stability.

**Parameters:**
- `window_size` (int, default: `2048`): Analysis window size
- `hop_length` (int, default: `512`): Hop between windows

**Measurements (per-channel):**
```python
{
  "channel_name": {
    "temporal_stability": float,     # Consistency of temporal features
    "spectral_stability": float,     # Consistency of spectral features
    "overall_stability": float      # Combined stability score
  }
}
```

**Metrics:**
```python
{
  "window_size": int,
  "hop_length": int
}
```

**Visualization:** Not supported

---

### 10.3 `inter_segment_comparison`

**Description:** Compare segments if segmentation is enabled.

**Parameters:** None (requires segmentation in preprocessing)

**Measurements (per-channel):**
```python
{
  "channel_name": {
    "num_segments": int,             # Number of segments
    "mean_similarity": float,        # Mean inter-segment similarity
    "segment_variance": float,       # Variance across segments
    "distinct_segments": int        # Number of distinct segment types
  }
}
```

**Metrics:** `{}`

**Visualization:** Not supported

**Requirements:** `preprocessing.segmentation.enabled: true` in protocol

---

### 10.4 `segment_clustering`

**Description:** Cluster segments based on features.

**Parameters:**
- `n_clusters` (int, default: `3`): Number of clusters
- `features` (list[str], default: `["energy", "zcr"]`): Features to use

**Measurements (per-channel):**
```python
{
  "channel_name": {
    "num_clusters": int,             # Number of clusters created
    "cluster_labels": list[int],     # Cluster assignment per segment
    "cluster_sizes": list[int],      # Number of segments per cluster
    "silhouette_score": float       # Clustering quality metric
  }
}
```

**Metrics:**
```python
{
  "n_clusters": int,
  "features": list[str]
}
```

**Visualization:** Not supported

**Requirements:** `preprocessing.segmentation.enabled: true` in protocol

**Dependencies:** May require `scikit-learn` - optional dependency, not required by SAT core

---

## 11. Summary statistics

### 11.1 Methods by category

| Category | Methods | With Visualization |
|----------|---------|-------------------|
| Temporal | 4 | 3 (envelope, autocorrelation, pulse_detection) |
| Spectral | 9 | 4 (fft_global, peak_detection, harmonic_analysis, cepstrum) |
| Time-frequency | 3 | 3 (stft, wavelet, band_stability) |
| Modulation | 5 | 3 (am_detection, fm_detection, phase_analysis) |
| Information | 5 | 1 (local_entropy) |
| Inter-channel | 4 | 1 (cross_correlation) |
| Steganography | 5 | 0 |
| Meta-analysis | 4 | 0 |
| **Total** | **39** | **15** |

### 11.2 Methods by scope

| Scope | Count | Examples |
|-------|-------|----------|
| Per-channel | 28 | envelope, fft_global, shannon_entropy, lsb_analysis |
| Global | 11 | mutual_information, lr_difference, cross_correlation, phase_difference |
| Mixed | 0 | (none currently) |

### 11.3 Performance-critical methods

Methods with **mandatory performance limits** (O(n²) or worse):

| Method | Limit | Default | Reason |
|--------|-------|---------|--------|
| `autocorrelation` | max_samples | 50,000 | O(n²) correlation computation |
| `cross_correlation` | max_samples | 50,000 | O(n²) per channel pair |
| `approximate_complexity` | max_samples | 5,000 | O(n²) pattern matching |
| `compression_ratio` | implicit | 100,000 | gzip compression time |
| `mutual_information` | implicit | 50,000 | 2D histogram computation |

---

## 12. Document status and maintenance

This catalog was generated on **2025-01-22** after comprehensive review of all analysis modules.

**Sources verified:**
- `audio_toolkit/analyses/temporal.py` (262 lines, 4 methods)
- `audio_toolkit/analyses/spectral.py` (533 lines, 9 methods)
- `audio_toolkit/analyses/time_frequency.py` (431 lines, 3 methods)
- `audio_toolkit/analyses/modulation.py` (379 lines, 5 methods)
- `audio_toolkit/analyses/information.py` (369 lines, 5 methods)
- `audio_toolkit/analyses/inter_channel.py` (305 lines, 4 methods)
- `audio_toolkit/analyses/steganography.py` (390 lines, 5 methods)
- `audio_toolkit/analyses/meta_analysis.py` (305 lines, 4 methods)

**Total:** 2,974 lines of analysis code documenting 39 methods.

**This catalog is believed to be complete and accurate at the time of writing (2025-01-22).** Parameters, measurement structures, and method behaviors are verified against source code, but may evolve in future versions.