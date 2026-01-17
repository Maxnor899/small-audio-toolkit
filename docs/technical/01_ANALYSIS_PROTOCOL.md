# Analysis Protocols — Technical Description

This document describes the **technical role and structure** of analysis protocol files
used by the Small Audio Tool (SAT).

It is a **technical reference document**.
It does not explain why particular analyses should be run, nor how results should be interpreted.

For methodological rationale and reading constraints, see:
- `docs/analysis_explanations/`
- `Analysis_examples/01_protocols/README.md`

---

## Scope of This Document

This document explains:

- what an analysis protocol file is,
- how it is structured,
- how it is interpreted by the analysis engine,
- how it controls analysis execution.

It does **not**:
- justify analytical choices,
- recommend specific protocols,
- describe how to read or interpret results.

---

## Role of Analysis Protocols

An analysis protocol defines **what is measured and how**.

Protocols are declarative configuration files that:
- select analysis families and methods,
- define channels and signal representations,
- specify method parameters,
- control which analyses are executed.

Protocols do not:
- perform analysis,
- alter signal data,
- interpret results.

---

## Protocol File Format

Analysis protocols are defined as **YAML files**.

They are consumed directly by the analysis engine at runtime.
The engine does not modify protocol content.

---

## High-Level Structure

A protocol file is expected to define, at minimum:

- a list of channels to analyze,
- one or more analysis families,
- the methods to run within each family,
- optional parameters for each method.

The exact structure is validated before execution.

---

## Channels Definition

The protocol defines which signal representations are analyzed.

Typical channel identifiers include:
- individual audio channels (e.g. `left`, `right`),
- derived representations (e.g. `difference`, `sum`).

The protocol specifies:
- which channels are enabled,
- how they are derived when applicable.

The protocol does not define semantic meaning for channels.

---

## Analysis Families and Methods

Protocols organize analysis execution by **family**.

For each family, the protocol may specify:
- one or more analysis methods,
- optional parameters for each method.

Family and method identifiers must match those implemented
in the analysis code.

The engine executes only what is explicitly declared.

---

## Method Parameters

Each method may accept a set of parameters.

Parameters:
- are passed verbatim to the analysis function,
- control algorithmic behavior (e.g. window size, thresholds),
- are not interpreted or validated beyond type and presence.

Default values are used when parameters are omitted.

---

## Validation and Error Handling

Before execution, the analysis engine performs validation:

- unknown families or methods are rejected,
- invalid parameter structures cause execution to fail,
- missing required fields are reported.

Validation errors prevent analysis execution.

---

## Relationship With Other Documentation

- This document describes **how protocols are structured and consumed**.
- `analysis_explanations/` documents describe **why interpretation is constrained**.
- `Analysis_examples/01_protocols/` contains **example protocol files**.

These documents are complementary and non-overlapping.

---

End of document.
