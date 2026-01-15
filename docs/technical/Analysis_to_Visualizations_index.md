# Analysis ↔ Visualization Index (Code-Accurate Mapping)

This document provides a **maintenance-oriented mapping** between:
- analysis methods (registry identifiers)
- visualization functions (`plots.py`)

Only mappings supported by **actual `visualization_data` produced by analyses** are listed.

This document is strictly descriptive:
- no interpretation
- no classification
- no assumptions about signal intent

---

## Conditions

- A mapping is meaningful only if the execution pipeline calls the plotter with the required data.
- Some analyses may have plotting functions available but **do not currently produce `visualization_data`** (those are not mapped here).
- Optional dependencies may affect availability (notably `librosa` for CQT).

---

## Analysis → Visualization(s)

### Temporal
- `envelope` → `plot_envelope`
- `autocorrelation` → `plot_autocorrelation`
- `pulse_detection` → *(no visualization_data produced)*
- `duration_ratios` → *(no visualization_data produced)*

### Spectral
- `fft_global` → `plot_spectrum`
- `peak_detection` → `plot_peaks`
- `harmonic_analysis` → `plot_harmonics`
- `cepstrum` → `plot_cepstrum`
- `spectral_centroid` → *(no visualization_data produced)*
- `spectral_bandwidth` → *(no visualization_data produced)*
- `spectral_flatness` → *(no visualization_data produced)*

### Time–Frequency
- `stft` → `plot_stft_spectrogram`
- `cqt` → `plot_cqt_spectrogram` *(requires `librosa` at analysis time)*
- `wavelet` → `plot_wavelet_scalogram`
- `band_stability` → `plot_band_stability`

### Modulation
- `am_detection` → `plot_am_detection`
- `fm_detection` → `plot_fm_detection`
- `phase_analysis` → `plot_phase_analysis`
- `modulation_index` → *(no visualization_data produced)*

### Information
- `shannon_entropy` → *(no visualization_data produced)*
- `local_entropy` → *(no visualization_data produced)*
- `compression_ratio` → *(no visualization_data produced)*
- `approximate_complexity` → *(no visualization_data produced)*

### Inter-channel
- `lr_difference` → *(no visualization_data produced)*
- `cross_correlation` → *(no visualization_data produced in current analysis implementation)*
- `phase_difference` → *(no visualization_data produced)*
- `time_delay` → *(no visualization_data produced)*

### Steganography
- `lsb_analysis` → *(no visualization_data produced)*
- `quantization_noise` → *(no visualization_data produced)*
- `signal_residual` → *(no visualization_data produced)*

### Meta-analysis
- `inter_segment_comparison` → *(no visualization_data produced)*
- `segment_clustering` → *(no visualization_data produced)*
- `stability_scores` → *(no visualization_data produced)*

---

## Visualization → Analysis source(s)

- `plot_waveform` → *(generic; can be used for any 1D signal)*
- `plot_spectrum` → `fft_global`
- `plot_multi_channel` → *(generic; multi-channel 1D overlay)*
- `plot_envelope` → `envelope`
- `plot_autocorrelation` → `autocorrelation`
- `plot_peaks` → `peak_detection`
- `plot_harmonics` → `harmonic_analysis`
- `plot_cepstrum` → `cepstrum`
- `plot_band_stability` → `band_stability`
- `plot_wavelet_scalogram` → `wavelet`
- `plot_am_detection` → `am_detection`
- `plot_fm_detection` → `fm_detection`
- `plot_phase_analysis` → `phase_analysis`
- `plot_cross_correlation` → *(plotter exists; no mapped analysis currently produces required visualization_data)*
- `plot_stft_spectrogram` → `stft`
- `plot_cqt_spectrogram` → `cqt`
