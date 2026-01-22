# Context Files (Technical)

## Role
Context files are declarative inputs consumed only by the reporting step.

## Types
- Official contexts (per analysis family)
- User context (single file)

## Guarantees
- Contexts never affect calculations
- Missing or invalid contexts are reported explicitly

## Constraints
- USER contexts require explicit ranges
- Context coverage may be partial
