# Configuration Schema and Extension Notes 

This document describes **conceptual, experimental, or planned configuration options**.

Anything listed here:

* may not be implemented
* may have no effect if used
* is provided for design clarity only

When an option becomes active and has a measurable effect, it should be moved to `configuration.md`.

---

## Visualization extensions

### visualization.backend (conceptual)

Select visualization backend.

Example:

```yaml
visualization:
  backend: extended
```

Status:

* Not currently consumed by the runner
* Intended to route plots between standard and advanced backends

---

### visualization.per_channel / per_method (conceptual)

Fine-grained visualization toggles.

Status:

* Not implemented

---

## Preprocessing extensions

### preprocessing.silence_detection (future integration idea)

The silence detector implementation exists, but the runner does not call it.
A future integration could:

* compute silence ranges per channel
* expose them in metadata/results
* optionally segment around non-silent regions

---

## Output extensions

### output.export_formats (future integration idea)

The validator accepts `json` and `csv`, but the runner currently exports JSON only.
A future implementation could:

* add CSV export for selected metrics
* add structured tables per method

---

## Notes

* This file documents design intent only.
* No option listed here is relied upon by execution.
