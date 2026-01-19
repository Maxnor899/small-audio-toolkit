# Small Audio Toolkit

Small Audio Toolkit is a Python-based audio analysis framework focused on **objective signal measurements**.
It is designed to extract factual, reproducible metrics from audio files, without automated interpretation or classification.
All conclusions are intentionally left to the human analyst.

The project is built around the idea that:
- analyses compute measurements,
- contexts provide reference ranges,
- reports compare values to ranges **without inferring meaning**.

---

## Analysis_Workspace

The main entry point for users is the `Analysis_Workspace/` directory.
It contains everything needed to run analyses, manage reference contexts, and collect results in a reproducible way.

```
Analysis_Workspace/
├── 01_protocols/
├── 02_contexts/
│   ├── Official/
│   └── User_Defined/
├── 03_launchers/
├── 04_input_sounds/
└── 05_results/
```

### 01_protocols
Analysis protocol definitions.
A protocol specifies **what analyses are run** and with which parameters.
Protocols do not contain reference values or interpretation logic.

### 02_contexts
Reference contexts used during report generation.

- `Official/`  
  Project-maintained reference contexts based on documented signal processing literature.

- `User_Defined/`  
  User-provided contexts, intended for domain-specific or experimental reference ranges.
  These contexts follow the same structure as official ones, but are explicitly marked as user-provided.

Contexts are only used for **comparison in reports**, never during analysis computation.

### 03_launchers
Helper scripts or launch configurations used to run analyses with a given protocol and input set.

### 04_input_sounds
Audio files to be analyzed.
These files are treated as raw input and are never modified by the toolkit.

### 05_results
Outputs produced by analysis runs and report generation.
This directory is expected to be populated automatically.

---

## Core Principles

- No automated interpretation or classification
- No mixing of measurement and reference logic
- Full separation between analysis, context, and reporting
- Reproducible and transparent results

If a metric is not measured, it is not reported.
If a reference range is not provided, no comparison is made.

---

## Typical Workflow

1. Place audio files in `Analysis_Workspace/04_input_sounds`
2. Select or create an analysis protocol in `01_protocols`
3. Run an analysis using a launcher from `03_launchers`
4. Generate one or more reports using official and/or user-defined contexts
5. Inspect results in `05_results`

---

This structure is intentional and stable.
Renaming, reorganizing, or extending it should preserve the strict separation between measurement, reference, and interpretation.
