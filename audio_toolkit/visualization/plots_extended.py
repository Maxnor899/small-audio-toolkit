"""
plots_extended.py

Conservé pour cohérence avec la documentation d'architecture.

Ce module ne contient plus d'implémentations : les fonctions "extended"
sont centralisées dans plots.py (source de vérité).
On garde uniquement des ré-exports pour compatibilité.
"""

from .plots import (
    plot_harmonics,
    plot_cepstrum,
    plot_wavelet_scalogram,
    plot_cross_correlation,
    plot_band_stability,
    plot_stft_spectrogram,
    plot_am_detection,
    plot_fm_detection,
    plot_phase_analysis,
)
