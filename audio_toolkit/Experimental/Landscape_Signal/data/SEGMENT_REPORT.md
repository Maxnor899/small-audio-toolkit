# Morphological Timeline Segmentation Report

This report segments time into 'chunks' based on the presence of a narrowband spectral line around a carrier frequency.
It uses binary thresholding on band energy followed by 1D morphological cleaning (closing/opening).

## Input
- file: `lsig.flac`
- domain: `diff`
- fc: 393.000 Hz (rel_bw=0.03)

## STFT configuration
- nperseg: 4096
- noverlap: 3072
- window: hann
- frames: 5136

## Thresholding
- method: hybrid
- q: 0.8
- zthr: 1.0
- thr_quantile: 0.18081438711260345
- ez_median: -1.0858284757442327e-16
- ez_std: 1.3454543367669285
- thr_used: {'quantile': 0.18081438711260345, 'robust_z': 1.0}

## Morphology
- closing_len_frames: 5
- opening_len_frames: 3

## Segments
- count: 34

| # | start (s) | end (s) | duration (s) |
|---:|---:|---:|---:|
| 1 | 8.043 | 11.968 | 3.925 |
| 2 | 12.523 | 12.949 | 0.427 |
| 3 | 14.421 | 14.720 | 0.299 |
| 4 | 15.531 | 15.659 | 0.128 |
| 5 | 16.171 | 16.384 | 0.213 |
| 6 | 18.667 | 18.773 | 0.107 |
| 7 | 27.563 | 27.733 | 0.171 |
| 8 | 27.968 | 28.203 | 0.235 |
| 9 | 28.331 | 31.744 | 3.413 |
| 10 | 31.957 | 33.643 | 1.685 |
| 11 | 33.792 | 34.432 | 0.640 |
| 12 | 34.581 | 35.435 | 0.853 |
| 13 | 46.379 | 46.507 | 0.128 |
| 14 | 46.635 | 50.069 | 3.435 |
| 15 | 50.197 | 50.731 | 0.533 |
| 16 | 50.923 | 51.947 | 1.024 |
| 17 | 52.096 | 52.309 | 0.213 |
| 18 | 52.480 | 52.629 | 0.149 |
| 19 | 53.333 | 53.504 | 0.171 |
| 20 | 61.888 | 62.080 | 0.192 |
| 21 | 62.571 | 66.496 | 3.925 |
| 22 | 66.688 | 67.072 | 0.384 |
| 23 | 80.043 | 83.264 | 3.221 |
| 24 | 83.392 | 83.627 | 0.235 |
| 25 | 83.755 | 86.293 | 2.539 |
| 26 | 86.464 | 87.019 | 0.555 |
| 27 | 87.189 | 87.381 | 0.192 |
| 28 | 87.509 | 87.979 | 0.469 |
| 29 | 101.504 | 101.739 | 0.235 |
| 30 | 101.931 | 102.571 | 0.640 |
| 31 | 102.699 | 102.869 | 0.171 |
| 32 | 103.061 | 103.893 | 0.832 |
| 33 | 104.043 | 104.512 | 0.469 |
| 34 | 104.981 | 105.280 | 0.299 |

## Outputs
- `segments.csv`: list of segments
- `band_energy.csv`: band energy + raw/morph masks
- `band_energy.png`, `mask_raw.png`, `mask_morph.png`, `spectrogram_roi.png`
