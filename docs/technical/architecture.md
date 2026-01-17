# Software Architecture

## Overview 

The tool is structured around a **generic execution engine**, driven by an **analysis protocol**, and relying on a set of **independent analysis modules** registered dynamically.

The architecture ensures:

- Strong decoupling between orchestration and implementation
- Extensibility without modifying the core
- Complete traceability and reproducibility

## File Organization

```
pipeline_audio/
│
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
│   ├── inter_channel.py     # Inter-channel analyses
│   ├── steganography/       # Steganography-oriented analyses
│   └── meta_analysis/       # Cross-analysis / meta metrics
│
├── visualization/
│   └── plots.py             # Graph generation
│   └── plots_extended.py    # OLD AND DEPRECATED Advanced / experimental visualizations kept only for compatibility - DO NOT USE
│
└── utils/
    ├── math.py              # Common math functions
    ├── windowing.py         # Windowing functions
    └── logging.py           # Logging

```

## Execution Engine

The execution engine is responsible for orchestrating the analysis run.

It is implemented in the `engine/` directory and includes:

- `runner.py`: execution orchestration and method dispatch
- `context.py`: shared analysis context (audio, channels, metadata)
- `registry.py`: analysis methods registry
- `results.py`: results aggregation and serialization

### Responsibilities

The engine is responsible for:

1. Consuming execution inputs (analysis protocol and execution parameters)
2. Loading audio data
3. Preparing analysis channels
4. Executing declared analysis methods
5. Aggregating and exporting results

The engine **contains no signal processing logic**.

---

## Configuration

The `config/` directory contains components related to execution configuration.

It includes:

- `loader.py`: loading and validation of configuration files
- `schema.md`: formal description of the supported configuration format

Configuration files act as an **execution contract**:
only options explicitly consumed by the code have an effect on execution.
Unknown or unsupported keys are ignored or may trigger validation warnings.

---

## Audio Handling

The `audio/` directory contains all components related to audio input handling.

It includes:

- `loader.py`: multi-channel audio loading
- `channels.py`: channel management (left, right, sum, difference)
- `preprocessing.py`: configurable preprocessing steps

These components are responsible for preparing audio data before analysis methods are executed.

---

## Analysis Modules

The `analyses/` directory contains all analysis method implementations.

Each submodule corresponds to an analysis family:

- `temporal/`: temporal analyses
- `spectral/`: frequency-domain analyses
- `time_frequency/`: time–frequency analyses (STFT, CQT, wavelets)
- `modulation/`: amplitude and frequency modulation analyses
- `information/`: entropy and information-theoretic measures
- `inter_channel/`: inter-channel analyses
- `steganography/`: steganography-oriented analyses
- `meta_analysis/`: cross-analysis and structural metrics

Analysis methods:

- take the shared context as input,
- receive parameters from the analysis protocol,
- return structured result objects.

No analysis method calls another method.

---

## Visualization

The `visualization/` directory contains visualization components.

It includes:

- `plots.py`: current visualization implementation
- `plots_extended.py`: deprecated module kept for compatibility and documentation purposes (not used)

Visualization is optional and does not influence analytical results.
Only analyses explicitly supporting visualization can produce graphical output.

---

## Utilities

The `utils/` directory contains shared utility functions.

It includes:

- `math.py`: common mathematical helpers
- `windowing.py`: windowing functions
- `logging.py`: logging utilities

These modules support the rest of the codebase and contain no analysis logic.


# Command Line Interface

Example call:

```bash
python run_analysis.py \
  --audio <path_to>/guardian_signal.wav \
  --config <path_to>/config.yaml \
  --output <analysis_output_directory>

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

