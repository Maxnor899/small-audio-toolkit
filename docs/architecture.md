# Software Architecture

## Overview

The tool is structured around a **generic execution engine**, driven by a configuration file, and a set of **independent analysis modules** registered dynamically.

The architecture ensures:

- Strong decoupling between orchestration and implementation
- Extensibility without modifying the core
- Complete traceability and reproducibility

## File Organization

```
pipeline_audio/
│
├── main.py                  # CLI entry point
├── engine/
│   ├── runner.py            # Main orchestrator
│   ├── context.py           # Analysis context (audio, channels, metadata)
│   ├── registry.py          # Analysis methods registry
│   └── results.py           # Results aggregation and serialization
│
├── config/
│   ├── loader.py            # Configuration file loading and validation
│   └── schema.md            # Formal description of config format
│
├── audio/
│   ├── loader.py            # Multi-channel audio loading
│   ├── channels.py          # L / R / sum / difference management
│   └── preprocessing.py     # Configurable preprocessing
│
├── analyses/
│   ├── temporal.py          # Temporal analyses
│   ├── spectral.py          # Frequency analyses
│   ├── time_frequency.py    # STFT, CQT, wavelets
│   ├── modulation.py        # AM / FM / phase
│   ├── information.py       # Entropy, compression
│   └── inter_channel.py     # Inter-channel analyses
│
├── visualization/
│   └── plots.py             # Graph generation
│   └── plots_extended.py    # Advanced / experimental visualizations
│
├── utils/
│   ├── math.py              # Common math functions
│   ├── windowing.py         # Windowing functions
│   └── logging.py           # Logging
│
└── outputs/
    └── run_YYYYMMDD_HHMMSS/ # Execution results
```

## Execution Engine

### Role

The engine is responsible for:

1. Loading the configuration
2. Loading the audio
3. Preparing analysis channels
4. Executing declared methods
5. Collecting and exporting results

It **contains no sound processing logic**.

### Flow

```
Configuration → Audio Loading → Channel Preparation →
Method Execution → Results Aggregation → Export
```
## Configuration as a Contract

The configuration file is treated as a **strict execution contract**.

Only configuration keys explicitly consumed by the engine have an effect on execution.
Unknown or undocumented keys are ignored or may trigger validation warnings.

The project distinguishes between:
- **Contractual configuration** (`configuration.md`), which documents options actively consumed by the code
- **Conceptual configuration notes** (`configuration_schema.md`), which document design ideas or future extensions with no runtime effect

This separation ensures reproducibility and prevents implicit or undocumented behavior.

## Analysis Context

The context is a shared object passed to each method. It contains:

- Audio data per channel
- Sample rate
- Temporal segments
- Execution metadata

The context is **immutable** for analysis methods.

## Methods Registry

All methods are registered in a global registry.

Each registry entry associates:

- A unique identifier
- A category
- An analysis function

The engine calls methods **by their identifier**, as defined in the configuration file.

## Analysis Modules

### Principle

Each module groups methods sharing the same intent.

Methods:

- Take the context as input
- Take parameters from a dictionary derived from configuration
- Return a structured result object

No method calls another method.

### Categories

- **Preprocessing**: Normalization, silence detection, segmentation
- **Temporal**: Envelope, autocorrelation, pulse detection
- **Spectral**: FFT, peak detection, cepstrum
- **Time-Frequency**: STFT, CQT, wavelets
- **Modulation**: AM/FM/phase analysis
- **Information**: Shannon entropy, compression ratios
- **Inter-Channel**: Cross-correlation, phase differences
- **Steganography**: LSB analysis, structured quantization noise
- **Meta-Analysis**: Segment comparison, clustering

Note : Meta-analysis methods provide **structural indicators only**.

They operate on previously computed measurements and do not perform
classification, labeling, or interpretation of signal meaning.

Meta-analysis outputs are intended to guide further human inspection,
not to produce conclusions.


## Results

Each method returns:

- Numerical values
- Derived metrics
- Stability or anomaly indicators

The engine aggregates everything into a hierarchical structure:

```
run
 ├── metadata
 ├── preprocessing
 ├── temporal
 ├── spectral
 ├── time_frequency
 ├── modulation
 ├── information
 ├── inter_channel
 ├── steganography
 └── meta_analysis
```

Results are exported as:

- JSON (raw data)
- Images (visualizations)
- Exact copy of configuration file

## Visualization

Graphs are produced **optionally**, driven by configuration.
No visualization is required for analytical functionality.

Visualization is an optional, non-intrusive layer.

Not all analyses guarantee associated visual output.
Visualizations are generated only when explicitly supported by the analysis method
and enabled through configuration.

Visualization does not influence analytical results and must remain purely descriptive.

## Command Line Interface

Example call:

```bash
python main.py \
  --audio guardian_signal.wav \
  --config config.yaml \
  --output outputs/
```

## Explicit Constraints

- No global state modified by methods
- No implicit ordering between analyses
- No automatic semantic interpretation
- All information used must be traceable

## Extensibility

Adding a new method only requires:

1. Implementing the function
2. Registering it in the registry
3. Activating it in the configuration file

The engine should never be modified to add an analysis.

## Design Philosophy

This architecture is designed to produce an ** audio analysis tool**, reproducible and shareable, suitable for exploring intentionally designed artificial signals (game design, ARG, steganography).
