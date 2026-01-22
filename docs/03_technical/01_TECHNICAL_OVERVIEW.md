# 01 – Technical Overview

## 1. Purpose and scope

Small Audio Toolkit (SAT) is a Python-based audio analysis system whose sole purpose is to **compute and serialize objective signal measurements** from audio files.

SAT is explicitly **not** a detector, classifier, or decision engine. From a technical standpoint, SAT:

- loads audio data from disk,
- applies optional preprocessing steps,
- executes a configurable set of analysis methods,
- serializes all produced measurements (including failures),
- optionally generates human-readable reports that *position* selected scalar values against declarative references.

SAT does **not**:
- infer intent, meaning, or origin of a signal,
- decide whether a signal is artificial, encoded, or anomalous,
- adapt computations based on contextual information.

All interpretation is explicitly left to humans or external systems.

---

## 2. Global architecture and execution flow

SAT is composed of three strictly separated layers:

1. **Execution & computation layer**
2. **Configuration & orchestration layer**
3. **Reporting & contextualization layer**

This separation is enforced in the codebase and is a core architectural invariant.

### 2.1 End-to-end execution flow

The complete execution pipeline is:

```
Audio file
   ↓
Analysis protocol (YAML)
   ↓
01_run_analysis.py
   ↓
audio_toolkit (analysis engine)
   ↓
results.json (+ config_used.json)
   ↓
02_Generate_Report.py (optional)
   ↓
Markdown reports (01–04)
```

Each stage consumes outputs from the previous one and **never mutates upstream data**.

---

## 3. Entry points and scripts

### 3.1 01_run_analysis.py

**Role:** sole supported entry point for executing analyses.

**Responsibilities:**
- resolve input, config, and output paths,
- load and validate the analysis protocol YAML,
- instantiate the analysis engine,
- execute all configured analyses,
- write raw outputs to disk.

**Inputs:**
- audio file path (mandatory),
- protocol YAML (optional, default baseline),
- output directory (optional).

**Outputs:**
- results.json (mandatory),
- config_used.json (if enabled by engine).

**Explicit non-responsibilities:**
- no contextual logic,
- no thresholds,
- no reporting,
- no interpretation.

If this script completes successfully, `results.json` is guaranteed to exist.

---

### 3.2 02_Generate_Report.py

**Role:** transform raw analysis results into human-readable reports.

**Responsibilities:**
- load results.json,
- optionally load protocol and context YAML files,
- generate four Markdown reports:
  - 01_MEASUREMENT_SUMMARY.md
  - 02_METHODOLOGY_AND_READING_GUIDE.md
  - 03_CONTEXTUAL_POSITIONING.md
  - 04_CONTEXTUAL_POSITIONING_USER.md

**Key constraints:**
- operates strictly in read-only mode on results.json,
- never recomputes or alters measurements,
- contexts influence presentation only.

---

## 4. Physical architecture of the audio_toolkit package

```
audio_toolkit/
├── audio/
│   ├── loader.py        # audio file I/O (soundfile → numpy)
│   ├── channels.py      # channel derivation (L, R, mono, sum, difference)
│   └── preprocessing.py # normalization, segmentation, silence handling
│
├── analyses/
│   ├── __init__.py      # imports modules to register analyses
│   ├── temporal.py
│   ├── spectral.py
│   ├── time_frequency.py
│   ├── modulation.py
│   ├── information.py
│   ├── inter_channel.py
│   ├── steganography.py
│   └── meta_analysis.py
│
├── engine/
│   ├── runner.py        # orchestrates full analysis execution
│   ├── registry.py      # analysis method registration and lookup
│   ├── results.py       # result objects and JSON serialization
│   └── context.py       # runtime AnalysisContext (NOT YAML contexts)
│
├── visualization/
│   ├── plots.py
│   └── plots_extended.py
│
├── config/
│   ├── loader.py        # YAML loading and validation
│   └── schema.py        # allowed keys, enums, constraints
│
└── __init__.py
```

### 4.1 Call path (simplified)

- 01_run_analysis.py
  → ConfigLoader.load()
  → AnalysisRunner.run()
  → AudioLoader.load()
  → channels / preprocessing
  → registry.resolve()
  → analysis_method(context)
  → ResultsAggregator.export_json()

- 02_Generate_Report.py
  → load_json(results.json)
  → iter_result_methods()
  → generate_*_report()
  → write Markdown files

---

## 5. Data flow and immutability guarantees

SAT enforces a strict unidirectional data flow:

```
audio → measurements → serialization → presentation
```

Once a value is written to results.json:
- it is never modified,
- it is never recomputed,
- it is never filtered.

This guarantees reproducibility and auditability.

---

## 6. Error handling model

SAT uses a **fail-soft** execution model:

- each analysis method is isolated,
- exceptions are caught per method,
- failures are serialized as data,
- the global pipeline continues.

Errors are treated as first-class results, not control flow.

---

## 7. Invariants and non-goals

### Guaranteed invariants
- separation of computation and contextualization,
- deterministic execution given identical inputs,
- explicit serialization of failures,
- absence of implicit thresholds.

### Explicit non-goals
- automated detection or classification,
- probability or likelihood estimation,
- embedding domain assumptions in code.

---

## 8. Annex A — Analysis_Workspace structure and role

The `Analysis_Workspace` directory is an **operational layer**, not an example folder.

```
Analysis_Workspace/
├── 01_protocols/
│   ├── 01_Baseline/
│   └── 02_Focused/
├── 02_contexts/
│   ├── Official/
│   └── User/
└── 03_launchers/
```

### 8.1 Protocols
- YAML files defining which analyses run and how.
- Consumed exclusively by 01_run_analysis.py.

### 8.2 Contexts
- Declarative YAML files used only by 02_Generate_Report.py.
- Provide reference ranges and documentary notes.
- Never influence computation.

### 8.3 Launchers
- Convenience scripts (e.g. .bat).
- No logic; wrap calls to Python entry points.

---

## 9. Status

This document was written after explicit recross-checking with:
- small-audio-toolkit source code,
- 01_run_analysis.py,
- 02_Generate_Report.py.

It is **technically exhaustive** with respect to architecture, responsibilities,
and execution flow.
