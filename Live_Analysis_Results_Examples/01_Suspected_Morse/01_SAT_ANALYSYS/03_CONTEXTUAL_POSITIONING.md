# Audio Analysis Report - Contextual Positioning

- Timestamp: `2026-01-23T11:16:32.449349`
- Source: `C:\Autres_Devs\small-audio-toolkit\Analysis_Workspace\04_input_sounds\morse_hidden_am.wav`

## File Information

- format: `WAV`
- subtype: `PCM_16`
- sample_rate: `22050`
- channels: `1`
- duration: `15.0`
- frames: `330750`

## Preprocessing

- normalize: enabled=True
- segmentation: enabled=False

## Contextual Positioning

This section uses **official context files** to position a selected subset of scalar metrics.
Contexts affect presentation only; they never affect computation.

### time_frequency

- Objective: Identify stable or structured time–frequency organization inconsistent with random variation.
- Coverage: `partial`
- Rationale: Only scalar summaries of time–frequency behavior are contextualized.

- Documentary references:
  - L. Cohen — "Time-Frequency Analysis" — (1995). Central reference for time–frequency representations.
  - B. Boashash — "Time-Frequency Signal Analysis" — (2003). Applied reference for time–frequency structure detection.

#### 3.A Metrics with reference zones (Status A)

_No status A metrics were applicable for this family._

#### 3.B Metrics without reference zones

**Status B — context-dependent (no stable zone)**

- `stft` / `mono`: **dominant_freq_mean** = 4995.7 — Mean dominant frequency over time.
- `stft` / `mono`: **spectral_flux_mean** = 0.000690805 — Average spectral flux magnitude.
- `stft` / `mono`: **temporal_stability** = 0.808704 — Stability of spectral content over time.

**Status C — descriptive only (no stable zone)**

_No status C metrics listed for this family._

**Unmapped / missing context coverage**

- `stft` / `mono` / **num_time_frames**: 5169 — _not covered by context (missing metric entry)_
- `stft` / `mono` / **num_freq_bins**: 1025 — _not covered by context (missing metric entry)_
- `stft` / `mono` / **frequency_resolution**: 10.7666 — _not covered by context (missing metric entry)_
- `stft` / `mono` / **time_resolution**: 0.00290249 — _not covered by context (missing metric entry)_
- `stft` / `mono` / **mean_magnitude**: 0.000163918 — _not covered by context (missing metric entry)_
- `stft` / `mono` / **max_magnitude**: 0.0717187 — _not covered by context (missing metric entry)_
- `stft` / `mono` / **dominant_freq_std**: 0 — _not covered by context (missing metric entry)_
- `stft` / `mono` / **spectral_flux_max**: 0.00645624 — _not covered by context (missing metric entry)_

**Expected by context but missing in results (not evaluated)**

_No expected scalar metrics were missing for this family._


### spectral

- Objective: Identify spectral concentration, tonal structure, or non-diffuse frequency distributions.
- Coverage: `partial`
- Rationale: Focuses on global spectral organization rather than perceptual or musical descriptors.

- Documentary references:
  - J. G. Proakis & D. G. Manolakis — "Digital Signal Processing" — (2007). Foundational DSP reference for spectral analysis.
  - J. O. Smith — "Spectral Audio Signal Processing" — (2011). Audio-oriented reference for spectral structure and flatness.

#### 3.A Metrics with reference zones (Status A)

- `fft_global` / `mono`: **peak_frequency** = 5000 (reference [0, 22050]) → **within**. Frequency of the dominant spectral peak.
- `fft_global` / `mono`: **spectral_energy** = 2.05137e+08 (reference [0, 1]) → **above**. Total normalized spectral energy.
- `spectral_flatness` / `mono`: **spectral_flatness** = 0.186417 (reference [0, 1]) → **within**. Noise-like versus tonal spectral indicator.

#### 3.B Metrics without reference zones

**Status B — context-dependent (no stable zone)**

- `peak_detection` / `mono`: **num_peaks** = 2645 — Number of detected spectral peaks.

**Status C — descriptive only (no stable zone)**

_No status C metrics listed for this family._

**Unmapped / missing context coverage**

- `fft_global` / `mono` / **n_fft**: 330750 — _not covered by context (missing metric entry)_
- `fft_global` / `mono` / **frequency_resolution**: 0.0666667 — _not covered by context (missing metric entry)_
- `fft_global` / `mono` / **peak_magnitude**: 11610.3 — _not covered by context (missing metric entry)_
- `peak_detection` / `mono` / **dominant_frequency**: 2.73333 — _not covered by context (missing metric entry)_
- `peak_detection` / `mono` / **frequency_spread**: 3183.24 — _not covered by context (missing metric entry)_
- `spectral_centroid` / `mono` / **spectral_centroid**: 5031.47 — _not covered by context (missing method entry)_
- `spectral_centroid` / `mono` / **normalized_centroid**: 0.456369 — _not covered by context (missing method entry)_
- `spectral_bandwidth` / `mono` / **spectral_bandwidth**: 13.0339 — _not covered by context (missing method entry)_
- `spectral_bandwidth` / `mono` / **spectral_centroid_Hz**: 5000 — _not covered by context (missing method entry)_
- `spectral_flatness` / `mono` / **tonality**: 0.813583 — _not covered by context (missing metric entry)_

**Expected by context but missing in results (not evaluated)**

_No expected scalar metrics were missing for this family._


### temporal

- Objective: Identify periodicity, repetition, and non-random temporal structure in audio signals.
- Coverage: `partial`
- Rationale: This context focuses on stable scalar temporal metrics suitable for high-level forensic screening. It does not aim to exhaustively cover all temporal-domain measurements.

- Documentary references:
  - A. V. Oppenheim & A. S. Willsky — "Signals and Systems" — (2010). Foundational reference for temporal analysis and autocorrelation.
  - L. R. Rabiner & R. W. Schafer — "Digital Processing of Speech Signals" — (1978). Classic reference on temporal structure and periodicity in signals.

#### 3.A Metrics with reference zones (Status A)

- `autocorrelation` / `mono`: **autocorr_max** = 0.99743 (reference [0, 1]) → **within**. Normalized maximum autocorrelation excluding zero lag.
- `autocorrelation` / `mono`: **periodicity_score** = 0.99743 (reference [0, 1]) → **within**. Proxy for temporal periodicity strength.

#### 3.B Metrics without reference zones

**Status B — context-dependent (no stable zone)**

- `envelope` / `mono`: **envelope_std** = 0.0183527 — Variability of the amplitude envelope.
- `autocorrelation` / `mono`: **first_peak_lag** = 4 — Lag of first significant autocorrelation peak.
- `autocorrelation` / `mono`: **num_peaks** = 1133 — Number of detected autocorrelation peaks.

**Status C — descriptive only (no stable zone)**

_No status C metrics listed for this family._

**Unmapped / missing context coverage**

- `envelope` / `mono` / **envelope_mean**: 0.140225 — _not covered by context (missing metric entry)_
- `envelope` / `mono` / **envelope_max**: 0.163971 — _not covered by context (missing metric entry)_
- `envelope` / `mono` / **envelope_length**: 330750 — _not covered by context (missing metric entry)_
- `autocorrelation` / `mono` / **autocorr_mean**: -2.48124e-05 — _not covered by context (missing metric entry)_
- `pulse_detection` / `mono` / **num_pulses**: 228 — _not covered by context (missing method entry)_
- `pulse_detection` / `mono` / **interval_mean**: 1453.15 — _not covered by context (missing method entry)_
- `pulse_detection` / `mono` / **interval_std**: 285.408 — _not covered by context (missing method entry)_
- `pulse_detection` / `mono` / **regularity_score**: 0.803593 — _not covered by context (missing method entry)_

**Expected by context but missing in results (not evaluated)**

_No expected scalar metrics were missing for this family._


### modulation

- Objective: Identify the presence and stability of non-random amplitude or frequency modulations.
- Coverage: `partial`
- Rationale: This context targets scalar modulation indicators suitable for forensic screening, not detailed demodulation.

- Documentary references:
  - S. Haykin — "Communication Systems" — (2001). Canonical reference for AM/FM modulation and detection.
  - L. L. Scharf — "Statistical Signal Processing" — (1991). Detection of structured signals in noise.

#### 3.A Metrics with reference zones (Status A)

- `am_detection` / `mono`: **modulation_detected** = False (reference [0, 1]) → **within**. Binary indicator of detected amplitude modulation.
- `fm_detection` / `mono`: **fm_detected** = False (reference [0, 1]) → **within**. Binary indicator of detected frequency modulation.

#### 3.B Metrics without reference zones

**Status B — context-dependent (no stable zone)**

- `am_detection` / `mono`: **dominant_modulation_freq** = 0 — Dominant modulation frequency.
- `am_detection` / `mono`: **modulation_depth** = 0.330887 — Estimated modulation depth.
- `fm_detection` / `mono`: **frequency_deviation** = 37.9915 — Estimated frequency deviation.

**Status C — descriptive only (no stable zone)**

_No status C metrics listed for this family._

**Unmapped / missing context coverage**

- `am_detection` / `mono` / **num_modulation_frequencies**: 0 — _not covered by context (missing metric entry)_
- `am_detection` / `mono` / **modulation_index**: 0.13088 — _not covered by context (missing metric entry)_
- `am_detection` / `mono` / **envelope_mean**: 0.140225 — _not covered by context (missing metric entry)_
- `am_detection` / `mono` / **envelope_std**: 0.0183527 — _not covered by context (missing metric entry)_
- `fm_detection` / `mono` / **carrier_frequency_mean**: 4998.57 — _not covered by context (missing metric entry)_
- `fm_detection` / `mono` / **frequency_range**: 137.085 — _not covered by context (missing metric entry)_
- `fm_detection` / `mono` / **frequency_std**: 37.9915 — _not covered by context (missing metric entry)_
- `fm_detection` / `mono` / **num_fm_components**: 0 — _not covered by context (missing metric entry)_
- `fm_detection` / `mono` / **modulation_index_fm**: 0.00760048 — _not covered by context (missing metric entry)_
- `phase_analysis` / `mono` / **phase_mean**: -0.00356091 — _not covered by context (missing method entry)_
- `phase_analysis` / `mono` / **phase_std**: 1.81386 — _not covered by context (missing method entry)_
- `phase_analysis` / `mono` / **phase_range**: 6.26956 — _not covered by context (missing method entry)_
- `phase_analysis` / `mono` / **unwrapped_phase_total**: 471102 — _not covered by context (missing method entry)_
- `phase_analysis` / `mono` / **phase_coherence**: 0.9924 — _not covered by context (missing method entry)_
- `phase_analysis` / `mono` / **num_phase_jumps**: 75000 — _not covered by context (missing method entry)_
- `phase_analysis` / `mono` / **phase_jump_rate**: 5000 — _not covered by context (missing method entry)_

**Expected by context but missing in results (not evaluated)**

_No expected scalar metrics were missing for this family._


### information

- Objective: Position the global degree of randomness or organization of the audio signal.
- Coverage: `partial`
- Rationale: Information-theoretic metrics provide coarse indicators without semantic interpretation.

- Documentary references:
  - T. M. Cover & J. A. Thomas — "Elements of Information Theory" — (2006). Canonical reference for entropy and information measures.

#### 3.A Metrics with reference zones (Status A)

- `shannon_entropy` / `mono`: **shannon_entropy** = 7.79336 (reference [0, 16]) → **within**. Shannon entropy of the signal.
- `shannon_entropy` / `mono`: **normalized_entropy** = 0.974169 (reference [0, 1]) → **within**. Entropy normalized by maximum possible entropy.

#### 3.B Metrics without reference zones

**Status B — context-dependent (no stable zone)**

_No status B metrics listed for this family._

**Status C — descriptive only (no stable zone)**

_No status C metrics listed for this family._

**Unmapped / missing context coverage**

- `shannon_entropy` / `mono` / **max_entropy**: 8 — _not covered by context (missing metric entry)_
- `shannon_entropy` / `mono` / **num_bins**: 256 — _not covered by context (missing metric entry)_
- `local_entropy` / `mono` / **mean_entropy**: 5.79357 — _not covered by context (missing method entry)_
- `local_entropy` / `mono` / **std_entropy**: 0.0797437 — _not covered by context (missing method entry)_
- `local_entropy` / `mono` / **min_entropy**: 5.48334 — _not covered by context (missing method entry)_
- `local_entropy` / `mono` / **max_entropy**: 5.86279 — _not covered by context (missing method entry)_
- `local_entropy` / `mono` / **num_windows**: 192 — _not covered by context (missing method entry)_
- `local_entropy` / `mono` / **entropy_variation**: 0.0137642 — _not covered by context (missing method entry)_

**Expected by context but missing in results (not evaluated)**

_No expected scalar metrics were missing for this family._


### steganography

- Objective: Identify statistical alterations compatible with discrete encoding or quantization-based manipulation.
- Coverage: `partial`
- Rationale: Metrics target low-level statistical artifacts without asserting the presence of hidden data.

- Documentary references:
  - J. Fridrich — "Steganography in Digital Media" — (2009). Reference for LSB-based steganalysis and statistical artifacts.
  - F. A. P. Petitcolas et al. — "Information Hiding Techniques" — (1999). Foundational work on digital information hiding.

#### 3.A Metrics with reference zones (Status A)

- `lsb_analysis` / `mono`: **lsb_mean** = 0.49781 (reference [0.4, 0.6]) → **within**. Mean value of least significant bits.

#### 3.B Metrics without reference zones

**Status B — context-dependent (no stable zone)**

- `lsb_analysis` / `mono`: **transition_rate** = 0.47946 — Transition rate of the LSB sequence.
- `quantization_noise` / `mono`: **noise_std** = 2.80469e-05 — Standard deviation of quantization noise.

**Status C — descriptive only (no stable zone)**

_No status C metrics listed for this family._

**Unmapped / missing context coverage**

- `lsb_analysis` / `mono` / **lsb_std**: 0.499995 — _not covered by context (missing metric entry)_
- `lsb_analysis` / `mono` / **mean_zero_run**: 2.09473 — _not covered by context (missing metric entry)_
- `lsb_analysis` / `mono` / **mean_one_run**: 2.07654 — _not covered by context (missing metric entry)_
- `lsb_analysis` / `mono` / **samples_analyzed**: 100000 — _not covered by context (missing metric entry)_
- `quantization_noise` / `mono` / **noise_power**: 7.86626e-10 — _not covered by context (missing metric entry)_
- `quantization_noise` / `mono` / **autocorr_peak**: 0.979429 — _not covered by context (missing metric entry)_
- `quantization_noise` / `mono` / **spectral_flatness**: 0.256936 — _not covered by context (missing metric entry)_
- `quantization_noise` / `mono` / **samples_analyzed**: 50000 — _not covered by context (missing metric entry)_
- `signal_residual` / `mono` / **signal_power**: 1.49061e-08 — _not covered by context (missing method entry)_
- `signal_residual` / `mono` / **residual_power**: 0.0101983 — _not covered by context (missing method entry)_
- `signal_residual` / `mono` / **snr_db**: -58.3516 — _not covered by context (missing method entry)_
- `signal_residual` / `mono` / **residual_peak_freq**: 5000.06 — _not covered by context (missing method entry)_
- `signal_residual` / `mono` / **energy_ratio**: 679609 — _not covered by context (missing method entry)_
- `signal_residual` / `mono` / **samples_analyzed**: 100000 — _not covered by context (missing method entry)_
- `statistical_anomalies` / `mono` / **num_outliers**: 0 — _not covered by context (missing method entry)_
- `statistical_anomalies` / `mono` / **outlier_rate**: 0 — _not covered by context (missing method entry)_
- `statistical_anomalies` / `mono` / **max_z_score**: 1.57582 — _not covered by context (missing method entry)_
- `statistical_anomalies` / `mono` / **mean_z_score**: 0.892856 — _not covered by context (missing method entry)_
- `statistical_anomalies` / `mono` / **chi2_statistic**: 99304.4 — _not covered by context (missing method entry)_
- `statistical_anomalies` / `mono` / **chi2_pvalue**: 0 — _not covered by context (missing method entry)_
- `statistical_anomalies` / `mono` / **normality_test**: False — _not covered by context (missing method entry)_
- `statistical_anomalies` / `mono` / **samples_analyzed**: 100000 — _not covered by context (missing method entry)_
- `parity_analysis` / `mono` / **parity_mean**: 0.49781 — _not covered by context (missing method entry)_
- `parity_analysis` / `mono` / **parity_std**: 0.499995 — _not covered by context (missing method entry)_
- `parity_analysis` / `mono` / **transition_rate**: 0.479465 — _not covered by context (missing method entry)_
- `parity_analysis` / `mono` / **transition_anomaly**: 0.0205352 — _not covered by context (missing method entry)_
- `parity_analysis` / `mono` / **mean_run_length**: 2.08564 — _not covered by context (missing method entry)_
- `parity_analysis` / `mono` / **std_run_length**: 1.43346 — _not covered by context (missing method entry)_
- `parity_analysis` / `mono` / **chi2_statistic**: 1.91844 — _not covered by context (missing method entry)_
- `parity_analysis` / `mono` / **chi2_pvalue**: 0.166029 — _not covered by context (missing method entry)_
- `parity_analysis` / `mono` / **appears_random**: True — _not covered by context (missing method entry)_
- `parity_analysis` / `mono` / **samples_analyzed**: 100000 — _not covered by context (missing method entry)_

**Expected by context but missing in results (not evaluated)**

_No expected scalar metrics were missing for this family._

