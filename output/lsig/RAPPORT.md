# Audio Analysis Report

**Analysis timestamp:** 2026-01-13T11:48:25.925673
**Input file:** lsig.flac

## File Information

- Duration: 109.63 seconds
- Sample rate: 48000 Hz
- Channels: 2
- Format: FLAC / PCM_16
- Total frames: 5262400

## Preprocessing Applied

### normalize
- method: rms
- target_level: -20.0

### silence_detection
- threshold_db: -40.0
- min_duration: 0.1

## Measurement Summary

This section provides key measured values across all channels.
Reference thresholds are provided for context only.

### Periodicity Score (Autocorrelation)

**Measured values:**

- left: 0.999
- right: 0.999
- sum: 1.000
- difference: 0.993

**Reference thresholds:** high > 0.8, very_high > 0.95
**Unit:** normalized (0-1)

### Harmonicity Score

**Measured values:**

- left: 1.000
- right: 1.000
- sum: 1.000
- difference: 1.000

**Reference thresholds:** harmonic > 0.7, strongly_harmonic > 0.9
**Unit:** normalized (0-1)

### Fundamental Frequency

**Measured values:**

- left: 65.965
- right: 65.965
- sum: 65.965
- difference: 393.019
**Unit:** Hz

### Tonality (1 - Spectral Flatness)

**Measured values:**

- left: 0.954
- right: 0.957
- sum: 0.963
- difference: 0.930

**Reference thresholds:** tonal > 0.7, highly_tonal > 0.9
**Unit:** normalized (0-1)

### Modulation Index (AM)

**Measured values:**

- left: 0.537
- right: 0.538
- sum: 0.538
- difference: 0.653

**Reference thresholds:** low < 0.1, moderate < 0.3, high > 0.5
**Unit:** ratio (AC/DC)

### Phase Coherence

**Measured values:**

- left: 0.000e+00
- right: 0.000e+00
- sum: 0.000e+00
- difference: 0.125

**Reference thresholds:** low < 0.3, moderate < 0.6, high > 0.8
**Unit:** normalized (0-1)

## Detailed Measurements by Category

### TEMPORAL

#### Method: envelope

**Key metrics to observe:**

- **left:**
  - envelope_mean: 0.125
  - envelope_max: 0.560
  - envelope_std: 0.067
- **right:**
  - envelope_mean: 0.125
  - envelope_max: 0.608
  - envelope_std: 0.067
- **sum:**
  - envelope_mean: 0.125
  - envelope_max: 0.594
  - envelope_std: 0.067
- **difference:**
  - envelope_mean: 0.118
  - envelope_max: 0.785
  - envelope_std: 0.077

**Parameters:**

- method: hilbert

<details>
<summary><b>All measurements (click to expand)</b></summary>

**Channel: left**

- envelope_mean: 0.125
- envelope_max: 0.560
- envelope_std: 0.067
- envelope_length: 5262400

**Channel: right**

- envelope_mean: 0.125
- envelope_max: 0.608
- envelope_std: 0.067
- envelope_length: 5262400

**Channel: sum**

- envelope_mean: 0.125
- envelope_max: 0.594
- envelope_std: 0.067
- envelope_length: 5262400

**Channel: difference**

- envelope_mean: 0.118
- envelope_max: 0.785
- envelope_std: 0.077
- envelope_length: 5262400

</details>

---

#### Method: autocorrelation

**Key metrics to observe:**

- **left:**
  - periodicity_score: 0.999
  - first_peak_lag: 54
  - num_peaks: 5
- **right:**
  - periodicity_score: 0.999
  - first_peak_lag: 52
  - num_peaks: 7
- **sum:**
  - periodicity_score: 1.000
  - first_peak_lag: 675
  - num_peaks: 3
- **difference:**
  - periodicity_score: 0.993
  - first_peak_lag: 57
  - num_peaks: 18

**Parameters:**

- max_lag: 1000
- normalized: True
- max_samples: 50000

<details>
<summary><b>All measurements (click to expand)</b></summary>

**Channel: left**

- autocorr_max: 0.999
- autocorr_mean: 0.009
- first_peak_lag: 54
- num_peaks: 5
- periodicity_score: 0.999

**Channel: right**

- autocorr_max: 0.999
- autocorr_mean: 0.009
- first_peak_lag: 52
- num_peaks: 7
- periodicity_score: 0.999

**Channel: sum**

- autocorr_max: 1.000
- autocorr_mean: 0.010
- first_peak_lag: 675
- num_peaks: 3
- periodicity_score: 1.000

**Channel: difference**

- autocorr_max: 0.993
- autocorr_mean: 0.002
- first_peak_lag: 57
- num_peaks: 18
- periodicity_score: 0.993

</details>

---

#### Method: pulse_detection

**Key metrics to observe:**

- **left:**
  - num_pulses: 2818
  - interval_mean: 1842.492
  - regularity_score: 0.000e+00
- **right:**
  - num_pulses: 1891
  - interval_mean: 2735.688
  - regularity_score: 0.000e+00
- **sum:**
  - num_pulses: 1868
  - interval_mean: 2647.499
  - regularity_score: 0.000e+00
- **difference:**
  - num_pulses: 1083
  - interval_mean: 4312.419
  - regularity_score: 0.000e+00

**Parameters:**

- threshold: 0.500
- min_distance: 100

<details>
<summary><b>All measurements (click to expand)</b></summary>

**Channel: left**

- num_pulses: 2818
- interval_mean: 1842.492
- interval_std: 4784.619
- regularity_score: 0.000e+00

**Channel: right**

- num_pulses: 1891
- interval_mean: 2735.688
- interval_std: 7482.272
- regularity_score: 0.000e+00

**Channel: sum**

- num_pulses: 1868
- interval_mean: 2647.499
- interval_std: 6421.591
- regularity_score: 0.000e+00

**Channel: difference**

- num_pulses: 1083
- interval_mean: 4312.419
- interval_std: 29772.817
- regularity_score: 0.000e+00

</details>

---

#### Method: duration_ratios

**Parameters:**

- threshold: 0.500

<details>
<summary><b>All measurements (click to expand)</b></summary>

**Channel: left**

- num_events: 2818
- num_intervals: 2817
- ratio_mean: 8.428
- ratio_std: 24.683

**Channel: right**

- num_events: 1891
- num_intervals: 1890
- ratio_mean: 11.516
- ratio_std: 41.874

**Channel: sum**

- num_events: 1868
- num_intervals: 1867
- ratio_mean: 12.902
- ratio_std: 42.994

**Channel: difference**

- num_events: 1083
- num_intervals: 1082
- ratio_mean: 3.724
- ratio_std: 10.623

</details>

---

### SPECTRAL

#### Method: fft_global

**Key metrics to observe:**

- **left:**
  - peak_frequency: 65.965
  - peak_magnitude: 40227.295
  - spectral_energy: 5.573e+10
- **right:**
  - peak_frequency: 65.965
  - peak_magnitude: 39675.806
  - spectral_energy: 5.584e+10
- **sum:**
  - peak_frequency: 65.965
  - peak_magnitude: 40761.736
  - spectral_energy: 5.594e+10
- **difference:**
  - peak_frequency: 391.998
  - peak_magnitude: 11707.582
  - spectral_energy: 5.205e+10

**Parameters:**

- window: hann
- sample_rate: 48000

<details>
<summary><b>All measurements (click to expand)</b></summary>

**Channel: left**

- n_fft: 5262400
- frequency_resolution: 0.009
- peak_frequency: 65.965
- peak_magnitude: 40227.295
- spectral_energy: 5.573e+10

**Channel: right**

- n_fft: 5262400
- frequency_resolution: 0.009
- peak_frequency: 65.965
- peak_magnitude: 39675.806
- spectral_energy: 5.584e+10

**Channel: sum**

- n_fft: 5262400
- frequency_resolution: 0.009
- peak_frequency: 65.965
- peak_magnitude: 40761.736
- spectral_energy: 5.594e+10

**Channel: difference**

- n_fft: 5262400
- frequency_resolution: 0.009
- peak_frequency: 391.998
- peak_magnitude: 11707.582
- spectral_energy: 5.205e+10

</details>

---

#### Method: peak_detection

**Key metrics to observe:**

- **left:**
  - num_peaks: 19690
  - dominant_frequency: 0.867
  - frequency_spread: 6930.628
- **right:**
  - num_peaks: 19650
  - dominant_frequency: 0.638
  - frequency_spread: 6931.842
- **sum:**
  - num_peaks: 19649
  - dominant_frequency: 0.638
  - frequency_spread: 6928.734
- **difference:**
  - num_peaks: 19609
  - dominant_frequency: 0.374
  - frequency_spread: 6937.689

**Parameters:**

- prominence: 0.010
- distance: 100

<details>
<summary><b>All measurements (click to expand)</b></summary>

**Channel: left**

- num_peaks: 19690
- dominant_frequency: 0.867
- frequency_spread: 6930.628

**Channel: right**

- num_peaks: 19650
- dominant_frequency: 0.638
- frequency_spread: 6931.842

**Channel: sum**

- num_peaks: 19649
- dominant_frequency: 0.638
- frequency_spread: 6928.734

**Channel: difference**

- num_peaks: 19609
- dominant_frequency: 0.374
- frequency_spread: 6937.689

</details>

---

#### Method: harmonic_analysis

**Key metrics to observe:**

- **left:**
  - fundamental_frequency: 65.965
  - harmonicity_score: 1.000
  - harmonics_detected: 10
- **right:**
  - fundamental_frequency: 65.965
  - harmonicity_score: 1.000
  - harmonics_detected: 10
- **sum:**
  - fundamental_frequency: 65.965
  - harmonicity_score: 1.000
  - harmonics_detected: 10
- **difference:**
  - fundamental_frequency: 393.019
  - harmonicity_score: 1.000
  - harmonics_detected: 10

**Parameters:**

- fundamental_range: [50, 500]
- max_harmonics: 10

<details>
<summary><b>All measurements (click to expand)</b></summary>

**Channel: left**

- fundamental_frequency: 65.965
- harmonics_detected: 10
- harmonicity_score: 1.000

**Channel: right**

- fundamental_frequency: 65.965
- harmonics_detected: 10
- harmonicity_score: 1.000

**Channel: sum**

- fundamental_frequency: 65.965
- harmonics_detected: 10
- harmonicity_score: 1.000

**Channel: difference**

- fundamental_frequency: 393.019
- harmonics_detected: 10
- harmonicity_score: 1.000

</details>

---

#### Method: spectral_centroid

**Key metrics to observe:**

- **left:**
  - spectral_centroid: 1097.006
  - normalized_centroid: 0.046
- **right:**
  - spectral_centroid: 1087.009
  - normalized_centroid: 0.045
- **sum:**
  - spectral_centroid: 1038.323
  - normalized_centroid: 0.043
- **difference:**
  - spectral_centroid: 1404.339
  - normalized_centroid: 0.059

<details>
<summary><b>All measurements (click to expand)</b></summary>

**Channel: left**

- spectral_centroid: 1097.006
- normalized_centroid: 0.046

**Channel: right**

- spectral_centroid: 1087.009
- normalized_centroid: 0.045

**Channel: sum**

- spectral_centroid: 1038.323
- normalized_centroid: 0.043

**Channel: difference**

- spectral_centroid: 1404.339
- normalized_centroid: 0.059

</details>

---

#### Method: spectral_flatness

**Key metrics to observe:**

- **left:**
  - spectral_flatness: 0.046
  - tonality: 0.954
- **right:**
  - spectral_flatness: 0.043
  - tonality: 0.957
- **sum:**
  - spectral_flatness: 0.037
  - tonality: 0.963
- **difference:**
  - spectral_flatness: 0.070
  - tonality: 0.930

<details>
<summary><b>All measurements (click to expand)</b></summary>

**Channel: left**

- spectral_flatness: 0.046
- tonality: 0.954

**Channel: right**

- spectral_flatness: 0.043
- tonality: 0.957

**Channel: sum**

- spectral_flatness: 0.037
- tonality: 0.963

**Channel: difference**

- spectral_flatness: 0.070
- tonality: 0.930

</details>

---

#### Method: cepstrum

<details>
<summary><b>All measurements (click to expand)</b></summary>

**Channel: left**

- peak_quefrency: 2.083e-05
- peak_magnitude: 0.683
- cepstrum_mean: 0.001
- cepstrum_std: 0.009
- samples_analyzed: 100000

**Channel: right**

- peak_quefrency: 2.083e-05
- peak_magnitude: 0.703
- cepstrum_mean: 0.002
- cepstrum_std: 0.010
- samples_analyzed: 100000

**Channel: sum**

- peak_quefrency: 2.083e-05
- peak_magnitude: 0.665
- cepstrum_mean: 0.001
- cepstrum_std: 0.009
- samples_analyzed: 100000

**Channel: difference**

- peak_quefrency: 2.083e-05
- peak_magnitude: 0.741
- cepstrum_mean: 0.002
- cepstrum_std: 0.007
- samples_analyzed: 100000

</details>

---

#### Method: spectral_bandwidth

<details>
<summary><b>All measurements (click to expand)</b></summary>

**Channel: left**

- spectral_bandwidth: 287.922
- spectral_centroid_Hz: 160.907

**Channel: right**

- spectral_bandwidth: 307.451
- spectral_centroid_Hz: 178.145

**Channel: sum**

- spectral_bandwidth: 267.026
- spectral_centroid_Hz: 144.241

**Channel: difference**

- spectral_bandwidth: 344.414
- spectral_centroid_Hz: 787.472

</details>

---

### TIME_FREQUENCY

#### Method: stft

**Key metrics to observe:**

- **left:**
  - temporal_stability: 0.719
  - dominant_freq_mean: 67.935
  - spectral_flux_mean: 0.034
- **right:**
  - temporal_stability: 0.711
  - dominant_freq_mean: 72.390
  - spectral_flux_mean: 0.034
- **sum:**
  - temporal_stability: 0.693
  - dominant_freq_mean: 66.601
  - spectral_flux_mean: 0.034
- **difference:**
  - temporal_stability: 0.669
  - dominant_freq_mean: 670.383
  - spectral_flux_mean: 0.035

**Parameters:**

- window_size: 2048
- hop_length: 512
- window_type: hann

<details>
<summary><b>All measurements (click to expand)</b></summary>

**Channel: left**

| Metric | Value |
|--------|-------|
| num_time_frames | 10280 |
| num_freq_bins | 1025 |
| frequency_resolution | 23.438 |
| time_resolution | 0.011 |
| mean_magnitude | 3.452e-04 |
| max_magnitude | 0.140 |
| dominant_freq_mean | 67.935 |
| dominant_freq_std | 66.249 |
| spectral_flux_mean | 0.034 |
| spectral_flux_max | 0.097 |
| temporal_stability | 0.719 |

**Channel: right**

| Metric | Value |
|--------|-------|
| num_time_frames | 10280 |
| num_freq_bins | 1025 |
| frequency_resolution | 23.438 |
| time_resolution | 0.011 |
| mean_magnitude | 3.550e-04 |
| max_magnitude | 0.140 |
| dominant_freq_mean | 72.390 |
| dominant_freq_std | 86.759 |
| spectral_flux_mean | 0.034 |
| spectral_flux_max | 0.096 |
| temporal_stability | 0.711 |

**Channel: sum**

| Metric | Value |
|--------|-------|
| num_time_frames | 10280 |
| num_freq_bins | 1025 |
| frequency_resolution | 23.438 |
| time_resolution | 0.011 |
| mean_magnitude | 3.243e-04 |
| max_magnitude | 0.143 |
| dominant_freq_mean | 66.601 |
| dominant_freq_std | 57.614 |
| spectral_flux_mean | 0.034 |
| spectral_flux_max | 0.098 |
| temporal_stability | 0.693 |

**Channel: difference**

| Metric | Value |
|--------|-------|
| num_time_frames | 10280 |
| num_freq_bins | 1025 |
| frequency_resolution | 23.438 |
| time_resolution | 0.011 |
| mean_magnitude | 5.326e-04 |
| max_magnitude | 0.136 |
| dominant_freq_mean | 670.383 |
| dominant_freq_std | 227.987 |
| spectral_flux_mean | 0.035 |
| spectral_flux_max | 0.097 |
| temporal_stability | 0.669 |

</details>

---

#### Method: band_stability

**Key metrics to observe:**

**Parameters:**

- num_bands: 5
- bands: [[0, 100], [100, 500], [500, 2000], [2000, 8000], [8000, 20000]]

<details>
<summary><b>All measurements (click to expand)</b></summary>

**Channel: left**


**Channel: right**


**Channel: sum**


**Channel: difference**


</details>

---

#### Method: wavelet

**Key metrics to observe:**

**Parameters:**

- execution_failed: True

<details>
<summary><b>All measurements (click to expand)</b></summary>

</details>

---

### MODULATION

#### Method: am_detection

**Key metrics to observe:**

- **left:**
  - modulation_detected: False
  - modulation_index: 0.537
  - modulation_depth: 4.493
- **right:**
  - modulation_detected: False
  - modulation_index: 0.538
  - modulation_depth: 4.880
- **sum:**
  - modulation_detected: False
  - modulation_index: 0.538
  - modulation_depth: 4.768
- **difference:**
  - modulation_detected: False
  - modulation_index: 0.653
  - modulation_depth: 6.629

<details>
<summary><b>All measurements (click to expand)</b></summary>

**Channel: left**

| Metric | Value |
|--------|-------|
| modulation_detected | False |
| num_modulation_frequencies | 0 |
| dominant_modulation_freq | 0.000e+00 |
| modulation_depth | 4.493 |
| modulation_index | 0.537 |
| envelope_mean | 0.125 |
| envelope_std | 0.067 |

**Channel: right**

| Metric | Value |
|--------|-------|
| modulation_detected | False |
| num_modulation_frequencies | 0 |
| dominant_modulation_freq | 0.000e+00 |
| modulation_depth | 4.880 |
| modulation_index | 0.538 |
| envelope_mean | 0.125 |
| envelope_std | 0.067 |

**Channel: sum**

| Metric | Value |
|--------|-------|
| modulation_detected | False |
| num_modulation_frequencies | 0 |
| dominant_modulation_freq | 0.000e+00 |
| modulation_depth | 4.768 |
| modulation_index | 0.538 |
| envelope_mean | 0.125 |
| envelope_std | 0.067 |

**Channel: difference**

| Metric | Value |
|--------|-------|
| modulation_detected | False |
| num_modulation_frequencies | 0 |
| dominant_modulation_freq | 0.000e+00 |
| modulation_depth | 6.629 |
| modulation_index | 0.653 |
| envelope_mean | 0.118 |
| envelope_std | 0.077 |

</details>

---

#### Method: fm_detection

**Key metrics to observe:**

- **left:**
  - fm_detected: True
  - frequency_deviation: 601.477
  - carrier_frequency_mean: 159.077
- **right:**
  - fm_detected: True
  - frequency_deviation: 626.681
  - carrier_frequency_mean: 173.165
- **sum:**
  - fm_detected: True
  - frequency_deviation: 547.191
  - carrier_frequency_mean: 141.579
- **difference:**
  - fm_detected: True
  - frequency_deviation: 742.770
  - carrier_frequency_mean: 776.586

<details>
<summary><b>All measurements (click to expand)</b></summary>

**Channel: left**

| Metric | Value |
|--------|-------|
| fm_detected | True |
| carrier_frequency_mean | 159.077 |
| frequency_deviation | 601.477 |
| frequency_range | 47990.809 |
| frequency_std | 601.477 |
| num_fm_components | 0 |
| modulation_index_fm | 3.781 |

**Channel: right**

| Metric | Value |
|--------|-------|
| fm_detected | True |
| carrier_frequency_mean | 173.165 |
| frequency_deviation | 626.681 |
| frequency_range | 48000.133 |
| frequency_std | 626.681 |
| num_fm_components | 0 |
| modulation_index_fm | 3.619 |

**Channel: sum**

| Metric | Value |
|--------|-------|
| fm_detected | True |
| carrier_frequency_mean | 141.579 |
| frequency_deviation | 547.191 |
| frequency_range | 48000.133 |
| frequency_std | 547.191 |
| num_fm_components | 1 |
| modulation_index_fm | 3.865 |

**Channel: difference**

| Metric | Value |
|--------|-------|
| fm_detected | True |
| carrier_frequency_mean | 776.586 |
| frequency_deviation | 742.770 |
| frequency_range | 48223.945 |
| frequency_std | 742.770 |
| num_fm_components | 0 |
| modulation_index_fm | 0.956 |

</details>

---

#### Method: phase_analysis

**Key metrics to observe:**

- **left:**
  - phase_coherence: 0.000e+00
  - num_phase_jumps: 34673
  - phase_std: 1.814
- **right:**
  - phase_coherence: 0.000e+00
  - num_phase_jumps: 36966
  - phase_std: 1.814
- **sum:**
  - phase_coherence: 0.000e+00
  - num_phase_jumps: 30865
  - phase_std: 1.815
- **difference:**
  - phase_coherence: 0.125
  - num_phase_jumps: 94594
  - phase_std: 1.813

<details>
<summary><b>All measurements (click to expand)</b></summary>

**Channel: left**

| Metric | Value |
|--------|-------|
| phase_mean | -0.022 |
| phase_std | 1.814 |
| phase_range | 6.283 |
| unwrapped_phase_total | 109579.500 |
| phase_coherence | 0.000e+00 |
| num_phase_jumps | 34673 |
| phase_jump_rate | 316.263 |

**Channel: right**

| Metric | Value |
|--------|-------|
| phase_mean | -0.022 |
| phase_std | 1.814 |
| phase_range | 6.283 |
| unwrapped_phase_total | 119283.930 |
| phase_coherence | 0.000e+00 |
| num_phase_jumps | 36966 |
| phase_jump_rate | 337.178 |

**Channel: sum**

| Metric | Value |
|--------|-------|
| phase_mean | -0.022 |
| phase_std | 1.815 |
| phase_range | 6.283 |
| unwrapped_phase_total | 97526.016 |
| phase_coherence | 0.000e+00 |
| num_phase_jumps | 30865 |
| phase_jump_rate | 281.529 |

**Channel: difference**

| Metric | Value |
|--------|-------|
| phase_mean | 0.001 |
| phase_std | 1.813 |
| phase_range | 6.283 |
| unwrapped_phase_total | 534948.188 |
| phase_coherence | 0.125 |
| num_phase_jumps | 94594 |
| phase_jump_rate | 862.822 |

</details>

---

#### Method: modulation_index

**Key metrics to observe:**

- **left:**
  - modulation_index: 0.537
  - modulation_depth: 4.493
  - peak_to_average_ratio: 4.493
- **right:**
  - modulation_index: 0.538
  - modulation_depth: 4.880
  - peak_to_average_ratio: 4.880
- **sum:**
  - modulation_index: 0.538
  - modulation_depth: 4.768
  - peak_to_average_ratio: 4.769
- **difference:**
  - modulation_index: 0.653
  - modulation_depth: 6.629
  - peak_to_average_ratio: 6.629

<details>
<summary><b>All measurements (click to expand)</b></summary>

**Channel: left**

- modulation_index: 0.537
- modulation_depth: 4.493
- ac_component: 0.067
- dc_component: 0.125
- peak_to_average_ratio: 4.493

**Channel: right**

- modulation_index: 0.538
- modulation_depth: 4.880
- ac_component: 0.067
- dc_component: 0.125
- peak_to_average_ratio: 4.880

**Channel: sum**

- modulation_index: 0.538
- modulation_depth: 4.768
- ac_component: 0.067
- dc_component: 0.125
- peak_to_average_ratio: 4.769

**Channel: difference**

- modulation_index: 0.653
- modulation_depth: 6.629
- ac_component: 0.077
- dc_component: 0.118
- peak_to_average_ratio: 6.629

</details>

---

### INTER_CHANNEL

#### Method: cross_correlation

**Key metrics to observe:**

- **left_vs_right:**
  - max_correlation: 1.061
  - peak_lag: 22
  - correlation_at_zero: 1.000
- **left_vs_sum:**
  - max_correlation: 1.000
  - peak_lag: 0
  - correlation_at_zero: 1.000
- **left_vs_difference:**
  - max_correlation: 1.000
  - peak_lag: 0
  - correlation_at_zero: 1.000
- **right_vs_sum:**
  - max_correlation: 1.000
  - peak_lag: 0
  - correlation_at_zero: 1.000
- **right_vs_difference:**
  - max_correlation: 1.000
  - peak_lag: 0
  - correlation_at_zero: 1.000
- **sum_vs_difference:**
  - max_correlation: 1.369
  - peak_lag: 389
  - correlation_at_zero: 1.000

**Parameters:**

- max_lag: 1000
- max_samples: 50000

<details>
<summary><b>All measurements (click to expand)</b></summary>

**Channel: left_vs_right**

- max_correlation: 1.061
- peak_lag: 22
- peak_value: 1.061
- mean_correlation: 0.010
- correlation_at_zero: 1.000

**Channel: left_vs_sum**

- max_correlation: 1.000
- peak_lag: 0
- peak_value: 1.000
- mean_correlation: 0.010
- correlation_at_zero: 1.000

**Channel: left_vs_difference**

- max_correlation: 1.000
- peak_lag: 0
- peak_value: 1.000
- mean_correlation: 0.002
- correlation_at_zero: 1.000

**Channel: right_vs_sum**

- max_correlation: 1.000
- peak_lag: 0
- peak_value: 1.000
- mean_correlation: 0.010
- correlation_at_zero: 1.000

**Channel: right_vs_difference**

- max_correlation: 1.000
- peak_lag: 0
- peak_value: 1.000
- mean_correlation: 0.003
- correlation_at_zero: 1.000

**Channel: sum_vs_difference**

- max_correlation: 1.369
- peak_lag: 389
- peak_value: -1.369
- mean_correlation: 0.007
- correlation_at_zero: 1.000

</details>

---

#### Method: lr_difference

**Key metrics to observe:**

- **lr_difference:**
  - energy_ratio: 0.079
  - difference_peak_freq: 785.245
  - contains_unique_info: True

<details>
<summary><b>All measurements (click to expand)</b></summary>

**Channel: lr_difference**

| Metric | Value |
|--------|-------|
| left_energy | 52623.965 |
| right_energy | 52623.969 |
| difference_energy | 8302.969 |
| energy_ratio | 0.079 |
| difference_rms | 0.040 |
| difference_peak_freq | 785.245 |
| difference_peak_magnitude | 8462.853 |
| contains_unique_info | True |

</details>

---

#### Method: phase_difference

**Key metrics to observe:**

- **left_vs_right:**
  - phase_diff_mean: 0.006
  - phase_coherence: 0.852
  - in_phase: True
- **left_vs_sum:**
  - phase_diff_mean: 0.003
  - phase_coherence: 0.949
  - in_phase: True
- **left_vs_difference:**
  - phase_diff_mean: -0.017
  - phase_coherence: 0.127
  - in_phase: True
- **right_vs_sum:**
  - phase_diff_mean: -0.003
  - phase_coherence: 0.950
  - in_phase: True
- **right_vs_difference:**
  - phase_diff_mean: -0.022
  - phase_coherence: 0.175
  - in_phase: True
- **sum_vs_difference:**
  - phase_diff_mean: -0.020
  - phase_coherence: 0.027
  - in_phase: True

<details>
<summary><b>All measurements (click to expand)</b></summary>

**Channel: left_vs_right**

| Metric | Value |
|--------|-------|
| phase_diff_mean | 0.006 |
| phase_diff_std | 0.628 |
| phase_diff_range | 6.283 |
| phase_coherence | 0.852 |
| in_phase | True |
| out_of_phase | False |

**Channel: left_vs_sum**

| Metric | Value |
|--------|-------|
| phase_diff_mean | 0.003 |
| phase_diff_std | 0.358 |
| phase_diff_range | 6.283 |
| phase_coherence | 0.949 |
| in_phase | True |
| out_of_phase | False |

**Channel: left_vs_difference**

| Metric | Value |
|--------|-------|
| phase_diff_mean | -0.017 |
| phase_diff_std | 1.672 |
| phase_diff_range | 6.283 |
| phase_coherence | 0.127 |
| in_phase | True |
| out_of_phase | False |

**Channel: right_vs_sum**

| Metric | Value |
|--------|-------|
| phase_diff_mean | -0.003 |
| phase_diff_std | 0.352 |
| phase_diff_range | 6.283 |
| phase_coherence | 0.950 |
| in_phase | True |
| out_of_phase | False |

**Channel: right_vs_difference**

| Metric | Value |
|--------|-------|
| phase_diff_mean | -0.022 |
| phase_diff_std | 2.005 |
| phase_diff_range | 6.283 |
| phase_coherence | 0.175 |
| in_phase | True |
| out_of_phase | False |

**Channel: sum_vs_difference**

| Metric | Value |
|--------|-------|
| phase_diff_mean | -0.020 |
| phase_diff_std | 1.842 |
| phase_diff_range | 6.283 |
| phase_coherence | 0.027 |
| in_phase | True |
| out_of_phase | False |

</details>

---

#### Method: time_delay

**Key metrics to observe:**

- **left_vs_right:**
  - delay_samples: -22
  - delay_ms: -0.458
  - is_synchronized: False
- **left_vs_sum:**
  - delay_samples: 0
  - delay_ms: 0.000e+00
  - is_synchronized: True
- **left_vs_difference:**
  - delay_samples: 0
  - delay_ms: 0.000e+00
  - is_synchronized: True
- **right_vs_sum:**
  - delay_samples: 0
  - delay_ms: 0.000e+00
  - is_synchronized: True
- **right_vs_difference:**
  - delay_samples: 0
  - delay_ms: 0.000e+00
  - is_synchronized: True
- **sum_vs_difference:**
  - delay_samples: 26
  - delay_ms: 0.542
  - is_synchronized: False

**Parameters:**

- max_delay: 100
- max_samples: 50000

<details>
<summary><b>All measurements (click to expand)</b></summary>

**Channel: left_vs_right**

- delay_samples: -22
- delay_ms: -0.458
- correlation_at_delay: 205.348
- is_synchronized: False

**Channel: left_vs_sum**

- delay_samples: 0
- delay_ms: 0.000e+00
- correlation_at_delay: 214.997
- is_synchronized: True

**Channel: left_vs_difference**

- delay_samples: 0
- delay_ms: 0.000e+00
- correlation_at_delay: 101.626
- is_synchronized: True

**Channel: right_vs_sum**

- delay_samples: 0
- delay_ms: 0.000e+00
- correlation_at_delay: 217.602
- is_synchronized: True

**Channel: right_vs_difference**

- delay_samples: 0
- delay_ms: 0.000e+00
- correlation_at_delay: -126.944
- is_synchronized: True

**Channel: sum_vs_difference**

- delay_samples: 26
- delay_ms: 0.542
- correlation_at_delay: 15.838
- is_synchronized: False

</details>

---

### INFORMATION

#### Method: shannon_entropy

**Parameters:**

- num_bins: 256

<details>
<summary><b>All measurements (click to expand)</b></summary>

**Channel: left**

- shannon_entropy: 6.599
- max_entropy: 8.000
- normalized_entropy: 0.825
- num_bins: 256

**Channel: right**

- shannon_entropy: 6.573
- max_entropy: 8.000
- normalized_entropy: 0.822
- num_bins: 256

**Channel: sum**

- shannon_entropy: 6.580
- max_entropy: 8.000
- normalized_entropy: 0.822
- num_bins: 256

**Channel: difference**

- shannon_entropy: 6.130
- max_entropy: 8.000
- normalized_entropy: 0.766
- num_bins: 256

</details>

---

#### Method: local_entropy

**Parameters:**

- window_size: 2048
- hop_length: 512
- num_bins: 64

<details>
<summary><b>All measurements (click to expand)</b></summary>

**Channel: left**

| Metric | Value |
|--------|-------|
| mean_entropy | 5.663 |
| std_entropy | 0.118 |
| min_entropy | 4.836 |
| max_entropy | 5.900 |
| num_windows | 387 |
| entropy_variation | 0.021 |

**Channel: right**

| Metric | Value |
|--------|-------|
| mean_entropy | 5.653 |
| std_entropy | 0.117 |
| min_entropy | 4.890 |
| max_entropy | 5.869 |
| num_windows | 387 |
| entropy_variation | 0.021 |

**Channel: sum**

| Metric | Value |
|--------|-------|
| mean_entropy | 5.687 |
| std_entropy | 0.126 |
| min_entropy | 4.826 |
| max_entropy | 5.902 |
| num_windows | 387 |
| entropy_variation | 0.022 |

**Channel: difference**

| Metric | Value |
|--------|-------|
| mean_entropy | 5.508 |
| std_entropy | 0.115 |
| min_entropy | 5.164 |
| max_entropy | 5.768 |
| num_windows | 387 |
| entropy_variation | 0.021 |

</details>

---

#### Method: compression_ratio

<details>
<summary><b>All measurements (click to expand)</b></summary>

**Channel: left**

- original_size: 200000
- compressed_size: 114488
- compression_ratio: 1.747
- samples_analyzed: 100000

**Channel: right**

- original_size: 200000
- compressed_size: 118611
- compression_ratio: 1.686
- samples_analyzed: 100000

**Channel: sum**

- original_size: 200000
- compressed_size: 132355
- compression_ratio: 1.511
- samples_analyzed: 100000

**Channel: difference**

- original_size: 200000
- compressed_size: 120965
- compression_ratio: 1.653
- samples_analyzed: 100000

</details>

---

#### Method: approximate_complexity

**Parameters:**

- m: 2
- r_factor: 0.200

<details>
<summary><b>All measurements (click to expand)</b></summary>

**Channel: left**

- approximate_complexity: 0.143
- pattern_length: 2
- tolerance: 0.013
- samples_analyzed: 5000

**Channel: right**

- approximate_complexity: 0.139
- pattern_length: 2
- tolerance: 0.013
- samples_analyzed: 5000

**Channel: sum**

- approximate_complexity: 0.079
- pattern_length: 2
- tolerance: 0.012
- samples_analyzed: 5000

**Channel: difference**

- approximate_complexity: 0.456
- pattern_length: 2
- tolerance: 0.018
- samples_analyzed: 5000

</details>

---

### STEGANOGRAPHY

#### Method: lsb_analysis

<details>
<summary><b>All measurements (click to expand)</b></summary>

**Channel: left**

| Metric | Value |
|--------|-------|
| lsb_mean | 0.497 |
| lsb_std | 0.500 |
| transition_rate | 0.496 |
| mean_zero_run | 2.026 |
| mean_one_run | 2.002 |
| samples_analyzed | 100000 |

**Channel: right**

| Metric | Value |
|--------|-------|
| lsb_mean | 0.503 |
| lsb_std | 0.500 |
| transition_rate | 0.498 |
| mean_zero_run | 1.997 |
| mean_one_run | 2.021 |
| samples_analyzed | 100000 |

**Channel: sum**

| Metric | Value |
|--------|-------|
| lsb_mean | 0.508 |
| lsb_std | 0.500 |
| transition_rate | 0.381 |
| mean_zero_run | 2.580 |
| mean_one_run | 2.663 |
| samples_analyzed | 100000 |

**Channel: difference**

| Metric | Value |
|--------|-------|
| lsb_mean | 0.506 |
| lsb_std | 0.500 |
| transition_rate | 0.500 |
| mean_zero_run | 1.977 |
| mean_one_run | 2.025 |
| samples_analyzed | 100000 |

</details>

---

#### Method: quantization_noise

<details>
<summary><b>All measurements (click to expand)</b></summary>

**Channel: left**

- noise_power: 3.314e-10
- noise_std: 1.820e-05
- autocorr_peak: 0.763
- spectral_flatness: 0.732
- samples_analyzed: 50000

**Channel: right**

- noise_power: 3.127e-10
- noise_std: 1.768e-05
- autocorr_peak: 0.731
- spectral_flatness: 0.748
- samples_analyzed: 50000

**Channel: sum**

- noise_power: 3.112e-10
- noise_std: 1.764e-05
- autocorr_peak: 0.738
- spectral_flatness: 0.755
- samples_analyzed: 50000

**Channel: difference**

- noise_power: 3.033e-10
- noise_std: 1.741e-05
- autocorr_peak: 0.702
- spectral_flatness: 0.742
- samples_analyzed: 50000

</details>

---

#### Method: signal_residual

**Parameters:**

- cutoff_freq: 1000

<details>
<summary><b>All measurements (click to expand)</b></summary>

**Channel: left**

| Metric | Value |
|--------|-------|
| signal_power | 0.005 |
| residual_power | 1.287e-04 |
| snr_db | 16.043 |
| residual_peak_freq | 1565.280 |
| energy_ratio | 0.025 |
| samples_analyzed | 100000 |

**Channel: right**

| Metric | Value |
|--------|-------|
| signal_power | 0.005 |
| residual_power | 1.810e-04 |
| snr_db | 14.528 |
| residual_peak_freq | 930.720 |
| energy_ratio | 0.035 |
| samples_analyzed | 100000 |

**Channel: sum**

| Metric | Value |
|--------|-------|
| signal_power | 0.005 |
| residual_power | 6.156e-05 |
| snr_db | 19.156 |
| residual_peak_freq | 930.720 |
| energy_ratio | 0.012 |
| samples_analyzed | 100000 |

**Channel: difference**

| Metric | Value |
|--------|-------|
| signal_power | 0.007 |
| residual_power | 0.002 |
| snr_db | 4.749 |
| residual_peak_freq | 1565.280 |
| energy_ratio | 0.335 |
| samples_analyzed | 100000 |

</details>

---

### META_ANALYSIS

#### Method: inter_segment_comparison

**Parameters:**

- num_segments: 10

<details>
<summary><b>All measurements (click to expand)</b></summary>

**Channel: left**

| Metric | Value |
|--------|-------|
| num_segments | 10 |
| mean_distance | 1318.926 |
| std_distance | 808.678 |
| min_distance | 153.818 |
| max_distance | 3316.930 |
| similarity_score | 7.576e-04 |

**Channel: right**

| Metric | Value |
|--------|-------|
| num_segments | 10 |
| mean_distance | 1341.266 |
| std_distance | 804.905 |
| min_distance | 151.325 |
| max_distance | 3211.927 |
| similarity_score | 7.450e-04 |

**Channel: sum**

| Metric | Value |
|--------|-------|
| num_segments | 10 |
| mean_distance | 1389.773 |
| std_distance | 857.411 |
| min_distance | 144.534 |
| max_distance | 3452.944 |
| similarity_score | 7.190e-04 |

**Channel: difference**

| Metric | Value |
|--------|-------|
| num_segments | 10 |
| mean_distance | 2991.141 |
| std_distance | 1857.980 |
| min_distance | 395.548 |
| max_distance | 8028.861 |
| similarity_score | 3.342e-04 |

</details>

---

#### Method: segment_clustering

**Parameters:**

- num_segments: 20

<details>
<summary><b>All measurements (click to expand)</b></summary>

**Channel: left**

- num_segments: 20
- avg_intra_distance: 0.144
- unique_segments: 0
- repetition_rate: 1.000

**Channel: right**

- num_segments: 20
- avg_intra_distance: 0.153
- unique_segments: 0
- repetition_rate: 1.000

**Channel: sum**

- num_segments: 20
- avg_intra_distance: 0.139
- unique_segments: 0
- repetition_rate: 1.000

**Channel: difference**

- num_segments: 20
- avg_intra_distance: 0.218
- unique_segments: 0
- repetition_rate: 1.000

</details>

---

#### Method: stability_scores

**Parameters:**

- window_size: 2048
- hop_length: 512

<details>
<summary><b>All measurements (click to expand)</b></summary>

**Channel: left**

- energy_stability: 0.666
- spectral_stability: 0.724
- overall_stability: 0.695
- num_windows: 387

**Channel: right**

- energy_stability: 0.668
- spectral_stability: 0.724
- overall_stability: 0.696
- num_windows: 387

**Channel: sum**

- energy_stability: 0.650
- spectral_stability: 0.715
- overall_stability: 0.682
- num_windows: 387

**Channel: difference**

- energy_stability: 0.709
- spectral_stability: 0.799
- overall_stability: 0.754
- num_windows: 387

</details>

---

## Appendix A: Reference Thresholds

The following thresholds are provided as reference values from 
signal processing literature. They are not used for automated 
classification in this tool.

### periodicity_score

*Autocorrelation peak normalized value*

- high: 0.8
- very_high: 0.95

### harmonicity_score

*Ratio of harmonic energy to total energy*

- harmonic: 0.7
- strongly_harmonic: 0.9

### tonality

*1 - spectral_flatness, inverse of flatness*

- tonal: 0.7
- highly_tonal: 0.9

### modulation_index

*AC component / DC component ratio*

- low: 0.1
- moderate: 0.3
- high: 0.5

### phase_coherence

*Inter-channel phase consistency (0-1)*

- low: 0.3
- moderate: 0.6
- high: 0.8

## Appendix B: Interpretation Guide

This section provides general context from signal processing literature 
to assist in human interpretation of measured values. It does not 
constitute automated classification or conclusions.

### Characteristics of Artificial vs Natural Signals

**Artificial signals** (designed, synthesized, or encoded) typically exhibit:

- **High periodicity** (autocorrelation > 0.9): Exact repetition of patterns
- **Strong harmonic structure** (harmonicity > 0.9): Integer frequency ratios
- **High tonality** (> 0.9): Discrete frequency components, not broadband
- **Temporal stability**: Constant spectral content over time
- **Low entropy**: Predictable, compressible structure

**Natural signals** (speech, music, environmental sounds) typically exhibit:

- **Moderate periodicity** (0.3-0.7): Some repetition but with variation
- **Variable harmonic content**: Changes over time
- **Mixed tonality** (0.4-0.8): Combination of tonal and noise components
- **Temporal variation**: Evolving spectral content
- **Higher entropy**: Less predictable structure

### Indicators of Encoded Data

Signals carrying encoded information may show:

**Amplitude Modulation (AM) encoding:**
- Modulation index > 0.3: Significant amplitude variation
- Discrete modulation frequencies: Regular envelope patterns
- Stable carrier frequency: Constant fundamental

**Frequency Modulation (FM) encoding:**
- Frequency deviation > 10% of carrier: Significant frequency shifts
- Discrete frequency transitions: Step changes rather than continuous
- Consistent modulation index: Repeating pattern

**Phase Shift Keying (PSK) encoding:**
- Numerous phase jumps (> 100): Discrete phase transitions
- Low phase coherence (< 0.5): Intentional phase discontinuities
- Regular jump intervals: Systematic timing

**Frequency Shift Keying (FSK) encoding:**
- Multiple discrete peak frequencies: Fixed set of carriers
- Rapid frequency switching: Transitions between fixed frequencies
- Time-frequency patterns: Regular structure in spectrogram

### Stereo Field Encoding

Information may be encoded in the spatial field:

**L-R difference channel:**
- Energy ratio > 0.05: Significant information in difference
- Different fundamental frequency: Distinct content from L+R
- Higher frequency content: Often used for data encoding

**Phase relationships:**
- Out-of-phase content (phase diff ≈ π): Intentional opposition
- Phase coherence < 0.3: Decorrelated signals
- Consistent phase differences: Systematic relationship

**Time delays:**
- Fixed inter-channel delay: Intentional offset
- Delay > 5 samples: Beyond natural spatial differences

### Common Signal Types

**Pure tones:**
- Periodicity ≈ 1.0, Harmonicity ≈ 0, Tonality ≈ 1.0
- Single spectral peak, no harmonics

**Harmonic signals (musical notes):**
- Periodicity > 0.9, Harmonicity > 0.8, Tonality > 0.8
- Clear fundamental + integer harmonic series

**DTMF tones (phone keys):**
- Two discrete frequencies, Tonality > 0.95
- Short duration (50-100ms), rectangular envelope

**White noise:**
- Periodicity ≈ 0, Flatness ≈ 1.0, Tonality ≈ 0
- Uniform spectral energy distribution

**Modulated carrier:**
- High periodicity carrier + modulation in envelope or frequency
- Stable spectral centroid with envelope variation

### Analysis Strategy

When analyzing unknown signals:

1. **Check periodicity and harmonicity**: Indicates natural vs artificial origin
2. **Examine temporal stability**: Constant vs varying content
3. **Compare channels**: Look for L-R differences or phase relationships
4. **Analyze modulation**: Check for AM, FM, or phase modulation
5. **Inspect time-frequency**: STFT reveals temporal structure
6. **Look for patterns**: Regular intervals, discrete states, systematic behavior

**Important:** These indicators are not definitive. Context, domain knowledge, 
and multiple converging measurements are required for reliable interpretation.

## Appendix C: Observations on Measured Values

This section compares measured values from this analysis to the reference 
thresholds and patterns described in Appendix B. These are factual observations 
only, not conclusions or automated interpretations.

**Disclaimer:** The observations below are intended to assist human analysis 
by highlighting relationships between measured values and documented patterns. 
They do not constitute definitive classification or conclusions.

### Periodicity Score

Comparison of measured periodicity scores to reference thresholds.

**Measured values:**

- left: 0.999
- right: 0.999
- sum: 1.000
- difference: 0.993

**Reference from Appendix B:** Appendix B states: Artificial signals typically exhibit high periodicity (> 0.8), natural signals show moderate periodicity (0.3-0.7)

**Factual observation:** Channels left, right, sum, difference exceed very_high threshold (0.95)

**Possible indication:** Values in range documented for signals with exact pattern repetition (see Appendix B: Artificial signals)

### Harmonic Structure

Comparison of measured harmonicity scores to reference thresholds.

**Measured values:**

- left: harmonicity=1.000, fundamental=66.0 Hz
- right: harmonicity=1.000, fundamental=66.0 Hz
- sum: harmonicity=1.000, fundamental=66.0 Hz
- difference: harmonicity=1.000, fundamental=393.0 Hz

**Reference from Appendix B:** Appendix B states: Artificial signals show strong harmonic structure (> 0.9) with integer frequency ratios

**Factual observation:** Channels left, right, sum, difference meet or exceed strongly_harmonic threshold (0.9). Note: difference channel has distinct fundamental (393.0 Hz vs 66.0 Hz)

**Possible indication:** Harmonic structure consistent with artificial signals. Different fundamental in difference channel consistent with stereo field encoding (see Appendix B)

### Tonality

Comparison of measured tonality values to reference thresholds.

**Measured values:**

- left: 0.954
- right: 0.957
- sum: 0.963
- difference: 0.930

**Reference from Appendix B:** Appendix B states: Artificial signals show high tonality (> 0.9) with discrete frequency components, natural signals show mixed tonality (0.4-0.8)

**Factual observation:** Channels left, right, sum, difference exceed highly_tonal threshold (0.9)

**Possible indication:** Values consistent with signals composed of discrete frequencies rather than broadband noise (see Appendix B)

### Frequency Modulation

Frequency modulation detected on one or more channels.

**Measured values:**

- left: deviation=601.48 Hz, carrier=159.1 Hz
- right: deviation=626.68 Hz, carrier=173.2 Hz
- sum: deviation=547.19 Hz, carrier=141.6 Hz
- difference: deviation=742.77 Hz, carrier=776.6 Hz

**Reference from Appendix B:** Appendix B states: FM encoding typically shows frequency deviation > 10% of carrier

**Factual observation:** FM detected on channels: left, right, sum, difference. Channels with >10% deviation: left (378.1%), right (361.9%), sum (386.5%), difference (95.6%)

**Possible indication:** Deviation levels consistent with intentional frequency modulation encoding (see Appendix B: FM encoding)

### Phase Discontinuities

Significant number of phase jumps detected.

**Measured values:**

- left: 34673 jumps, coherence=0.000
- right: 36966 jumps, coherence=0.000
- sum: 30865 jumps, coherence=0.000
- difference: 94594 jumps, coherence=0.125

**Reference from Appendix B:** Appendix B states: PSK encoding typically shows numerous phase jumps (> 100) with low coherence (< 0.5)

**Factual observation:** Channels left, right, sum, difference show > 100 phase jumps

**Possible indication:** Pattern consistent with phase-based encoding or discrete phase transitions (see Appendix B: PSK encoding)

### Stereo Field Analysis (L-R)

Significant energy detected in L-R difference channel.

**Measured values:**

- Energy ratio (difference/total): 0.079
- Difference peak frequency: 785.2 Hz

**Reference from Appendix B:** Appendix B states: L-R encoding typically shows energy ratio > 0.05 and different fundamental frequency

**Factual observation:** L-R channel contains distinct information (energy ratio: 0.079)

**Possible indication:** Pattern consistent with intentional stereo field encoding with information in difference channel (see Appendix B: Stereo Field Encoding)

### Frequency Band Stability

Specific frequency bands show high stability over time.

**Measured values:**

- left: 8000-20000Hz (0.842)
- right: 8000-20000Hz (0.846)
- sum: 8000-20000Hz (0.862)
- difference: 8000-20000Hz (0.820)

**Reference from Appendix B:** Stable frequency bands may indicate carrier frequencies or continuous tones

**Factual observation:** One or more frequency bands maintain constant energy over time

**Possible indication:** Pattern consistent with stable carriers (see Appendix B)

### Irregular Pulse Distribution

Many pulses with irregular spacing.

**Measured values:**

- left (2818 pulses, reg=0.00)
- right (1891 pulses, reg=0.00)
- sum (1868 pulses, reg=0.00)
- difference (1083 pulses, reg=0.00)

**Factual observation:** Channels show numerous pulses with irregular timing

### High Spectral Peak Count

Numerous discrete frequency peaks detected.

**Measured values:**

- left: 19690 peaks
- right: 19650 peaks
- sum: 19649 peaks
- difference: 19609 peaks

**Reference from Appendix B:** Appendix B states: Multiple peaks may indicate complex harmonics or FSK

**Factual observation:** Channels show > 1000 peaks

**Possible indication:** Pattern consistent with complex multi-carrier or FSK (see Appendix B)

### Out-of-Phase Channel Pairs

Channel pairs in phase opposition detected.

**Measured values:**

- left_vs_right (coh=0.852)
- left_vs_sum (coh=0.949)
- left_vs_difference (coh=0.127)
- right_vs_sum (coh=0.950)
- right_vs_difference (coh=0.175)
- sum_vs_difference (coh=0.027)

**Reference from Appendix B:** Appendix B states: Phase opposition indicates intentional encoding

**Factual observation:** Channel pairs show phase opposition

**Possible indication:** Pattern consistent with phase-based stereo encoding (see Appendix B)

### Low Phase Coherence

Weak phase relationship between channels.

**Measured values:**

- left_vs_difference (0.127)
- right_vs_difference (0.175)
- sum_vs_difference (0.027)

**Reference from Appendix B:** Appendix B states: Low coherence indicates decorrelated signals

**Factual observation:** Channel pairs show inconsistent phase

**Final reminder:** These observations should be interpreted in context with 
domain knowledge, acquisition conditions, and intended signal use. Multiple 
converging measurements increase confidence but do not guarantee conclusions.
