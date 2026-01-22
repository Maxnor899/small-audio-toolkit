# Technical Overview

## Scope
SAT (Small Audio Toolkit) is a measurement-oriented audio analysis framework.
It computes objective signal metrics and serializes them without interpretation.

SAT does NOT:
- classify signals
- infer intent or meaning
- decide whether a signal is artificial or natural

## Architecture
Pipeline:
audio file → analysis protocol (YAML) → analysis engine → results.json → reporting scripts

Components:
- 01_run_analysis.py: analysis launcher
- audio_toolkit: analysis engine and registries
- 02_Generate_Report.py: reporting and contextual positioning

## Core invariants
- Calculations and presentation are strictly separated
- Context files never affect computation
- Errors do not stop the pipeline; they are serialized
