# Audio Analysis Report

**Analysis timestamp:** 2026-01-12T17:19:59.604889
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
- sum: 0.999
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

- left: 81.034
- right: 81.034
- sum: 81.034
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
  - first_peak_lag: 43
  - num_peaks: 6
- **right:**
  - periodicity_score: 0.999
  - first_peak_lag: 45
  - num_peaks: 7
- **sum:**
  - periodicity_score: 0.999
  - first_peak_lag: 40
  - num_peaks: 5
- **difference:**
  - periodicity_score: 0.993
  - first_peak_lag: 124
  - num_peaks: 9

**Parameters:**

- max_lag: 1000
- normalized: True

<details>
<summary><b>All measurements (click to expand)</b></summary>

**Channel: left**

- autocorr_max: 0.999
- autocorr_mean: 0.008
- first_peak_lag: 43
- num_peaks: 6
- periodicity_score: 0.999

**Channel: right**

- autocorr_max: 0.999
- autocorr_mean: 0.008
- first_peak_lag: 45
- num_peaks: 7
- periodicity_score: 0.999

**Channel: sum**

- autocorr_max: 0.999
- autocorr_mean: 0.008
- first_peak_lag: 40
- num_peaks: 5
- periodicity_score: 0.999

**Channel: difference**

- autocorr_max: 0.993
- autocorr_mean: 0.003
- first_peak_lag: 124
- num_peaks: 9
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

### SPECTRAL

#### Method: fft_global

**Key metrics to observe:**

- **left:**
  - peak_frequency: 65.965
  - peak_magnitude: 40227.319
  - spectral_energy: 5.573e+10
- **right:**
  - peak_frequency: 65.965
  - peak_magnitude: 39675.813
  - spectral_energy: 5.584e+10
- **sum:**
  - peak_frequency: 65.965
  - peak_magnitude: 40761.731
  - spectral_energy: 5.594e+10
- **difference:**
  - peak_frequency: 391.998
  - peak_magnitude: 11707.580
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
- peak_magnitude: 40227.319
- spectral_energy: 5.573e+10

**Channel: right**

- n_fft: 5262400
- frequency_resolution: 0.009
- peak_frequency: 65.965
- peak_magnitude: 39675.813
- spectral_energy: 5.584e+10

**Channel: sum**

- n_fft: 5262400
- frequency_resolution: 0.009
- peak_frequency: 65.965
- peak_magnitude: 40761.731
- spectral_energy: 5.594e+10

**Channel: difference**

- n_fft: 5262400
- frequency_resolution: 0.009
- peak_frequency: 391.998
- peak_magnitude: 11707.580
- spectral_energy: 5.205e+10

</details>

---

#### Method: peak_detection

**Key metrics to observe:**

- **left:**
  - num_peaks: 3074
  - dominant_frequency: 0.867
  - frequency_spread: 1229.111
- **right:**
  - num_peaks: 2954
  - dominant_frequency: 0.638
  - frequency_spread: 1199.202
- **sum:**
  - num_peaks: 2884
  - dominant_frequency: 0.638
  - frequency_spread: 1147.791
- **difference:**
  - num_peaks: 6248
  - dominant_frequency: 0.374
  - frequency_spread: 2372.531

**Parameters:**

- prominence: 10.000
- distance: 100

<details>
<summary><b>All measurements (click to expand)</b></summary>

**Channel: left**

- num_peaks: 3074
- dominant_frequency: 0.867
- frequency_spread: 1229.111

**Channel: right**

- num_peaks: 2954
- dominant_frequency: 0.638
- frequency_spread: 1199.202

**Channel: sum**

- num_peaks: 2884
- dominant_frequency: 0.638
- frequency_spread: 1147.791

**Channel: difference**

- num_peaks: 6248
- dominant_frequency: 0.374
- frequency_spread: 2372.531

</details>

---

#### Method: harmonic_analysis

**Key metrics to observe:**

- **left:**
  - fundamental_frequency: 81.034
  - harmonicity_score: 1.000
  - harmonics_detected: 10
- **right:**
  - fundamental_frequency: 81.034
  - harmonicity_score: 1.000
  - harmonics_detected: 10
- **sum:**
  - fundamental_frequency: 81.034
  - harmonicity_score: 1.000
  - harmonics_detected: 10
- **difference:**
  - fundamental_frequency: 393.019
  - harmonicity_score: 1.000
  - harmonics_detected: 10

**Parameters:**

- fundamental_range: [80.0, 400.0]
- max_harmonics: 10

<details>
<summary><b>All measurements (click to expand)</b></summary>

**Channel: left**

- fundamental_frequency: 81.034
- harmonics_detected: 10
- harmonicity_score: 1.000

**Channel: right**

- fundamental_frequency: 81.034
- harmonics_detected: 10
- harmonicity_score: 1.000

**Channel: sum**

- fundamental_frequency: 81.034
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
- sum: 0.999
- difference: 0.993

**Reference from Appendix B:** Appendix B states: Artificial signals typically exhibit high periodicity (> 0.8), natural signals show moderate periodicity (0.3-0.7)

**Factual observation:** Channels left, right, sum, difference exceed very_high threshold (0.95)

**Possible indication:** Values in range documented for signals with exact pattern repetition (see Appendix B: Artificial signals)

### Harmonic Structure

Comparison of measured harmonicity scores to reference thresholds.

**Measured values:**

- left: harmonicity=1.000, fundamental=81.0 Hz
- right: harmonicity=1.000, fundamental=81.0 Hz
- sum: harmonicity=1.000, fundamental=81.0 Hz
- difference: harmonicity=1.000, fundamental=393.0 Hz

**Reference from Appendix B:** Appendix B states: Artificial signals show strong harmonic structure (> 0.9) with integer frequency ratios

**Factual observation:** Channels left, right, sum, difference meet or exceed strongly_harmonic threshold (0.9). Note: difference channel has distinct fundamental (393.0 Hz vs 81.0 Hz)

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

- left: 3074 peaks
- right: 2954 peaks
- sum: 2884 peaks
- difference: 6248 peaks

**Reference from Appendix B:** Appendix B states: Multiple peaks may indicate complex harmonics or FSK

**Factual observation:** Channels show > 1000 peaks

**Possible indication:** Pattern consistent with complex multi-carrier or FSK (see Appendix B)

**Final reminder:** These observations should be interpreted in context with 
domain knowledge, acquisition conditions, and intended signal use. Multiple 
converging measurements increase confidence but do not guarantee conclusions.
