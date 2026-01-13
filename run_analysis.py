"""
Complete audio analysis script - runs ALL available analysis methods.

Usage:
    python run_analysis.py <audio_file>
    
Example:
    python run_analysis.py lsig.flac
"""

import sys
from pathlib import Path

# Import configuration loader and runner
from audio_toolkit.config.loader import ConfigLoader
from audio_toolkit.engine.runner import AnalysisRunner
from audio_toolkit.utils.logging import setup_logging

# Import ALL analysis modules (required to register methods)
import audio_toolkit.analyses.temporal
import audio_toolkit.analyses.spectral
import audio_toolkit.analyses.time_frequency
import audio_toolkit.analyses.modulation
import audio_toolkit.analyses.inter_channel
import audio_toolkit.analyses.information
import audio_toolkit.analyses.steganography
import audio_toolkit.analyses.meta_analysis


def main():
    # Setup logging
    setup_logging(verbose=True)
    
    # Check arguments
    if len(sys.argv) < 2:
        print("Usage: python run_analysis.py <audio_file>")
        print("\nExample:")
        print("  python run_analysis.py lsig.flac")
        sys.exit(1)
    
    # Get audio file path
    audio_file = Path(sys.argv[1])
    
    if not audio_file.exists():
        print(f"Error: Audio file not found: {audio_file}")
        sys.exit(1)
    
    print(f"\n{'='*60}")
    print(f"Audio Analysis Tool - COMPLETE ANALYSIS")
    print(f"{'='*60}")
    print(f"\nAudio file: {audio_file}")
    
    # Load configuration
    config_path = Path(__file__).parent / "config_complete.yaml"
    
    if not config_path.exists():
        print(f"Error: Configuration file not found: {config_path}")
        print("Please create config_complete.yaml in the project root.")
        sys.exit(1)
    
    print(f"Config file: {config_path}")
    
    config = ConfigLoader.load(config_path)
    print("Configuration loaded successfully")
    
    # Create output directory
    output_dir = Path("results") / audio_file.stem
    print(f"Output directory: {output_dir}")
    
    # Create and run analysis pipeline
    print(f"\n{'='*60}")
    print("Starting COMPLETE analysis...")
    print(f"{'='*60}\n")
    
    runner = AnalysisRunner(config)
    runner.run(
        audio_path=audio_file,
        output_path=output_dir
    )
    
    # Summary
    print(f"\n{'='*60}")
    print("Analysis complete!")
    print(f"{'='*60}\n")
    print(f"Results saved to: {output_dir}/")
    print(f"  - results.json : All measurements")
    print(f"  - config_used.json : Configuration used")
    print(f"  - visualizations/ : Plots")
    print("\nTo generate report:")
    print(f"  python generate_report.py {output_dir}")


if __name__ == "__main__":
    main()