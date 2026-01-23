# Audio Analysis Report - Measurement Summary

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

## Measured Outputs

This report lists measured outputs as produced by the analysis engine. No interpretation is applied.

### time_frequency / stft

- `mono` / **num_time_frames**: 5169
- `mono` / **num_freq_bins**: 1025
- `mono` / **frequency_resolution**: 10.7666
- `mono` / **time_resolution**: 0.00290249
- `mono` / **mean_magnitude**: 0.000163918
- `mono` / **max_magnitude**: 0.0717187
- `mono` / **dominant_freq_mean**: 4995.7
- `mono` / **dominant_freq_std**: 0
- `mono` / **spectral_flux_mean**: 0.000690805
- `mono` / **spectral_flux_max**: 0.00645624
- `mono` / **temporal_stability**: 0.808704

### time_frequency / band_stability

_No scalar measurements found for this method._

### spectral / fft_global

- `mono` / **n_fft**: 330750
- `mono` / **frequency_resolution**: 0.0666667
- `mono` / **peak_frequency**: 5000
- `mono` / **peak_magnitude**: 11610.3
- `mono` / **spectral_energy**: 2.05137e+08

### spectral / peak_detection

- `mono` / **num_peaks**: 2645
- `mono` / **dominant_frequency**: 2.73333
- `mono` / **frequency_spread**: 3183.24

### spectral / spectral_centroid

- `mono` / **spectral_centroid**: 5031.47
- `mono` / **normalized_centroid**: 0.456369

### spectral / spectral_bandwidth

- `mono` / **spectral_bandwidth**: 13.0339
- `mono` / **spectral_centroid_Hz**: 5000

### spectral / spectral_flatness

- `mono` / **spectral_flatness**: 0.186417
- `mono` / **tonality**: 0.813583

### temporal / envelope

- `mono` / **envelope_mean**: 0.140225
- `mono` / **envelope_max**: 0.163971
- `mono` / **envelope_std**: 0.0183527
- `mono` / **envelope_length**: 330750

### temporal / autocorrelation

- `mono` / **autocorr_max**: 0.99743
- `mono` / **autocorr_mean**: -2.48124e-05
- `mono` / **first_peak_lag**: 4
- `mono` / **num_peaks**: 1133
- `mono` / **periodicity_score**: 0.99743

### temporal / pulse_detection

- `mono` / **num_pulses**: 228
- `mono` / **interval_mean**: 1453.15
- `mono` / **interval_std**: 285.408
- `mono` / **regularity_score**: 0.803593

### modulation / am_detection

- `mono` / **modulation_detected**: False
- `mono` / **num_modulation_frequencies**: 0
- `mono` / **dominant_modulation_freq**: 0
- `mono` / **modulation_depth**: 0.330887
- `mono` / **modulation_index**: 0.13088
- `mono` / **envelope_mean**: 0.140225
- `mono` / **envelope_std**: 0.0183527

### modulation / fm_detection

- `mono` / **fm_detected**: False
- `mono` / **carrier_frequency_mean**: 4998.57
- `mono` / **frequency_deviation**: 37.9915
- `mono` / **frequency_range**: 137.085
- `mono` / **frequency_std**: 37.9915
- `mono` / **num_fm_components**: 0
- `mono` / **modulation_index_fm**: 0.00760048

### modulation / phase_analysis

- `mono` / **phase_mean**: -0.00356091
- `mono` / **phase_std**: 1.81386
- `mono` / **phase_range**: 6.26956
- `mono` / **unwrapped_phase_total**: 471102
- `mono` / **phase_coherence**: 0.9924
- `mono` / **num_phase_jumps**: 75000
- `mono` / **phase_jump_rate**: 5000

### information / shannon_entropy

- `mono` / **shannon_entropy**: 7.79336
- `mono` / **max_entropy**: 8
- `mono` / **normalized_entropy**: 0.974169
- `mono` / **num_bins**: 256

### information / local_entropy

- `mono` / **mean_entropy**: 5.79357
- `mono` / **std_entropy**: 0.0797437
- `mono` / **min_entropy**: 5.48334
- `mono` / **max_entropy**: 5.86279
- `mono` / **num_windows**: 192
- `mono` / **entropy_variation**: 0.0137642

### steganography / lsb_analysis

- `mono` / **lsb_mean**: 0.49781
- `mono` / **lsb_std**: 0.499995
- `mono` / **transition_rate**: 0.47946
- `mono` / **mean_zero_run**: 2.09473
- `mono` / **mean_one_run**: 2.07654
- `mono` / **samples_analyzed**: 100000

### steganography / quantization_noise

- `mono` / **noise_power**: 7.86626e-10
- `mono` / **noise_std**: 2.80469e-05
- `mono` / **autocorr_peak**: 0.979429
- `mono` / **spectral_flatness**: 0.256936
- `mono` / **samples_analyzed**: 50000

### steganography / signal_residual

- `mono` / **signal_power**: 1.49061e-08
- `mono` / **residual_power**: 0.0101983
- `mono` / **snr_db**: -58.3516
- `mono` / **residual_peak_freq**: 5000.06
- `mono` / **energy_ratio**: 679609
- `mono` / **samples_analyzed**: 100000

### steganography / statistical_anomalies

- `mono` / **num_outliers**: 0
- `mono` / **outlier_rate**: 0
- `mono` / **max_z_score**: 1.57582
- `mono` / **mean_z_score**: 0.892856
- `mono` / **chi2_statistic**: 99304.4
- `mono` / **chi2_pvalue**: 0
- `mono` / **normality_test**: False
- `mono` / **samples_analyzed**: 100000

### steganography / parity_analysis

- `mono` / **parity_mean**: 0.49781
- `mono` / **parity_std**: 0.499995
- `mono` / **transition_rate**: 0.479465
- `mono` / **transition_anomaly**: 0.0205352
- `mono` / **mean_run_length**: 2.08564
- `mono` / **std_run_length**: 1.43346
- `mono` / **chi2_statistic**: 1.91844
- `mono` / **chi2_pvalue**: 0.166029
- `mono` / **appears_random**: True
- `mono` / **samples_analyzed**: 100000
