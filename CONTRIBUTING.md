# Contributing to Small Audio Toolkit

Thank you for your interest in contributing to this project.

## Core Principles

This project aims at mintaining rigor:

1. No semantic interpretation - only objective measurements
2. Full reproducibility and traceability
3. Configuration-driven execution
4. Strong separation between engine and analysis logic

## How to Contribute

### Reporting Issues

When reporting bugs or issues:

- Provide the configuration file used
- Include audio file characteristics (sample rate, channels, duration)
- Share relevant log output
- Describe expected vs actual behavior

### Adding Analysis Methods

See `docs/extending.md` for detailed instructions.

Key requirements:

1. Implement as pure function taking context and params
2. Register in appropriate module
3. Include comprehensive docstring with references
4. Validate all parameters
5. Handle edge cases gracefully
6. Return structured AnalysisResult

### Code Standards

- Python 3.10+
- PEP8 compliance
- Type hints required
- Concise docstrings (no excessive commentary)
- No dead code or speculative features

### Documentation

- Update relevant docs/*.md files
- Keep README.md current
- Document new parameters in configuration.md
- Add examples where appropriate

### Testing

Before submitting:

1. Test with various audio formats (mono, stereo, different sample rates)
2. Verify configuration validation works
3. Ensure results are reproducible
4. Check JSON export is valid

## Proven Validity

New analysis methods should:

- Be based on established principles
- Include references to papers/standards where applicable
- Produce measurements, not interpretations
- Handle numerical edge cases appropriately

## What We Don't Accept

- Methods that perform semantic interpretation
- Undocumented or speculative analyses
- Code that modifies the core engine for specific analyses
- Dependencies that duplicate existing functionality

## Questions

For questions about:

- Architecture: see `docs/architecture.md`
- Configuration: see `docs/configuration.md`
- Analysis methods: see `docs/analyses.md`
- Extending: see `docs/extending.md`

## Code of Conduct

Be respectful, and constructive. This is a hopefully cool tool meant for exploration and discovery.
