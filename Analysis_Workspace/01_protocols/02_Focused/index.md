# Focused Analysis Protocols

This directory contains **focused analysis protocols** designed to target
specific signal characteristics or investigative angles.

No protocol in this directory performs interpretation or classification.
They only define *what is measured* and *how it is measured*.

---

## How to Read These Protocols

Each protocol:

- may combine methods from different families,
- keeps default parameters unless a deviation is necessary and justified,
- is safe to run independently of all others.

Results must always be interpreted by a human analyst in context.

---

## Protocol Overview

### Family-Oriented Focused Protocols

These files correspond to focused subsets of the main analysis families.
They are useful when only one analytical dimension is of interest.

- **`01_temporal.yaml`**  
  Focuses on temporal structure: envelopes, periodicity, pulse patterns,
  and interval relationships.

- **`02_spectral.yaml`**  
  Focuses on frequency-domain structure: global spectrum, peaks,
  harmonics, dispersion, and spectral dynamics.

- **`03_time_frequency.yaml`**  
  Focuses on time–frequency representations such as STFT, wavelets,
  band stability, and frequency evolution.

- **`04_modulation.yaml`**  
  Focuses on modulation-related phenomena including AM, FM,
  phase behavior, and chirp detection.

- **`05_information.yaml`**  
  Focuses on information-theoretic descriptors such as entropy,
  complexity, and mutual information.

- **`06_inter_channel.yaml`**  
  Focuses on relationships between channels: correlation,
  phase differences, delays, and L/R structure.

- **`07_steganography.yaml`**  
  Focuses on low-level statistical structures often examined
  in steganographic or tampering analysis.

- **`08_meta_analysis.yaml`**  
  Focuses on cross-segment, cross-metric, and distribution-level
  statistical descriptors.

---

### Scenario-Oriented Focused Protocols

These protocols combine methods across families to explore
specific *structural hypotheses*.

They do not assert that such structures are present;
they simply expose measurements relevant to each scenario.

- **`generic_audio.yaml`**  
  A broad but lightweight protocol intended as a neutral baseline
  for unknown audio material.

- **`temporal_regularities.yaml`**  
  Targets repeating or structured temporal patterns such as
  pulses, rhythms, and regular interval relationships.

- **`dynamic_profiles.yaml`**  
  Targets evolving behavior over time, including spectral change,
  modulation dynamics, and stability variations.

- **`spectral_dispersion.yaml`**  
  Targets how energy is distributed and spread across frequencies,
  including bandwidth, rolloff, and spectral variability.

- **`stereo_relations.yaml`**  
  Targets inter-channel dependency and structure,
  including correlation and mutual information.

- **`synthetic_structures.yaml`**  
  Targets statistical and structural traits often associated
  with synthetic generation, heavy processing, or embedding artifacts.

---

## Usage Guidance

- Start with **family-oriented protocols** when exploring a single dimension.
- Use **scenario-oriented protocols** when testing a specific structural idea.
- Multiple protocols may be run on the same file without conflict.
- Absence of notable observations is a valid and expected outcome.

---

## Important Note

These protocols **do not define conclusions**.

They define *measurement scopes only*.
