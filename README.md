## A Note on This Project's Development

Yes, this project was built with extensive assistance from AI to compensate for the author's chronic lack of development skills. 
Even worse, AI and the author share an equal talent for wild hallucinations, which is probably why they work so well together.
If you think this makes the author a monster, a fraud, an illusionist, or a coding muggle, feel free to move along.
However, if you're willing to give this project the benefit of curiosity, you'll have the opportunity to judge its relevance for yourself. 
Who knows, you might even want to contribute.

**most questions (hopefully) are answered in the documentation and in the wiki, please read it !**

# Small Audio Tool

Small Audio Tool is a Python-based audio analysis toolkit designed to explore
**structural properties of audio signals** using a broad set of classical
digital signal processing (DSP) techniques.

The tool focuses on **measurement and observation**, not interpretation or classification.

## What this project does

Small Audio Tool analyzes audio files and produces:

- numerical measurements,
- visualizations,
- and structured reports,

covering multiple analytical domains, including:

- temporal analysis,
- spectral analysis,
- time–frequency representations,
- modulation-related measurements,
- information-theoretic metrics,
- inter-channel relationships (including difference channels),
- residual and quantization-related statistics.

All analyses are configuration-driven and reproducible.

## What this project does *not* do

This tool does **not**:

- detect messages,
- infer intent,
- classify signals as natural or artificial,
- determine whether a signal is meaningful,
- draw conclusions or probabilities.

Measured structure is reported as-is.
Any interpretation remains entirely the responsibility of the user.
A lack of notable observations is considered a valid outcome.

## Configuration-driven design

The tool relies on two distinct YAML configuration files:

### Analysis protocol

The analysis protocol configuration defines:
- which analyses are executed,
- on which channels,
- with which parameters and resolutions.

This file controls **what is measured and how**.
It has no influence on report interpretation.

### Contextual references

Contextual reference files define:
- typical value ranges,
- orders of magnitude,
- explanatory notes and references.

They are used **only during report generation** to provide contextual positioning
of measurements, without thresholds or decisions.

They never influence the analysis itself.

## Installation

```bash
cd small-audio-toolkit
pip install -r requirements.txt
```

## Usage

```bash
python run_analysis.py audio_file.ext --config examples/config_example.yaml --output outputs/
```
## Report generation

Generated reports are intentionally structured to separate:

1. Raw measurements and visualizations  
2. Methodology and reading guidance  
3. Contextual positioning of results  

Reports describe observations and reference contexts, but do not produce conclusions.

After running the analysis, generate human-readable reports from the JSON results:

```bash
python Generate_Report.py output_folder/results.json
```

Or simply provide the output directory:

```bash
python Generate_Report.py output_folder
```

## Documentation

Project documentation is split into two main sections:

- `docs/analysis_explanations/`  
  Documentation intended for users and analysts, explaining how measurements
  should be read and what their limitations are.

- `docs/technical/`  
  Developer-oriented documentation covering architecture, configuration schemas,
  and extension mechanisms.

### Important Notes

This project exists because humans are very good at seeing patterns, 
sometimes more patterns than actually exist.


---


### Example Workflow

```bash
# Run complete analysis
python run_analysis.py audio.flac --config config.yaml --output output_audio

# Generate reports
python Generate_Report.py output_audio

# Review reports
working on it...

# Examine visualizations (if enabled)
ls output_audio/visualizations/
```

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
