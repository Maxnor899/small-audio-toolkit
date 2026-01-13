"""
Generate objective analysis reports from results.json

This script produces factual outputs based on measured values.
It does NOT perform automated classification.

Outputs (3 files):
- 01_MEASUREMENT_SUMMARY.md : key values overview (Measurement Summary only)
- 02_APPENDICES_AB.md       : Appendix A + B, rewritten for clarity/readability
- 03_FUNNEL_HYPOTHESIS.md   : hypothesis-driven funnel based on observations (no conclusions)
"""

import json
from pathlib import Path
from typing import Dict, Any, List


# ---------------------------------------------------------------------
# Reference thresholds from signal processing literature
# ---------------------------------------------------------------------
REFERENCE_THRESHOLDS = {
    'periodicity_score': {
        'high': 0.8,
        'very_high': 0.95,
        'note': 'Autocorrelation peak normalized value'
    },
    'harmonicity_score': {
        'harmonic': 0.7,
        'strongly_harmonic': 0.9,
        'note': 'Ratio of harmonic energy to total energy'
    },
    'tonality': {
        'tonal': 0.7,
        'highly_tonal': 0.9,
        'note': '1 - spectral_flatness, inverse of flatness'
    },
    'modulation_index': {
        'low': 0.1,
        'moderate': 0.3,
        'high': 0.5,
        'note': 'AC component / DC component ratio'
    },
    'phase_coherence': {
        'low': 0.3,
        'moderate': 0.6,
        'high': 0.8,
        'note': 'Inter-channel phase consistency (0-1)'
    },
    'shannon_entropy': {
        'low': 3.0,
        'moderate': 5.0,
        'high': 7.0,
        'note': 'Information entropy in bits (higher = more random/complex)'
    },
    'compression_ratio': {
        'high_compressibility': 0.3,
        'moderate': 0.5,
        'low_compressibility': 0.7,
        'note': 'Compressed size / original size (lower = more compressible/structured)'
    },
    'spectral_bandwidth': {
        'narrow': 1000,
        'moderate': 5000,
        'wide': 10000,
        'note': 'Spectral bandwidth in Hz'
    }
}

# Key metrics to observe for each method
KEY_METRICS_PER_METHOD = {
    # TEMPORAL
    'envelope': ['envelope_mean', 'envelope_max', 'envelope_std'],
    'autocorrelation': ['periodicity_score', 'first_peak_lag', 'num_peaks'],
    'pulse_detection': ['num_pulses', 'interval_mean', 'regularity_score'],
    'duration_ratios': ['num_events', 'ratio_mean', 'ratio_std'],
    
    # SPECTRAL
    'fft_global': ['peak_frequency', 'peak_magnitude', 'spectral_energy'],
    'peak_detection': ['num_peaks', 'dominant_frequency', 'frequency_spread'],
    'harmonic_analysis': ['fundamental_frequency', 'harmonicity_score', 'harmonics_detected'],
    'spectral_centroid': ['spectral_centroid', 'normalized_centroid'],
    'spectral_flatness': ['spectral_flatness', 'tonality'],
    'cepstrum': ['peak_quefrency', 'peak_magnitude', 'cepstrum_mean'],
    'spectral_bandwidth': ['spectral_bandwidth', 'spectral_centroid_Hz'],
    
    # TIME-FREQUENCY
    'stft': ['temporal_stability', 'dominant_freq_mean', 'spectral_flux_mean'],
    'band_stability': ['stability_score', 'mean_energy', 'variation_coefficient'],
    'wavelet': ['mean_magnitude', 'max_magnitude', 'energy_concentration'],
    
    # MODULATION
    'am_detection': ['modulation_detected', 'modulation_index', 'modulation_depth'],
    'fm_detection': ['fm_detected', 'frequency_deviation', 'carrier_frequency_mean'],
    'phase_analysis': ['phase_coherence', 'num_phase_jumps', 'phase_std'],
    'modulation_index': ['modulation_index', 'modulation_depth', 'peak_to_average_ratio'],
    
    # INFORMATION
    'shannon_entropy': ['entropy', 'normalized_entropy'],
    'local_entropy': ['mean_local_entropy', 'std_local_entropy', 'max_local_entropy'],
    'compression_ratio': ['compression_ratio', 'original_size', 'compressed_size'],
    'approximate_complexity': ['complexity_score', 'normalized_complexity'],
    
    # INTER-CHANNEL
    'cross_correlation': ['max_correlation', 'peak_lag', 'correlation_at_zero'],
    'lr_difference': ['energy_ratio', 'difference_peak_freq', 'contains_unique_info'],
    'phase_difference': ['phase_diff_mean', 'phase_coherence', 'in_phase'],
    'time_delay': ['delay_samples', 'delay_ms', 'is_synchronized'],
    
    # STEGANOGRAPHY
    'lsb_analysis': ['lsb_entropy', 'lsb_randomness', 'chi_square_stat'],
    'quantization_noise': ['noise_periodicity', 'noise_energy', 'autocorr_peak'],
    'signal_residual': ['residual_energy', 'residual_to_signal_ratio', 'residual_peaks'],
    
    # META-ANALYSIS
    'inter_segment_comparison': ['num_segments', 'similarity_mean', 'similarity_std'],
    'segment_clustering': ['num_clusters', 'silhouette_score', 'cluster_sizes'],
    'stability_scores': ['temporal_stability', 'spectral_stability', 'overall_stability']
}


# ---------------------------------------------------------------------
# IO helpers
# ---------------------------------------------------------------------
def load_results(results_path: Path) -> dict:
    """Load results.json file."""
    with open(results_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def format_value(value: Any, precision: int = 3) -> str:
    """Format numeric value for display."""
    if isinstance(value, bool):
        return str(value)
    if isinstance(value, float):
        if abs(value) > 1e6 or (abs(value) < 1e-3 and value != 0.0):
            return f"{value:.{precision}e}"
        return f"{value:.{precision}f}"
    if isinstance(value, int):
        return str(value)
    return str(value)


def _header_lines(results: dict, title: str) -> List[str]:
    lines = []
    lines.append(f"# {title}")
    lines.append("")
    lines.append(f"**Analysis timestamp:** {results.get('timestamp', 'N/A')}")
    lines.append(f"**Input file:** {results.get('metadata', {}).get('audio_file', 'N/A')}")
    lines.append("")
    return lines


def _file_information_lines(results: dict) -> List[str]:
    lines = []
    audio_info = results.get('metadata', {}).get('audio_info', {}) or {}
    lines.append("## File Information")
    lines.append("")
    if audio_info:
        if 'duration' in audio_info:
            try:
                lines.append(f"- Duration: {float(audio_info['duration']):.2f} seconds")
            except Exception:
                lines.append(f"- Duration: {audio_info['duration']}")
        if 'sample_rate' in audio_info:
            lines.append(f"- Sample rate: {audio_info['sample_rate']} Hz")
        if 'channels' in audio_info:
            lines.append(f"- Channels: {audio_info['channels']}")
        if 'format' in audio_info and 'subtype' in audio_info:
            lines.append(f"- Format: {audio_info['format']} / {audio_info['subtype']}")
        if 'frames' in audio_info:
            lines.append(f"- Total frames: {audio_info['frames']}")
    else:
        lines.append("- No audio_info available in results.json")
    lines.append("")
    return lines


def _preprocessing_lines(results: dict) -> List[str]:
    lines = []
    preproc = results.get('metadata', {}).get('preprocessing', None)
    if not preproc:
        return lines

    lines.append("## Preprocessing Applied")
    lines.append("")
    for key, settings in preproc.items():
        if isinstance(settings, dict) and settings.get('enabled', False):
            lines.append(f"### {key}")
            for param, value in settings.items():
                if param != 'enabled':
                    lines.append(f"- {param}: {value}")
            lines.append("")
    return lines


# ---------------------------------------------------------------------
# Extract key metrics (extended for all methods)
# ---------------------------------------------------------------------
def extract_key_metrics(results: dict) -> List[Dict[str, Any]]:
    """Extract key metrics for summary section."""
    metrics = []

    # Periodicity score
    periodicity_values = {}
    for method in results.get('results', {}).get('temporal', []):
        if method.get('method') == 'autocorrelation':
            for channel, data in method.get('measurements', {}).items():
                if isinstance(data, dict) and 'periodicity_score' in data:
                    periodicity_values[channel] = data['periodicity_score']

    if periodicity_values:
        ref = REFERENCE_THRESHOLDS['periodicity_score']
        metrics.append({
            'name': 'Periodicity Score (Autocorrelation)',
            'values': periodicity_values,
            'reference': f"high > {ref['high']}, very_high > {ref['very_high']}",
            'unit': 'normalized (0-1)'
        })

    # Harmonicity score + fundamental
    harmonicity_values = {}
    fundamental_values = {}
    for method in results.get('results', {}).get('spectral', []):
        if method.get('method') == 'harmonic_analysis':
            for channel, data in method.get('measurements', {}).items():
                if isinstance(data, dict):
                    if 'harmonicity_score' in data:
                        harmonicity_values[channel] = data['harmonicity_score']
                    if 'fundamental_frequency' in data:
                        fundamental_values[channel] = data['fundamental_frequency']

    if harmonicity_values:
        ref = REFERENCE_THRESHOLDS['harmonicity_score']
        metrics.append({
            'name': 'Harmonicity Score',
            'values': harmonicity_values,
            'reference': f"harmonic > {ref['harmonic']}, strongly_harmonic > {ref['strongly_harmonic']}",
            'unit': 'normalized (0-1)'
        })

    if fundamental_values:
        metrics.append({
            'name': 'Fundamental Frequency',
            'values': fundamental_values,
            'unit': 'Hz'
        })

    # Tonality
    tonality_values = {}
    for method in results.get('results', {}).get('spectral', []):
        if method.get('method') == 'spectral_flatness':
            for channel, data in method.get('measurements', {}).items():
                if isinstance(data, dict) and 'tonality' in data:
                    tonality_values[channel] = data['tonality']

    if tonality_values:
        ref = REFERENCE_THRESHOLDS['tonality']
        metrics.append({
            'name': 'Tonality (1 - Spectral Flatness)',
            'values': tonality_values,
            'reference': f"tonal > {ref['tonal']}, highly_tonal > {ref['highly_tonal']}",
            'unit': 'normalized (0-1)'
        })

    # Modulation index (AM)
    mod_index_values = {}
    for method in results.get('results', {}).get('modulation', []):
        if method.get('method') == 'am_detection':
            for channel, data in method.get('measurements', {}).items():
                if isinstance(data, dict) and 'modulation_index' in data:
                    mod_index_values[channel] = data['modulation_index']

    if mod_index_values:
        ref = REFERENCE_THRESHOLDS['modulation_index']
        metrics.append({
            'name': 'Modulation Index (AM)',
            'values': mod_index_values,
            'reference': f"low < {ref['low']}, moderate < {ref['moderate']}, high > {ref['high']}",
            'unit': 'ratio (AC/DC)'
        })

    # Phase coherence
    phase_coh_values = {}
    for method in results.get('results', {}).get('modulation', []):
        if method.get('method') == 'phase_analysis':
            for channel, data in method.get('measurements', {}).items():
                if isinstance(data, dict) and 'phase_coherence' in data:
                    phase_coh_values[channel] = data['phase_coherence']

    if phase_coh_values:
        ref = REFERENCE_THRESHOLDS['phase_coherence']
        metrics.append({
            'name': 'Phase Coherence',
            'values': phase_coh_values,
            'reference': f"low < {ref['low']}, moderate < {ref['moderate']}, high > {ref['high']}",
            'unit': 'normalized (0-1)'
        })

    # Shannon Entropy
    entropy_values = {}
    for method in results.get('results', {}).get('information', []):
        if method.get('method') == 'shannon_entropy':
            for channel, data in method.get('measurements', {}).items():
                if isinstance(data, dict) and 'entropy' in data:
                    entropy_values[channel] = data['entropy']

    if entropy_values:
        ref = REFERENCE_THRESHOLDS['shannon_entropy']
        metrics.append({
            'name': 'Shannon Entropy',
            'values': entropy_values,
            'reference': f"low < {ref['low']}, moderate < {ref['moderate']}, high > {ref['high']}",
            'unit': 'bits'
        })

    # Compression Ratio
    compression_values = {}
    for method in results.get('results', {}).get('information', []):
        if method.get('method') == 'compression_ratio':
            for channel, data in method.get('measurements', {}).items():
                if isinstance(data, dict) and 'compression_ratio' in data:
                    compression_values[channel] = data['compression_ratio']

    if compression_values:
        ref = REFERENCE_THRESHOLDS['compression_ratio']
        metrics.append({
            'name': 'Compression Ratio',
            'values': compression_values,
            'reference': f"high_compressibility < {ref['high_compressibility']}, low_compressibility > {ref['low_compressibility']}",
            'unit': 'ratio (compressed/original)'
        })

    # L-R Difference Energy Ratio
    lr_values = {}
    for method in results.get('results', {}).get('inter_channel', []):
        if method.get('method') == 'lr_difference':
            for key, data in method.get('measurements', {}).items():
                if isinstance(data, dict) and 'energy_ratio' in data:
                    lr_values[key] = data['energy_ratio']

    if lr_values:
        metrics.append({
            'name': 'L-R Energy Ratio',
            'values': lr_values,
            'reference': 'higher values indicate more unique information in stereo field',
            'unit': 'ratio'
        })

    return metrics


# ---------------------------------------------------------------------
# Observations: factual, cautious, non-conclusive (EXTENDED)
# ---------------------------------------------------------------------
def generate_observations(results: dict) -> List[Dict[str, Any]]:
    """
    Generate factual observations by comparing measured values to reference thresholds.
    Produces cautious, non-conclusive statements designed for human interpretation.
    """
    observations: List[Dict[str, Any]] = []

    def add_obs(category: str,
                description: str,
                measurements: List[str],
                reference: str,
                observation: str,
                possible_indication: str) -> None:
        observations.append({
            "category": category,
            "description": description,
            "measurements": measurements,
            "reference": reference,
            "observation": observation,
            "possible_indication": possible_indication,
        })

    def iter_methods(section_name: str):
        for method in results.get("results", {}).get(section_name, []):
            yield method

    # TEMPORAL
    for method in iter_methods("temporal"):
        mname = method.get("method", "")
        meas = method.get("measurements", {})

        if mname == "autocorrelation":
            ref = REFERENCE_THRESHOLDS.get("periodicity_score", {})
            high = ref.get("high")
            very_high = ref.get("very_high")

            lines = []
            flagged = False

            for ch, data in meas.items():
                if not isinstance(data, dict):
                    continue
                ps = data.get("periodicity_score")
                if ps is None:
                    continue
                lines.append(f"{ch}: periodicity_score={format_value(ps)}")
                if isinstance(ps, (int, float)):
                    if very_high is not None and ps >= very_high:
                        flagged = True
                    elif high is not None and ps >= high:
                        flagged = True

            if flagged:
                add_obs(
                    category="Periodicity (Autocorrelation)",
                    description="Periodicity is estimated from normalized autocorrelation peak values.",
                    measurements=lines,
                    reference=f"high > {high}, very_high > {very_high}",
                    observation="One or more channels show high periodicity relative to reference thresholds.",
                    possible_indication="High periodicity can be consistent with highly regular or synthetic patterns; further checks are needed to rule out natural periodic sources (e.g., sustained tones)."
                )

        elif mname == "pulse_detection":
            lines = []
            flagged = False
            for ch, data in meas.items():
                if not isinstance(data, dict):
                    continue
                num = data.get("num_pulses")
                reg = data.get("regularity_score")
                if num is None:
                    continue
                lines.append(f"{ch}: num_pulses={num}, regularity_score={format_value(reg)}")
                if isinstance(reg, (int, float)) and reg >= 0.9 and isinstance(num, int) and num >= 10:
                    flagged = True

            if flagged:
                add_obs(
                    category="Regular Pulse Pattern",
                    description="Pulse detection identifies discrete impulse-like events in the signal.",
                    measurements=lines,
                    reference="high regularity (>0.9) with many pulses suggests systematic events",
                    observation="At least one channel shows highly regular pulse patterns.",
                    possible_indication="Regular pulses can be consistent with clock signals or discrete state transitions; verify temporal context and modulation patterns."
                )

    # SPECTRAL
    for method in iter_methods("spectral"):
        mname = method.get("method", "")
        meas = method.get("measurements", {})

        if mname == "harmonic_analysis":
            ref = REFERENCE_THRESHOLDS.get("harmonicity_score", {})
            harmonic = ref.get("harmonic")
            strong = ref.get("strongly_harmonic")

            lines = []
            flagged = False

            for ch, data in meas.items():
                if not isinstance(data, dict):
                    continue
                hs = data.get("harmonicity_score")
                ff = data.get("fundamental_frequency")
                if hs is None:
                    continue
                lines.append(f"{ch}: harmonicity_score={format_value(hs)}, fundamental_frequency={format_value(ff)} Hz")
                if isinstance(hs, (int, float)):
                    if strong is not None and hs >= strong:
                        flagged = True
                    elif harmonic is not None and hs >= harmonic:
                        flagged = True

            if flagged:
                add_obs(
                    category="Harmonic Structure",
                    description="Harmonicity reflects how much energy aligns with integer multiples of a fundamental frequency.",
                    measurements=lines,
                    reference=f"harmonic > {harmonic}, strongly_harmonic > {strong}",
                    observation="One or more channels show strong harmonic structure relative to reference thresholds.",
                    possible_indication="Strong harmonicity can be consistent with tonal carriers or synthetic sources; verify with tonality/flatness and time-frequency stability."
                )

        elif mname == "spectral_flatness":
            ref = REFERENCE_THRESHOLDS.get("tonality", {})
            tonal = ref.get("tonal")
            highly = ref.get("highly_tonal")

            lines = []
            flagged = False

            for ch, data in meas.items():
                if not isinstance(data, dict):
                    continue
                t = data.get("tonality")
                sf = data.get("spectral_flatness")
                if t is None:
                    continue
                lines.append(f"{ch}: tonality={format_value(t)}, spectral_flatness={format_value(sf)}")
                if isinstance(t, (int, float)):
                    if highly is not None and t >= highly:
                        flagged = True
                    elif tonal is not None and t >= tonal:
                        flagged = True

            if flagged:
                add_obs(
                    category="Tonality vs Broadband Noise",
                    description="Tonality (1 - spectral_flatness) indicates whether the spectrum is more tonal or noise-like.",
                    measurements=lines,
                    reference=f"tonal > {tonal}, highly_tonal > {highly}",
                    observation="One or more channels show high tonality relative to reference thresholds.",
                    possible_indication="High tonality can be consistent with discrete carriers or synthetic tones; check for modulation or discrete state changes to assess data-bearing hypotheses."
                )

        elif mname == "spectral_bandwidth":
            ref = REFERENCE_THRESHOLDS.get("spectral_bandwidth", {})
            narrow = ref.get("narrow")
            
            lines = []
            flagged = False
            for ch, data in meas.items():
                if not isinstance(data, dict):
                    continue
                bw = data.get("spectral_bandwidth")
                if bw is None:
                    continue
                lines.append(f"{ch}: spectral_bandwidth={format_value(bw)} Hz")
                if isinstance(bw, (int, float)) and narrow is not None and bw < narrow:
                    flagged = True

            if flagged:
                add_obs(
                    category="Narrow Spectral Bandwidth",
                    description="Spectral bandwidth measures the concentration of spectral energy.",
                    measurements=lines,
                    reference=f"narrow < {narrow} Hz",
                    observation="At least one channel shows narrow spectral bandwidth.",
                    possible_indication="Narrow bandwidth can indicate concentrated carrier frequency; typical of synthesized or modulated signals."
                )

    # TIME-FREQUENCY
    for method in iter_methods("time_frequency"):
        mname = method.get("method", "")
        meas = method.get("measurements", {})

        if mname == "stft":
            lines = []
            flagged = False
            for ch, data in meas.items():
                if not isinstance(data, dict):
                    continue
                ts = data.get("temporal_stability")
                flux = data.get("spectral_flux_mean")
                if ts is None:
                    continue
                lines.append(f"{ch}: temporal_stability={format_value(ts)}, spectral_flux_mean={format_value(flux)}")
                if isinstance(ts, (int, float)) and ts >= 0.8:
                    flagged = True

            if flagged:
                add_obs(
                    category="Time-Frequency Stability (STFT)",
                    description="STFT-derived metrics can indicate how stable spectral content remains over time.",
                    measurements=lines,
                    reference="high temporal_stability suggests low variation across frames",
                    observation="At least one channel shows high time-frequency stability.",
                    possible_indication="Unusually stable spectral content can be consistent with engineered carriers; validate against natural sustained tones and check modulation signatures."
                )

        elif mname == "band_stability":
            lines = []
            flagged = False
            for ch, data in meas.items():
                if not isinstance(data, dict):
                    continue
                # data is actually a dict of bands
                for band_name, band_data in data.items():
                    if isinstance(band_data, dict):
                        stab = band_data.get("stability_score")
                        if isinstance(stab, (int, float)) and stab >= 0.9:
                            lines.append(f"{ch}/{band_name}: stability_score={format_value(stab)}")
                            flagged = True

            if flagged:
                add_obs(
                    category="High Band Stability",
                    description="Band stability measures how constant energy remains in specific frequency bands over time.",
                    measurements=lines,
                    reference="stability_score > 0.9 indicates very stable energy",
                    observation="One or more frequency bands show very high stability over time.",
                    possible_indication="High band stability can indicate sustained carrier or tonal component; verify with harmonic and modulation analysis."
                )

    # MODULATION
    for method in iter_methods("modulation"):
        mname = method.get("method", "")
        meas = method.get("measurements", {})

        if mname == "am_detection":
            ref = REFERENCE_THRESHOLDS.get("modulation_index", {})
            moderate = ref.get("moderate")
            high = ref.get("high")

            lines = []
            flagged = False
            for ch, data in meas.items():
                if not isinstance(data, dict):
                    continue
                md = data.get("modulation_detected")
                mi = data.get("modulation_index")
                if md is None and mi is None:
                    continue
                lines.append(f"{ch}: modulation_detected={md}, modulation_index={format_value(mi) if mi is not None else 'N/A'}")
                if md is True:
                    flagged = True
                if isinstance(mi, (int, float)) and (
                    (high is not None and mi >= high) or (moderate is not None and mi >= moderate)
                ):
                    flagged = True

            if flagged:
                add_obs(
                    category="Amplitude Modulation Indicators (AM)",
                    description="AM detection metrics summarize whether the amplitude envelope exhibits structured modulation.",
                    measurements=lines,
                    reference=f"moderate >= {moderate}, high >= {high}",
                    observation="AM-related indicators exceed moderate thresholds or are explicitly detected on at least one channel.",
                    possible_indication="Consistent AM patterns can be compatible with envelope-based encoding hypotheses; verify with time-frequency and periodicity context."
                )

        elif mname == "fm_detection":
            lines = []
            flagged = False
            for ch, data in meas.items():
                if not isinstance(data, dict):
                    continue
                fm_det = data.get("fm_detected")
                freq_dev = data.get("frequency_deviation")
                if fm_det is True and freq_dev is not None:
                    lines.append(f"{ch}: fm_detected={fm_det}, frequency_deviation={format_value(freq_dev)} Hz")
                    flagged = True

            if flagged:
                add_obs(
                    category="Frequency Modulation Detected (FM)",
                    description="FM detection identifies significant variations in instantaneous frequency.",
                    measurements=lines,
                    reference="fm_detected=True indicates non-trivial frequency modulation",
                    observation="At least one channel shows frequency modulation.",
                    possible_indication="FM can be consistent with FSK or frequency-based encoding; examine STFT for discrete frequency states."
                )

        elif mname == "phase_analysis":
            ref = REFERENCE_THRESHOLDS.get("phase_coherence", {})
            low = ref.get("low")
            moderate = ref.get("moderate")

            lines = []
            flagged = False
            for ch, data in meas.items():
                if not isinstance(data, dict):
                    continue
                pc = data.get("phase_coherence")
                jumps = data.get("num_phase_jumps")
                if pc is None and jumps is None:
                    continue
                lines.append(f"{ch}: phase_coherence={format_value(pc) if pc is not None else 'N/A'}, num_phase_jumps={format_value(jumps) if jumps is not None else 'N/A'}")
                if isinstance(jumps, int) and jumps >= 100:
                    flagged = True
                if isinstance(pc, (int, float)) and low is not None and pc <= low:
                    flagged = True
                if isinstance(pc, (int, float)) and moderate is not None and pc <= moderate and isinstance(jumps, int) and jumps > 0:
                    flagged = True

            if flagged:
                add_obs(
                    category="Phase Discontinuities / Coherence",
                    description="Phase analysis can reveal discrete phase jumps and coherence changes.",
                    measurements=lines,
                    reference=f"low coherence < {low}, moderate < {moderate}; many jumps can suggest discrete switching",
                    observation="At least one channel shows low/moderate phase coherence and/or numerous phase jumps.",
                    possible_indication="This can be compatible with phase-based switching hypotheses (e.g., PSK-like behavior), but requires corroboration from other indicators."
                )

    # INFORMATION
    for method in iter_methods("information"):
        mname = method.get("method", "")
        meas = method.get("measurements", {})

        if mname == "shannon_entropy":
            ref = REFERENCE_THRESHOLDS.get("shannon_entropy", {})
            low = ref.get("low")
            
            lines = []
            flagged = False
            for ch, data in meas.items():
                if not isinstance(data, dict):
                    continue
                ent = data.get("entropy")
                if ent is None:
                    continue
                lines.append(f"{ch}: entropy={format_value(ent)} bits")
                if isinstance(ent, (int, float)) and low is not None and ent < low:
                    flagged = True

            if flagged:
                add_obs(
                    category="Low Information Entropy",
                    description="Shannon entropy measures the unpredictability/randomness of the signal.",
                    measurements=lines,
                    reference=f"low entropy < {low} bits indicates high structure/predictability",
                    observation="At least one channel shows low entropy relative to reference.",
                    possible_indication="Low entropy suggests high structure or repetition; can be consistent with encoded data or synthetic patterns."
                )

        elif mname == "compression_ratio":
            ref = REFERENCE_THRESHOLDS.get("compression_ratio", {})
            high_comp = ref.get("high_compressibility")
            
            lines = []
            flagged = False
            for ch, data in meas.items():
                if not isinstance(data, dict):
                    continue
                ratio = data.get("compression_ratio")
                if ratio is None:
                    continue
                lines.append(f"{ch}: compression_ratio={format_value(ratio)}")
                if isinstance(ratio, (int, float)) and high_comp is not None and ratio < high_comp:
                    flagged = True

            if flagged:
                add_obs(
                    category="High Compressibility",
                    description="Compression ratio indicates how much redundancy/structure exists in the signal.",
                    measurements=lines,
                    reference=f"high compressibility < {high_comp} (lower = more compressible)",
                    observation="At least one channel shows high compressibility.",
                    possible_indication="High compressibility suggests redundant structure; natural audio typically compresses less efficiently than structured data."
                )

    # INTER-CHANNEL
    for method in iter_methods("inter_channel"):
        mname = method.get("method", "")
        meas = method.get("measurements", {})

        if mname == "lr_difference":
            lines = []
            flagged = False
            for key, data in meas.items():
                if not isinstance(data, dict):
                    continue
                unique = data.get("contains_unique_info")
                ratio = data.get("energy_ratio")
                if unique is True:
                    lines.append(f"{key}: contains_unique_info=True, energy_ratio={format_value(ratio)}")
                    flagged = True

            if flagged:
                add_obs(
                    category="L-R Stereo Field Contains Unique Information",
                    description="L-R difference analysis reveals information not present in left or right channels alone.",
                    measurements=lines,
                    reference="contains_unique_info=True indicates non-redundant stereo content",
                    observation="Stereo difference channel contains unique information.",
                    possible_indication="Unique L-R content can indicate stereo-encoded data or spatial modulation; examine L-R spectrum and phase relationships."
                )

    # STEGANOGRAPHY
    for method in iter_methods("steganography"):
        mname = method.get("method", "")
        meas = method.get("measurements", {})

        if mname == "lsb_analysis":
            lines = []
            flagged = False
            for ch, data in meas.items():
                if not isinstance(data, dict):
                    continue
                lsb_ent = data.get("lsb_entropy")
                chi = data.get("chi_square_stat")
                if lsb_ent is not None and isinstance(lsb_ent, (int, float)) and lsb_ent > 0.9:
                    lines.append(f"{ch}: lsb_entropy={format_value(lsb_ent)}, chi_square={format_value(chi)}")
                    flagged = True

            if flagged:
                add_obs(
                    category="LSB Anomaly Detected",
                    description="LSB analysis examines the least significant bits for non-random patterns.",
                    measurements=lines,
                    reference="high LSB entropy (>0.9) can indicate data in lower bits",
                    observation="At least one channel shows high LSB entropy.",
                    possible_indication="LSB anomalies can be consistent with steganographic encoding in uncompressed audio; verify with other steganography tests."
                )

    return observations


# ---------------------------------------------------------------------
# Report 1: Measurement Summary
# ---------------------------------------------------------------------
def generate_measurement_summary_report(results: dict) -> str:
    lines: List[str] = []
    lines += _header_lines(results, "Audio Analysis Report - Measurement Summary")
    lines += _file_information_lines(results)
    lines += _preprocessing_lines(results)

    lines.append("## Measurement Summary")
    lines.append("")
    lines.append("This report provides key measured values across all channels.")
    lines.append("Reference thresholds are provided for context only.")
    lines.append("")

    key_metrics = extract_key_metrics(results)
    if not key_metrics:
        lines.append("_No key metrics found in results.json._")
        lines.append("")
        return "\n".join(lines)

    for metric in key_metrics:
        lines.append(f"### {metric['name']}")
        lines.append("")
        lines.append("**Measured values:**")
        lines.append("")
        for channel, value in metric.get('values', {}).items():
            lines.append(f"- {channel}: {format_value(value)}")

        if 'reference' in metric:
            lines.append("")
            lines.append(f"**Reference thresholds:** {metric['reference']}")

        if 'unit' in metric:
            lines.append(f"**Unit:** {metric['unit']}")

        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------
# Report 2: Appendices A + B
# ---------------------------------------------------------------------
def generate_appendices_ab_report(results: dict) -> str:
    lines: List[str] = []
    lines += _header_lines(results, "Audio Analysis - Appendices (A & B)")
    lines.append("This document is a reference companion to the analysis outputs.")
    lines.append("It is not used for automated classification.")
    lines.append("")

    # Appendix A
    lines.append("## Appendix A: Reference Thresholds")
    lines.append("")
    lines.append("Thresholds are provided as contextual reference values from signal processing literature.")
    lines.append("They are not used for automated classification.")
    lines.append("")

    for metric, thresholds in REFERENCE_THRESHOLDS.items():
        lines.append(f"### {metric}")
        lines.append("")
        note = thresholds.get('note')
        if note:
            lines.append(f"*Note:* {note}")
            lines.append("")

        lines.append("| Level | Value |")
        lines.append("|------:|:------|")
        for level, value in thresholds.items():
            if level == 'note':
                continue
            lines.append(f"| {level} | {value} |")
        lines.append("")

    # Appendix B
    lines.append("## Appendix B: Interpretation Guide (Context Only)")
    lines.append("")
    lines.append("This section provides general context to assist human interpretation of measured values.")
    lines.append("It does not constitute automated classification or conclusions.")
    lines.append("")

    lines.append("### Natural vs Artificial Signal Characteristics")
    lines.append("")
    lines.append("**Artificial signals** (designed, synthesized, or encoded) typically exhibit:")
    lines.append("- High periodicity (e.g., autocorrelation > 0.9): exact repetition of patterns")
    lines.append("- Strong harmonic structure (e.g., harmonicity > 0.9): integer frequency ratios")
    lines.append("- High tonality (> 0.9): discrete components, not broadband")
    lines.append("- Temporal stability: constant spectral content over time")
    lines.append("- Low entropy/complexity: more predictable structure")
    lines.append("- High compressibility: structured/redundant data")
    lines.append("")
    lines.append("**Natural signals** (speech, music, environmental sounds) typically exhibit:")
    lines.append("- Moderate periodicity (0.3–0.7): repetition with variation")
    lines.append("- Variable harmonic content: changes over time")
    lines.append("- Mixed tonality (0.4–0.8): tonal + noise components")
    lines.append("- Temporal variation: evolving spectral content")
    lines.append("- Higher entropy/complexity: less predictable")
    lines.append("- Lower compressibility: less structured")
    lines.append("")

    lines.append("### Indicators of Encoded Data (Examples)")
    lines.append("")
    lines.append("These indicators are non-definitive; they suggest hypotheses worth exploring.")
    lines.append("")
    lines.append("**AM (Amplitude Modulation):** modulation index elevated, discrete modulation components, stable carrier")
    lines.append("**FM/FSK (Frequency behavior):** non-trivial deviation, discrete states, switching patterns visible in STFT")
    lines.append("**PSK (Phase behavior):** many phase jumps with reduced coherence, systematic transitions")
    lines.append("**Stereo-field:** non-redundant L-R content, systematic phase/time relationships")
    lines.append("**Information theory:** low entropy, high compressibility indicate structure/redundancy")
    lines.append("**Steganography:** LSB anomalies, quantization noise patterns, signal residuals")
    lines.append("")

    lines.append("### Analysis Strategy (Practical Checklist)")
    lines.append("")
    lines.append("1. Check periodicity/harmonicity/tonality")
    lines.append("2. Inspect time-frequency stability (STFT/bands)")
    lines.append("3. Check modulation family indicators (AM/FM/phase)")
    lines.append("4. Compare channels (correlation, differences, delays)")
    lines.append("5. Examine information-theoretic measures (entropy, compression)")
    lines.append("6. Look for steganographic indicators if applicable")
    lines.append("7. Prefer converging evidence over single metrics")
    lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------
# Report 3: Funnel Hypothesis (built from observations)
# ---------------------------------------------------------------------
def _funnel_stage_for_observation(category: str) -> str:
    c = (category or "").lower()
    if any(k in c for k in ["periodicity", "harmonic", "tonality", "stability", "bandwidth", "pulse"]):
        return "Stage 1 - Natural vs Artificial Indicators"
    if any(k in c for k in ["entropy", "compression", "complexity", "residual", "quantization", "lsb", "stegan"]):
        return "Stage 2 - Data-Bearing Likelihood Indicators"
    if any(k in c for k in ["modulation", "fm", "am", "phase", "correlation", "stereo", "delay", "lr"]):
        return "Stage 3 - Plausible Encoding Families"
    return "Other / Unmapped"


def generate_funnel_report(results: dict) -> str:
    lines: List[str] = []
    lines += _header_lines(results, "Audio Analysis - Funnel (Hypothesis Only)")

    lines.append("## Purpose")
    lines.append("")
    lines.append("This document organizes factual observations into a funnel-like reasoning flow.")
    lines.append("It helps a human analyst decide which hypotheses are worth exploring next.")
    lines.append("")
    lines.append("### Important disclaimers")
    lines.append("")
    lines.append("- The funnel does **not** prove the presence of hidden information.")
    lines.append("- It does **not** provide automated classification.")
    lines.append("- It highlights **relationships** between measured values and documented patterns only.")
    lines.append("- Converging evidence can increase confidence, but does not guarantee conclusions.")
    lines.append("")

    observations = generate_observations(results)

    lines.append("## Observations (Grouped by Funnel Stage)")
    lines.append("")
    if not observations:
        lines.append("_No notable observations triggered by the current ruleset._")
        lines.append("")
        return "\n".join(lines)

    grouped: Dict[str, List[Dict[str, Any]]] = {}
    for obs in observations:
        stage = _funnel_stage_for_observation(obs.get('category', ''))
        grouped.setdefault(stage, []).append(obs)

    stage_order = [
        "Stage 1 - Natural vs Artificial Indicators",
        "Stage 2 - Data-Bearing Likelihood Indicators",
        "Stage 3 - Plausible Encoding Families",
        "Other / Unmapped",
    ]

    for stage in stage_order:
        if stage not in grouped:
            continue
        lines.append(f"### {stage}")
        lines.append("")
        for obs in grouped[stage]:
            lines.append(f"#### {obs.get('category', 'Observation')}")
            lines.append("")
            if obs.get('description'):
                lines.append(obs['description'])
                lines.append("")
            if obs.get('measurements'):
                lines.append("**Measured values:**")
                lines.append("")
                for m in obs['measurements']:
                    lines.append(f"- {m}")
                lines.append("")
            if obs.get('reference'):
                lines.append(f"**Context reference:** {obs['reference']}")
                lines.append("")
            if obs.get('observation'):
                lines.append(f"**Factual observation:** {obs['observation']}")
                lines.append("")
            if obs.get('possible_indication'):
                lines.append("**Hypothesis worth exploring (non-conclusive):**")
                lines.append("")
                lines.append(f"- {obs['possible_indication']}")
                lines.append("")
        lines.append("")

    lines.append("## Suggested Next Steps (Procedural, Not Interpretative)")
    lines.append("")
    lines.append("- If Stage 1 flags artificiality indicators, inspect Stage 2 and Stage 3 items with plots/time-frequency views.")
    lines.append("- If Stage 3 suggests a modulation family, examine spectrograms for discrete states or stable carriers.")
    lines.append("- If Stage 2 shows information-theoretic anomalies, cross-check with steganography and modulation tests.")
    lines.append("- Prefer multiple converging indicators over any single metric.")
    lines.append("")
    lines.append("**Reminder:** These are workflow suggestions, not conclusions.")
    lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------
# Main: write 3 outputs
# ---------------------------------------------------------------------
def main():
    import sys

    if len(sys.argv) < 2:
        print("Usage: python Generate_Report.py results.json")
        print("   Or: python Generate_Report.py output_dir")
        sys.exit(1)

    input_path = Path(sys.argv[1])

    if input_path.is_dir():
        results_file = input_path / "results.json"
    else:
        results_file = input_path

    if not results_file.exists():
        print(f"Error: File not found: {results_file}")
        sys.exit(1)

    print(f"Loading: {results_file}")
    results = load_results(results_file)

    out_dir = results_file.parent

    print("Generating reports...")
    r1 = generate_measurement_summary_report(results)
    r2 = generate_appendices_ab_report(results)
    r3 = generate_funnel_report(results)

    f1 = out_dir / "01_MEASUREMENT_SUMMARY.md"
    f2 = out_dir / "02_APPENDICES_AB.md"
    f3 = out_dir / "03_FUNNEL_HYPOTHESIS.md"

    f1.write_text(r1, encoding="utf-8")
    f2.write_text(r2, encoding="utf-8")
    f3.write_text(r3, encoding="utf-8")

    print(f"Wrote: {f1}")
    print(f"Wrote: {f2}")
    print(f"Wrote: {f3}")
    print("\n✅ Report generation complete!")


if __name__ == "__main__":
    main()