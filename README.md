## A Note on This Project's Development

Yes, this project was built with extensive assistance from Claude AI to compensate for the author's chronic lack of development skills. 
Even worse, Claude and the author share an equal talent for wild hallucinations, which is probably why they work so well together.
If you think this makes the author a monster, a fraud, an illusionist, or a coding muggle, feel free to move along.
However, if you're willing to give this project the benefit of curiosity, you'll have the opportunity to judge its relevance for yourself. 
Who knows, you might even want to contribute.

# Small Audio Toolkit

A configurable, audio analysis toolkit designed to detect non-trivial informational structures in audio files through objective measurements.

## Overview

This toolkit provides a reproducible framework for analyzing audio signals using proven methods. It is particularly suited for exploring intentionally designed audio signals (game design, ARGs, steganography) without automatic semantic interpretation.

## Key Principles

- **Configuration-driven**: All analyses are declared in an external configuration file
- **No interpretation**: The system only extracts, measures, compares and reports measurable properties
- **Multi-channel preservation**: Spatial and inter-channel information is preserved throughout analysis
- **Reproducibility**: All parameters and results are fully traceable and auditable
- **Extensibility**: New analysis methods can be added without modifying the core engine

## Features

- Multi-channel audio support (mono, stereo, multi-channel)
- 9 categories of analyses:
  - Preprocessing
  - Temporal analysis
  - Frequency analysis
  - Time-frequency analysis
  - Modulation analysis
  - Information theory analysis
  - Inter-channel analysis
  - Steganography exploration
  - Meta-analysis
- Configurable preprocessing pipeline
- Optional visualization generation
- JSON export with full parameter traceability

## Installation

```bash
cd small-audio-toolkit
pip install -r requirements.txt
```

## Usage

```bash
python run_analysis.py audio_file.ext --config examples/config_example.yaml --output outputs/
```

## Configuration

All analyses are controlled via a YAML configuration file. See `examples/config_example.yaml` and `docs/configuration.md` for details.

## Documentation

Documentation is available in the `docs/` directory:

- `architecture.md` - Software architecture overview
- `configuration.md` - Configuration file format
- `analyses.md` - Complete catalog of available analyses
- `extending.md` - Guide for adding new analysis methods

## Requirements

- Python 3.10+
- NumPy
- SciPy
- librosa
- soundfile
- PyYAML

See `requirements.txt` for complete list.

## License

MIT License - see `LICENSE` file.

## Context

This toolkit was developed for analyzing audio files from games like Elite Dangerous, where intentional informational structures may be embedded in audio signals.
