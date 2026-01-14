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
i hope most questions are answered in this project's wiki, so please read it !

## Key Principles

The tool intentionally separates measurable signal properties from any semantic interpretation.
Documentation follows the same principle.

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
## Report Generation

After running the analysis, generate human-readable reports from the JSON results:

```bash
python Generate_Report.py output_folder/results.json
```

Or simply provide the output directory:

```bash
python Generate_Report.py output_folder
```

### Generated Reports

Three complementary Markdown reports are created:

**1. `01_MEASUREMENT_SUMMARY.md`**
- Key measured values across all channels
- Reference thresholds for context
- No interpretation, just measurements

**2. `02_APPENDICES_AB.md`**
- Appendix A: Reference thresholds from signal processing literature
- Appendix B: Interpretation guide for understanding measured values
- Distinguishing characteristics of natural vs artificial signals

**3. `03_FUNNEL_HYPOTHESIS.md`**
- Factual observations organized by analysis stage
- Stage 1: Natural vs Artificial indicators
- Stage 2: Data-bearing likelihood indicators  
- Stage 3: Plausible encoding families
- Suggested next steps for investigation

### Important Notes

- Reports provide **factual observations** based on measured values
- **No automated classification** or definitive conclusions
- Reference thresholds are for **context only**, not automated decision-making
- Designed to assist human interpretation, not replace it
- Multiple converging indicators are more significant than single metrics

### Example Workflow

```bash
# Run complete analysis
python run_analysis.py audio.flac --config config.yaml --output output_audio

# Generate reports
python Generate_Report.py output_audio

# Review reports
cat output_audio/01_MEASUREMENT_SUMMARY.md
cat output_audio/02_APPENDICES_AB.md  
cat output_audio/03_FUNNEL_HYPOTHESIS.md

# Examine visualizations (if enabled)
ls output_audio/visualizations/
```

The approach whishes to help prioritizing which analysis results deserve closer inspection based on converging evidence across multiple measurement categories.

## Configuration

All analyses are controlled via a YAML configuration file. See `examples/config_example.yaml` and `docs/configuration.md` for details.

## Documentation

This project distinguishes clearly between **effective behavior** and **design intent**.

- `docs/architecture.md`  
  Describes the execution engine, module boundaries, and design constraints.

- `docs/analyses.md`  
  Function-by-function documentation of all analysis methods effectively implemented in the codebase.
  No interpretation or classification is performed.

- `docs/configuration.md`  
  **Contractual configuration reference.**  
  This document defines the exact configuration keys consumed by the engine.
  Any undocumented key is ignored.

- `docs/configuration_schema.md`  
  **Conceptual configuration notes (non-contractual).**  
  Documents experimental ideas, planned extensions, and design considerations.
  Options listed here have no effect unless explicitly implemented.


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
