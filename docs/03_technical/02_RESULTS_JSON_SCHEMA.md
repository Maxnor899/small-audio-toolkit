# results.json Schema

## Role
results.json is the sole source of truth produced by the analysis engine.

## High-level structure
- metadata
- preprocessing
- analyses / families
- per-method results

## AnalysisResult fields
- method: string
- measurements: dict
- metrics: dict or null
- anomaly_score: float or null
- visualization_data: dict or null

## Scalar metrics
Scalar metrics are values suitable for contextual positioning.
They must be numeric or simple scalar types.
