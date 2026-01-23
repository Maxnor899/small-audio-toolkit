# Audio Analysis Report - Measurement Summary

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

## Measured Outputs

This report lists measured outputs as produced by the analysis engine. No interpretation is applied.

### temporal / envelope

- `left` / **envelope_mean**: 0.123242
- `left` / **envelope_max**: 0.742441
- `left` / **envelope_std**: 0.0956545
- `left` / **envelope_length**: 110308
- `right` / **envelope_mean**: 0.123241
- `right` / **envelope_max**: 0.697046
- `right` / **envelope_std**: 0.0958798
- `right` / **envelope_length**: 110308
- `difference` / **envelope_mean**: 0.0239492
- `difference` / **envelope_max**: 0.204019
- `difference` / **envelope_std**: 0.0196696
- `difference` / **envelope_length**: 110308

### temporal / autocorrelation

- `left` / **autocorr_max**: 0.607014
- `left` / **autocorr_mean**: 9.44442e-05
- `left` / **first_peak_lag**: 5
- `left` / **num_peaks**: 438
- `left` / **periodicity_score**: 0.607014
- `right` / **autocorr_max**: 0.610112
- `right` / **autocorr_mean**: 9.4145e-05
- `right` / **first_peak_lag**: 5
- `right` / **num_peaks**: 444
- `right` / **periodicity_score**: 0.610112
- `difference` / **autocorr_max**: 0.704082
- `difference` / **autocorr_mean**: 9.91905e-05
- `difference` / **first_peak_lag**: 5
- `difference` / **num_peaks**: 111
- `difference` / **periodicity_score**: 0.704082

### temporal / pulse_detection

- `left` / **num_pulses**: 304
- `left` / **interval_mean**: 342.462
- `left` / **interval_std**: 328.087
- `left` / **regularity_score**: 0.0419769
- `right` / **num_pulses**: 310
- `right` / **interval_mean**: 336.544
- `right` / **interval_std**: 315.911
- `right` / **regularity_score**: 0.0613063
- `difference` / **num_pulses**: 236
- `difference` / **interval_mean**: 443.17
- `difference` / **interval_std**: 491.67
- `difference` / **regularity_score**: 0

### temporal / pulse_detection

- `left` / **num_pulses**: 132
- `left` / **interval_mean**: 792.962
- `left` / **interval_std**: 474.179
- `left` / **regularity_score**: 0.402015
- `right` / **num_pulses**: 131
- `right` / **interval_mean**: 799.069
- `right` / **interval_std**: 476.937
- `right` / **regularity_score**: 0.403134
- `difference` / **num_pulses**: 102
- `difference` / **interval_mean**: 1031.14
- `difference` / **interval_std**: 677.309
- `difference` / **regularity_score**: 0.343145

### temporal / pulse_detection

- `left` / **num_pulses**: 195
- `left` / **interval_mean**: 530.113
- `left` / **interval_std**: 715.629
- `left` / **regularity_score**: 0
- `right` / **num_pulses**: 211
- `right` / **interval_mean**: 489.724
- `right` / **interval_std**: 645.527
- `right` / **regularity_score**: 0
- `difference` / **num_pulses**: 59
- `difference` / **interval_mean**: 1590.26
- `difference` / **interval_std**: 1631.96
- `difference` / **regularity_score**: 0

### temporal / pulse_detection

- `left` / **num_pulses**: 89
- `left` / **interval_mean**: 1168.66
- `left` / **interval_std**: 933.518
- `left` / **regularity_score**: 0.201206
- `right` / **num_pulses**: 94
- `right` / **interval_mean**: 1105.83
- `right` / **interval_std**: 895.914
- `right` / **regularity_score**: 0.189825
- `difference` / **num_pulses**: 45
- `difference` / **interval_mean**: 2090.48
- `difference` / **interval_std**: 1656.01
- `difference` / **regularity_score**: 0.207833

### temporal / pulse_detection

- `left` / **num_pulses**: 50
- `left` / **interval_mean**: 1860.45
- `left` / **interval_std**: 3375.02
- `left` / **regularity_score**: 0
- `right` / **num_pulses**: 76
- `right` / **interval_mean**: 1215.4
- `right` / **interval_std**: 2114.03
- `right` / **regularity_score**: 0
- `difference` / **num_pulses**: 12
- `difference` / **interval_mean**: 6992.36
- `difference` / **interval_std**: 7295.91
- `difference` / **regularity_score**: 0

### temporal / pulse_detection

- `left` / **num_pulses**: 29
- `left` / **interval_mean**: 3247.86
- `left` / **interval_std**: 4065.32
- `left` / **regularity_score**: 0
- `right` / **num_pulses**: 41
- `right` / **interval_mean**: 2273.47
- `right` / **interval_std**: 2584.69
- `right` / **regularity_score**: 0
- `difference` / **num_pulses**: 11
- `difference` / **interval_mean**: 7666.2
- `difference` / **interval_std**: 7318.39
- `difference` / **regularity_score**: 0.0453698

### temporal / duration_ratios

- `left` / **num_events**: 516
- `left` / **num_intervals**: 515
- `left` / **ratio_mean**: 1.50472
- `left` / **ratio_std**: 2.6896
- `right` / **num_events**: 543
- `right` / **num_intervals**: 542
- `right` / **ratio_mean**: 1.46663
- `right` / **ratio_std**: 2.62852
- `difference` / **num_events**: 214
- `difference` / **num_intervals**: 213
- `difference` / **ratio_mean**: 3.10578
- `difference` / **ratio_std**: 5.8222

### modulation / am_detection

- `left` / **modulation_detected**: True
- `left` / **num_modulation_frequencies**: 1
- `left` / **dominant_modulation_freq**: 2.99842
- `left` / **modulation_depth**: 6.02428
- `left` / **modulation_index**: 0.776155
- `left` / **envelope_mean**: 0.123242
- `left` / **envelope_std**: 0.0956545
- `right` / **modulation_detected**: True
- `right` / **num_modulation_frequencies**: 1
- `right` / **dominant_modulation_freq**: 2.99842
- `right` / **modulation_depth**: 5.65594
- `right` / **modulation_index**: 0.777984
- `right` / **envelope_mean**: 0.123241
- `right` / **envelope_std**: 0.0958798
- `difference` / **modulation_detected**: False
- `difference` / **num_modulation_frequencies**: 0
- `difference` / **dominant_modulation_freq**: 0
- `difference` / **modulation_depth**: 8.51884
- `difference` / **modulation_index**: 0.821304
- `difference` / **envelope_mean**: 0.0239492
- `difference` / **envelope_std**: 0.0196696

### modulation / fm_detection

- `left` / **fm_detected**: True
- `left` / **carrier_frequency_mean**: 4168.66
- `left` / **frequency_deviation**: 2378.41
- `left` / **frequency_range**: 22072.2
- `left` / **frequency_std**: 2378.41
- `left` / **num_fm_components**: 0
- `left` / **modulation_index_fm**: 0.570545
- `right` / **fm_detected**: True
- `right` / **carrier_frequency_mean**: 4157.71
- `right` / **frequency_deviation**: 2191.06
- `right` / **frequency_range**: 22070.6
- `right` / **frequency_std**: 2191.06
- `right` / **num_fm_components**: 0
- `right` / **modulation_index_fm**: 0.526986
- `difference` / **fm_detected**: True
- `difference` / **carrier_frequency_mean**: 3993.93
- `difference` / **frequency_deviation**: 3170.16
- `difference` / **frequency_range**: 22084.3
- `difference` / **frequency_std**: 3170.16
- `difference` / **num_fm_components**: 0
- `difference` / **modulation_index_fm**: 0.793746

### modulation / phase_analysis

- `left` / **phase_mean**: 0.0518149
- `left` / **phase_std**: 1.79831
- `left` / **phase_range**: 6.28317
- `left` / **unwrapped_phase_total**: 131030
- `left` / **phase_coherence**: 0.477477
- `left` / **num_phase_jumps**: 32996
- `left` / **phase_jump_rate**: 6595.73
- `right` / **phase_mean**: 0.0731416
- `right` / **phase_std**: 1.7949
- `right` / **phase_range**: 6.28317
- `right` / **unwrapped_phase_total**: 130686
- `right` / **phase_coherence**: 0.506555
- `right` / **num_phase_jumps**: 32252
- `right` / **phase_jump_rate**: 6447.01
- `difference` / **phase_mean**: -0.0354586
- `difference` / **phase_std**: 1.78953
- `difference` / **phase_range**: 6.28317
- `difference` / **unwrapped_phase_total**: 125538
- `difference` / **phase_coherence**: 0.324723
- `difference` / **num_phase_jumps**: 35717
- `difference` / **phase_jump_rate**: 7139.64

### modulation / modulation_index

- `left` / **modulation_index**: 0.776155
- `left` / **modulation_depth**: 6.02428
- `left` / **ac_component**: 0.0956545
- `left` / **dc_component**: 0.123242
- `left` / **peak_to_average_ratio**: 6.02428
- `right` / **modulation_index**: 0.777984
- `right` / **modulation_depth**: 5.65594
- `right` / **ac_component**: 0.0958798
- `right` / **dc_component**: 0.123241
- `right` / **peak_to_average_ratio**: 5.65594
- `difference` / **modulation_index**: 0.821304
- `difference` / **modulation_depth**: 8.51884
- `difference` / **ac_component**: 0.0196696
- `difference` / **dc_component**: 0.0239492
- `difference` / **peak_to_average_ratio**: 8.51884

### modulation / chirp_detection

- `left` / **num_chirps**: 48
- `left` / **total_chirp_duration**: 3.34367
- `left` / **mean_chirp_rate**: 14366.3
- `right` / **num_chirps**: 47
- `right` / **total_chirp_duration**: 3.27401
- `right` / **mean_chirp_rate**: 14509.2
- `difference` / **num_chirps**: 53
- `difference` / **total_chirp_duration**: 3.69197
- `difference` / **mean_chirp_rate**: 14744.1

### spectral / fft_global

- `left` / **n_fft**: 110308
- `left` / **frequency_resolution**: 0.199895
- `left` / **peak_frequency**: 4528.02
- `left` / **peak_magnitude**: 692.123
- `left` / **spectral_energy**: 3.16892e+07
- `right` / **n_fft**: 110308
- `right` / **frequency_resolution**: 0.199895
- `right` / **peak_frequency**: 4528.02
- `right` / **peak_magnitude**: 701.486
- `right` / **spectral_energy**: 3.17133e+07
- `difference` / **n_fft**: 110308
- `difference` / **frequency_resolution**: 0.199895
- `difference` / **peak_frequency**: 4326.52
- `difference` / **peak_magnitude**: 74.9876
- `difference` / **spectral_energy**: 1.21887e+06

### spectral / peak_detection

- `left` / **num_peaks**: 1172
- `left` / **dominant_frequency**: 2832.91
- `left` / **frequency_spread**: 906.082
- `right` / **num_peaks**: 1187
- `right` / **dominant_frequency**: 2832.71
- `right` / **frequency_spread**: 911.815
- `difference` / **num_peaks**: 1104
- `difference` / **dominant_frequency**: 2883.48
- `difference` / **frequency_spread**: 884.846

### spectral / harmonic_analysis

- `left` / **fundamental_frequency**: 168.911
- `left` / **harmonics_detected**: 10
- `left` / **harmonicity_score**: 1
- `right` / **fundamental_frequency**: 223.882
- `right` / **harmonics_detected**: 10
- `right` / **harmonicity_score**: 1
- `difference` / **fundamental_frequency**: 218.085
- `difference` / **harmonics_detected**: 10
- `difference` / **harmonicity_score**: 1

### spectral / cepstrum

- `left` / **peak_quefrency**: 9.07029e-05
- `left` / **peak_magnitude**: 0.782014
- `left` / **cepstrum_mean**: 0.00101421
- `left` / **cepstrum_std**: 0.00693496
- `left` / **samples_analyzed**: 100000
- `right` / **peak_quefrency**: 9.07029e-05
- `right` / **peak_magnitude**: 0.762119
- `right` / **cepstrum_mean**: 0.000993905
- `right` / **cepstrum_std**: 0.00669667
- `right` / **samples_analyzed**: 100000
- `difference` / **peak_quefrency**: 9.07029e-05
- `difference` / **peak_magnitude**: 0.859355
- `difference` / **cepstrum_mean**: 0.00122812
- `difference` / **cepstrum_std**: 0.0129848
- `difference` / **samples_analyzed**: 100000

### spectral / spectral_centroid

- `left` / **spectral_centroid**: 4486.72
- `left` / **normalized_centroid**: 0.406959
- `right` / **spectral_centroid**: 4485.65
- `right` / **normalized_centroid**: 0.406862
- `difference` / **spectral_centroid**: 4468.52
- `difference` / **normalized_centroid**: 0.405308

### spectral / spectral_bandwidth

- `left` / **spectral_bandwidth**: 705.377
- `left` / **spectral_centroid_Hz**: 4559.72
- `right` / **spectral_bandwidth**: 704.499
- `right` / **spectral_centroid_Hz**: 4557.51
- `difference` / **spectral_bandwidth**: 659.933
- `difference` / **spectral_centroid_Hz**: 4496.29

### spectral / spectral_rolloff

- `left` / **rolloff_frequency**: 5472.72
- `left` / **rolloff_percent**: 0.85
- `left` / **normalized_rolloff**: 0.496392
- `left` / **energy_concentration**: 0.496392
- `right` / **rolloff_frequency**: 5472.72
- `right` / **rolloff_percent**: 0.85
- `right` / **normalized_rolloff**: 0.496392
- `right` / **energy_concentration**: 0.496392
- `difference` / **rolloff_frequency**: 5227.05
- `difference` / **rolloff_percent**: 0.85
- `difference` / **normalized_rolloff**: 0.474109
- `difference` / **energy_concentration**: 0.474109

### spectral / spectral_flux

- `left` / **mean_flux**: 0.0359413
- `left` / **std_flux**: 0.0150067
- `left` / **max_flux**: 0.0703315
- `left` / **min_flux**: 0
- `left` / **num_frames**: 216
- `left` / **flux_variation**: 0.417535
- `right` / **mean_flux**: 0.035772
- `right` / **std_flux**: 0.0154473
- `right` / **max_flux**: 0.0804406
- `right` / **min_flux**: 0
- `right` / **num_frames**: 216
- `right` / **flux_variation**: 0.431825
- `difference` / **mean_flux**: 0.00993179
- `difference` / **std_flux**: 0.00379441
- `difference` / **max_flux**: 0.0229072
- `difference` / **min_flux**: 0
- `difference` / **num_frames**: 216
- `difference` / **flux_variation**: 0.382047

### spectral / spectral_flatness

- `left` / **spectral_flatness**: 0.00494548
- `left` / **tonality**: 0.995055
- `right` / **spectral_flatness**: 0.00493943
- `right` / **tonality**: 0.995061
- `difference` / **spectral_flatness**: 0.0130293
- `difference` / **tonality**: 0.986971

### time_frequency / stft

- `left` / **num_time_frames**: 217
- `left` / **num_freq_bins**: 1025
- `left` / **frequency_resolution**: 10.7666
- `left` / **time_resolution**: 0.02322
- `left` / **mean_magnitude**: 0.000477322
- `left` / **max_magnitude**: 0.0398015
- `left` / **dominant_freq_mean**: 4455.34
- `left` / **dominant_freq_std**: 1087.3
- `left` / **spectral_flux_mean**: 0.0359413
- `left` / **spectral_flux_max**: 0.0703315
- `left` / **temporal_stability**: 0.470107
- `right` / **num_time_frames**: 217
- `right` / **num_freq_bins**: 1025
- `right` / **frequency_resolution**: 10.7666
- `right` / **time_resolution**: 0.02322
- `right` / **mean_magnitude**: 0.000477419
- `right` / **max_magnitude**: 0.0398025
- `right` / **dominant_freq_mean**: 4443.18
- `right` / **dominant_freq_std**: 1097.28
- `right` / **spectral_flux_mean**: 0.035772
- `right` / **spectral_flux_max**: 0.0804406
- `right` / **temporal_stability**: 0.469756
- `difference` / **num_time_frames**: 217
- `difference` / **num_freq_bins**: 1025
- `difference` / **frequency_resolution**: 10.7666
- `difference` / **time_resolution**: 0.02322
- `difference` / **mean_magnitude**: 0.000121589
- `difference` / **max_magnitude**: 0.00757549
- `difference` / **dominant_freq_mean**: 4364.24
- `difference` / **dominant_freq_std**: 1143.04
- `difference` / **spectral_flux_mean**: 0.00993179
- `difference` / **spectral_flux_max**: 0.0229072
- `difference` / **temporal_stability**: 0.450192

### time_frequency / cqt

- `left` / **samples_analyzed**: 110308
- `left` / **hop_length**: 512
- `left` / **fmin_hz**: 32.7032
- `left` / **n_bins**: 84
- `left` / **bins_per_octave**: 12
- `left` / **num_time_frames**: 216
- `left` / **num_freq_bins**: 84
- `left` / **mean_magnitude_db**: -76.9567
- `left` / **max_magnitude_db**: 0
- `right` / **samples_analyzed**: 110308
- `right` / **hop_length**: 512
- `right` / **fmin_hz**: 32.7032
- `right` / **n_bins**: 84
- `right` / **bins_per_octave**: 12
- `right` / **num_time_frames**: 216
- `right` / **num_freq_bins**: 84
- `right` / **mean_magnitude_db**: -76.9375
- `right` / **max_magnitude_db**: 0
- `difference` / **samples_analyzed**: 110308
- `difference` / **hop_length**: 512
- `difference` / **fmin_hz**: 32.7032
- `difference` / **n_bins**: 84
- `difference` / **bins_per_octave**: 12
- `difference` / **num_time_frames**: 216
- `difference` / **num_freq_bins**: 84
- `difference` / **mean_magnitude_db**: -77.1647
- `difference` / **max_magnitude_db**: 0

### time_frequency / wavelet

- `global` / **error**: Morlet wavelet not available. Please upgrade scipy to >= 1.4.0 or install PyWavelets: pip install PyWavelets

### time_frequency / band_stability

_No scalar measurements found for this method._

### information / shannon_entropy

- `left` / **shannon_entropy**: 6.22797
- `left` / **max_entropy**: 8
- `left` / **normalized_entropy**: 0.778496
- `left` / **num_bins**: 256
- `right` / **shannon_entropy**: 6.32017
- `right` / **max_entropy**: 8
- `right` / **normalized_entropy**: 0.790021
- `right` / **num_bins**: 256
- `difference` / **shannon_entropy**: 5.66076
- `difference` / **max_entropy**: 8
- `difference` / **normalized_entropy**: 0.707595
- `difference` / **num_bins**: 256

### information / local_entropy

- `left` / **mean_entropy**: 4.93372
- `left` / **std_entropy**: 1.05616
- `left` / **min_entropy**: -0
- `left` / **max_entropy**: 5.72964
- `left` / **num_windows**: 214
- `left` / **entropy_variation**: 0.214069
- `right` / **mean_entropy**: 4.94732
- `right` / **std_entropy**: 1.03907
- `right` / **min_entropy**: -0
- `right` / **max_entropy**: 5.72564
- `right` / **num_windows**: 214
- `right` / **entropy_variation**: 0.210027
- `difference` / **mean_entropy**: 4.73365
- `difference` / **std_entropy**: 1.34727
- `difference` / **min_entropy**: -0
- `difference` / **max_entropy**: 5.81319
- `difference` / **num_windows**: 214
- `difference` / **entropy_variation**: 0.284616

### information / compression_ratio

- `left` / **original_size**: 200000
- `left` / **compressed_size**: 176955
- `left` / **compression_ratio**: 1.13023
- `left` / **samples_analyzed**: 100000
- `right` / **original_size**: 200000
- `right` / **compressed_size**: 177029
- `right` / **compression_ratio**: 1.12976
- `right` / **samples_analyzed**: 100000
- `difference` / **original_size**: 200000
- `difference` / **compressed_size**: 151392
- `difference` / **compression_ratio**: 1.32107
- `difference` / **samples_analyzed**: 100000

### information / approximate_complexity

- `left` / **approximate_complexity**: 0.039417
- `left` / **pattern_length**: 2
- `left` / **tolerance**: 0.0137036
- `left` / **samples_analyzed**: 5000
- `right` / **approximate_complexity**: 0.0683778
- `right` / **pattern_length**: 2
- `right` / **tolerance**: 0.0141817
- `right` / **samples_analyzed**: 5000
- `difference` / **approximate_complexity**: 0.0541399
- `difference` / **pattern_length**: 2
- `difference` / **tolerance**: 0.00296747
- `difference` / **samples_analyzed**: 5000

### information / mutual_information

- `global` / **num_channels**: 3
- `global` / **mean_mi**: 0.868203
- `global` / **max_mi**: 2.36954
- `global` / **samples_analyzed**: 50000

### inter_channel / lr_difference

- `lr_difference` / **left_energy**: 1342.35
- `lr_difference` / **right_energy**: 1344.73
- `lr_difference` / **difference_energy**: 52.9729
- `lr_difference` / **energy_ratio**: 0.0197139
- `lr_difference` / **difference_rms**: 0.0219141
- `lr_difference` / **difference_peak_freq**: 4738.11
- `lr_difference` / **difference_peak_magnitude**: 118.059
- `lr_difference` / **contains_unique_info**: True

### inter_channel / cross_correlation

- `left_vs_right` / **max_correlation**: 1
- `left_vs_right` / **peak_lag**: 0
- `left_vs_right` / **peak_value**: 1
- `left_vs_right` / **mean_correlation**: 9.50192e-05
- `left_vs_right` / **correlation_at_zero**: 1
- `left_vs_difference` / **max_correlation**: 2.46977
- `left_vs_difference` / **peak_lag**: 730
- `left_vs_difference` / **peak_value**: -2.46977
- `left_vs_difference` / **mean_correlation**: 5.27438e-05
- `left_vs_difference` / **correlation_at_zero**: 1
- `right_vs_difference` / **max_correlation**: 1.66652
- `right_vs_difference` / **peak_lag**: 511
- `right_vs_difference` / **peak_value**: 1.66652
- `right_vs_difference` / **mean_correlation**: 0.000132197
- `right_vs_difference` / **correlation_at_zero**: 1

### inter_channel / phase_difference

- `left_vs_right` / **phase_diff_mean**: 0.00299536
- `left_vs_right` / **phase_diff_std**: 0.601359
- `left_vs_right` / **phase_diff_range**: 6.28319
- `left_vs_right` / **phase_coherence**: 0.887528
- `left_vs_right` / **in_phase**: True
- `left_vs_right` / **out_of_phase**: False
- `left_vs_difference` / **phase_diff_mean**: -0.00306565
- `left_vs_difference` / **phase_diff_std**: 1.77759
- `left_vs_difference` / **phase_diff_range**: 6.28319
- `left_vs_difference` / **phase_coherence**: 0.0986272
- `left_vs_difference` / **in_phase**: True
- `left_vs_difference` / **out_of_phase**: False
- `right_vs_difference` / **phase_diff_mean**: -0.00361172
- `right_vs_difference` / **phase_diff_std**: 1.99876
- `right_vs_difference` / **phase_diff_range**: 6.28319
- `right_vs_difference` / **phase_coherence**: 0.0818634
- `right_vs_difference` / **in_phase**: True
- `right_vs_difference` / **out_of_phase**: False

### inter_channel / time_delay

- `left_vs_right` / **delay_samples**: 0
- `left_vs_right` / **delay_ms**: 0
- `left_vs_right` / **correlation_at_delay**: 618.019
- `left_vs_right` / **is_synchronized**: True
- `left_vs_difference` / **delay_samples**: -97
- `left_vs_difference` / **delay_ms**: -4.39909
- `left_vs_difference` / **correlation_at_delay**: 9.32
- `left_vs_difference` / **is_synchronized**: False
- `right_vs_difference` / **delay_samples**: 0
- `right_vs_difference` / **delay_ms**: 0
- `right_vs_difference` / **correlation_at_delay**: -11.9944
- `right_vs_difference` / **is_synchronized**: True

### steganography / lsb_analysis

- `left` / **lsb_mean**: 0.47027
- `left` / **lsb_std**: 0.499115
- `left` / **transition_rate**: 0.4706
- `left` / **mean_zero_run**: 2.25125
- `left` / **mean_one_run**: 1.9986
- `left` / **samples_analyzed**: 100000
- `right` / **lsb_mean**: 0.47163
- `right` / **lsb_std**: 0.499194
- `right` / **transition_rate**: 0.46999
- `right` / **mean_zero_run**: 2.24838
- `right` / **mean_one_run**: 2.00698
- `right` / **samples_analyzed**: 100000
- `difference` / **lsb_mean**: 0.4483
- `difference` / **lsb_std**: 0.49732
- `difference` / **transition_rate**: 0.45038
- `difference` / **mean_zero_run**: 2.4498
- `difference` / **mean_one_run**: 1.99076
- `difference` / **samples_analyzed**: 100000

### steganography / quantization_noise

- `left` / **noise_power**: 7.35647e-10
- `left` / **noise_std**: 2.71228e-05
- `left` / **autocorr_peak**: 0.418062
- `left` / **spectral_flatness**: 0.752233
- `left` / **samples_analyzed**: 50000
- `right` / **noise_power**: 7.35207e-10
- `right` / **noise_std**: 2.71147e-05
- `right` / **autocorr_peak**: 0.415448
- `right` / **spectral_flatness**: 0.750377
- `right` / **samples_analyzed**: 50000
- `difference` / **noise_power**: 7.74341e-10
- `difference` / **noise_std**: 2.78269e-05
- `difference` / **autocorr_peak**: 0.4805
- `difference` / **spectral_flatness**: 0.72345
- `difference` / **samples_analyzed**: 50000

### steganography / signal_residual

- `left` / **signal_power**: 9.88691e-07
- `left` / **residual_power**: 0.0126421
- `left` / **snr_db**: -41.0676
- `left` / **residual_peak_freq**: 4528.19
- `left` / **energy_ratio**: 12785.4
- `left` / **samples_analyzed**: 100000
- `right` / **signal_power**: 1.21327e-06
- `right` / **residual_power**: 0.0126712
- `right` / **snr_db**: -40.1886
- `right` / **residual_peak_freq**: 4528.19
- `right` / **energy_ratio**: 10443
- `right` / **samples_analyzed**: 100000
- `difference` / **signal_power**: 1.15074e-08
- `difference` / **residual_power**: 0.000488204
- `difference` / **snr_db**: -46.2762
- `difference` / **residual_peak_freq**: 4540.1
- `difference` / **energy_ratio**: 42059.7
- `difference` / **samples_analyzed**: 100000

### steganography / statistical_anomalies

- `left` / **num_outliers**: 912
- `left` / **outlier_rate**: 0.00912
- `left` / **max_z_score**: 6.41013
- `left` / **mean_z_score**: 0.719912
- `left` / **chi2_statistic**: 23579.3
- `left` / **chi2_pvalue**: 0
- `left` / **normality_test**: False
- `left` / **samples_analyzed**: 100000
- `right` / **num_outliers**: 905
- `right` / **outlier_rate**: 0.00905
- `right` / **max_z_score**: 6.11429
- `right` / **mean_z_score**: 0.719931
- `right` / **chi2_statistic**: 24868.3
- `right` / **chi2_pvalue**: 0
- `right` / **normality_test**: False
- `right` / **samples_analyzed**: 100000
- `difference` / **num_outliers**: 1179
- `difference` / **outlier_rate**: 0.01179
- `difference` / **max_z_score**: 8.70676
- `difference` / **mean_z_score**: 0.703478
- `difference` / **chi2_statistic**: 23661.1
- `difference` / **chi2_pvalue**: 0
- `difference` / **normality_test**: False
- `difference` / **samples_analyzed**: 100000

### steganography / parity_analysis

- `left` / **parity_mean**: 0.47027
- `left` / **parity_std**: 0.499115
- `left` / **transition_rate**: 0.470605
- `left` / **transition_anomaly**: 0.0293953
- `left` / **mean_run_length**: 2.1249
- `left` / **std_run_length**: 11.9946
- `left` / **chi2_statistic**: 353.549
- `left` / **chi2_pvalue**: 0
- `left` / **appears_random**: False
- `left` / **samples_analyzed**: 100000
- `right` / **parity_mean**: 0.47163
- `right` / **parity_std**: 0.499194
- `right` / **transition_rate**: 0.469995
- `right` / **transition_anomaly**: 0.0300053
- `right` / **mean_run_length**: 2.12766
- `right` / **std_run_length**: 10.1725
- `right` / **chi2_statistic**: 321.943
- `right` / **chi2_pvalue**: 0
- `right` / **appears_random**: False
- `right` / **samples_analyzed**: 100000
- `difference` / **parity_mean**: 0.4483
- `difference` / **parity_std**: 0.49732
- `difference` / **transition_rate**: 0.450385
- `difference` / **transition_anomaly**: 0.0496155
- `difference` / **mean_run_length**: 2.2203
- `difference` / **std_run_length**: 21.0122
- `difference` / **chi2_statistic**: 1069.16
- `difference` / **chi2_pvalue**: 0
- `difference` / **appears_random**: False
- `difference` / **samples_analyzed**: 100000

### meta_analysis / inter_segment_comparison

- `left` / **num_segments**: 10
- `left` / **mean_distance**: 81.7184
- `left` / **std_distance**: 39.1338
- `left` / **min_distance**: 14.7506
- `left` / **max_distance**: 183.843
- `left` / **similarity_score**: 0.0120892
- `right` / **num_segments**: 10
- `right` / **mean_distance**: 81.472
- `right` / **std_distance**: 38.4887
- `right` / **min_distance**: 17.3519
- `right` / **max_distance**: 173.597
- `right` / **similarity_score**: 0.0121253
- `difference` / **num_segments**: 10
- `difference` / **mean_distance**: 63.7597
- `difference` / **std_distance**: 44.0901
- `difference` / **min_distance**: 1.22234
- `difference` / **max_distance**: 181.911
- `difference` / **similarity_score**: 0.0154417

### meta_analysis / segment_clustering

- `left` / **num_segments**: 20
- `left` / **avg_intra_distance**: 0.00037259
- `left` / **unique_segments**: 0
- `left` / **repetition_rate**: 1
- `right` / **num_segments**: 20
- `right` / **avg_intra_distance**: 0.0013335
- `right` / **unique_segments**: 0
- `right` / **repetition_rate**: 1
- `difference` / **num_segments**: 20
- `difference` / **avg_intra_distance**: 0.0154789
- `difference` / **unique_segments**: 0
- `difference` / **repetition_rate**: 1

### meta_analysis / stability_scores

- `left` / **energy_stability**: 0.641394
- `left` / **spectral_stability**: 0.896676
- `left` / **overall_stability**: 0.769035
- `left` / **num_windows**: 212
- `right` / **energy_stability**: 0.641517
- `right` / **spectral_stability**: 0.89751
- `right` / **overall_stability**: 0.769514
- `right` / **num_windows**: 212
- `difference` / **energy_stability**: 0.664153
- `difference` / **spectral_stability**: 0.866389
- `difference` / **overall_stability**: 0.765271
- `difference` / **num_windows**: 212

### meta_analysis / high_order_statistics

- `left` / **mean**: 3.29223e-08
- `left` / **std**: 0.110314
- `left` / **variance**: 0.0121691
- `left` / **skewness**: 4.78574e-06
- `left` / **kurtosis**: 1.43866
- `left` / **peak_value**: 0.720734
- `left` / **crest_factor**: 6.53349
- `left` / **samples_analyzed**: 110308
- `right` / **mean**: -2.21326e-09
- `right` / **std**: 0.110411
- `right` / **variance**: 0.0121907
- `right` / **skewness**: 4.25942e-06
- `right` / **kurtosis**: 1.41182
- `right` / **peak_value**: 0.688263
- `right` / **crest_factor**: 6.23362
- `right` / **samples_analyzed**: 110308
- `difference` / **mean**: 3.51356e-08
- `difference` / **std**: 0.0219141
- `difference` / **variance**: 0.000480227
- `difference` / **skewness**: 2.4019e-05
- `difference` / **kurtosis**: 2.99061
- `difference` / **peak_value**: 0.192383
- `difference` / **crest_factor**: 8.77896
- `difference` / **samples_analyzed**: 110308
