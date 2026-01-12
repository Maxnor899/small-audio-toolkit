"""
Generate objective analysis report from results.json

This script produces a factual report of measured values without interpretation.
All thresholds are provided as reference values from signal processing literature.
"""

import json
from pathlib import Path
from typing import Dict, Any, List


# Reference thresholds from signal processing literature
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
    }
}

# Key metrics to observe for each method
KEY_METRICS_PER_METHOD = {
    'envelope': ['envelope_mean', 'envelope_max', 'envelope_std'],
    'autocorrelation': ['periodicity_score', 'first_peak_lag', 'num_peaks'],
    'pulse_detection': ['num_pulses', 'interval_mean', 'regularity_score'],
    'fft_global': ['peak_frequency', 'peak_magnitude', 'spectral_energy'],
    'peak_detection': ['num_peaks', 'dominant_frequency', 'frequency_spread'],
    'harmonic_analysis': ['fundamental_frequency', 'harmonicity_score', 'harmonics_detected'],
    'spectral_centroid': ['spectral_centroid', 'normalized_centroid'],
    'spectral_flatness': ['spectral_flatness', 'tonality'],
    'stft': ['temporal_stability', 'dominant_freq_mean', 'spectral_flux_mean'],
    'band_stability': ['stability_score', 'mean_energy', 'variation_coefficient'],
    'wavelet': ['mean_magnitude', 'max_magnitude', 'energy_concentration'],
    'am_detection': ['modulation_detected', 'modulation_index', 'modulation_depth'],
    'fm_detection': ['fm_detected', 'frequency_deviation', 'carrier_frequency_mean'],
    'phase_analysis': ['phase_coherence', 'num_phase_jumps', 'phase_std'],
    'modulation_index': ['modulation_index', 'modulation_depth', 'peak_to_average_ratio'],
    'cross_correlation': ['max_correlation', 'peak_lag', 'correlation_at_zero'],
    'lr_difference': ['energy_ratio', 'difference_peak_freq', 'contains_unique_info'],
    'phase_difference': ['phase_diff_mean', 'phase_coherence', 'in_phase'],
    'time_delay': ['delay_samples', 'delay_ms', 'is_synchronized']
}


def load_results(results_path: Path) -> dict:
    """Load results.json file."""
    with open(results_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def format_value(value: Any, precision: int = 3) -> str:
    """Format numeric value for display."""
    if isinstance(value, bool):
        return str(value)
    elif isinstance(value, float):
        if abs(value) > 1e6 or abs(value) < 1e-3:
            return f"{value:.{precision}e}"
        else:
            return f"{value:.{precision}f}"
    elif isinstance(value, int):
        return str(value)
    else:
        return str(value)


def generate_report(results: dict) -> str:
    """Generate objective markdown report from results."""
    
    lines = []
    
    # Header
    lines.append("# Audio Analysis Report")
    lines.append("")
    lines.append(f"**Analysis timestamp:** {results['timestamp']}")
    lines.append(f"**Input file:** {results['metadata']['audio_file']}")
    lines.append("")
    
    # Audio file information
    audio_info = results['metadata']['audio_info']
    lines.append("## File Information")
    lines.append("")
    lines.append(f"- Duration: {audio_info['duration']:.2f} seconds")
    lines.append(f"- Sample rate: {audio_info['sample_rate']} Hz")
    lines.append(f"- Channels: {audio_info['channels']}")
    lines.append(f"- Format: {audio_info['format']} / {audio_info['subtype']}")
    lines.append(f"- Total frames: {audio_info['frames']}")
    lines.append("")
    
    # Preprocessing info
    if 'preprocessing' in results['metadata']:
        lines.append("## Preprocessing Applied")
        lines.append("")
        preproc = results['metadata']['preprocessing']
        for key, settings in preproc.items():
            if settings.get('enabled', False):
                lines.append(f"### {key}")
                for param, value in settings.items():
                    if param != 'enabled':
                        lines.append(f"- {param}: {value}")
                lines.append("")
    
    # Measurements summary table
    lines.append("## Measurement Summary")
    lines.append("")
    lines.append("This section provides key measured values across all channels.")
    lines.append("Reference thresholds are provided for context only.")
    lines.append("")
    
    # Extract key metrics
    key_metrics = extract_key_metrics(results)
    
    if key_metrics:
        for metric in key_metrics:
            lines.append(f"### {metric['name']}")
            lines.append("")
            lines.append(f"**Measured values:**")
            lines.append("")
            
            for channel, value in metric['values'].items():
                lines.append(f"- {channel}: {format_value(value)}")
            
            if 'reference' in metric:
                lines.append("")
                lines.append(f"**Reference thresholds:** {metric['reference']}")
            
            if 'unit' in metric:
                lines.append(f"**Unit:** {metric['unit']}")
            
            lines.append("")
    
    # Detailed results by category
    lines.append("## Detailed Measurements by Category")
    lines.append("")
    
    for category, methods in results['results'].items():
        lines.append(f"### {category.upper()}")
        lines.append("")
        
        for method in methods:
            method_name = method['method']
            lines.append(f"#### Method: {method_name}")
            lines.append("")
            
            # Key metrics to observe
            if method_name in KEY_METRICS_PER_METHOD:
                lines.append("**Key metrics to observe:**")
                lines.append("")
                key_metrics = KEY_METRICS_PER_METHOD[method_name]
                
                # Extract key metric values from measurements
                key_values_found = False
                for channel, data in method['measurements'].items():
                    if isinstance(data, dict):
                        channel_key_values = {}
                        for key_metric in key_metrics:
                            if key_metric in data:
                                channel_key_values[key_metric] = data[key_metric]
                        
                        if channel_key_values:
                            key_values_found = True
                            lines.append(f"- **{channel}:**")
                            for metric, value in channel_key_values.items():
                                lines.append(f"  - {metric}: {format_value(value)}")
                
                if key_values_found:
                    lines.append("")
            
            # Metrics used
            if method.get('metrics'):
                lines.append("**Parameters:**")
                lines.append("")
                for key, value in method['metrics'].items():
                    lines.append(f"- {key}: {format_value(value)}")
                lines.append("")
            
            # All measurements per channel (collapsed format)
            lines.append("<details>")
            lines.append("<summary><b>All measurements (click to expand)</b></summary>")
            lines.append("")
            
            for channel, data in method['measurements'].items():
                if isinstance(data, dict):
                    lines.append(f"**Channel: {channel}**")
                    lines.append("")
                    
                    # Display as table if many values
                    if len(data) > 5:
                        lines.append("| Metric | Value |")
                        lines.append("|--------|-------|")
                        for key, value in data.items():
                            if not isinstance(value, (list, dict)):
                                lines.append(f"| {key} | {format_value(value)} |")
                        lines.append("")
                    else:
                        for key, value in data.items():
                            if not isinstance(value, (list, dict)):
                                lines.append(f"- {key}: {format_value(value)}")
                        lines.append("")
            
            lines.append("</details>")
            lines.append("")
            lines.append("---")
            lines.append("")
    
    # Reference thresholds appendix
    lines.append("## Appendix A: Reference Thresholds")
    lines.append("")
    lines.append("The following thresholds are provided as reference values from ")
    lines.append("signal processing literature. They are not used for automated ")
    lines.append("classification in this tool.")
    lines.append("")
    
    for metric, thresholds in REFERENCE_THRESHOLDS.items():
        lines.append(f"### {metric}")
        lines.append("")
        note = thresholds.pop('note', None)
        if note:
            lines.append(f"*{note}*")
            lines.append("")
        for level, value in thresholds.items():
            lines.append(f"- {level}: {value}")
        lines.append("")
    
    # Interpretation guide
    lines.append("## Appendix B: Interpretation Guide")
    lines.append("")
    lines.append("This section provides general context from signal processing literature ")
    lines.append("to assist in human interpretation of measured values. It does not ")
    lines.append("constitute automated classification or conclusions.")
    lines.append("")
    
    lines.append("### Characteristics of Artificial vs Natural Signals")
    lines.append("")
    lines.append("**Artificial signals** (designed, synthesized, or encoded) typically exhibit:")
    lines.append("")
    lines.append("- **High periodicity** (autocorrelation > 0.9): Exact repetition of patterns")
    lines.append("- **Strong harmonic structure** (harmonicity > 0.9): Integer frequency ratios")
    lines.append("- **High tonality** (> 0.9): Discrete frequency components, not broadband")
    lines.append("- **Temporal stability**: Constant spectral content over time")
    lines.append("- **Low entropy**: Predictable, compressible structure")
    lines.append("")
    lines.append("**Natural signals** (speech, music, environmental sounds) typically exhibit:")
    lines.append("")
    lines.append("- **Moderate periodicity** (0.3-0.7): Some repetition but with variation")
    lines.append("- **Variable harmonic content**: Changes over time")
    lines.append("- **Mixed tonality** (0.4-0.8): Combination of tonal and noise components")
    lines.append("- **Temporal variation**: Evolving spectral content")
    lines.append("- **Higher entropy**: Less predictable structure")
    lines.append("")
    
    lines.append("### Indicators of Encoded Data")
    lines.append("")
    lines.append("Signals carrying encoded information may show:")
    lines.append("")
    lines.append("**Amplitude Modulation (AM) encoding:**")
    lines.append("- Modulation index > 0.3: Significant amplitude variation")
    lines.append("- Discrete modulation frequencies: Regular envelope patterns")
    lines.append("- Stable carrier frequency: Constant fundamental")
    lines.append("")
    lines.append("**Frequency Modulation (FM) encoding:**")
    lines.append("- Frequency deviation > 10% of carrier: Significant frequency shifts")
    lines.append("- Discrete frequency transitions: Step changes rather than continuous")
    lines.append("- Consistent modulation index: Repeating pattern")
    lines.append("")
    lines.append("**Phase Shift Keying (PSK) encoding:**")
    lines.append("- Numerous phase jumps (> 100): Discrete phase transitions")
    lines.append("- Low phase coherence (< 0.5): Intentional phase discontinuities")
    lines.append("- Regular jump intervals: Systematic timing")
    lines.append("")
    lines.append("**Frequency Shift Keying (FSK) encoding:**")
    lines.append("- Multiple discrete peak frequencies: Fixed set of carriers")
    lines.append("- Rapid frequency switching: Transitions between fixed frequencies")
    lines.append("- Time-frequency patterns: Regular structure in spectrogram")
    lines.append("")
    
    lines.append("### Stereo Field Encoding")
    lines.append("")
    lines.append("Information may be encoded in the spatial field:")
    lines.append("")
    lines.append("**L-R difference channel:**")
    lines.append("- Energy ratio > 0.05: Significant information in difference")
    lines.append("- Different fundamental frequency: Distinct content from L+R")
    lines.append("- Higher frequency content: Often used for data encoding")
    lines.append("")
    lines.append("**Phase relationships:**")
    lines.append("- Out-of-phase content (phase diff ≈ π): Intentional opposition")
    lines.append("- Phase coherence < 0.3: Decorrelated signals")
    lines.append("- Consistent phase differences: Systematic relationship")
    lines.append("")
    lines.append("**Time delays:**")
    lines.append("- Fixed inter-channel delay: Intentional offset")
    lines.append("- Delay > 5 samples: Beyond natural spatial differences")
    lines.append("")
    
    lines.append("### Common Signal Types")
    lines.append("")
    lines.append("**Pure tones:**")
    lines.append("- Periodicity ≈ 1.0, Harmonicity ≈ 0, Tonality ≈ 1.0")
    lines.append("- Single spectral peak, no harmonics")
    lines.append("")
    lines.append("**Harmonic signals (musical notes):**")
    lines.append("- Periodicity > 0.9, Harmonicity > 0.8, Tonality > 0.8")
    lines.append("- Clear fundamental + integer harmonic series")
    lines.append("")
    lines.append("**DTMF tones (phone keys):**")
    lines.append("- Two discrete frequencies, Tonality > 0.95")
    lines.append("- Short duration (50-100ms), rectangular envelope")
    lines.append("")
    lines.append("**White noise:**")
    lines.append("- Periodicity ≈ 0, Flatness ≈ 1.0, Tonality ≈ 0")
    lines.append("- Uniform spectral energy distribution")
    lines.append("")
    lines.append("**Modulated carrier:**")
    lines.append("- High periodicity carrier + modulation in envelope or frequency")
    lines.append("- Stable spectral centroid with envelope variation")
    lines.append("")
    
    lines.append("### Analysis Strategy")
    lines.append("")
    lines.append("When analyzing unknown signals:")
    lines.append("")
    lines.append("1. **Check periodicity and harmonicity**: Indicates natural vs artificial origin")
    lines.append("2. **Examine temporal stability**: Constant vs varying content")
    lines.append("3. **Compare channels**: Look for L-R differences or phase relationships")
    lines.append("4. **Analyze modulation**: Check for AM, FM, or phase modulation")
    lines.append("5. **Inspect time-frequency**: STFT reveals temporal structure")
    lines.append("6. **Look for patterns**: Regular intervals, discrete states, systematic behavior")
    lines.append("")
    lines.append("**Important:** These indicators are not definitive. Context, domain knowledge, ")
    lines.append("and multiple converging measurements are required for reliable interpretation.")
    lines.append("")
    
    # Observations section
    lines.append("## Appendix C: Observations on Measured Values")
    lines.append("")
    lines.append("This section compares measured values from this analysis to the reference ")
    lines.append("thresholds and patterns described in Appendix B. These are factual observations ")
    lines.append("only, not conclusions or automated interpretations.")
    lines.append("")
    lines.append("**Disclaimer:** The observations below are intended to assist human analysis ")
    lines.append("by highlighting relationships between measured values and documented patterns. ")
    lines.append("They do not constitute definitive classification or conclusions.")
    lines.append("")
    
    observations = generate_observations(results)
    
    if observations:
        for obs in observations:
            lines.append(f"### {obs['category']}")
            lines.append("")
            lines.append(obs['description'])
            lines.append("")
            
            if 'measurements' in obs:
                lines.append("**Measured values:**")
                lines.append("")
                for measurement in obs['measurements']:
                    lines.append(f"- {measurement}")
                lines.append("")
            
            if 'reference' in obs:
                lines.append(f"**Reference from Appendix B:** {obs['reference']}")
                lines.append("")
            
            if 'observation' in obs:
                lines.append(f"**Factual observation:** {obs['observation']}")
                lines.append("")
            
            if 'possible_indication' in obs:
                lines.append(f"**Possible indication:** {obs['possible_indication']}")
                lines.append("")
    else:
        lines.append("No significant deviations from typical ranges observed.")
        lines.append("")
    
    lines.append("**Final reminder:** These observations should be interpreted in context with ")
    lines.append("domain knowledge, acquisition conditions, and intended signal use. Multiple ")
    lines.append("converging measurements increase confidence but do not guarantee conclusions.")
    lines.append("")
    
    return "\n".join(lines)


def extract_key_metrics(results: dict) -> List[Dict[str, Any]]:
    """Extract key metrics for summary table."""
    
    metrics = []
    
    # Periodicity score
    periodicity_values = {}
    for method in results['results'].get('temporal', []):
        if method['method'] == 'autocorrelation':
            for channel, data in method['measurements'].items():
                if 'periodicity_score' in data:
                    periodicity_values[channel] = data['periodicity_score']
    
    if periodicity_values:
        ref = REFERENCE_THRESHOLDS['periodicity_score']
        metrics.append({
            'name': 'Periodicity Score (Autocorrelation)',
            'values': periodicity_values,
            'reference': f"high > {ref['high']}, very_high > {ref['very_high']}",
            'unit': 'normalized (0-1)'
        })
    
    # Harmonicity score
    harmonicity_values = {}
    fundamental_values = {}
    for method in results['results'].get('spectral', []):
        if method['method'] == 'harmonic_analysis':
            for channel, data in method['measurements'].items():
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
    for method in results['results'].get('spectral', []):
        if method['method'] == 'spectral_flatness':
            for channel, data in method['measurements'].items():
                if 'tonality' in data:
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
    for method in results['results'].get('modulation', []):
        if method['method'] == 'am_detection':
            for channel, data in method['measurements'].items():
                if 'modulation_index' in data:
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
    for method in results['results'].get('modulation', []):
        if method['method'] == 'phase_analysis':
            for channel, data in method['measurements'].items():
                if 'phase_coherence' in data:
                    phase_coh_values[channel] = data['phase_coherence']
    
    if phase_coh_values:
        ref = REFERENCE_THRESHOLDS['phase_coherence']
        metrics.append({
            'name': 'Phase Coherence',
            'values': phase_coh_values,
            'reference': f"low < {ref['low']}, moderate < {ref['moderate']}, high > {ref['high']}",
            'unit': 'normalized (0-1)'
        })
    
    return metrics


def generate_observations(results: dict) -> List[Dict[str, Any]]:
    """
    Generate factual observations by comparing measured values to reference thresholds.
    Does not make conclusions, only states relationships to documented patterns.
    """
    observations = []
    
    # Observation 1: Periodicity analysis
    periodicity_values = {}
    for method in results['results'].get('temporal', []):
        if method['method'] == 'autocorrelation':
            for channel, data in method['measurements'].items():
                if 'periodicity_score' in data:
                    periodicity_values[channel] = data['periodicity_score']
    
    if periodicity_values:
        high_threshold = REFERENCE_THRESHOLDS['periodicity_score']['high']
        very_high_threshold = REFERENCE_THRESHOLDS['periodicity_score']['very_high']
        
        channels_very_high = [ch for ch, val in periodicity_values.items() if val > very_high_threshold]
        
        if channels_very_high:
            obs = {
                'category': 'Periodicity Score',
                'description': 'Comparison of measured periodicity scores to reference thresholds.',
                'measurements': [f"{ch}: {val:.3f}" for ch, val in periodicity_values.items()],
                'reference': f"Appendix B states: Artificial signals typically exhibit high periodicity (> {high_threshold}), natural signals show moderate periodicity (0.3-0.7)",
                'observation': f"Channels {', '.join(channels_very_high)} exceed very_high threshold ({very_high_threshold})",
                'possible_indication': "Values in range documented for signals with exact pattern repetition (see Appendix B: Artificial signals)"
            }
            observations.append(obs)
    
    # Observation 2: Harmonic structure
    harmonicity_values = {}
    fundamental_values = {}
    for method in results['results'].get('spectral', []):
        if method['method'] == 'harmonic_analysis':
            for channel, data in method['measurements'].items():
                if 'harmonicity_score' in data:
                    harmonicity_values[channel] = data['harmonicity_score']
                if 'fundamental_frequency' in data:
                    fundamental_values[channel] = data['fundamental_frequency']
    
    if harmonicity_values:
        strongly_harmonic_threshold = REFERENCE_THRESHOLDS['harmonicity_score']['strongly_harmonic']
        
        channels_strong = [ch for ch, val in harmonicity_values.items() if val >= strongly_harmonic_threshold]
        
        if channels_strong:
            obs = {
                'category': 'Harmonic Structure',
                'description': 'Comparison of measured harmonicity scores to reference thresholds.',
                'measurements': [f"{ch}: harmonicity={harmonicity_values[ch]:.3f}, fundamental={fundamental_values.get(ch, 'N/A'):.1f} Hz" 
                               for ch in harmonicity_values.keys()],
                'reference': f"Appendix B states: Artificial signals show strong harmonic structure (> {strongly_harmonic_threshold}) with integer frequency ratios",
                'observation': f"Channels {', '.join(channels_strong)} meet or exceed strongly_harmonic threshold ({strongly_harmonic_threshold})"
            }
            
            # Check for different fundamental in difference channel
            if 'difference' in fundamental_values and 'left' in fundamental_values:
                freq_diff = fundamental_values['difference']
                freq_left = fundamental_values['left']
                if abs(freq_diff - freq_left) > 50:  # Significant difference
                    obs['observation'] += f". Note: difference channel has distinct fundamental ({freq_diff:.1f} Hz vs {freq_left:.1f} Hz)"
                    obs['possible_indication'] = "Harmonic structure consistent with artificial signals. Different fundamental in difference channel consistent with stereo field encoding (see Appendix B)"
                else:
                    obs['possible_indication'] = "Values consistent with strongly harmonic signals (see Appendix B: Harmonic signals)"
            
            observations.append(obs)
    
    # Observation 3: Tonality
    tonality_values = {}
    for method in results['results'].get('spectral', []):
        if method['method'] == 'spectral_flatness':
            for channel, data in method['measurements'].items():
                if 'tonality' in data:
                    tonality_values[channel] = data['tonality']
    
    if tonality_values:
        highly_tonal_threshold = REFERENCE_THRESHOLDS['tonality']['highly_tonal']
        
        channels_high_tonal = [ch for ch, val in tonality_values.items() if val > highly_tonal_threshold]
        
        if channels_high_tonal:
            obs = {
                'category': 'Tonality',
                'description': 'Comparison of measured tonality values to reference thresholds.',
                'measurements': [f"{ch}: {val:.3f}" for ch, val in tonality_values.items()],
                'reference': f"Appendix B states: Artificial signals show high tonality (> {highly_tonal_threshold}) with discrete frequency components, natural signals show mixed tonality (0.4-0.8)",
                'observation': f"Channels {', '.join(channels_high_tonal)} exceed highly_tonal threshold ({highly_tonal_threshold})",
                'possible_indication': "Values consistent with signals composed of discrete frequencies rather than broadband noise (see Appendix B)"
            }
            observations.append(obs)
    
    # Observation 4: Modulation detection
    modulation_detected = {}
    for method in results['results'].get('modulation', []):
        if method['method'] == 'am_detection':
            for channel, data in method['measurements'].items():
                if data.get('modulation_detected', False) and data.get('modulation_index', 0) > 0.3:
                    modulation_detected[channel] = {
                        'index': data['modulation_index'],
                        'freq': data.get('dominant_modulation_freq', 0)
                    }
    
    if modulation_detected:
        obs = {
            'category': 'Amplitude Modulation',
            'description': 'Amplitude modulation detected on one or more channels.',
            'measurements': [f"{ch}: modulation_index={info['index']:.3f}, dominant_freq={info['freq']:.2f} Hz" 
                           for ch, info in modulation_detected.items()],
            'reference': "Appendix B states: AM encoding typically shows modulation index > 0.3 with discrete modulation frequencies",
            'observation': f"Modulation detected on channels: {', '.join(modulation_detected.keys())}",
            'possible_indication': "Pattern consistent with intentional amplitude modulation encoding (see Appendix B: AM encoding)"
        }
        observations.append(obs)
    
    # Observation 5: FM detection
    fm_detected = {}
    for method in results['results'].get('modulation', []):
        if method['method'] == 'fm_detection':
            for channel, data in method['measurements'].items():
                if data.get('fm_detected', False):
                    fm_detected[channel] = {
                        'deviation': data.get('frequency_deviation', 0),
                        'carrier': data.get('carrier_frequency_mean', 0)
                    }
    
    if fm_detected:
        obs = {
            'category': 'Frequency Modulation',
            'description': 'Frequency modulation detected on one or more channels.',
            'measurements': [f"{ch}: deviation={info['deviation']:.2f} Hz, carrier={info['carrier']:.1f} Hz" 
                           for ch, info in fm_detected.items()],
            'reference': "Appendix B states: FM encoding typically shows frequency deviation > 10% of carrier",
            'observation': f"FM detected on channels: {', '.join(fm_detected.keys())}"
        }
        
        # Check deviation percentage
        high_deviation_channels = []
        for ch, info in fm_detected.items():
            if info['carrier'] > 0:
                deviation_pct = (info['deviation'] / info['carrier']) * 100
                if deviation_pct > 10:
                    high_deviation_channels.append(f"{ch} ({deviation_pct:.1f}%)")
        
        if high_deviation_channels:
            obs['observation'] += f". Channels with >10% deviation: {', '.join(high_deviation_channels)}"
            obs['possible_indication'] = "Deviation levels consistent with intentional frequency modulation encoding (see Appendix B: FM encoding)"
        
        observations.append(obs)
    
    # Observation 6: Phase analysis
    phase_jumps = {}
    for method in results['results'].get('modulation', []):
        if method['method'] == 'phase_analysis':
            for channel, data in method['measurements'].items():
                if data.get('num_phase_jumps', 0) > 100:
                    phase_jumps[channel] = {
                        'jumps': data['num_phase_jumps'],
                        'coherence': data.get('phase_coherence', 0)
                    }
    
    if phase_jumps:
        obs = {
            'category': 'Phase Discontinuities',
            'description': 'Significant number of phase jumps detected.',
            'measurements': [f"{ch}: {info['jumps']} jumps, coherence={info['coherence']:.3f}" 
                           for ch, info in phase_jumps.items()],
            'reference': "Appendix B states: PSK encoding typically shows numerous phase jumps (> 100) with low coherence (< 0.5)",
            'observation': f"Channels {', '.join(phase_jumps.keys())} show > 100 phase jumps",
            'possible_indication': "Pattern consistent with phase-based encoding or discrete phase transitions (see Appendix B: PSK encoding)"
        }
        observations.append(obs)
    
    # Observation 7: Stereo field encoding (L-R)
    for method in results['results'].get('inter_channel', []):
        if method['method'] == 'lr_difference':
            lr_data = method['measurements'].get('lr_difference', {})
            if lr_data.get('contains_unique_info', False):
                energy_ratio = lr_data.get('energy_ratio', 0)
                diff_freq = lr_data.get('difference_peak_freq', 0)
                
                obs = {
                    'category': 'Stereo Field Analysis (L-R)',
                    'description': 'Significant energy detected in L-R difference channel.',
                    'measurements': [
                        f"Energy ratio (difference/total): {energy_ratio:.3f}",
                        f"Difference peak frequency: {diff_freq:.1f} Hz"
                    ],
                    'reference': "Appendix B states: L-R encoding typically shows energy ratio > 0.05 and different fundamental frequency",
                    'observation': f"L-R channel contains distinct information (energy ratio: {energy_ratio:.3f})",
                    'possible_indication': "Pattern consistent with intentional stereo field encoding with information in difference channel (see Appendix B: Stereo Field Encoding)"
                }
                observations.append(obs)
    
    # Observation 8: Temporal stability
    for method in results['results'].get('time_frequency', []):
        if method['method'] == 'stft':
            stable_channels = []
            for channel, data in method['measurements'].items():
                stability = data.get('temporal_stability', 0)
                if stability > 0.8:
                    stable_channels.append(f"{channel} ({stability:.3f})")
            
            if stable_channels:
                obs = {
                    'category': 'Temporal Stability',
                    'description': 'High temporal stability detected in spectral content.',
                    'measurements': [f"Channels with stability > 0.8: {', '.join(stable_channels)}"],
                    'reference': "Appendix B states: Artificial signals typically show temporal stability with constant spectral content",
                    'observation': "Spectral content remains highly consistent over time",
                    'possible_indication': "Stability level consistent with signals having constant frequency composition (see Appendix B)"
                }
                observations.append(obs)
    
    # Observation 9: Band stability
    for method in results['results'].get('time_frequency', []):
        if method['method'] == 'band_stability':
            stable_bands = {}
            for channel, bands_data in method['measurements'].items():
                if isinstance(bands_data, dict):
                    for band_name, band_metrics in bands_data.items():
                        if isinstance(band_metrics, dict):
                            stability = band_metrics.get('stability_score', 0)
                            if stability > 0.8:
                                if channel not in stable_bands:
                                    stable_bands[channel] = []
                                stable_bands[channel].append(f"{band_name} ({stability:.3f})")
            
            if stable_bands:
                measurements = []
                for channel, bands in stable_bands.items():
                    measurements.append(f"{channel}: {', '.join(bands)}")
                
                obs = {
                    'category': 'Frequency Band Stability',
                    'description': 'Specific frequency bands show high stability over time.',
                    'measurements': measurements,
                    'reference': "Stable frequency bands may indicate carrier frequencies or continuous tones",
                    'observation': "One or more frequency bands maintain constant energy over time",
                    'possible_indication': "Pattern consistent with stable carriers (see Appendix B)"
                }
                observations.append(obs)
    
    # Observation 10: Pulse patterns
    for method in results['results'].get('temporal', []):
        if method['method'] == 'pulse_detection':
            many_pulses = {}
            for channel, data in method['measurements'].items():
                num_pulses = data.get('num_pulses', 0)
                regularity = data.get('regularity_score', 0)
                if num_pulses > 100:
                    many_pulses[channel] = {'count': num_pulses, 'regularity': regularity}
            
            if many_pulses:
                high_reg = [f"{ch} ({info['count']} pulses, reg={info['regularity']:.2f})" 
                           for ch, info in many_pulses.items() if info['regularity'] > 0.7]
                low_reg = [f"{ch} ({info['count']} pulses, reg={info['regularity']:.2f})" 
                          for ch, info in many_pulses.items() if info['regularity'] < 0.3]
                
                if high_reg:
                    obs = {
                        'category': 'Regular Pulse Pattern',
                        'description': 'Regular pulse intervals detected.',
                        'measurements': high_reg,
                        'observation': "Channels show regularly-spaced pulses",
                        'possible_indication': "Pattern consistent with timing signals or data markers"
                    }
                    observations.append(obs)
                
                if low_reg:
                    obs = {
                        'category': 'Irregular Pulse Distribution',
                        'description': 'Many pulses with irregular spacing.',
                        'measurements': low_reg,
                        'observation': "Channels show numerous pulses with irregular timing"
                    }
                    observations.append(obs)
    
    # Observation 11: Spectral peak count
    for method in results['results'].get('spectral', []):
        if method['method'] == 'peak_detection':
            channels_data = {}
            for channel, data in method['measurements'].items():
                num_peaks = data.get('num_peaks', 0)
                if num_peaks > 1000 or num_peaks < 10:
                    channels_data[channel] = num_peaks
            
            many = {ch: n for ch, n in channels_data.items() if n > 1000}
            few = {ch: n for ch, n in channels_data.items() if n < 10}
            
            if many:
                obs = {
                    'category': 'High Spectral Peak Count',
                    'description': 'Numerous discrete frequency peaks detected.',
                    'measurements': [f"{ch}: {n} peaks" for ch, n in many.items()],
                    'reference': "Appendix B states: Multiple peaks may indicate complex harmonics or FSK",
                    'observation': "Channels show > 1000 peaks",
                    'possible_indication': "Pattern consistent with complex multi-carrier or FSK (see Appendix B)"
                }
                observations.append(obs)
            
            if few:
                obs = {
                    'category': 'Low Spectral Peak Count',
                    'description': 'Few discrete frequency peaks detected.',
                    'measurements': [f"{ch}: {n} peaks" for ch, n in few.items()],
                    'reference': "Appendix B states: Few peaks indicate simple tones (pure tones, DTMF)",
                    'observation': "Channels show < 10 peaks",
                    'possible_indication': "Pattern consistent with simple tone signals (see Appendix B)"
                }
                observations.append(obs)
    
    # Observation 12: Cross-correlation
    for method in results['results'].get('inter_channel', []):
        if method['method'] == 'cross_correlation':
            low_corr = []
            
            for pair_key, data in method['measurements'].items():
                if isinstance(data, dict) and 'error' not in data:
                    max_corr = data.get('max_correlation', 0)
                    if max_corr < 0.3:
                        low_corr.append(f"{pair_key} ({max_corr:.3f})")
            
            if low_corr:
                obs = {
                    'category': 'Low Inter-Channel Correlation',
                    'description': 'Weak correlation between channel pairs.',
                    'measurements': low_corr,
                    'reference': "Appendix B states: Low correlation may indicate independent information",
                    'observation': "Channel pairs show weak correlation",
                    'possible_indication': "Channels contain distinct information (see Appendix B: Stereo encoding)"
                }
                observations.append(obs)
    
    # Observation 13: Phase difference
    for method in results['results'].get('inter_channel', []):
        if method['method'] == 'phase_difference':
            out_phase = []
            low_coh = []
            
            for pair_key, data in method['measurements'].items():
                if isinstance(data, dict) and 'error' not in data:
                    if data.get('out_of_phase', False):
                        coherence = data.get('phase_coherence', 0)
                        out_phase.append(f"{pair_key} (coh={coherence:.3f})")
                    if data.get('phase_coherence', 1.0) < 0.3:
                        low_coh.append(f"{pair_key} ({data['phase_coherence']:.3f})")
            
            if out_phase:
                obs = {
                    'category': 'Out-of-Phase Channel Pairs',
                    'description': 'Channel pairs in phase opposition detected.',
                    'measurements': out_phase,
                    'reference': "Appendix B states: Phase opposition indicates intentional encoding",
                    'observation': "Channel pairs show phase opposition",
                    'possible_indication': "Pattern consistent with phase-based stereo encoding (see Appendix B)"
                }
                observations.append(obs)
            
            if low_coh:
                obs = {
                    'category': 'Low Phase Coherence',
                    'description': 'Weak phase relationship between channels.',
                    'measurements': low_coh,
                    'reference': "Appendix B states: Low coherence indicates decorrelated signals",
                    'observation': "Channel pairs show inconsistent phase"
                }
                observations.append(obs)
    
    return observations


def main():
    """Main function."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python generate_report.py results/results.json")
        print("   Or: python generate_report.py results")
        sys.exit(1)
    
    input_path = Path(sys.argv[1])
    
    # If directory provided, look for results.json inside
    if input_path.is_dir():
        results_file = input_path / 'results.json'
    else:
        results_file = input_path
    
    if not results_file.exists():
        print(f"Error: File not found: {results_file}")
        sys.exit(1)
    
    print(f"Loading: {results_file}")
    results = load_results(results_file)
    
    print("Generating objective report...")
    report = generate_report(results)
    
    # Save report
    output_file = results_file.parent / 'RAPPORT.md'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"Report generated: {output_file}")


if __name__ == "__main__":
    main()