# SAP² Analysis Report

- SAT source: `C:\MORSE_AM\results.json`
- Matrix schema_version: `1.0`

## Channel: mono

### Applicability

| method_id | status | missing_required | unstable_required |
|---|---:|---:|---:|
| `amplitude_modulation_am` | `applicable` | 0 | 0 |
| `clock_plus_data_temporal_encoding` | `applicable` | 0 | 0 |
| `duration_based_morse_like` | `applicable` | 0 | 0 |
| `entropy_based_encoding` | `applicable` | 0 | 0 |
| `frame_based_temporal_encoding` | `applicable` | 0 | 0 |
| `frequency_displacement` | `applicable` | 0 | 0 |
| `frequency_modulation_fm` | `applicable` | 0 | 0 |
| `frequency_presence_fsk_like` | `applicable` | 0 | 0 |
| `harmonic_structure_encoding` | `applicable` | 0 | 0 |
| `inter_channel_phase_encoding` | `missing_inputs` | 1 | 0 |
| `inter_channel_time_delay` | `missing_inputs` | 1 | 0 |
| `left_right_difference_encoding` | `missing_inputs` | 1 | 0 |
| `multi_band_temporal_encoding` | `applicable` | 0 | 0 |
| `multi_scale_wavelet_encoding` | `underconstrained` | 0 | 1 |
| `phase_modulation` | `missing_inputs` | 1 | 0 |
| `pulse_duration_binary` | `applicable` | 0 | 0 |
| `pulse_presence_absence` | `applicable` | 0 | 0 |
| `redundancy_compressibility_encoding` | `applicable` | 0 | 0 |
| `residual_noise_floor_encoding` | `applicable` | 0 | 0 |
| `spectral_stability_encoding` | `underconstrained` | 0 | 1 |
| `stft_pattern_encoding` | `underconstrained` | 0 | 1 |
| `temporal_ratio_encoding` | `applicable` | 0 | 0 |

### Experiments

| method_id | status | diagnostics |
|---|---:|---|
| `amplitude_modulation_am` | `ExperimentStatus.REFUSED` | Decoder not implemented for method_id 'amplitude_modulation_am'. |
| `clock_plus_data_temporal_encoding` | `ExperimentStatus.REFUSED` | Decoder not implemented for method_id 'clock_plus_data_temporal_encoding'. |
| `duration_based_morse_like` | `ExperimentStatus.SUCCESS` | Intervals transformed: 99; dot_max=0.12, dash_min=0.2, letter_gap_min=None, word_gap_min=None; symbol counts: dot=0, dash=99, ambiguous=0, letter_sep=0, word_sep=0; bitstream mapping: dot_bit=0, dash_bit=1; bitstream counts: bits=99, none=0 (ambiguous + separators map to None) |
| `entropy_based_encoding` | `ExperimentStatus.REFUSED` | Decoder not implemented for method_id 'entropy_based_encoding'. |
| `frame_based_temporal_encoding` | `ExperimentStatus.REFUSED` | Decoder not implemented for method_id 'frame_based_temporal_encoding'. |
| `frequency_displacement` | `ExperimentStatus.REFUSED` | Decoder not implemented for method_id 'frequency_displacement'. |
| `frequency_modulation_fm` | `ExperimentStatus.REFUSED` | Decoder not implemented for method_id 'frequency_modulation_fm'. |
| `frequency_presence_fsk_like` | `ExperimentStatus.REFUSED` | Decoder not implemented for method_id 'frequency_presence_fsk_like'. |
| `harmonic_structure_encoding` | `ExperimentStatus.REFUSED` | Decoder not implemented for method_id 'harmonic_structure_encoding'. |
| `multi_band_temporal_encoding` | `ExperimentStatus.REFUSED` | Decoder not implemented for method_id 'multi_band_temporal_encoding'. |
| `pulse_duration_binary` | `ExperimentStatus.REFUSED` | Decoder not implemented for method_id 'pulse_duration_binary'. |
| `pulse_presence_absence` | `ExperimentStatus.REFUSED` | Decoder not implemented for method_id 'pulse_presence_absence'. |
| `redundancy_compressibility_encoding` | `ExperimentStatus.REFUSED` | Decoder not implemented for method_id 'redundancy_compressibility_encoding'. |
| `residual_noise_floor_encoding` | `ExperimentStatus.REFUSED` | Decoder not implemented for method_id 'residual_noise_floor_encoding'. |
| `temporal_ratio_encoding` | `ExperimentStatus.REFUSED` | Decoder not implemented for method_id 'temporal_ratio_encoding'. |
