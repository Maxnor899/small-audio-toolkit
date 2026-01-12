"""
Command-line interface for the audio analysis toolkit.
"""

import argparse
from pathlib import Path


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Small Audio Toolkit - audio signal analysis"
    )
    
    parser.add_argument(
        "--audio",
        type=Path,
        required=True,
        help="Path to audio file to analyze"
    )
    
    parser.add_argument(
        "--config",
        type=Path,
        required=True,
        help="Path to YAML configuration file"
    )
    
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("outputs/"),
        help="Output directory for results (default: outputs/)"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    
    return parser.parse_args()


def main():
    """Main entry point."""
    args = parse_args()
    
    print(f"Audio file: {args.audio}")
    print(f"Config file: {args.config}")
    print(f"Output directory: {args.output}")
    
    # Implementation will be added in Phase 2
    print("\nToolkit implementation pending...")


if __name__ == "__main__":
    main()
