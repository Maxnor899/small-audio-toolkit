# Analysis Examples

This directory contains **example analysis material** for the Small Audio Tool (SAT).
It is the main entry point for users who want to *run analyses*, *understand methodology*,
and *inspect results* without modifying the core codebase.

The contents of this directory are **illustrative, reproducible, and modular**.
They demonstrate how SAT is intended to be used, not what should be concluded.

---

## Purpose of This Directory

`Analysis_examples/` serves as a **demo working environment** that brings together:

- analysis protocols (what to measure),
- contextual references (how to read measurements),
- launch scripts (how to run analyses),
- input signals (what is analyzed),
- generated results (what was observed).

Each subdirectory has a distinct methodological role.
None of them embed interpretation.

---

## Directory Structure

```
Analysis_examples/
├── 01_protocols/
├── 02_contexts/
├── 03_launchers/
├── 04_input_sounds/
├── 05_Results/
└── README.md
```

---

## 01_protocols/

Contains **analysis protocols**.

Protocols define:
- which analysis families are executed,
- which methods are applied,
- with which parameters.

They define *what is observed*.
They never define how results are interpreted.

See `01_protocols/README.md` for details.

---

## 02_contexts/

Contains **contextual reference files**.

Contexts define:
- which metrics admit reference zones,
- which metrics are context-dependent or descriptive,
- how values may be positioned during report generation.

Contexts affect **presentation only**.
They never affect computation.

Context files are **methodological artifacts**.
They should not be modified without understanding:
- how metrics are derived in the analysis code,
- how reference statuses (A / B / C) are assigned,
- and the methodological documentation that justifies them.

See `02_contexts/README.md` for details.

---

## 03_launchers/

Contains **execution scripts**.

Launchers:
- tie protocols, inputs, and outputs together,
- define reproducible execution commands,
- do not embed analytical assumptions.

They are orchestration utilities only.

---

## 04_input_sounds/

Contains **audio input material** used for analysis examples.

These files are:
- not authoritative datasets,
- not representative of any class by default,
- provided solely for demonstration and testing.

Users are expected to replace or extend them with their own material.

---

## 05_Results/

Contains **generated analysis results**.

Results include:
- raw measurement outputs,
- generated reports,
- copied protocol and context references used for the run.

Results are descriptive artifacts.
They do not represent conclusions.

---

## How This Directory Is Used

Users who want to run their **own analyses** should work from
`Small_Audio_Tool/Analysis/`.

To do so:

1. Copy the directory `Small_Audio_Tool/Analysis_examples/`.
2. Rename the copy to `Small_Audio_Tool/Analysis/`.
3. Modify the launcher scripts in `03_launchers/` to point to the appropriate
   input, output, and working paths.

This workflow preserves the original examples while providing
a clean, user-controlled analysis workspace.

The directory layout is intentional and stable.

---

## Design Principles

This directory is structured to enforce:

- separation of observation and interpretation,
- reproducibility of analysis runs,
- transparency of methodological limits,
- modular reuse of protocols and contexts.

Every file here can be read independently.
No file asserts meaning.

