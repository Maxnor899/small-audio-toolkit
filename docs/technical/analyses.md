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
### envelope
**Registry identifier:** `envelope`
**Function:** `envelope_analysis`

#### Objective

Amplitude envelope analysis

#### Parameters

| Name | Default (code) | Notes |
|---|---:|---|
| `method` | `'hilbert'` |  |
| `window_size` | `1024` |  |

#### Outputs

**Measurements:**

* `envelope_length`
* `envelope_max`
* `envelope_mean`
* `envelope_std`

**Visualization data:**

* `envelope`

---
### autocorrelation
**Registry identifier:** `autocorrelation`
**Function:** `autocorrelation_analysis`

#### Objective

Temporal autocorrelation

#### Parameters

| Name | Default (code) | Notes |
|---|---:|---|
| `max_lag` | `1000` |  |
| `max_samples` | `50000` |  |
| `normalize` | `True` |  |

#### Outputs

**Measurements:**

* `autocorr_max`
* `autocorr_mean`
* `first_peak_lag`
* `num_peaks`
* `periodicity_score`

**Visualization data:**

* `autocorr`

---
### pulse_detection
**Registry identifier:** `pulse_detection`
**Function:** `pulse_detection`

#### Objective

Pulse/impulse detection

#### Parameters

| Name | Default (code) | Notes |
|---|---:|---|
| `min_distance` | `100` |  |
| `threshold` | `0.5` |  |

#### Outputs

**Measurements:**

* `interval_mean`
* `interval_std`
* `num_pulses`
* `pulse_positions`
* `regularity_score`

**Visualization data:** *(none)*

---
### duration_ratios
**Registry identifier:** `duration_ratios`
**Function:** `duration_ratios`

#### Objective

Event interval ratios

#### Parameters

| Name | Default (code) | Notes |
|---|---:|---|
| `min_distance` | `100` |  |
| `threshold` | `0.3` |  |

#### Outputs

**Measurements:**

* `num_events`
* `num_intervals`
* `ratio_mean`
* `ratio_std`
* `ratios`

**Visualization data:** *(none)*

---
## Spectral Analyses (`analyses/spectral.py`)
### fft_global
**Registry identifier:** `fft_global`
**Function:** `fft_global`

#### Objective

Global FFT spectrum

#### Parameters

| Name | Default (code) | Notes |
|---|---:|---|
| `window` | `'hann'` |  |

#### Outputs

**Measurements:**

* `frequency_resolution`
* `n_fft`
* `peak_frequency`
* `peak_magnitude`
* `spectral_energy`

**Visualization data:**

* `frequencies`
* `magnitudes`

---
### peak_detection
**Registry identifier:** `peak_detection`
**Function:** `peak_detection`

#### Objective

Spectral peak detection

#### Parameters

| Name | Default (code) | Notes |
|---|---:|---|
| `distance` | `100` |  |
| `height` | `None` |  |
| `prominence` | `10.0` |  |

#### Outputs

**Measurements:**

* `dominant_frequency`
* `frequency_spread`
* `num_peaks`
* `peak_frequencies`
* `peak_magnitudes`

**Visualization data:**

* `peaks`
* `spectrum`

---
### harmonic_analysis
**Registry identifier:** `harmonic_analysis`
**Function:** `harmonic_analysis`

#### Objective

Harmonic structure analysis

#### Parameters

| Name | Default (code) | Notes |
|---|---:|---|
| `fundamental_range` | `[80.0, 400.0]` |  |
| `max_harmonics` | `10` |  |

#### Outputs

**Measurements:**

* `fundamental_frequency`
* `harmonic_numbers`
* `harmonic_ratios`
* `harmonicity_score`
* `harmonics_detected`

**Visualization data:**

* `frequencies`
* `fundamental`
* `harmonics`
* `spectrum`

---
### spectral_centroid
**Registry identifier:** `spectral_centroid`
**Function:** `spectral_centroid`

#### Objective

Spectral centroid

#### Outputs

**Measurements:**

* `normalized_centroid`
* `spectral_centroid`

**Visualization data:** *(none)*

---
### spectral_flatness
**Registry identifier:** `spectral_flatness`
**Function:** `spectral_flatness`

#### Objective

Spectral flatness

#### Outputs

**Measurements:**

* `spectral_flatness`
* `tonality`

**Visualization data:** *(none)*

---
### cepstrum
**Registry identifier:** `cepstrum`
**Function:** `cepstrum_analysis`

#### Objective

Cepstrum analysis

#### Outputs

**Measurements:**

* `cepstrum_mean`
* `cepstrum_std`
* `peak_magnitude`
* `peak_quefrency`
* `samples_analyzed`

**Visualization data:**

* `cepstrum`
* `peak_quefrency`
* `quefrency`

---
### spectral_bandwidth
**Registry identifier:** `spectral_bandwidth`
**Function:** `spectral_bandwidth`

#### Objective

Spectral bandwidth

#### Outputs

**Measurements:**

* `spectral_bandwidth`
* `spectral_centroid_Hz`

**Visualization data:** *(none)*

---
## Time–Frequency Analyses (`analyses/time_frequency.py`)
### stft
**Registry identifier:** `stft`
**Function:** `stft_analysis`

#### Objective

Short-Time Fourier Transform

#### Parameters

| Name | Default (code) | Notes |
|---|---:|---|
| `hop_length` | `512` |  |
| `window_size` | `2048` |  |
| `window_type` | `'hann'` |  |

#### Outputs

**Measurements:**

* `dominant_freq_mean`
* `dominant_freq_std`
* `frequency_resolution`
* `max_magnitude`
* `mean_magnitude`
* `num_freq_bins`
* `num_time_frames`
* `spectral_flux_max`
* `spectral_flux_mean`
* `temporal_stability`
* `time_resolution`

**Visualization data:**

* `frequencies`
* `stft_matrix`
* `times`

---
### cqt
**Registry identifier:** `cqt`
**Function:** `cqt_analysis`

#### Objective

Constant-Q Transform

#### Parameters

| Name | Default (code) | Notes |
|---|---:|---|
| `bins_per_octave` | `12` |  |
| `fmin` | `32.70319566257483` |  |
| `hop_length` | `512` |  |
| `max_samples` | `200000` |  |
| `max_time_frames` | `500` |  |
| `n_bins` | `84` |  |

#### Outputs

**Measurements:**

* `bins_per_octave`
* `fmin_hz`
* `hop_length`
* `max_magnitude_db`
* `mean_magnitude_db`
* `n_bins`
* `note`
* `num_freq_bins`
* `num_time_frames`
* `samples_analyzed`

**Visualization data:**

* `cqt_db`
* `frequencies`
* `times`

**Registry default_params:**

```python
{'hop_length': 512, 'fmin': 32.70319566257483, 'n_bins': 84, 'bins_per_octave': 12, 'max_time_frames': 500, 'max_samples': 200000}
```

---
### wavelet
**Registry identifier:** `wavelet`
**Function:** `wavelet_analysis`

#### Objective

Wavelet transform

#### Parameters

| Name | Default (code) | Notes |
|---|---:|---|
| `num_scales` | `64` |  |
| `wavelet` | `'morlet'` |  |

#### Outputs

**Measurements:**

* `energy_concentration`
* `max_magnitude`
* `mean_magnitude`
* `num_scales`
* `samples_analyzed`
* `scale_of_max`

**Visualization data:**

* `scales`
* `scalogram`

---
### band_stability
**Registry identifier:** `band_stability`
**Function:** `band_stability`

#### Objective

Frequency band stability

#### Parameters

| Name | Default (code) | Notes |
|---|---:|---|
| `bands` | `[(0, 100), (100, 500), (500, 2000), (2000, 8000), (8000, 20000)]` |  |
| `hop_length` | `512` |  |
| `window_size` | `2048` |  |

#### Outputs

**Measurements:**

* `band_stability_data`

**Visualization data:**

* `bands_data`
* `times`

---
## Modulation Analyses (`analyses/modulation.py`)
### am_detection
**Registry identifier:** `am_detection`
**Function:** `am_detection`

#### Objective

AM detection

#### Outputs

**Measurements:**

* `dominant_modulation_freq`
* `envelope_mean`
* `envelope_std`
* `modulation_depth`
* `modulation_detected`
* `modulation_frequencies`
* `modulation_index`
* `modulation_magnitudes`
* `num_modulation_frequencies`

**Visualization data:**

* `envelope`
* `modulation_frequencies`
* `modulation_spectrum`
* `time`

---
### fm_detection
**Registry identifier:** `fm_detection`
**Function:** `fm_detection`

#### Objective

FM detection

#### Outputs

**Measurements:**

* `carrier_frequency_mean`
* `fm_detected`
* `fm_modulation_frequencies`
* `frequency_deviation`
* `frequency_range`
* `frequency_std`
* `modulation_index_fm`
* `num_fm_components`

**Visualization data:**

* `carrier_frequency`
* `instantaneous_frequency`
* `time`

---
### phase_analysis
**Registry identifier:** `phase_analysis`
**Function:** `phase_analysis`

#### Objective

Phase analysis

#### Outputs

**Measurements:**

* `num_phase_jumps`
* `phase_coherence`
* `phase_jump_rate`
* `phase_mean`
* `phase_range`
* `phase_std`
* `unwrapped_phase_total`

**Visualization data:**

* `jumps`
* `phase`
* `time`

---
### modulation_index
**Registry identifier:** `modulation_index`
**Function:** `modulation_index`

#### Objective

Modulation index

#### Outputs

**Measurements:**

* `ac_component`
* `dc_component`
* `modulation_depth`
* `modulation_index`
* `peak_to_average_ratio`

**Visualization data:** *(none)*

---
## Information Analyses (`analyses/information.py`)
### shannon_entropy
**Registry identifier:** `shannon_entropy`
**Function:** `shannon_entropy`

#### Objective

Shannon entropy

#### Parameters

| Name | Default (code) | Notes |
|---|---:|---|
| `num_bins` | `256` |  |

#### Outputs

**Measurements:**

* `max_entropy`
* `normalized_entropy`
* `num_bins`
* `shannon_entropy`

**Visualization data:** *(none)*

---
### local_entropy
**Registry identifier:** `local_entropy`
**Function:** `local_entropy`

#### Objective

Local windowed entropy

#### Parameters

| Name | Default (code) | Notes |
|---|---:|---|
| `hop_length` | `512` |  |
| `num_bins` | `64` |  |
| `window_size` | `2048` |  |

#### Outputs

**Measurements:**

* `entropy_variation`
* `max_entropy`
* `mean_entropy`
* `min_entropy`
* `num_windows`
* `std_entropy`

**Visualization data:** *(none)*

---
### compression_ratio
**Registry identifier:** `compression_ratio`
**Function:** `compression_ratio`

#### Objective

Compression ratio

#### Outputs

**Measurements:**

* `compressed_size`
* `compression_ratio`
* `original_size`
* `samples_analyzed`

**Visualization data:** *(none)*

---
### approximate_complexity
**Registry identifier:** `approximate_complexity`
**Function:** `approximate_complexity`

#### Objective

Approximate complexity

#### Parameters

| Name | Default (code) | Notes |
|---|---:|---|
| `m` | `2` |  |
| `r_factor` | `0.2` |  |

#### Outputs

**Measurements:**

* `approximate_complexity`
* `pattern_length`
* `samples_analyzed`
* `tolerance`

**Visualization data:** *(none)*

---
## Inter-Channel Analyses (`analyses/inter_channel.py`)
### cross_correlation
**Registry identifier:** `cross_correlation`
**Function:** `cross_correlation`

#### Objective

Cross-correlation

#### Parameters

| Name | Default (code) | Notes |
|---|---:|---|
| `max_lag` | `1000` |  |
| `max_samples` | `50000` |  |

#### Outputs

**Measurements:**

* `correlation_at_zero`
* `max_correlation`
* `mean_correlation`
* `peak_lag`
* `peak_value`

**Visualization data:**

* `correlation`
* `lags`

---
### lr_difference
**Registry identifier:** `lr_difference`
**Function:** `lr_difference`

#### Objective

L-R difference

#### Outputs

**Measurements:**

* `contains_unique_info`
* `difference_energy`
* `difference_peak_freq`
* `difference_peak_magnitude`
* `difference_rms`
* `energy_ratio`
* `left_energy`
* `right_energy`

**Visualization data:**

* `frequencies`
* `spectrum`
* `waveform`

---
### phase_difference
**Registry identifier:** `phase_difference`
**Function:** `phase_difference`

#### Objective

Phase difference

#### Outputs

**Measurements:**

* `in_phase`
* `out_of_phase`
* `phase_coherence`
* `phase_diff_mean`
* `phase_diff_range`
* `phase_diff_std`

**Visualization data:** *(none)*

---
### time_delay
**Registry identifier:** `time_delay`
**Function:** `time_delay`

#### Objective

Time delay (ITD)

#### Parameters

| Name | Default (code) | Notes |
|---|---:|---|
| `max_delay_samples` | `100` |  |
| `max_samples` | `50000` |  |

#### Outputs

**Measurements:**

* `correlation_at_delay`
* `delay_ms`
* `delay_samples`
* `is_synchronized`

**Visualization data:** *(none)*

---
## Steganography Analyses (`analyses/steganography.py`)
### lsb_analysis
**Registry identifier:** `lsb_analysis`
**Function:** `lsb_analysis`

#### Objective

LSB analysis

#### Outputs

**Measurements:**

* `lsb_mean`
* `lsb_std`
* `mean_one_run`
* `mean_zero_run`
* `samples_analyzed`
* `transition_rate`

**Visualization data:** *(none)*

---
### quantization_noise
**Registry identifier:** `quantization_noise`
**Function:** `quantization_noise`

#### Objective

Quantization noise structure

#### Outputs

**Measurements:**

* `autocorr_peak`
* `noise_power`
* `noise_std`
* `samples_analyzed`
* `spectral_flatness`

**Visualization data:** *(none)*

---
### signal_residual
**Registry identifier:** `signal_residual`
**Function:** `signal_residual`

#### Objective

Signal vs residual comparison

#### Parameters

| Name | Default (code) | Notes |
|---|---:|---|
| `cutoff_freq` | `1000` |  |

#### Outputs

**Measurements:**

* `energy_ratio`
* `residual_peak_freq`
* `residual_power`
* `samples_analyzed`
* `signal_power`
* `snr_db`

**Visualization data:** *(none)*

---
## Meta-Analyses (`analyses/meta_analysis.py`)
### inter_segment_comparison
**Registry identifier:** `inter_segment_comparison`
**Function:** `inter_segment_comparison`

#### Objective

Inter-segment comparison

#### Parameters

| Name | Default (code) | Notes |
|---|---:|---|
| `num_segments` | `10` |  |

#### Outputs

**Measurements:**

* `max_distance`
* `mean_distance`
* `min_distance`
* `num_segments`
* `similarity_score`
* `std_distance`

**Visualization data:** *(none)*

---
### segment_clustering
**Registry identifier:** `segment_clustering`
**Function:** `segment_clustering`

#### Objective

Segment clustering

#### Parameters

| Name | Default (code) | Notes |
|---|---:|---|
| `num_segments` | `20` |  |

#### Outputs

**Measurements:**

* `avg_intra_distance`
* `num_segments`
* `repetition_rate`
* `unique_segments`

**Visualization data:** *(none)*

---
### stability_scores
**Registry identifier:** `stability_scores`
**Function:** `stability_scores`

#### Objective

Temporal/spectral stability

#### Parameters

| Name | Default (code) | Notes |
|---|---:|---|
| `hop_length` | `512` |  |
| `window_size` | `2048` |  |

#### Outputs

**Measurements:**

* `energy_stability`
* `num_windows`
* `overall_stability`
* `spectral_stability`

**Visualization data:** *(none)*

---
