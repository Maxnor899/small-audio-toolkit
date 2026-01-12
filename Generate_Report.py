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