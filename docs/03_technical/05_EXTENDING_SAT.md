# Extending SAT

## Adding an analysis
- Implement AnalysisResult
- Register the method
- Emit structured measurements

## Adding visualizations
- Consume results.json only
- Never modify analysis outputs

## Stability rules
- Avoid breaking scalar metric names
- Prefer additive changes
