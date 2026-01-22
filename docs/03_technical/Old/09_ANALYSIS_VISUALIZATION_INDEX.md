# Analysis ↔ Visualization Index (Runner/Plots Accurate)

This index is a **maintenance mapping** between:
- analysis method identifiers (registry names)
- visualization functions (in `visualization/plots.py` and the `Visualizer` wrapper)

A mapping is listed only when the **runner explicitly consumes `visualization_data`** for that method.

No interpretation is performed here.

---

## Notes

- Some plot functions exist without being wired in the runner (those are not mapped).
- Some methods may produce only measurements (no visualization data).
- Optional dependencies may affect availability (e.g., `librosa` for CQT generation).

---

## Analysis → Visualization(s)

### Temporal
- `envelope` → `plot_envelope`
- `autocorrelation` → `plot_autocorrelation`
- `pulse_detection` → *(plotter exists; runner mapping not present in current runner)*
- `duration_ratios` → *(no visualization mapping)*

### Spectral
- `fft_global` → `plot_spectrum`
- `peak_detection` → `plot_peaks`
- `harmonic_analysis` → `plot_harmonics`
- `cepstrum` → `plot_cepstrum`
- `spectral_rolloff` → `plot_spectral_rolloff`
- `spectral_flux` → `plot_spectral_flux`
- `spectral_centroid` → *(plotter exists; runner mapping not present in current runner)*
- `spectral_bandwidth` → *(plotter exists; runner mapping not present in current runner)*
- `spectral_flatness` → *(no visualization mapping)*

### Time–Frequency
- `stft` → `plot_stft_spectrogram`
- `cqt` → `plot_cqt_spectrogram`
- `wavelet` → `plot_wavelet_scalogram`
- `band_stability` → `plot_band_stability`

### Modulation
- `am_detection` → `plot_am_detection`
- `fm_detection` → `plot_fm_detection`
- `phase_analysis` → `plot_phase_analysis`
- `chirp_detection` → `plot_chirp_detection`
- `modulation_index` → *(no visualization mapping)*

### Information
- `shannon_entropy` → *(no visualization mapping)*
- `local_entropy` → `plot_temporal_curve`
- `compression_ratio` → *(no visualization mapping)*
- `approximate_complexity` → *(no visualization mapping)*
- `mutual_information` → `plot_mutual_information`

### Inter-channel
- `cross_correlation` → `plot_cross_correlation`
- `lr_difference` → `plot_waveform`, `plot_spectrum`
- `phase_difference` → *(no visualization mapping)*
- `time_delay` → *(no visualization mapping)*

### Steganography
- `lsb_analysis` → `plot_lsb_analysis`
- `parity_analysis` → `plot_parity_analysis`
- `statistical_anomalies` → `plot_statistical_anomalies`
- `quantization_noise` → *(no visualization mapping)*
- `signal_residual` → *(no visualization mapping)*

### Meta-analysis
- `stability_scores` → `plot_stability_dual`
- `high_order_statistics` → `plot_high_order_statistics`
- `inter_segment_comparison` → *(no visualization mapping)*
- `segment_clustering` → *(no visualization mapping)*

---

## Visualization → Analysis source(s)

- `plot_waveform` → `lr_difference` (and generic waveform plots)
- `plot_spectrum` → `fft_global`, `lr_difference`
- `plot_envelope` → `envelope`
- `plot_autocorrelation` → `autocorrelation`
- `plot_peaks` → `peak_detection`
- `plot_harmonics` → `harmonic_analysis`
- `plot_cepstrum` → `cepstrum`
- `plot_band_stability` → `band_stability`
- `plot_wavelet_scalogram` → `wavelet`
- `plot_stft_spectrogram` → `stft`
- `plot_cqt_spectrogram` → `cqt`
- `plot_am_detection` → `am_detection`
- `plot_fm_detection` → `fm_detection`
- `plot_phase_analysis` → `phase_analysis`
- `plot_cross_correlation` → `cross_correlation`
- `plot_temporal_curve` → `local_entropy`
- `plot_stability_dual` → `stability_scores`
- `plot_spectral_rolloff` → `spectral_rolloff`
- `plot_spectral_flux` → `spectral_flux`
- `plot_chirp_detection` → `chirp_detection`
- `plot_mutual_information` → `mutual_information`
- `plot_lsb_analysis` → `lsb_analysis`
- `plot_parity_analysis` → `parity_analysis`
- `plot_statistical_anomalies` → `statistical_anomalies`
- `plot_high_order_statistics` → `high_order_statistics`
