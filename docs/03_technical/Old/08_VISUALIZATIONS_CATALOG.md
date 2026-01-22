# Visualization Catalog (Code-Accurate Documentation)

This document describes **all visualization functions effectively implemented** in `audio_toolkit/visualization/plots.py`.

For each plotter, the documentation specifies:
- the **function name**
- the **expected inputs** (typical origin: `AnalysisResult.visualization_data`)
- the **rendering parameters** actually supported by the function signature
- the **output artifact** (saved figure formats)

This document is strictly descriptive:
- no interpretation
- no classification
- no assumptions about signal intent

---

## Conventions

### File output
All plotters save figures via `save_figure(fig, output_path, formats, dpi)`:
- `output_path` is **a path without extension**
- one file is written per format in `formats` (e.g. `png`, `pdf`)
- `dpi` applies to raster formats (PNG)

### Axes and units
- Time axes are in **seconds** when the plotter is provided time vectors in seconds (most analyses do this).
- Frequency axes are in **Hz** when provided as Hz vectors.

---

## Basic Plots

### Waveform
**Function:** `plot_waveform(signal, sample_rate, output_path, title, ...)`

**Expected inputs:**
- `signal`: 1D array (audio samples)
- `sample_rate`: integer (Hz)

**Rendering parameters (signature):**
- `figsize` (default `(12, 4)`)
- `dpi` (default `150`)
- `formats` (default `["png"]`)

**Output:**
- Time-domain waveform (amplitude vs time)

---

### Spectrum
**Function:** `plot_spectrum(frequencies, magnitudes, output_path, title, ..., db=True)`

**Expected inputs:**
- `frequencies`: 1D array (Hz)
- `magnitudes`: 1D array (linear magnitude)

**Rendering parameters:**
- `db` (bool, default `True`): convert magnitudes to dB via `20*log10`

**Output:**
- Magnitude spectrum (frequency vs magnitude)

---

### Multi-channel waveform overlay
**Function:** `plot_multi_channel(channels, sample_rate, output_path, title, ...)`

**Expected inputs:**
- `channels`: dict `{channel_name: 1D array}`
- `sample_rate`: integer (Hz)

**Output:**
- Multiple waveforms overlaid on the same axes

---

### Envelope
**Function:** `plot_envelope(envelope, sample_rate, output_path, title, ...)`

**Expected inputs:**
- `envelope`: 1D array
- `sample_rate`: integer (Hz)

**Output:**
- Envelope amplitude vs time

---

### Autocorrelation
**Function:** `plot_autocorrelation(autocorr, sample_rate, output_path, title, ...)`

**Expected inputs:**
- `autocorr`: 1D array (autocorrelation values)
- `sample_rate`: integer (Hz)

**Output:**
- Autocorrelation vs lag (lag displayed in seconds)

---

### Peaks on 1D spectrum
**Function:** `plot_peaks(spectrum, peaks, output_path, title, ...)`

**Expected inputs:**
- `spectrum`: 1D array (typically magnitude per FFT bin)
- `peaks`: 1D array of indices (bin indices)

**Output:**
- 1D curve with peak markers at provided indices

---

## Extended Plots

### Harmonic markers on spectrum
**Function:** `plot_harmonics(frequencies, magnitudes, fundamental, harmonics, output_path, ...)`

**Expected inputs:**
- `frequencies`: 1D array (Hz)
- `magnitudes`: 1D array (linear magnitude)
- `fundamental`: float (Hz)
- `harmonics`: list of floats (Hz)

**Output:**
- Spectrum in dB with vertical markers at fundamental and harmonics

---

### Cepstrum
**Function:** `plot_cepstrum(quefrency, cepstrum, peak_quefrency, output_path, ...)`

**Expected inputs:**
- `quefrency`: 1D array (seconds)
- `cepstrum`: 1D array
- `peak_quefrency`: float (seconds)

**Output:**
- Cepstrum with a vertical marker at the detected peak (displayed in ms)

---

### Band stability over time
**Function:** `plot_band_stability(times, bands_data, output_path, ...)`

**Expected inputs:**
- `times`: 1D array (seconds)
- `bands_data`: dict `{band_name: 1D array}` (energy over time)

**Output:**
- One curve per band: energy vs time

---

### Wavelet scalogram
**Function:** `plot_wavelet_scalogram(scalogram, scales, sample_rate, output_path, ...)`

**Expected inputs:**
- `scalogram`: 2D array (magnitude, scale x time)
- `scales`: 1D array (scale values)
- `sample_rate`: integer (Hz) — used to express time extent

**Output:**
- 2D image (imshow) of `abs(scalogram)` with scale axis

---

### AM detection (envelope + modulation spectrum)
**Function:** `plot_am_detection(time, envelope, modulation_frequencies, modulation_spectrum, output_path, ...)`

**Expected inputs:**
- `time`: 1D array (seconds)
- `envelope`: 1D array
- `modulation_frequencies`: 1D array (Hz)
- `modulation_spectrum`: 1D array

**Output:**
- Two stacked plots:
  - envelope vs time
  - modulation spectrum vs modulation frequency

---

### FM detection (instantaneous frequency)
**Function:** `plot_fm_detection(time, instantaneous_frequency, carrier_frequency, output_path, ...)`

**Expected inputs:**
- `time`: 1D array (seconds)
- `instantaneous_frequency`: 1D array (Hz)
- `carrier_frequency`: float (Hz)

**Output:**
- Instantaneous frequency vs time with a horizontal carrier marker

---

### Phase analysis (phase + jump markers)
**Function:** `plot_phase_analysis(time, phase, jumps, output_path, ...)`

**Expected inputs:**
- `time`: 1D array (seconds)
- `phase`: 1D array (radians)
- `jumps`: 1D array of indices

**Output:**
- Phase vs time with jump markers at provided indices

---

### Cross-correlation between channels
**Function:** `plot_cross_correlation(lags, correlation, channel_pair, output_path, ...)`

**Expected inputs:**
- `lags`: 1D array (samples)
- `correlation`: 1D array
- `channel_pair`: string label (e.g. `"left-right"`)

**Output:**
- Cross-correlation vs lag (samples) with a peak marker

---

### STFT spectrogram
**Function:** `plot_stft_spectrogram(frequencies, times, stft_matrix, sample_rate, output_path, ..., vmin=-80, vmax=0)`

**Expected inputs:**
- `frequencies`: 1D array (Hz)
- `times`: 1D array (seconds)
- `stft_matrix`: 2D complex array (freq x time)

**Rendering parameters:**
- `vmin`, `vmax` (floats): dB display range (applied after `20*log10(|STFT|)`)

**Output:**
- 2D time–frequency plot (pcolormesh) of magnitude in dB

**Notes:**
- Colormap is currently fixed to `viridis` in the implementation.

---

### CQT spectrogram
**Function:** `plot_cqt_spectrogram(frequencies, times, cqt_db, output_path, ..., vmin=None, vmax=None)`

**Expected inputs:**
- `frequencies`: 1D array (Hz)
- `times`: 1D array (seconds)
- `cqt_db`: 2D array (freq x time), already in dB

**Rendering parameters:**
- `vmin`, `vmax` default to percentile-based robust bounds when not provided

**Output:**
- 2D time–frequency plot (pcolormesh) of `cqt_db`
- Y axis is set to log scale if frequencies are strictly positive

**Notes:**
- Colormap is currently fixed to `viridis` in the implementation.

---
## New visualizations (Phases 3A–3B)

### plot_spectral_rolloff
Inputs: `frequencies`, `spectrum`, `rolloff_frequency`, `rolloff_percent`.

### plot_spectral_flux
Inputs: `times`, `flux`, `mean_flux`.

### plot_stability_dual
Inputs: `times`, `energy`, `spectral_centroid`, `energy_mean`, `centroid_mean`.

### plot_temporal_curve
Inputs: `times`, `values`, `mean_level`.

### plot_chirp_detection
Inputs: `times`, `frequencies`, `spectrogram`, `chirps` (list of dicts with `start_time`, `end_time`, `start_freq`, `end_freq`).

### plot_mutual_information
Inputs: `channel_names`, `mi_matrix`, `mi_pairs`.

### plot_lsb_analysis
Inputs: `lsb_bits`, `zero_runs`, `one_runs`, `transition_rate`.

### plot_parity_analysis
Inputs: `parity_bits`, `run_lengths`, `transition_rate`, `expected_transition_rate`.

### plot_statistical_anomalies
Inputs: `histogram`, `bin_centers`, `normal_distribution`, `outlier_indices`, `outlier_values`, `z_scores`, `z_threshold`.

### plot_high_order_statistics
Inputs: `histogram`, `bin_centers`, `normal_distribution`, `mean`, `std`, `skewness`, `kurtosis`.
