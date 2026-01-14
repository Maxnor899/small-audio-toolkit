# Contributing Guidelines

Thank you for your interest in contributing to this project.

This tool is designed as a **rigorous audio analysis framework**. Its primary goal is to produce **objective, reproducible measurements** from audio signals, without embedding interpretation or semantic conclusions in the codebase.

Contributions are welcome, but they must respect the core design and scientific constraints described below.

---

## Scope of Contributions

Contributions are welcome in the following areas:

* Implementation of new analysis methods producing **objective measurements**
* Performance optimizations and computational efficiency improvements
* Visualization improvements that **do not imply interpretation**
* Documentation improvements aligned with the actual code behavior
* Refactoring and code clarity improvements

All contributions should aim to improve **traceability, reproducibility, and clarity**.

---

## Out of Scope Contributions

The following types of contributions will **not be accepted**:

* Automatic classification of signals (e.g. “natural”, “artificial”, “encoded”)
* Semantic labeling or decision-making logic
* Heuristic conclusions embedded in analysis code
* Any form of automated interpretation of signal meaning
* Hidden thresholds intended to imply conclusions

Interpretation is intentionally left to **human analysts outside the codebase**.

---

## Analysis Method Contributions

When adding a new analysis method:

* The method must compute **measurable, objective quantities only**
* The method must not call or depend on other analysis methods
* All parameters must be explicit and validated
* Default parameter values must be justified
* The method must be registered in the analysis registry

Each analysis method should:

* Accept an immutable analysis context
* Return structured numerical results
* Avoid side effects

---

## Visualization Contributions

Visualizations are considered **representational tools**, not interpretative ones.

Add or modify plot functions in visualization/plots.py.
plots_extended.py is reserved for re-exports/compatibility and should not contain implementations.

When contributing visualizations:

* Plots must represent raw or derived measurements only
* No visual element should suggest conclusions or classifications
* Titles, labels, and legends must remain descriptive
* Visualization must not alter analytical results

---

## Configuration Contributions

This project distinguishes clearly between **effective configuration** and **design ideas**:

* `configuration.md` documents **contractual configuration options** that are actively consumed by the engine
* `configuration_schema.md` documents **conceptual or experimental ideas** with no runtime effect

Rules:

* Any configuration option with runtime effect **must** be documented in `configuration.md`
* Conceptual or future configuration ideas **must** be documented in `configuration_schema.md`
* The code must not rely on undocumented configuration keys

---

## Documentation Contributions

Documentation must reflect the **actual behavior of the codebase**.

* Do not document planned features as if they were implemented
* Avoid speculative or interpretative language
* Keep documentation aligned with the registry and configuration loader

---

## Design Philosophy Reminder

* Measurement and interpretation are strictly separated
* The codebase provides data, not conclusions
* Scientific rigor takes precedence over convenience

If in doubt, prefer **less interpretation, more transparency**.

---

## Final Note

If you are unsure whether a contribution fits within the project scope, please open an issue or discussion before submitting a pull request.

Thoughtful, minimal, and well-documented contributions are always appreciated.
