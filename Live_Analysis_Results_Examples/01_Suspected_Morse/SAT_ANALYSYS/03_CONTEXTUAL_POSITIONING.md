# Audio Analysis Report - Contextual Positioning

- Timestamp: `2026-01-23T09:25:55.792690`
- Source: `..\small-audio-toolkit\Analysis_Workspace\04_input_sounds\the_soothing_wavs.wav`

## File Information

- format: `WAV`
- subtype: `PCM_16`
- sample_rate: `22050`
- channels: `2`
- duration: `5.002630385487528`
- frames: `110308`

## Preprocessing

- normalize: enabled=False
- segmentation: enabled=False

## Contextual Positioning

This section uses **official context files** to position a selected subset of scalar metrics.
Contexts affect presentation only; they never affect computation.

### temporal

- Objective: Identify periodicity, repetition, and non-random temporal structure in audio signals.
- Coverage: `partial`
- Rationale: This context focuses on stable scalar temporal metrics suitable for high-level forensic screening. It does not aim to exhaustively cover all temporal-domain measurements.

- Documentary references:
  - A. V. Oppenheim & A. S. Willsky — "Signals and Systems" — (2010). Foundational reference for temporal analysis and autocorrelation.
  - L. R. Rabiner & R. W. Schafer — "Digital Processing of Speech Signals" — (1978). Classic reference on temporal structure and periodicity in signals.

#### 3.A Metrics with reference zones (Status A)

- `autocorrelation` / `left`: **autocorr_max** = 0.607014 (reference [0, 1]) → **within**. Normalized maximum autocorrelation excluding zero lag.
- `autocorrelation` / `left`: **periodicity_score** = 0.607014 (reference [0, 1]) → **within**. Proxy for temporal periodicity strength.
- `autocorrelation` / `right`: **autocorr_max** = 0.610112 (reference [0, 1]) → **within**. Normalized maximum autocorrelation excluding zero lag.
- `autocorrelation` / `right`: **periodicity_score** = 0.610112 (reference [0, 1]) → **within**. Proxy for temporal periodicity strength.
- `autocorrelation` / `difference`: **autocorr_max** = 0.704082 (reference [0, 1]) → **within**. Normalized maximum autocorrelation excluding zero lag.
- `autocorrelation` / `difference`: **periodicity_score** = 0.704082 (reference [0, 1]) → **within**. Proxy for temporal periodicity strength.

#### 3.B Metrics without reference zones

**Status B — context-dependent (no stable zone)**

- `envelope` / `left`: **envelope_std** = 0.0956545 — Variability of the amplitude envelope.
- `envelope` / `right`: **envelope_std** = 0.0958798 — Variability of the amplitude envelope.
- `envelope` / `difference`: **envelope_std** = 0.0196696 — Variability of the amplitude envelope.
- `autocorrelation` / `left`: **first_peak_lag** = 5 — Lag of first significant autocorrelation peak.
- `autocorrelation` / `left`: **num_peaks** = 438 — Number of detected autocorrelation peaks.
- `autocorrelation` / `right`: **first_peak_lag** = 5 — Lag of first significant autocorrelation peak.
- `autocorrelation` / `right`: **num_peaks** = 444 — Number of detected autocorrelation peaks.
- `autocorrelation` / `difference`: **first_peak_lag** = 5 — Lag of first significant autocorrelation peak.
- `autocorrelation` / `difference`: **num_peaks** = 111 — Number of detected autocorrelation peaks.

**Status C — descriptive only (no stable zone)**

_No status C metrics listed for this family._

**Unmapped / missing context coverage**

- `envelope` / `left` / **envelope_mean**: 0.123242 — _not covered by context (missing metric entry)_
- `envelope` / `left` / **envelope_max**: 0.742441 — _not covered by context (missing metric entry)_
- `envelope` / `left` / **envelope_length**: 110308 — _not covered by context (missing metric entry)_
- `envelope` / `right` / **envelope_mean**: 0.123241 — _not covered by context (missing metric entry)_
- `envelope` / `right` / **envelope_max**: 0.697046 — _not covered by context (missing metric entry)_
- `envelope` / `right` / **envelope_length**: 110308 — _not covered by context (missing metric entry)_
- `envelope` / `difference` / **envelope_mean**: 0.0239492 — _not covered by context (missing metric entry)_
- `envelope` / `difference` / **envelope_max**: 0.204019 — _not covered by context (missing metric entry)_
- `envelope` / `difference` / **envelope_length**: 110308 — _not covered by context (missing metric entry)_
- `autocorrelation` / `left` / **autocorr_mean**: 9.44442e-05 — _not covered by context (missing metric entry)_
- `autocorrelation` / `right` / **autocorr_mean**: 9.4145e-05 — _not covered by context (missing metric entry)_
- `autocorrelation` / `difference` / **autocorr_mean**: 9.91905e-05 — _not covered by context (missing metric entry)_
- `pulse_detection` / `left` / **num_pulses**: 304 — _not covered by context (missing method entry)_
- `pulse_detection` / `left` / **interval_mean**: 342.462 — _not covered by context (missing method entry)_
- `pulse_detection` / `left` / **interval_std**: 328.087 — _not covered by context (missing method entry)_
- `pulse_detection` / `left` / **regularity_score**: 0.0419769 — _not covered by context (missing method entry)_
- `pulse_detection` / `right` / **num_pulses**: 310 — _not covered by context (missing method entry)_
- `pulse_detection` / `right` / **interval_mean**: 336.544 — _not covered by context (missing method entry)_
- `pulse_detection` / `right` / **interval_std**: 315.911 — _not covered by context (missing method entry)_
- `pulse_detection` / `right` / **regularity_score**: 0.0613063 — _not covered by context (missing method entry)_
- `pulse_detection` / `difference` / **num_pulses**: 236 — _not covered by context (missing method entry)_
- `pulse_detection` / `difference` / **interval_mean**: 443.17 — _not covered by context (missing method entry)_
- `pulse_detection` / `difference` / **interval_std**: 491.67 — _not covered by context (missing method entry)_
- `pulse_detection` / `difference` / **regularity_score**: 0 — _not covered by context (missing method entry)_
- `pulse_detection` / `left` / **num_pulses**: 132 — _not covered by context (missing method entry)_
- `pulse_detection` / `left` / **interval_mean**: 792.962 — _not covered by context (missing method entry)_
- `pulse_detection` / `left` / **interval_std**: 474.179 — _not covered by context (missing method entry)_
- `pulse_detection` / `left` / **regularity_score**: 0.402015 — _not covered by context (missing method entry)_
- `pulse_detection` / `right` / **num_pulses**: 131 — _not covered by context (missing method entry)_
- `pulse_detection` / `right` / **interval_mean**: 799.069 — _not covered by context (missing method entry)_
- `pulse_detection` / `right` / **interval_std**: 476.937 — _not covered by context (missing method entry)_
- `pulse_detection` / `right` / **regularity_score**: 0.403134 — _not covered by context (missing method entry)_
- `pulse_detection` / `difference` / **num_pulses**: 102 — _not covered by context (missing method entry)_
- `pulse_detection` / `difference` / **interval_mean**: 1031.14 — _not covered by context (missing method entry)_
- `pulse_detection` / `difference` / **interval_std**: 677.309 — _not covered by context (missing method entry)_
- `pulse_detection` / `difference` / **regularity_score**: 0.343145 — _not covered by context (missing method entry)_
- `pulse_detection` / `left` / **num_pulses**: 195 — _not covered by context (missing method entry)_
- `pulse_detection` / `left` / **interval_mean**: 530.113 — _not covered by context (missing method entry)_
- `pulse_detection` / `left` / **interval_std**: 715.629 — _not covered by context (missing method entry)_
- `pulse_detection` / `left` / **regularity_score**: 0 — _not covered by context (missing method entry)_
- `pulse_detection` / `right` / **num_pulses**: 211 — _not covered by context (missing method entry)_
- `pulse_detection` / `right` / **interval_mean**: 489.724 — _not covered by context (missing method entry)_
- `pulse_detection` / `right` / **interval_std**: 645.527 — _not covered by context (missing method entry)_
- `pulse_detection` / `right` / **regularity_score**: 0 — _not covered by context (missing method entry)_
- `pulse_detection` / `difference` / **num_pulses**: 59 — _not covered by context (missing method entry)_
- `pulse_detection` / `difference` / **interval_mean**: 1590.26 — _not covered by context (missing method entry)_
- `pulse_detection` / `difference` / **interval_std**: 1631.96 — _not covered by context (missing method entry)_
- `pulse_detection` / `difference` / **regularity_score**: 0 — _not covered by context (missing method entry)_
- `pulse_detection` / `left` / **num_pulses**: 89 — _not covered by context (missing method entry)_
- `pulse_detection` / `left` / **interval_mean**: 1168.66 — _not covered by context (missing method entry)_
- `pulse_detection` / `left` / **interval_std**: 933.518 — _not covered by context (missing method entry)_
- `pulse_detection` / `left` / **regularity_score**: 0.201206 — _not covered by context (missing method entry)_
- `pulse_detection` / `right` / **num_pulses**: 94 — _not covered by context (missing method entry)_
- `pulse_detection` / `right` / **interval_mean**: 1105.83 — _not covered by context (missing method entry)_
- `pulse_detection` / `right` / **interval_std**: 895.914 — _not covered by context (missing method entry)_
- `pulse_detection` / `right` / **regularity_score**: 0.189825 — _not covered by context (missing method entry)_
- `pulse_detection` / `difference` / **num_pulses**: 45 — _not covered by context (missing method entry)_
- `pulse_detection` / `difference` / **interval_mean**: 2090.48 — _not covered by context (missing method entry)_
- `pulse_detection` / `difference` / **interval_std**: 1656.01 — _not covered by context (missing method entry)_
- `pulse_detection` / `difference` / **regularity_score**: 0.207833 — _not covered by context (missing method entry)_
- `pulse_detection` / `left` / **num_pulses**: 50 — _not covered by context (missing method entry)_
- `pulse_detection` / `left` / **interval_mean**: 1860.45 — _not covered by context (missing method entry)_
- `pulse_detection` / `left` / **interval_std**: 3375.02 — _not covered by context (missing method entry)_
- `pulse_detection` / `left` / **regularity_score**: 0 — _not covered by context (missing method entry)_
- `pulse_detection` / `right` / **num_pulses**: 76 — _not covered by context (missing method entry)_
- `pulse_detection` / `right` / **interval_mean**: 1215.4 — _not covered by context (missing method entry)_
- `pulse_detection` / `right` / **interval_std**: 2114.03 — _not covered by context (missing method entry)_
- `pulse_detection` / `right` / **regularity_score**: 0 — _not covered by context (missing method entry)_
- `pulse_detection` / `difference` / **num_pulses**: 12 — _not covered by context (missing method entry)_
- `pulse_detection` / `difference` / **interval_mean**: 6992.36 — _not covered by context (missing method entry)_
- `pulse_detection` / `difference` / **interval_std**: 7295.91 — _not covered by context (missing method entry)_
- `pulse_detection` / `difference` / **regularity_score**: 0 — _not covered by context (missing method entry)_
- `pulse_detection` / `left` / **num_pulses**: 29 — _not covered by context (missing method entry)_
- `pulse_detection` / `left` / **interval_mean**: 3247.86 — _not covered by context (missing method entry)_
- `pulse_detection` / `left` / **interval_std**: 4065.32 — _not covered by context (missing method entry)_
- `pulse_detection` / `left` / **regularity_score**: 0 — _not covered by context (missing method entry)_
- `pulse_detection` / `right` / **num_pulses**: 41 — _not covered by context (missing method entry)_
- `pulse_detection` / `right` / **interval_mean**: 2273.47 — _not covered by context (missing method entry)_
- `pulse_detection` / `right` / **interval_std**: 2584.69 — _not covered by context (missing method entry)_
- `pulse_detection` / `right` / **regularity_score**: 0 — _not covered by context (missing method entry)_
- `pulse_detection` / `difference` / **num_pulses**: 11 — _not covered by context (missing method entry)_
- `pulse_detection` / `difference` / **interval_mean**: 7666.2 — _not covered by context (missing method entry)_
- `pulse_detection` / `difference` / **interval_std**: 7318.39 — _not covered by context (missing method entry)_
- `pulse_detection` / `difference` / **regularity_score**: 0.0453698 — _not covered by context (missing method entry)_
- `duration_ratios` / `left` / **num_events**: 516 — _not covered by context (missing method entry)_
- `duration_ratios` / `left` / **num_intervals**: 515 — _not covered by context (missing method entry)_
- `duration_ratios` / `left` / **ratio_mean**: 1.50472 — _not covered by context (missing method entry)_
- `duration_ratios` / `left` / **ratio_std**: 2.6896 — _not covered by context (missing method entry)_
- `duration_ratios` / `right` / **num_events**: 543 — _not covered by context (missing method entry)_
- `duration_ratios` / `right` / **num_intervals**: 542 — _not covered by context (missing method entry)_
- `duration_ratios` / `right` / **ratio_mean**: 1.46663 — _not covered by context (missing method entry)_
- `duration_ratios` / `right` / **ratio_std**: 2.62852 — _not covered by context (missing method entry)_
- `duration_ratios` / `difference` / **num_events**: 214 — _not covered by context (missing method entry)_
- `duration_ratios` / `difference` / **num_intervals**: 213 — _not covered by context (missing method entry)_
- `duration_ratios` / `difference` / **ratio_mean**: 3.10578 — _not covered by context (missing method entry)_
- `duration_ratios` / `difference` / **ratio_std**: 5.8222 — _not covered by context (missing method entry)_

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

- `am_detection` / `left`: **modulation_detected** = True (reference [0, 1]) → **within**. Binary indicator of detected amplitude modulation.
- `am_detection` / `right`: **modulation_detected** = True (reference [0, 1]) → **within**. Binary indicator of detected amplitude modulation.
- `am_detection` / `difference`: **modulation_detected** = False (reference [0, 1]) → **within**. Binary indicator of detected amplitude modulation.
- `fm_detection` / `left`: **fm_detected** = True (reference [0, 1]) → **within**. Binary indicator of detected frequency modulation.
- `fm_detection` / `right`: **fm_detected** = True (reference [0, 1]) → **within**. Binary indicator of detected frequency modulation.
- `fm_detection` / `difference`: **fm_detected** = True (reference [0, 1]) → **within**. Binary indicator of detected frequency modulation.

#### 3.B Metrics without reference zones

**Status B — context-dependent (no stable zone)**

- `am_detection` / `left`: **dominant_modulation_freq** = 2.99842 — Dominant modulation frequency.
- `am_detection` / `left`: **modulation_depth** = 6.02428 — Estimated modulation depth.
- `am_detection` / `right`: **dominant_modulation_freq** = 2.99842 — Dominant modulation frequency.
- `am_detection` / `right`: **modulation_depth** = 5.65594 — Estimated modulation depth.
- `am_detection` / `difference`: **dominant_modulation_freq** = 0 — Dominant modulation frequency.
- `am_detection` / `difference`: **modulation_depth** = 8.51884 — Estimated modulation depth.
- `fm_detection` / `left`: **frequency_deviation** = 2378.41 — Estimated frequency deviation.
- `fm_detection` / `right`: **frequency_deviation** = 2191.06 — Estimated frequency deviation.
- `fm_detection` / `difference`: **frequency_deviation** = 3170.16 — Estimated frequency deviation.

**Status C — descriptive only (no stable zone)**

_No status C metrics listed for this family._

**Unmapped / missing context coverage**

- `am_detection` / `left` / **num_modulation_frequencies**: 1 — _not covered by context (missing metric entry)_
- `am_detection` / `left` / **modulation_index**: 0.776155 — _not covered by context (missing metric entry)_
- `am_detection` / `left` / **envelope_mean**: 0.123242 — _not covered by context (missing metric entry)_
- `am_detection` / `left` / **envelope_std**: 0.0956545 — _not covered by context (missing metric entry)_
- `am_detection` / `right` / **num_modulation_frequencies**: 1 — _not covered by context (missing metric entry)_
- `am_detection` / `right` / **modulation_index**: 0.777984 — _not covered by context (missing metric entry)_
- `am_detection` / `right` / **envelope_mean**: 0.123241 — _not covered by context (missing metric entry)_
- `am_detection` / `right` / **envelope_std**: 0.0958798 — _not covered by context (missing metric entry)_
- `am_detection` / `difference` / **num_modulation_frequencies**: 0 — _not covered by context (missing metric entry)_
- `am_detection` / `difference` / **modulation_index**: 0.821304 — _not covered by context (missing metric entry)_
- `am_detection` / `difference` / **envelope_mean**: 0.0239492 — _not covered by context (missing metric entry)_
- `am_detection` / `difference` / **envelope_std**: 0.0196696 — _not covered by context (missing metric entry)_
- `fm_detection` / `left` / **carrier_frequency_mean**: 4168.66 — _not covered by context (missing metric entry)_
- `fm_detection` / `left` / **frequency_range**: 22072.2 — _not covered by context (missing metric entry)_
- `fm_detection` / `left` / **frequency_std**: 2378.41 — _not covered by context (missing metric entry)_
- `fm_detection` / `left` / **num_fm_components**: 0 — _not covered by context (missing metric entry)_
- `fm_detection` / `left` / **modulation_index_fm**: 0.570545 — _not covered by context (missing metric entry)_
- `fm_detection` / `right` / **carrier_frequency_mean**: 4157.71 — _not covered by context (missing metric entry)_
- `fm_detection` / `right` / **frequency_range**: 22070.6 — _not covered by context (missing metric entry)_
- `fm_detection` / `right` / **frequency_std**: 2191.06 — _not covered by context (missing metric entry)_
- `fm_detection` / `right` / **num_fm_components**: 0 — _not covered by context (missing metric entry)_
- `fm_detection` / `right` / **modulation_index_fm**: 0.526986 — _not covered by context (missing metric entry)_
- `fm_detection` / `difference` / **carrier_frequency_mean**: 3993.93 — _not covered by context (missing metric entry)_
- `fm_detection` / `difference` / **frequency_range**: 22084.3 — _not covered by context (missing metric entry)_
- `fm_detection` / `difference` / **frequency_std**: 3170.16 — _not covered by context (missing metric entry)_
- `fm_detection` / `difference` / **num_fm_components**: 0 — _not covered by context (missing metric entry)_
- `fm_detection` / `difference` / **modulation_index_fm**: 0.793746 — _not covered by context (missing metric entry)_
- `phase_analysis` / `left` / **phase_mean**: 0.0518149 — _not covered by context (missing method entry)_
- `phase_analysis` / `left` / **phase_std**: 1.79831 — _not covered by context (missing method entry)_
- `phase_analysis` / `left` / **phase_range**: 6.28317 — _not covered by context (missing method entry)_
- `phase_analysis` / `left` / **unwrapped_phase_total**: 131030 — _not covered by context (missing method entry)_
- `phase_analysis` / `left` / **phase_coherence**: 0.477477 — _not covered by context (missing method entry)_
- `phase_analysis` / `left` / **num_phase_jumps**: 32996 — _not covered by context (missing method entry)_
- `phase_analysis` / `left` / **phase_jump_rate**: 6595.73 — _not covered by context (missing method entry)_
- `phase_analysis` / `right` / **phase_mean**: 0.0731416 — _not covered by context (missing method entry)_
- `phase_analysis` / `right` / **phase_std**: 1.7949 — _not covered by context (missing method entry)_
- `phase_analysis` / `right` / **phase_range**: 6.28317 — _not covered by context (missing method entry)_
- `phase_analysis` / `right` / **unwrapped_phase_total**: 130686 — _not covered by context (missing method entry)_
- `phase_analysis` / `right` / **phase_coherence**: 0.506555 — _not covered by context (missing method entry)_
- `phase_analysis` / `right` / **num_phase_jumps**: 32252 — _not covered by context (missing method entry)_
- `phase_analysis` / `right` / **phase_jump_rate**: 6447.01 — _not covered by context (missing method entry)_
- `phase_analysis` / `difference` / **phase_mean**: -0.0354586 — _not covered by context (missing method entry)_
- `phase_analysis` / `difference` / **phase_std**: 1.78953 — _not covered by context (missing method entry)_
- `phase_analysis` / `difference` / **phase_range**: 6.28317 — _not covered by context (missing method entry)_
- `phase_analysis` / `difference` / **unwrapped_phase_total**: 125538 — _not covered by context (missing method entry)_
- `phase_analysis` / `difference` / **phase_coherence**: 0.324723 — _not covered by context (missing method entry)_
- `phase_analysis` / `difference` / **num_phase_jumps**: 35717 — _not covered by context (missing method entry)_
- `phase_analysis` / `difference` / **phase_jump_rate**: 7139.64 — _not covered by context (missing method entry)_
- `modulation_index` / `left` / **modulation_index**: 0.776155 — _not covered by context (missing method entry)_
- `modulation_index` / `left` / **modulation_depth**: 6.02428 — _not covered by context (missing method entry)_
- `modulation_index` / `left` / **ac_component**: 0.0956545 — _not covered by context (missing method entry)_
- `modulation_index` / `left` / **dc_component**: 0.123242 — _not covered by context (missing method entry)_
- `modulation_index` / `left` / **peak_to_average_ratio**: 6.02428 — _not covered by context (missing method entry)_
- `modulation_index` / `right` / **modulation_index**: 0.777984 — _not covered by context (missing method entry)_
- `modulation_index` / `right` / **modulation_depth**: 5.65594 — _not covered by context (missing method entry)_
- `modulation_index` / `right` / **ac_component**: 0.0958798 — _not covered by context (missing method entry)_
- `modulation_index` / `right` / **dc_component**: 0.123241 — _not covered by context (missing method entry)_
- `modulation_index` / `right` / **peak_to_average_ratio**: 5.65594 — _not covered by context (missing method entry)_
- `modulation_index` / `difference` / **modulation_index**: 0.821304 — _not covered by context (missing method entry)_
- `modulation_index` / `difference` / **modulation_depth**: 8.51884 — _not covered by context (missing method entry)_
- `modulation_index` / `difference` / **ac_component**: 0.0196696 — _not covered by context (missing method entry)_
- `modulation_index` / `difference` / **dc_component**: 0.0239492 — _not covered by context (missing method entry)_
- `modulation_index` / `difference` / **peak_to_average_ratio**: 8.51884 — _not covered by context (missing method entry)_
- `chirp_detection` / `left` / **num_chirps**: 48 — _not covered by context (missing method entry)_
- `chirp_detection` / `left` / **total_chirp_duration**: 3.34367 — _not covered by context (missing method entry)_
- `chirp_detection` / `left` / **mean_chirp_rate**: 14366.3 — _not covered by context (missing method entry)_
- `chirp_detection` / `right` / **num_chirps**: 47 — _not covered by context (missing method entry)_
- `chirp_detection` / `right` / **total_chirp_duration**: 3.27401 — _not covered by context (missing method entry)_
- `chirp_detection` / `right` / **mean_chirp_rate**: 14509.2 — _not covered by context (missing method entry)_
- `chirp_detection` / `difference` / **num_chirps**: 53 — _not covered by context (missing method entry)_
- `chirp_detection` / `difference` / **total_chirp_duration**: 3.69197 — _not covered by context (missing method entry)_
- `chirp_detection` / `difference` / **mean_chirp_rate**: 14744.1 — _not covered by context (missing method entry)_

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

- `fft_global` / `left`: **peak_frequency** = 4528.02 (reference [0, 22050]) → **within**. Frequency of the dominant spectral peak.
- `fft_global` / `left`: **spectral_energy** = 3.16892e+07 (reference [0, 1]) → **above**. Total normalized spectral energy.
- `fft_global` / `right`: **peak_frequency** = 4528.02 (reference [0, 22050]) → **within**. Frequency of the dominant spectral peak.
- `fft_global` / `right`: **spectral_energy** = 3.17133e+07 (reference [0, 1]) → **above**. Total normalized spectral energy.
- `fft_global` / `difference`: **peak_frequency** = 4326.52 (reference [0, 22050]) → **within**. Frequency of the dominant spectral peak.
- `fft_global` / `difference`: **spectral_energy** = 1.21887e+06 (reference [0, 1]) → **above**. Total normalized spectral energy.
- `spectral_flatness` / `left`: **spectral_flatness** = 0.00494548 (reference [0, 1]) → **within**. Noise-like versus tonal spectral indicator.
- `spectral_flatness` / `right`: **spectral_flatness** = 0.00493943 (reference [0, 1]) → **within**. Noise-like versus tonal spectral indicator.
- `spectral_flatness` / `difference`: **spectral_flatness** = 0.0130293 (reference [0, 1]) → **within**. Noise-like versus tonal spectral indicator.

#### 3.B Metrics without reference zones

**Status B — context-dependent (no stable zone)**

- `peak_detection` / `left`: **num_peaks** = 1172 — Number of detected spectral peaks.
- `peak_detection` / `right`: **num_peaks** = 1187 — Number of detected spectral peaks.
- `peak_detection` / `difference`: **num_peaks** = 1104 — Number of detected spectral peaks.

**Status C — descriptive only (no stable zone)**

_No status C metrics listed for this family._

**Unmapped / missing context coverage**

- `fft_global` / `left` / **n_fft**: 110308 — _not covered by context (missing metric entry)_
- `fft_global` / `left` / **frequency_resolution**: 0.199895 — _not covered by context (missing metric entry)_
- `fft_global` / `left` / **peak_magnitude**: 692.123 — _not covered by context (missing metric entry)_
- `fft_global` / `right` / **n_fft**: 110308 — _not covered by context (missing metric entry)_
- `fft_global` / `right` / **frequency_resolution**: 0.199895 — _not covered by context (missing metric entry)_
- `fft_global` / `right` / **peak_magnitude**: 701.486 — _not covered by context (missing metric entry)_
- `fft_global` / `difference` / **n_fft**: 110308 — _not covered by context (missing metric entry)_
- `fft_global` / `difference` / **frequency_resolution**: 0.199895 — _not covered by context (missing metric entry)_
- `fft_global` / `difference` / **peak_magnitude**: 74.9876 — _not covered by context (missing metric entry)_
- `peak_detection` / `left` / **dominant_frequency**: 2832.91 — _not covered by context (missing metric entry)_
- `peak_detection` / `left` / **frequency_spread**: 906.082 — _not covered by context (missing metric entry)_
- `peak_detection` / `right` / **dominant_frequency**: 2832.71 — _not covered by context (missing metric entry)_
- `peak_detection` / `right` / **frequency_spread**: 911.815 — _not covered by context (missing metric entry)_
- `peak_detection` / `difference` / **dominant_frequency**: 2883.48 — _not covered by context (missing metric entry)_
- `peak_detection` / `difference` / **frequency_spread**: 884.846 — _not covered by context (missing metric entry)_
- `harmonic_analysis` / `left` / **fundamental_frequency**: 168.911 — _not covered by context (missing method entry)_
- `harmonic_analysis` / `left` / **harmonics_detected**: 10 — _not covered by context (missing method entry)_
- `harmonic_analysis` / `left` / **harmonicity_score**: 1 — _not covered by context (missing method entry)_
- `harmonic_analysis` / `right` / **fundamental_frequency**: 223.882 — _not covered by context (missing method entry)_
- `harmonic_analysis` / `right` / **harmonics_detected**: 10 — _not covered by context (missing method entry)_
- `harmonic_analysis` / `right` / **harmonicity_score**: 1 — _not covered by context (missing method entry)_
- `harmonic_analysis` / `difference` / **fundamental_frequency**: 218.085 — _not covered by context (missing method entry)_
- `harmonic_analysis` / `difference` / **harmonics_detected**: 10 — _not covered by context (missing method entry)_
- `harmonic_analysis` / `difference` / **harmonicity_score**: 1 — _not covered by context (missing method entry)_
- `cepstrum` / `left` / **peak_quefrency**: 9.07029e-05 — _not covered by context (missing method entry)_
- `cepstrum` / `left` / **peak_magnitude**: 0.782014 — _not covered by context (missing method entry)_
- `cepstrum` / `left` / **cepstrum_mean**: 0.00101421 — _not covered by context (missing method entry)_
- `cepstrum` / `left` / **cepstrum_std**: 0.00693496 — _not covered by context (missing method entry)_
- `cepstrum` / `left` / **samples_analyzed**: 100000 — _not covered by context (missing method entry)_
- `cepstrum` / `right` / **peak_quefrency**: 9.07029e-05 — _not covered by context (missing method entry)_
- `cepstrum` / `right` / **peak_magnitude**: 0.762119 — _not covered by context (missing method entry)_
- `cepstrum` / `right` / **cepstrum_mean**: 0.000993905 — _not covered by context (missing method entry)_
- `cepstrum` / `right` / **cepstrum_std**: 0.00669667 — _not covered by context (missing method entry)_
- `cepstrum` / `right` / **samples_analyzed**: 100000 — _not covered by context (missing method entry)_
- `cepstrum` / `difference` / **peak_quefrency**: 9.07029e-05 — _not covered by context (missing method entry)_
- `cepstrum` / `difference` / **peak_magnitude**: 0.859355 — _not covered by context (missing method entry)_
- `cepstrum` / `difference` / **cepstrum_mean**: 0.00122812 — _not covered by context (missing method entry)_
- `cepstrum` / `difference` / **cepstrum_std**: 0.0129848 — _not covered by context (missing method entry)_
- `cepstrum` / `difference` / **samples_analyzed**: 100000 — _not covered by context (missing method entry)_
- `spectral_centroid` / `left` / **spectral_centroid**: 4486.72 — _not covered by context (missing method entry)_
- `spectral_centroid` / `left` / **normalized_centroid**: 0.406959 — _not covered by context (missing method entry)_
- `spectral_centroid` / `right` / **spectral_centroid**: 4485.65 — _not covered by context (missing method entry)_
- `spectral_centroid` / `right` / **normalized_centroid**: 0.406862 — _not covered by context (missing method entry)_
- `spectral_centroid` / `difference` / **spectral_centroid**: 4468.52 — _not covered by context (missing method entry)_
- `spectral_centroid` / `difference` / **normalized_centroid**: 0.405308 — _not covered by context (missing method entry)_
- `spectral_bandwidth` / `left` / **spectral_bandwidth**: 705.377 — _not covered by context (missing method entry)_
- `spectral_bandwidth` / `left` / **spectral_centroid_Hz**: 4559.72 — _not covered by context (missing method entry)_
- `spectral_bandwidth` / `right` / **spectral_bandwidth**: 704.499 — _not covered by context (missing method entry)_
- `spectral_bandwidth` / `right` / **spectral_centroid_Hz**: 4557.51 — _not covered by context (missing method entry)_
- `spectral_bandwidth` / `difference` / **spectral_bandwidth**: 659.933 — _not covered by context (missing method entry)_
- `spectral_bandwidth` / `difference` / **spectral_centroid_Hz**: 4496.29 — _not covered by context (missing method entry)_
- `spectral_rolloff` / `left` / **rolloff_frequency**: 5472.72 — _not covered by context (missing method entry)_
- `spectral_rolloff` / `left` / **rolloff_percent**: 0.85 — _not covered by context (missing method entry)_
- `spectral_rolloff` / `left` / **normalized_rolloff**: 0.496392 — _not covered by context (missing method entry)_
- `spectral_rolloff` / `left` / **energy_concentration**: 0.496392 — _not covered by context (missing method entry)_
- `spectral_rolloff` / `right` / **rolloff_frequency**: 5472.72 — _not covered by context (missing method entry)_
- `spectral_rolloff` / `right` / **rolloff_percent**: 0.85 — _not covered by context (missing method entry)_
- `spectral_rolloff` / `right` / **normalized_rolloff**: 0.496392 — _not covered by context (missing method entry)_
- `spectral_rolloff` / `right` / **energy_concentration**: 0.496392 — _not covered by context (missing method entry)_
- `spectral_rolloff` / `difference` / **rolloff_frequency**: 5227.05 — _not covered by context (missing method entry)_
- `spectral_rolloff` / `difference` / **rolloff_percent**: 0.85 — _not covered by context (missing method entry)_
- `spectral_rolloff` / `difference` / **normalized_rolloff**: 0.474109 — _not covered by context (missing method entry)_
- `spectral_rolloff` / `difference` / **energy_concentration**: 0.474109 — _not covered by context (missing method entry)_
- `spectral_flux` / `left` / **mean_flux**: 0.0359413 — _not covered by context (missing method entry)_
- `spectral_flux` / `left` / **std_flux**: 0.0150067 — _not covered by context (missing method entry)_
- `spectral_flux` / `left` / **max_flux**: 0.0703315 — _not covered by context (missing method entry)_
- `spectral_flux` / `left` / **min_flux**: 0 — _not covered by context (missing method entry)_
- `spectral_flux` / `left` / **num_frames**: 216 — _not covered by context (missing method entry)_
- `spectral_flux` / `left` / **flux_variation**: 0.417535 — _not covered by context (missing method entry)_
- `spectral_flux` / `right` / **mean_flux**: 0.035772 — _not covered by context (missing method entry)_
- `spectral_flux` / `right` / **std_flux**: 0.0154473 — _not covered by context (missing method entry)_
- `spectral_flux` / `right` / **max_flux**: 0.0804406 — _not covered by context (missing method entry)_
- `spectral_flux` / `right` / **min_flux**: 0 — _not covered by context (missing method entry)_
- `spectral_flux` / `right` / **num_frames**: 216 — _not covered by context (missing method entry)_
- `spectral_flux` / `right` / **flux_variation**: 0.431825 — _not covered by context (missing method entry)_
- `spectral_flux` / `difference` / **mean_flux**: 0.00993179 — _not covered by context (missing method entry)_
- `spectral_flux` / `difference` / **std_flux**: 0.00379441 — _not covered by context (missing method entry)_
- `spectral_flux` / `difference` / **max_flux**: 0.0229072 — _not covered by context (missing method entry)_
- `spectral_flux` / `difference` / **min_flux**: 0 — _not covered by context (missing method entry)_
- `spectral_flux` / `difference` / **num_frames**: 216 — _not covered by context (missing method entry)_
- `spectral_flux` / `difference` / **flux_variation**: 0.382047 — _not covered by context (missing method entry)_
- `spectral_flatness` / `left` / **tonality**: 0.995055 — _not covered by context (missing metric entry)_
- `spectral_flatness` / `right` / **tonality**: 0.995061 — _not covered by context (missing metric entry)_
- `spectral_flatness` / `difference` / **tonality**: 0.986971 — _not covered by context (missing metric entry)_

**Expected by context but missing in results (not evaluated)**

_No expected scalar metrics were missing for this family._


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

- `stft` / `left`: **dominant_freq_mean** = 4455.34 — Mean dominant frequency over time.
- `stft` / `left`: **spectral_flux_mean** = 0.0359413 — Average spectral flux magnitude.
- `stft` / `left`: **temporal_stability** = 0.470107 — Stability of spectral content over time.
- `stft` / `right`: **dominant_freq_mean** = 4443.18 — Mean dominant frequency over time.
- `stft` / `right`: **spectral_flux_mean** = 0.035772 — Average spectral flux magnitude.
- `stft` / `right`: **temporal_stability** = 0.469756 — Stability of spectral content over time.
- `stft` / `difference`: **dominant_freq_mean** = 4364.24 — Mean dominant frequency over time.
- `stft` / `difference`: **spectral_flux_mean** = 0.00993179 — Average spectral flux magnitude.
- `stft` / `difference`: **temporal_stability** = 0.450192 — Stability of spectral content over time.

**Status C — descriptive only (no stable zone)**

_No status C metrics listed for this family._

**Unmapped / missing context coverage**

- `stft` / `left` / **num_time_frames**: 217 — _not covered by context (missing metric entry)_
- `stft` / `left` / **num_freq_bins**: 1025 — _not covered by context (missing metric entry)_
- `stft` / `left` / **frequency_resolution**: 10.7666 — _not covered by context (missing metric entry)_
- `stft` / `left` / **time_resolution**: 0.02322 — _not covered by context (missing metric entry)_
- `stft` / `left` / **mean_magnitude**: 0.000477322 — _not covered by context (missing metric entry)_
- `stft` / `left` / **max_magnitude**: 0.0398015 — _not covered by context (missing metric entry)_
- `stft` / `left` / **dominant_freq_std**: 1087.3 — _not covered by context (missing metric entry)_
- `stft` / `left` / **spectral_flux_max**: 0.0703315 — _not covered by context (missing metric entry)_
- `stft` / `right` / **num_time_frames**: 217 — _not covered by context (missing metric entry)_
- `stft` / `right` / **num_freq_bins**: 1025 — _not covered by context (missing metric entry)_
- `stft` / `right` / **frequency_resolution**: 10.7666 — _not covered by context (missing metric entry)_
- `stft` / `right` / **time_resolution**: 0.02322 — _not covered by context (missing metric entry)_
- `stft` / `right` / **mean_magnitude**: 0.000477419 — _not covered by context (missing metric entry)_
- `stft` / `right` / **max_magnitude**: 0.0398025 — _not covered by context (missing metric entry)_
- `stft` / `right` / **dominant_freq_std**: 1097.28 — _not covered by context (missing metric entry)_
- `stft` / `right` / **spectral_flux_max**: 0.0804406 — _not covered by context (missing metric entry)_
- `stft` / `difference` / **num_time_frames**: 217 — _not covered by context (missing metric entry)_
- `stft` / `difference` / **num_freq_bins**: 1025 — _not covered by context (missing metric entry)_
- `stft` / `difference` / **frequency_resolution**: 10.7666 — _not covered by context (missing metric entry)_
- `stft` / `difference` / **time_resolution**: 0.02322 — _not covered by context (missing metric entry)_
- `stft` / `difference` / **mean_magnitude**: 0.000121589 — _not covered by context (missing metric entry)_
- `stft` / `difference` / **max_magnitude**: 0.00757549 — _not covered by context (missing metric entry)_
- `stft` / `difference` / **dominant_freq_std**: 1143.04 — _not covered by context (missing metric entry)_
- `stft` / `difference` / **spectral_flux_max**: 0.0229072 — _not covered by context (missing metric entry)_
- `cqt` / `left` / **samples_analyzed**: 110308 — _not covered by context (missing method entry)_
- `cqt` / `left` / **hop_length**: 512 — _not covered by context (missing method entry)_
- `cqt` / `left` / **fmin_hz**: 32.7032 — _not covered by context (missing method entry)_
- `cqt` / `left` / **n_bins**: 84 — _not covered by context (missing method entry)_
- `cqt` / `left` / **bins_per_octave**: 12 — _not covered by context (missing method entry)_
- `cqt` / `left` / **num_time_frames**: 216 — _not covered by context (missing method entry)_
- `cqt` / `left` / **num_freq_bins**: 84 — _not covered by context (missing method entry)_
- `cqt` / `left` / **mean_magnitude_db**: -76.9567 — _not covered by context (missing method entry)_
- `cqt` / `left` / **max_magnitude_db**: 0 — _not covered by context (missing method entry)_
- `cqt` / `right` / **samples_analyzed**: 110308 — _not covered by context (missing method entry)_
- `cqt` / `right` / **hop_length**: 512 — _not covered by context (missing method entry)_
- `cqt` / `right` / **fmin_hz**: 32.7032 — _not covered by context (missing method entry)_
- `cqt` / `right` / **n_bins**: 84 — _not covered by context (missing method entry)_
- `cqt` / `right` / **bins_per_octave**: 12 — _not covered by context (missing method entry)_
- `cqt` / `right` / **num_time_frames**: 216 — _not covered by context (missing method entry)_
- `cqt` / `right` / **num_freq_bins**: 84 — _not covered by context (missing method entry)_
- `cqt` / `right` / **mean_magnitude_db**: -76.9375 — _not covered by context (missing method entry)_
- `cqt` / `right` / **max_magnitude_db**: 0 — _not covered by context (missing method entry)_
- `cqt` / `difference` / **samples_analyzed**: 110308 — _not covered by context (missing method entry)_
- `cqt` / `difference` / **hop_length**: 512 — _not covered by context (missing method entry)_
- `cqt` / `difference` / **fmin_hz**: 32.7032 — _not covered by context (missing method entry)_
- `cqt` / `difference` / **n_bins**: 84 — _not covered by context (missing method entry)_
- `cqt` / `difference` / **bins_per_octave**: 12 — _not covered by context (missing method entry)_
- `cqt` / `difference` / **num_time_frames**: 216 — _not covered by context (missing method entry)_
- `cqt` / `difference` / **num_freq_bins**: 84 — _not covered by context (missing method entry)_
- `cqt` / `difference` / **mean_magnitude_db**: -77.1647 — _not covered by context (missing method entry)_
- `cqt` / `difference` / **max_magnitude_db**: 0 — _not covered by context (missing method entry)_
- `wavelet` / `global` / **error**: Morlet wavelet not available. Please upgrade scipy to >= 1.4.0 or install PyWavelets: pip install PyWavelets — _not covered by context (missing method entry)_

**Expected by context but missing in results (not evaluated)**

_No expected scalar metrics were missing for this family._


### information

- Objective: Position the global degree of randomness or organization of the audio signal.
- Coverage: `partial`
- Rationale: Information-theoretic metrics provide coarse indicators without semantic interpretation.

- Documentary references:
  - T. M. Cover & J. A. Thomas — "Elements of Information Theory" — (2006). Canonical reference for entropy and information measures.

#### 3.A Metrics with reference zones (Status A)

- `shannon_entropy` / `left`: **shannon_entropy** = 6.22797 (reference [0, 16]) → **within**. Shannon entropy of the signal.
- `shannon_entropy` / `left`: **normalized_entropy** = 0.778496 (reference [0, 1]) → **within**. Entropy normalized by maximum possible entropy.
- `shannon_entropy` / `right`: **shannon_entropy** = 6.32017 (reference [0, 16]) → **within**. Shannon entropy of the signal.
- `shannon_entropy` / `right`: **normalized_entropy** = 0.790021 (reference [0, 1]) → **within**. Entropy normalized by maximum possible entropy.
- `shannon_entropy` / `difference`: **shannon_entropy** = 5.66076 (reference [0, 16]) → **within**. Shannon entropy of the signal.
- `shannon_entropy` / `difference`: **normalized_entropy** = 0.707595 (reference [0, 1]) → **within**. Entropy normalized by maximum possible entropy.

#### 3.B Metrics without reference zones

**Status B — context-dependent (no stable zone)**

_No status B metrics listed for this family._

**Status C — descriptive only (no stable zone)**

_No status C metrics listed for this family._

**Unmapped / missing context coverage**

- `shannon_entropy` / `left` / **max_entropy**: 8 — _not covered by context (missing metric entry)_
- `shannon_entropy` / `left` / **num_bins**: 256 — _not covered by context (missing metric entry)_
- `shannon_entropy` / `right` / **max_entropy**: 8 — _not covered by context (missing metric entry)_
- `shannon_entropy` / `right` / **num_bins**: 256 — _not covered by context (missing metric entry)_
- `shannon_entropy` / `difference` / **max_entropy**: 8 — _not covered by context (missing metric entry)_
- `shannon_entropy` / `difference` / **num_bins**: 256 — _not covered by context (missing metric entry)_
- `local_entropy` / `left` / **mean_entropy**: 4.93372 — _not covered by context (missing method entry)_
- `local_entropy` / `left` / **std_entropy**: 1.05616 — _not covered by context (missing method entry)_
- `local_entropy` / `left` / **min_entropy**: -0 — _not covered by context (missing method entry)_
- `local_entropy` / `left` / **max_entropy**: 5.72964 — _not covered by context (missing method entry)_
- `local_entropy` / `left` / **num_windows**: 214 — _not covered by context (missing method entry)_
- `local_entropy` / `left` / **entropy_variation**: 0.214069 — _not covered by context (missing method entry)_
- `local_entropy` / `right` / **mean_entropy**: 4.94732 — _not covered by context (missing method entry)_
- `local_entropy` / `right` / **std_entropy**: 1.03907 — _not covered by context (missing method entry)_
- `local_entropy` / `right` / **min_entropy**: -0 — _not covered by context (missing method entry)_
- `local_entropy` / `right` / **max_entropy**: 5.72564 — _not covered by context (missing method entry)_
- `local_entropy` / `right` / **num_windows**: 214 — _not covered by context (missing method entry)_
- `local_entropy` / `right` / **entropy_variation**: 0.210027 — _not covered by context (missing method entry)_
- `local_entropy` / `difference` / **mean_entropy**: 4.73365 — _not covered by context (missing method entry)_
- `local_entropy` / `difference` / **std_entropy**: 1.34727 — _not covered by context (missing method entry)_
- `local_entropy` / `difference` / **min_entropy**: -0 — _not covered by context (missing method entry)_
- `local_entropy` / `difference` / **max_entropy**: 5.81319 — _not covered by context (missing method entry)_
- `local_entropy` / `difference` / **num_windows**: 214 — _not covered by context (missing method entry)_
- `local_entropy` / `difference` / **entropy_variation**: 0.284616 — _not covered by context (missing method entry)_
- `compression_ratio` / `left` / **original_size**: 200000 — _not covered by context (missing method entry)_
- `compression_ratio` / `left` / **compressed_size**: 176955 — _not covered by context (missing method entry)_
- `compression_ratio` / `left` / **compression_ratio**: 1.13023 — _not covered by context (missing method entry)_
- `compression_ratio` / `left` / **samples_analyzed**: 100000 — _not covered by context (missing method entry)_
- `compression_ratio` / `right` / **original_size**: 200000 — _not covered by context (missing method entry)_
- `compression_ratio` / `right` / **compressed_size**: 177029 — _not covered by context (missing method entry)_
- `compression_ratio` / `right` / **compression_ratio**: 1.12976 — _not covered by context (missing method entry)_
- `compression_ratio` / `right` / **samples_analyzed**: 100000 — _not covered by context (missing method entry)_
- `compression_ratio` / `difference` / **original_size**: 200000 — _not covered by context (missing method entry)_
- `compression_ratio` / `difference` / **compressed_size**: 151392 — _not covered by context (missing method entry)_
- `compression_ratio` / `difference` / **compression_ratio**: 1.32107 — _not covered by context (missing method entry)_
- `compression_ratio` / `difference` / **samples_analyzed**: 100000 — _not covered by context (missing method entry)_
- `approximate_complexity` / `left` / **approximate_complexity**: 0.039417 — _not covered by context (missing method entry)_
- `approximate_complexity` / `left` / **pattern_length**: 2 — _not covered by context (missing method entry)_
- `approximate_complexity` / `left` / **tolerance**: 0.0137036 — _not covered by context (missing method entry)_
- `approximate_complexity` / `left` / **samples_analyzed**: 5000 — _not covered by context (missing method entry)_
- `approximate_complexity` / `right` / **approximate_complexity**: 0.0683778 — _not covered by context (missing method entry)_
- `approximate_complexity` / `right` / **pattern_length**: 2 — _not covered by context (missing method entry)_
- `approximate_complexity` / `right` / **tolerance**: 0.0141817 — _not covered by context (missing method entry)_
- `approximate_complexity` / `right` / **samples_analyzed**: 5000 — _not covered by context (missing method entry)_
- `approximate_complexity` / `difference` / **approximate_complexity**: 0.0541399 — _not covered by context (missing method entry)_
- `approximate_complexity` / `difference` / **pattern_length**: 2 — _not covered by context (missing method entry)_
- `approximate_complexity` / `difference` / **tolerance**: 0.00296747 — _not covered by context (missing method entry)_
- `approximate_complexity` / `difference` / **samples_analyzed**: 5000 — _not covered by context (missing method entry)_
- `mutual_information` / `global` / **num_channels**: 3 — _not covered by context (missing method entry)_
- `mutual_information` / `global` / **mean_mi**: 0.868203 — _not covered by context (missing method entry)_
- `mutual_information` / `global` / **max_mi**: 2.36954 — _not covered by context (missing method entry)_
- `mutual_information` / `global` / **samples_analyzed**: 50000 — _not covered by context (missing method entry)_

**Expected by context but missing in results (not evaluated)**

_No expected scalar metrics were missing for this family._


### inter_channel

- Objective: Identify inter-channel asymmetry, abnormal correlation, or structured information carried in the differential (L−R) signal.
- Coverage: `partial`
- Rationale: Metrics highlight structured inter-channel relationships rather than perceptual stereo quality.

- Documentary references:
  - J. Blauert — "Spatial Hearing" — (1997). Reference on binaural correlation and inter-channel structure.
  - V. Pulkki & M. Karjalainen — "Communication Acoustics" — (2015). Foundations of stereo and multichannel signal relationships.

#### 3.A Metrics with reference zones (Status A)

- `lr_difference` / `lr_difference`: **difference_energy** = 52.9729 (reference [0, 1]) → **above**. Energy of the L−R differential signal.
- `lr_difference` / `lr_difference`: **energy_ratio** = 0.0197139 (reference [0, 1]) → **within**. Energy ratio between differential and summed channels.
- `cross_correlation` / `left_vs_right`: **max_correlation** = 1 (reference [-1, 1]) → **within**. Maximum normalized cross-correlation.
- `cross_correlation` / `left_vs_right`: **correlation_at_zero** = 1 (reference [-1, 1]) → **within**. Zero-lag normalized inter-channel correlation.
- `cross_correlation` / `left_vs_difference`: **max_correlation** = 2.46977 (reference [-1, 1]) → **above**. Maximum normalized cross-correlation.
- `cross_correlation` / `left_vs_difference`: **correlation_at_zero** = 1 (reference [-1, 1]) → **within**. Zero-lag normalized inter-channel correlation.
- `cross_correlation` / `right_vs_difference`: **max_correlation** = 1.66652 (reference [-1, 1]) → **above**. Maximum normalized cross-correlation.
- `cross_correlation` / `right_vs_difference`: **correlation_at_zero** = 1 (reference [-1, 1]) → **within**. Zero-lag normalized inter-channel correlation.

#### 3.B Metrics without reference zones

**Status B — context-dependent (no stable zone)**

- `cross_correlation` / `left_vs_right`: **peak_lag** = 0 — Lag at which maximum correlation occurs.
- `cross_correlation` / `left_vs_difference`: **peak_lag** = 730 — Lag at which maximum correlation occurs.
- `cross_correlation` / `right_vs_difference`: **peak_lag** = 511 — Lag at which maximum correlation occurs.

**Status C — descriptive only (no stable zone)**

_No status C metrics listed for this family._

**Unmapped / missing context coverage**

- `lr_difference` / `lr_difference` / **left_energy**: 1342.35 — _not covered by context (missing metric entry)_
- `lr_difference` / `lr_difference` / **right_energy**: 1344.73 — _not covered by context (missing metric entry)_
- `lr_difference` / `lr_difference` / **difference_rms**: 0.0219141 — _not covered by context (missing metric entry)_
- `lr_difference` / `lr_difference` / **difference_peak_freq**: 4738.11 — _not covered by context (missing metric entry)_
- `lr_difference` / `lr_difference` / **difference_peak_magnitude**: 118.059 — _not covered by context (missing metric entry)_
- `lr_difference` / `lr_difference` / **contains_unique_info**: True — _not covered by context (missing metric entry)_
- `cross_correlation` / `left_vs_right` / **peak_value**: 1 — _not covered by context (missing metric entry)_
- `cross_correlation` / `left_vs_right` / **mean_correlation**: 9.50192e-05 — _not covered by context (missing metric entry)_
- `cross_correlation` / `left_vs_difference` / **peak_value**: -2.46977 — _not covered by context (missing metric entry)_
- `cross_correlation` / `left_vs_difference` / **mean_correlation**: 5.27438e-05 — _not covered by context (missing metric entry)_
- `cross_correlation` / `right_vs_difference` / **peak_value**: 1.66652 — _not covered by context (missing metric entry)_
- `cross_correlation` / `right_vs_difference` / **mean_correlation**: 0.000132197 — _not covered by context (missing metric entry)_
- `phase_difference` / `left_vs_right` / **phase_diff_mean**: 0.00299536 — _not covered by context (missing method entry)_
- `phase_difference` / `left_vs_right` / **phase_diff_std**: 0.601359 — _not covered by context (missing method entry)_
- `phase_difference` / `left_vs_right` / **phase_diff_range**: 6.28319 — _not covered by context (missing method entry)_
- `phase_difference` / `left_vs_right` / **phase_coherence**: 0.887528 — _not covered by context (missing method entry)_
- `phase_difference` / `left_vs_right` / **in_phase**: True — _not covered by context (missing method entry)_
- `phase_difference` / `left_vs_right` / **out_of_phase**: False — _not covered by context (missing method entry)_
- `phase_difference` / `left_vs_difference` / **phase_diff_mean**: -0.00306565 — _not covered by context (missing method entry)_
- `phase_difference` / `left_vs_difference` / **phase_diff_std**: 1.77759 — _not covered by context (missing method entry)_
- `phase_difference` / `left_vs_difference` / **phase_diff_range**: 6.28319 — _not covered by context (missing method entry)_
- `phase_difference` / `left_vs_difference` / **phase_coherence**: 0.0986272 — _not covered by context (missing method entry)_
- `phase_difference` / `left_vs_difference` / **in_phase**: True — _not covered by context (missing method entry)_
- `phase_difference` / `left_vs_difference` / **out_of_phase**: False — _not covered by context (missing method entry)_
- `phase_difference` / `right_vs_difference` / **phase_diff_mean**: -0.00361172 — _not covered by context (missing method entry)_
- `phase_difference` / `right_vs_difference` / **phase_diff_std**: 1.99876 — _not covered by context (missing method entry)_
- `phase_difference` / `right_vs_difference` / **phase_diff_range**: 6.28319 — _not covered by context (missing method entry)_
- `phase_difference` / `right_vs_difference` / **phase_coherence**: 0.0818634 — _not covered by context (missing method entry)_
- `phase_difference` / `right_vs_difference` / **in_phase**: True — _not covered by context (missing method entry)_
- `phase_difference` / `right_vs_difference` / **out_of_phase**: False — _not covered by context (missing method entry)_
- `time_delay` / `left_vs_right` / **delay_samples**: 0 — _not covered by context (missing method entry)_
- `time_delay` / `left_vs_right` / **delay_ms**: 0 — _not covered by context (missing method entry)_
- `time_delay` / `left_vs_right` / **correlation_at_delay**: 618.019 — _not covered by context (missing method entry)_
- `time_delay` / `left_vs_right` / **is_synchronized**: True — _not covered by context (missing method entry)_
- `time_delay` / `left_vs_difference` / **delay_samples**: -97 — _not covered by context (missing method entry)_
- `time_delay` / `left_vs_difference` / **delay_ms**: -4.39909 — _not covered by context (missing method entry)_
- `time_delay` / `left_vs_difference` / **correlation_at_delay**: 9.32 — _not covered by context (missing method entry)_
- `time_delay` / `left_vs_difference` / **is_synchronized**: False — _not covered by context (missing method entry)_
- `time_delay` / `right_vs_difference` / **delay_samples**: 0 — _not covered by context (missing method entry)_
- `time_delay` / `right_vs_difference` / **delay_ms**: 0 — _not covered by context (missing method entry)_
- `time_delay` / `right_vs_difference` / **correlation_at_delay**: -11.9944 — _not covered by context (missing method entry)_
- `time_delay` / `right_vs_difference` / **is_synchronized**: True — _not covered by context (missing method entry)_

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

- `lsb_analysis` / `left`: **lsb_mean** = 0.47027 (reference [0.4, 0.6]) → **within**. Mean value of least significant bits.
- `lsb_analysis` / `right`: **lsb_mean** = 0.47163 (reference [0.4, 0.6]) → **within**. Mean value of least significant bits.
- `lsb_analysis` / `difference`: **lsb_mean** = 0.4483 (reference [0.4, 0.6]) → **within**. Mean value of least significant bits.

#### 3.B Metrics without reference zones

**Status B — context-dependent (no stable zone)**

- `lsb_analysis` / `left`: **transition_rate** = 0.4706 — Transition rate of the LSB sequence.
- `lsb_analysis` / `right`: **transition_rate** = 0.46999 — Transition rate of the LSB sequence.
- `lsb_analysis` / `difference`: **transition_rate** = 0.45038 — Transition rate of the LSB sequence.
- `quantization_noise` / `left`: **noise_std** = 2.71228e-05 — Standard deviation of quantization noise.
- `quantization_noise` / `right`: **noise_std** = 2.71147e-05 — Standard deviation of quantization noise.
- `quantization_noise` / `difference`: **noise_std** = 2.78269e-05 — Standard deviation of quantization noise.

**Status C — descriptive only (no stable zone)**

_No status C metrics listed for this family._

**Unmapped / missing context coverage**

- `lsb_analysis` / `left` / **lsb_std**: 0.499115 — _not covered by context (missing metric entry)_
- `lsb_analysis` / `left` / **mean_zero_run**: 2.25125 — _not covered by context (missing metric entry)_
- `lsb_analysis` / `left` / **mean_one_run**: 1.9986 — _not covered by context (missing metric entry)_
- `lsb_analysis` / `left` / **samples_analyzed**: 100000 — _not covered by context (missing metric entry)_
- `lsb_analysis` / `right` / **lsb_std**: 0.499194 — _not covered by context (missing metric entry)_
- `lsb_analysis` / `right` / **mean_zero_run**: 2.24838 — _not covered by context (missing metric entry)_
- `lsb_analysis` / `right` / **mean_one_run**: 2.00698 — _not covered by context (missing metric entry)_
- `lsb_analysis` / `right` / **samples_analyzed**: 100000 — _not covered by context (missing metric entry)_
- `lsb_analysis` / `difference` / **lsb_std**: 0.49732 — _not covered by context (missing metric entry)_
- `lsb_analysis` / `difference` / **mean_zero_run**: 2.4498 — _not covered by context (missing metric entry)_
- `lsb_analysis` / `difference` / **mean_one_run**: 1.99076 — _not covered by context (missing metric entry)_
- `lsb_analysis` / `difference` / **samples_analyzed**: 100000 — _not covered by context (missing metric entry)_
- `quantization_noise` / `left` / **noise_power**: 7.35647e-10 — _not covered by context (missing metric entry)_
- `quantization_noise` / `left` / **autocorr_peak**: 0.418062 — _not covered by context (missing metric entry)_
- `quantization_noise` / `left` / **spectral_flatness**: 0.752233 — _not covered by context (missing metric entry)_
- `quantization_noise` / `left` / **samples_analyzed**: 50000 — _not covered by context (missing metric entry)_
- `quantization_noise` / `right` / **noise_power**: 7.35207e-10 — _not covered by context (missing metric entry)_
- `quantization_noise` / `right` / **autocorr_peak**: 0.415448 — _not covered by context (missing metric entry)_
- `quantization_noise` / `right` / **spectral_flatness**: 0.750377 — _not covered by context (missing metric entry)_
- `quantization_noise` / `right` / **samples_analyzed**: 50000 — _not covered by context (missing metric entry)_
- `quantization_noise` / `difference` / **noise_power**: 7.74341e-10 — _not covered by context (missing metric entry)_
- `quantization_noise` / `difference` / **autocorr_peak**: 0.4805 — _not covered by context (missing metric entry)_
- `quantization_noise` / `difference` / **spectral_flatness**: 0.72345 — _not covered by context (missing metric entry)_
- `quantization_noise` / `difference` / **samples_analyzed**: 50000 — _not covered by context (missing metric entry)_
- `signal_residual` / `left` / **signal_power**: 9.88691e-07 — _not covered by context (missing method entry)_
- `signal_residual` / `left` / **residual_power**: 0.0126421 — _not covered by context (missing method entry)_
- `signal_residual` / `left` / **snr_db**: -41.0676 — _not covered by context (missing method entry)_
- `signal_residual` / `left` / **residual_peak_freq**: 4528.19 — _not covered by context (missing method entry)_
- `signal_residual` / `left` / **energy_ratio**: 12785.4 — _not covered by context (missing method entry)_
- `signal_residual` / `left` / **samples_analyzed**: 100000 — _not covered by context (missing method entry)_
- `signal_residual` / `right` / **signal_power**: 1.21327e-06 — _not covered by context (missing method entry)_
- `signal_residual` / `right` / **residual_power**: 0.0126712 — _not covered by context (missing method entry)_
- `signal_residual` / `right` / **snr_db**: -40.1886 — _not covered by context (missing method entry)_
- `signal_residual` / `right` / **residual_peak_freq**: 4528.19 — _not covered by context (missing method entry)_
- `signal_residual` / `right` / **energy_ratio**: 10443 — _not covered by context (missing method entry)_
- `signal_residual` / `right` / **samples_analyzed**: 100000 — _not covered by context (missing method entry)_
- `signal_residual` / `difference` / **signal_power**: 1.15074e-08 — _not covered by context (missing method entry)_
- `signal_residual` / `difference` / **residual_power**: 0.000488204 — _not covered by context (missing method entry)_
- `signal_residual` / `difference` / **snr_db**: -46.2762 — _not covered by context (missing method entry)_
- `signal_residual` / `difference` / **residual_peak_freq**: 4540.1 — _not covered by context (missing method entry)_
- `signal_residual` / `difference` / **energy_ratio**: 42059.7 — _not covered by context (missing method entry)_
- `signal_residual` / `difference` / **samples_analyzed**: 100000 — _not covered by context (missing method entry)_
- `statistical_anomalies` / `left` / **num_outliers**: 912 — _not covered by context (missing method entry)_
- `statistical_anomalies` / `left` / **outlier_rate**: 0.00912 — _not covered by context (missing method entry)_
- `statistical_anomalies` / `left` / **max_z_score**: 6.41013 — _not covered by context (missing method entry)_
- `statistical_anomalies` / `left` / **mean_z_score**: 0.719912 — _not covered by context (missing method entry)_
- `statistical_anomalies` / `left` / **chi2_statistic**: 23579.3 — _not covered by context (missing method entry)_
- `statistical_anomalies` / `left` / **chi2_pvalue**: 0 — _not covered by context (missing method entry)_
- `statistical_anomalies` / `left` / **normality_test**: False — _not covered by context (missing method entry)_
- `statistical_anomalies` / `left` / **samples_analyzed**: 100000 — _not covered by context (missing method entry)_
- `statistical_anomalies` / `right` / **num_outliers**: 905 — _not covered by context (missing method entry)_
- `statistical_anomalies` / `right` / **outlier_rate**: 0.00905 — _not covered by context (missing method entry)_
- `statistical_anomalies` / `right` / **max_z_score**: 6.11429 — _not covered by context (missing method entry)_
- `statistical_anomalies` / `right` / **mean_z_score**: 0.719931 — _not covered by context (missing method entry)_
- `statistical_anomalies` / `right` / **chi2_statistic**: 24868.3 — _not covered by context (missing method entry)_
- `statistical_anomalies` / `right` / **chi2_pvalue**: 0 — _not covered by context (missing method entry)_
- `statistical_anomalies` / `right` / **normality_test**: False — _not covered by context (missing method entry)_
- `statistical_anomalies` / `right` / **samples_analyzed**: 100000 — _not covered by context (missing method entry)_
- `statistical_anomalies` / `difference` / **num_outliers**: 1179 — _not covered by context (missing method entry)_
- `statistical_anomalies` / `difference` / **outlier_rate**: 0.01179 — _not covered by context (missing method entry)_
- `statistical_anomalies` / `difference` / **max_z_score**: 8.70676 — _not covered by context (missing method entry)_
- `statistical_anomalies` / `difference` / **mean_z_score**: 0.703478 — _not covered by context (missing method entry)_
- `statistical_anomalies` / `difference` / **chi2_statistic**: 23661.1 — _not covered by context (missing method entry)_
- `statistical_anomalies` / `difference` / **chi2_pvalue**: 0 — _not covered by context (missing method entry)_
- `statistical_anomalies` / `difference` / **normality_test**: False — _not covered by context (missing method entry)_
- `statistical_anomalies` / `difference` / **samples_analyzed**: 100000 — _not covered by context (missing method entry)_
- `parity_analysis` / `left` / **parity_mean**: 0.47027 — _not covered by context (missing method entry)_
- `parity_analysis` / `left` / **parity_std**: 0.499115 — _not covered by context (missing method entry)_
- `parity_analysis` / `left` / **transition_rate**: 0.470605 — _not covered by context (missing method entry)_
- `parity_analysis` / `left` / **transition_anomaly**: 0.0293953 — _not covered by context (missing method entry)_
- `parity_analysis` / `left` / **mean_run_length**: 2.1249 — _not covered by context (missing method entry)_
- `parity_analysis` / `left` / **std_run_length**: 11.9946 — _not covered by context (missing method entry)_
- `parity_analysis` / `left` / **chi2_statistic**: 353.549 — _not covered by context (missing method entry)_
- `parity_analysis` / `left` / **chi2_pvalue**: 0 — _not covered by context (missing method entry)_
- `parity_analysis` / `left` / **appears_random**: False — _not covered by context (missing method entry)_
- `parity_analysis` / `left` / **samples_analyzed**: 100000 — _not covered by context (missing method entry)_
- `parity_analysis` / `right` / **parity_mean**: 0.47163 — _not covered by context (missing method entry)_
- `parity_analysis` / `right` / **parity_std**: 0.499194 — _not covered by context (missing method entry)_
- `parity_analysis` / `right` / **transition_rate**: 0.469995 — _not covered by context (missing method entry)_
- `parity_analysis` / `right` / **transition_anomaly**: 0.0300053 — _not covered by context (missing method entry)_
- `parity_analysis` / `right` / **mean_run_length**: 2.12766 — _not covered by context (missing method entry)_
- `parity_analysis` / `right` / **std_run_length**: 10.1725 — _not covered by context (missing method entry)_
- `parity_analysis` / `right` / **chi2_statistic**: 321.943 — _not covered by context (missing method entry)_
- `parity_analysis` / `right` / **chi2_pvalue**: 0 — _not covered by context (missing method entry)_
- `parity_analysis` / `right` / **appears_random**: False — _not covered by context (missing method entry)_
- `parity_analysis` / `right` / **samples_analyzed**: 100000 — _not covered by context (missing method entry)_
- `parity_analysis` / `difference` / **parity_mean**: 0.4483 — _not covered by context (missing method entry)_
- `parity_analysis` / `difference` / **parity_std**: 0.49732 — _not covered by context (missing method entry)_
- `parity_analysis` / `difference` / **transition_rate**: 0.450385 — _not covered by context (missing method entry)_
- `parity_analysis` / `difference` / **transition_anomaly**: 0.0496155 — _not covered by context (missing method entry)_
- `parity_analysis` / `difference` / **mean_run_length**: 2.2203 — _not covered by context (missing method entry)_
- `parity_analysis` / `difference` / **std_run_length**: 21.0122 — _not covered by context (missing method entry)_
- `parity_analysis` / `difference` / **chi2_statistic**: 1069.16 — _not covered by context (missing method entry)_
- `parity_analysis` / `difference` / **chi2_pvalue**: 0 — _not covered by context (missing method entry)_
- `parity_analysis` / `difference` / **appears_random**: False — _not covered by context (missing method entry)_
- `parity_analysis` / `difference` / **samples_analyzed**: 100000 — _not covered by context (missing method entry)_

**Expected by context but missing in results (not evaluated)**

_No expected scalar metrics were missing for this family._


### meta_analysis

- Objective: Identify excessive stability, repetition, or structural consistency across signal segments.
- Coverage: `partial`
- Rationale: Meta-analysis metrics summarize cross-segment behavior without inferring signal origin.

- Documentary references:
  - C. M. Bishop — "Pattern Recognition and Machine Learning" — (2006). Reference for similarity and structure in data.

#### 3.A Metrics with reference zones (Status A)

_No status A metrics were applicable for this family._

#### 3.B Metrics without reference zones

**Status B — context-dependent (no stable zone)**

- `inter_segment_comparison` / `left`: **similarity_score** = 0.0120892 — Similarity between consecutive segments.
- `inter_segment_comparison` / `right`: **similarity_score** = 0.0121253 — Similarity between consecutive segments.
- `inter_segment_comparison` / `difference`: **similarity_score** = 0.0154417 — Similarity between consecutive segments.
- `stability_scores` / `left`: **overall_stability** = 0.769035 — Aggregate stability score across segments.
- `stability_scores` / `right`: **overall_stability** = 0.769514 — Aggregate stability score across segments.
- `stability_scores` / `difference`: **overall_stability** = 0.765271 — Aggregate stability score across segments.

**Status C — descriptive only (no stable zone)**

_No status C metrics listed for this family._

**Unmapped / missing context coverage**

- `inter_segment_comparison` / `left` / **num_segments**: 10 — _not covered by context (missing metric entry)_
- `inter_segment_comparison` / `left` / **mean_distance**: 81.7184 — _not covered by context (missing metric entry)_
- `inter_segment_comparison` / `left` / **std_distance**: 39.1338 — _not covered by context (missing metric entry)_
- `inter_segment_comparison` / `left` / **min_distance**: 14.7506 — _not covered by context (missing metric entry)_
- `inter_segment_comparison` / `left` / **max_distance**: 183.843 — _not covered by context (missing metric entry)_
- `inter_segment_comparison` / `right` / **num_segments**: 10 — _not covered by context (missing metric entry)_
- `inter_segment_comparison` / `right` / **mean_distance**: 81.472 — _not covered by context (missing metric entry)_
- `inter_segment_comparison` / `right` / **std_distance**: 38.4887 — _not covered by context (missing metric entry)_
- `inter_segment_comparison` / `right` / **min_distance**: 17.3519 — _not covered by context (missing metric entry)_
- `inter_segment_comparison` / `right` / **max_distance**: 173.597 — _not covered by context (missing metric entry)_
- `inter_segment_comparison` / `difference` / **num_segments**: 10 — _not covered by context (missing metric entry)_
- `inter_segment_comparison` / `difference` / **mean_distance**: 63.7597 — _not covered by context (missing metric entry)_
- `inter_segment_comparison` / `difference` / **std_distance**: 44.0901 — _not covered by context (missing metric entry)_
- `inter_segment_comparison` / `difference` / **min_distance**: 1.22234 — _not covered by context (missing metric entry)_
- `inter_segment_comparison` / `difference` / **max_distance**: 181.911 — _not covered by context (missing metric entry)_
- `segment_clustering` / `left` / **num_segments**: 20 — _not covered by context (missing method entry)_
- `segment_clustering` / `left` / **avg_intra_distance**: 0.00037259 — _not covered by context (missing method entry)_
- `segment_clustering` / `left` / **unique_segments**: 0 — _not covered by context (missing method entry)_
- `segment_clustering` / `left` / **repetition_rate**: 1 — _not covered by context (missing method entry)_
- `segment_clustering` / `right` / **num_segments**: 20 — _not covered by context (missing method entry)_
- `segment_clustering` / `right` / **avg_intra_distance**: 0.0013335 — _not covered by context (missing method entry)_
- `segment_clustering` / `right` / **unique_segments**: 0 — _not covered by context (missing method entry)_
- `segment_clustering` / `right` / **repetition_rate**: 1 — _not covered by context (missing method entry)_
- `segment_clustering` / `difference` / **num_segments**: 20 — _not covered by context (missing method entry)_
- `segment_clustering` / `difference` / **avg_intra_distance**: 0.0154789 — _not covered by context (missing method entry)_
- `segment_clustering` / `difference` / **unique_segments**: 0 — _not covered by context (missing method entry)_
- `segment_clustering` / `difference` / **repetition_rate**: 1 — _not covered by context (missing method entry)_
- `stability_scores` / `left` / **energy_stability**: 0.641394 — _not covered by context (missing metric entry)_
- `stability_scores` / `left` / **spectral_stability**: 0.896676 — _not covered by context (missing metric entry)_
- `stability_scores` / `left` / **num_windows**: 212 — _not covered by context (missing metric entry)_
- `stability_scores` / `right` / **energy_stability**: 0.641517 — _not covered by context (missing metric entry)_
- `stability_scores` / `right` / **spectral_stability**: 0.89751 — _not covered by context (missing metric entry)_
- `stability_scores` / `right` / **num_windows**: 212 — _not covered by context (missing metric entry)_
- `stability_scores` / `difference` / **energy_stability**: 0.664153 — _not covered by context (missing metric entry)_
- `stability_scores` / `difference` / **spectral_stability**: 0.866389 — _not covered by context (missing metric entry)_
- `stability_scores` / `difference` / **num_windows**: 212 — _not covered by context (missing metric entry)_
- `high_order_statistics` / `left` / **mean**: 3.29223e-08 — _not covered by context (missing method entry)_
- `high_order_statistics` / `left` / **std**: 0.110314 — _not covered by context (missing method entry)_
- `high_order_statistics` / `left` / **variance**: 0.0121691 — _not covered by context (missing method entry)_
- `high_order_statistics` / `left` / **skewness**: 4.78574e-06 — _not covered by context (missing method entry)_
- `high_order_statistics` / `left` / **kurtosis**: 1.43866 — _not covered by context (missing method entry)_
- `high_order_statistics` / `left` / **peak_value**: 0.720734 — _not covered by context (missing method entry)_
- `high_order_statistics` / `left` / **crest_factor**: 6.53349 — _not covered by context (missing method entry)_
- `high_order_statistics` / `left` / **samples_analyzed**: 110308 — _not covered by context (missing method entry)_
- `high_order_statistics` / `right` / **mean**: -2.21326e-09 — _not covered by context (missing method entry)_
- `high_order_statistics` / `right` / **std**: 0.110411 — _not covered by context (missing method entry)_
- `high_order_statistics` / `right` / **variance**: 0.0121907 — _not covered by context (missing method entry)_
- `high_order_statistics` / `right` / **skewness**: 4.25942e-06 — _not covered by context (missing method entry)_
- `high_order_statistics` / `right` / **kurtosis**: 1.41182 — _not covered by context (missing method entry)_
- `high_order_statistics` / `right` / **peak_value**: 0.688263 — _not covered by context (missing method entry)_
- `high_order_statistics` / `right` / **crest_factor**: 6.23362 — _not covered by context (missing method entry)_
- `high_order_statistics` / `right` / **samples_analyzed**: 110308 — _not covered by context (missing method entry)_
- `high_order_statistics` / `difference` / **mean**: 3.51356e-08 — _not covered by context (missing method entry)_
- `high_order_statistics` / `difference` / **std**: 0.0219141 — _not covered by context (missing method entry)_
- `high_order_statistics` / `difference` / **variance**: 0.000480227 — _not covered by context (missing method entry)_
- `high_order_statistics` / `difference` / **skewness**: 2.4019e-05 — _not covered by context (missing method entry)_
- `high_order_statistics` / `difference` / **kurtosis**: 2.99061 — _not covered by context (missing method entry)_
- `high_order_statistics` / `difference` / **peak_value**: 0.192383 — _not covered by context (missing method entry)_
- `high_order_statistics` / `difference` / **crest_factor**: 8.77896 — _not covered by context (missing method entry)_
- `high_order_statistics` / `difference` / **samples_analyzed**: 110308 — _not covered by context (missing method entry)_

**Expected by context but missing in results (not evaluated)**

_No expected scalar metrics were missing for this family._

