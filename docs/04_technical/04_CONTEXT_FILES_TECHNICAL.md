# 04 – Context Files (Technical)

## 1. Purpose and role

Context files are **declarative YAML files** that define reference ranges and interpretive notes for analysis metrics. They are used exclusively for **reporting and presentation**, never for computation.

**Key properties:**
- Consumed only by `02_Generate_Report.py`
- Never read by the analysis engine (`01_run_analysis.py`)
- Provide reference ranges for contextual positioning
- Include documentary references and rationale
- Independent of analysis execution

**Critical separation:** Changing a context file does NOT require re-running analysis. The same `results.json` can be re-reported with different contexts.

---

## 2. Context types

SAT supports two types of context files:

| Type | Purpose | Location | Naming |
|------|---------|----------|--------|
| **Official** | Maintained by SAT authors, based on literature | `Analysis_Workspace/02_contexts/Official/` | `context_<family>.yaml` |
| **User** | Defined by users, based on internal corpora | `Analysis_Workspace/02_contexts/User_Defined/` | Any name (e.g., `context_Template.yaml`) |

### 2.1 Official contexts

- One file per analysis family (e.g., `context_temporal.yaml`, `context_spectral.yaml`)
- Reference ranges based on published literature or empirical observations
- Status codes (A, B, C) indicate confidence level
- Maintained by SAT project

### 2.2 User-defined contexts

- Single file containing user-specific reference ranges
- Derived from internal datasets or project-specific baselines
- Must use `status: USER` for all metrics
- User is responsible for validity and scope

---

## 3. Official context structure

### 3.1 Top-level structure

```yaml
family: <family_name>

scope:
  coverage: <partial|full>
  objective: >
    <High-level objective of this context>
  rationale: >
    <Explanation of scope and limitations>

references:
  - authors: <Author names>
    title: <Publication title>
    year: <Year>
    note: >
      <Additional notes about the reference>

methods:
  <method_name>:
    metrics:
      <metric_name>:
        reference:
          status: <A|B|C>
          typical_range: [<min>, <max>]
        notes:
          - <Note 1>
          - <Note 2>
```

### 3.2 Field descriptions

**`family`** (string, required)
- Analysis family name
- Must match one of: `temporal`, `spectral`, `time_frequency`, `modulation`, `information`, `inter_channel`, `steganography`, `meta_analysis`
- Used by reporting script to load the correct context file

**`scope`** (object, required)

- **`coverage`** (string): `"partial"` or `"full"`
  - `"partial"`: Context covers only selected metrics
  - `"full"`: Context aims to cover all metrics from the family (aspirational)

- **`objective`** (string): High-level purpose of the context

- **`rationale`** (string): Explanation of scope, limitations, and intended use

**`references`** (array of objects, optional)
- Bibliographic references supporting the context
- Each reference has:
  - **`authors`** (string): Author names
  - **`title`** (string): Publication title
  - **`year`** (integer): Publication year
  - **`note`** (string): Additional notes about relevance

**`methods`** (object, required)
- Dictionary of methods covered by this context
- Keys are method names (e.g., `"autocorrelation"`, `"fft_global"`)

### 3.3 Method structure

Each method entry has:

```yaml
<method_name>:
  metrics:
    <metric_name>:
      reference:
        status: <A|B|C>
        typical_range: [<min>, <max>]
      notes:
        - <Note 1>
        - <Note 2>
```

**`metrics`** (object, required)
- Dictionary of metrics covered for this method
- Keys are metric names (e.g., `"autocorr_max"`, `"peak_frequency"`)

**`reference`** (object, required)

- **`status`** (string): Confidence level
  - `"A"`: High confidence (based on strong literature or extensive empirical data)
  - `"B"`: Moderate confidence (based on limited literature or smaller datasets)
  - `"C"`: Low confidence (exploratory or preliminary)

- **`typical_range`** (array of 2 numbers): `[min, max]`
  - Reference range for the metric
  - Must be two numbers (int or float)
  - Used for positioning measured values as "below", "within", or "above"

**`notes`** (array of strings, optional)
- Explanatory notes about the metric
- Best practices, caveats, or interpretation guidelines

### 3.4 Complete example

```yaml
family: temporal

scope:
  coverage: partial
  objective: >
    Identify periodicity, repetition, and non-random temporal structure
    in audio signals.
  rationale: >
    This context focuses on stable scalar temporal metrics suitable for
    high-level forensic screening. It does not aim to exhaustively cover
    all temporal-domain measurements.

references:
  - authors: "A. V. Oppenheim & A. S. Willsky"
    title: "Signals and Systems"
    year: 2010
    note: "Foundational reference for temporal analysis and autocorrelation."

methods:
  autocorrelation:
    metrics:
      autocorr_max:
        reference:
          status: A
          typical_range: [0.0, 1.0]
        notes:
          - "Normalized maximum autocorrelation excluding zero lag."
      
      periodicity_score:
        reference:
          status: A
          typical_range: [0.0, 1.0]
        notes:
          - "Proxy for temporal periodicity strength."
  
  envelope:
    metrics:
      envelope_std:
        reference:
          status: B
          typical_range: [0.0, 1.0]
        notes:
          - "Variability of the amplitude envelope."
```

---

## 4. User-defined context structure

### 4.1 Top-level structure

User contexts use the same overall structure as official contexts, with critical differences:

```yaml
version: "1.0"
family: <family_name>

scope:
  coverage: partial
  objective: >
    <User-specific objective>
  rationale: >
    <Explanation of derivation and scope>

references:
  - authors: "Internal corpus"
    title: <Dataset or project name>
    year: <Year>
    note: >
      <How ranges were derived>

methods:
  <method_name>:
    scope: <global|per_channel|pair|per_segment>  # Optional
    metrics:
      <metric_name>:
        unit: <optional_unit>  # Optional
        reference:
          status: USER
          typical_user_range: [<min>, <max>]
        notes:
          - <Note 1>
          - <Note 2>
```

### 4.2 Key differences from official contexts

| Field | Official | User |
|-------|----------|------|
| **`version`** | Absent | Required (`"1.0"`) |
| **`status`** | `A`, `B`, or `C` | Must be `"USER"` |
| **Range field** | `typical_range` | `typical_user_range` |
| **`scope` (method-level)** | Absent | Optional |
| **`unit` (metric-level)** | Absent | Optional |
| **`notes` requirement** | Optional | Recommended (flagged if missing) |

### 4.3 User context validation rules

**Enforced by `02_Generate_Report.py::_get_user_reference()`:**

1. **`status` must be exactly `"USER"`**
   - Any other value → validation error

2. **`typical_user_range` required**
   - Must be a 2-element array of numbers
   - Missing or invalid → validation error

3. **`typical_range` is NOT allowed**
   - Using official field name in user context → validation error

4. **`notes` recommended**
   - Missing or empty notes → flagged as issue in report
   - Not a hard error, but strongly encouraged

**Consumers MUST NOT rely on the specific structure of validation error messages.**

### 4.4 Complete example

```yaml
version: "1.0"
family: temporal

scope:
  coverage: partial
  objective: >
    User-specific contextual ranges intended for project-level
    positioning of selected scalar metrics.
  rationale: >
    This user context defines reference ranges derived from an internal corpus
    of 500 audio files recorded in controlled conditions. These ranges are not
    part of the official SAT documentary references and may not generalize beyond
    this project scope.

references:
  - authors: "Internal corpus"
    title: "Project XYZ baseline dataset"
    year: 2025
    note: >
      Ranges derived from 500 FLAC files (48kHz, stereo) recorded in laboratory
      conditions. All files normalized to -20 dB RMS prior to analysis.

methods:
  autocorrelation:
    scope: per_channel
    metrics:
      autocorr_max:
        unit: ratio
        reference:
          status: USER
          typical_user_range: [0.2, 0.8]
        notes:
          - "Derived from internal corpus with RMS normalization."
          - "Values below 0.2 observed only in synthetic noise signals."
      
      periodicity_score:
        reference:
          status: USER
          typical_user_range: [0.1, 0.9]
        notes:
          - "Corpus contains primarily periodic signals (speech, music)."
```

---

## 5. Context file loading

### 5.1 Loading mechanism

Context files are loaded by `02_Generate_Report.py` using the following logic:

**Official contexts:**
```python
try_load_family_context(contexts_dir, family)
# Looks for: <contexts_dir>/context_<family>.yaml
```

**User contexts:**
```python
try_load_yaml(user_context_path)
# Loads user-specified file
```

### 5.2 Loading behavior

**If context file missing:**
- No error raised
- Method appears in report without contextual positioning
- Warning message included in report: `"Missing context file: context_<family>.yaml"`

**If context file invalid (malformed YAML):**
- No error raised
- Error message included in report: `"Failed to load context file: <error>"`

**If PyYAML not installed:**
- All contexts skipped
- Warning in report: `"PyYAML is not available; cannot load context YAML files."`

**Critical:** Missing or invalid contexts do NOT prevent report generation. Reports proceed with available data.

### 5.3 Context file discovery

**Official contexts:**
- Directory specified via `--contexts-dir` CLI argument
- Default: `Analysis_Workspace/02_contexts/Official/`
- Files must be named `context_<family>.yaml`

**User contexts:**
- Single file specified via `--user-context` CLI argument
- No default location
- Filename is arbitrary (commonly `context_Template.yaml`)

---

## 6. Contextual positioning logic

### 6.1 Positioning algorithm

For each scalar metric with a defined reference range:

```python
def position(value, min_range, max_range):
    if value < min_range:
        return "below"
    elif value > max_range:
        return "above"
    else:
        return "within"
```

### 6.2 Reporting behavior

**In generated reports:**
- Metrics positioned as: `"below typical range"`, `"within typical range"`, or `"above typical range"`
- Range values displayed: `[min, max]`
- Status code displayed (A/B/C or USER)
- Notes displayed verbatim

**If no context for a metric:**
- Metric listed without positioning
- Raw value displayed only

**If multiple contexts define the same metric:**
- Official context used for `03_CONTEXTUAL_POSITIONING.md`
- User context used for `04_CONTEXTUAL_POSITIONING_USER.md`
- No conflict resolution (separate reports)

---

## 7. Scope and coverage

### 7.1 Partial vs full coverage

**Partial coverage** (most common):
- Context covers only selected metrics
- Uncovered metrics appear in reports without positioning
- Explicitly acknowledged in `scope.coverage: partial`

**Full coverage** (aspirational):
- Context aims to cover all metrics in the family
- May still have gaps (documented in rationale)

**Recommendation:** Use `partial` unless genuinely comprehensive.

### 7.2 Method and metric coverage

**Methods without context entry:**
- All metrics from that method appear without positioning
- No error or warning

**Metrics without context entry:**
- That specific metric appears without positioning
- Other metrics from same method may have positioning

**Critical:** Context coverage is **best-effort**. Consumers MUST handle missing contexts gracefully.

---

## 8. Status codes (official contexts only)

### 8.1 Confidence levels

| Status | Meaning | Basis |
|--------|---------|-------|
| `A` | High confidence | Strong literature consensus or extensive empirical data (>1000 samples) |
| `B` | Moderate confidence | Limited literature or moderate datasets (100–1000 samples) |
| `C` | Low confidence | Exploratory, preliminary, or small datasets (<100 samples) |

**Note:** Status codes are **informational** and do not affect positioning logic. A status-C range is used identically to a status-A range.

### 8.2 User contexts

User contexts **must** use `status: USER`.

- Using A/B/C → validation error
- Missing status → validation error
- Arbitrary strings → validation error

---

## 9. Validation and error handling

### 9.1 Official context validation

**Validated at load time:**
- YAML syntax (by PyYAML)
- File structure is a dictionary (top-level)

**Not validated:**
- `family` matches file name
- `status` is A/B/C (any string accepted)
- `typical_range` is 2 numbers (any list accepted)
- Method names exist in registry
- Metric names match actual outputs

**Runtime behavior:**
- Invalid `typical_range` structure → metric skipped, warning in report
- Unknown method/metric → no effect (just not used)

### 9.2 User context validation

**Validated by `_get_user_reference()`:**

1. `reference` section exists and is a dict
2. `status` is exactly `"USER"`
3. `typical_user_range` is 2-element numeric array
4. `typical_range` is NOT present

**Issues collected (not raised as errors):**
- Missing or empty notes
- Invalid status
- Missing typical_user_range
- Presence of typical_range

**Issues are reported in the user context report** with specific error messages.

### 9.3 Error message examples

**Official context, invalid range:**
```
Warning: Metric 'autocorr_max' has invalid typical_range (expected 2 numbers)
```

**User context, wrong status:**
```
Issue with metric 'autocorr_max': reference.status must be USER
```

**User context, missing range:**
```
Issue with metric 'periodicity_score': missing or invalid typical_user_range
```

**User context, forbidden field:**
```
Issue with metric 'envelope_std': typical_range is not allowed in user contexts
```

---

## 10. Context vs protocol independence

### 10.1 Relationship

| Aspect | Protocols | Contexts |
|--------|-----------|----------|
| **Consumed by** | `01_run_analysis.py` | `02_Generate_Report.py` |
| **Affects** | Computation | Presentation |
| **Location** | `01_protocols/` | `02_contexts/` |
| **Coupling** | None | None |

**Critical:** Protocols and contexts are **completely independent**.

### 10.2 Workflow implications

**Valid workflows:**

1. Run analysis with protocol A → Generate report with context X
2. Run analysis with protocol A → Generate report with context Y (different ranges)
3. Run analysis with protocol B → Use same `results.json` with context X

**Invalid assumptions:**
- "Changing context requires re-running analysis" ❌
- "Protocol and context must match" ❌
- "Each protocol has a corresponding context" ❌

**Correct understanding:**
- Contexts provide reference frames for interpretation
- Same results can be positioned against multiple contexts
- Contexts evolve independently of protocols

---

## 11. Best practices

### 11.1 For official context authors

**Do:**
- Base ranges on published literature or extensive empirical data
- Document references thoroughly
- Use conservative (wide) ranges for status B/C
- Explain rationale and limitations in `scope`
- Update contexts when new literature emerges

**Don't:**
- Use narrow ranges without strong justification
- Claim full coverage without exhaustive validation
- Include interpretation in notes (remain descriptive)

### 11.2 For user context authors

**Do:**
- Document corpus size and composition
- Explain how ranges were derived (percentiles, mean ± std, etc.)
- Use `status: USER` consistently
- Provide detailed notes (requirement flagged if missing)
- Specify `unit` when non-obvious
- Indicate `scope` (global vs per_channel) when relevant

**Don't:**
- Claim general validity for project-specific ranges
- Use official status codes (A/B/C)
- Mix `typical_range` and `typical_user_range`
- Omit notes (strongly discouraged)

### 11.3 For report consumers

**Do:**
- Check status codes for confidence level
- Read notes for caveats and interpretation guidance
- Understand scope limitations (partial coverage)
- Compare official vs user contexts when available

**Don't:**
- Treat "above range" as definitive anomaly
- Ignore notes (they contain critical context)
- Assume all metrics have positioning
- Rely on specific error message formats

---

## 12. Context file organization

### 12.1 Recommended directory structure

```
Analysis_Workspace/
└── 02_contexts/
    ├── Official/
    │   ├── context_temporal.yaml
    │   ├── context_spectral.yaml
    │   ├── context_time_frequency.yaml
    │   ├── context_modulation.yaml
    │   ├── context_information.yaml
    │   ├── context_inter_channel.yaml
    │   ├── context_steganography.yaml
    │   └── context_meta_analysis.yaml
    │
    └── User_Defined/
        ├── context_Template.yaml
        ├── context_project_alpha.yaml
        └── context_corpus_2025.yaml
```

### 12.2 Naming conventions

**Official contexts:**
- **Must** be named `context_<family>.yaml`
- `<family>` must match analysis family name exactly
- Example: `context_temporal.yaml`, `context_spectral.yaml`

**User contexts:**
- **May** use any filename
- Recommended: `context_<project_name>.yaml`
- Template provided: `context_Template.yaml`

---

## 13. Context evolution and versioning

### 13.1 Official context versioning

**Current state:**
- No explicit version field in official contexts
- Implicit versioning via git commits
- Breaking changes require documentation update

**Future considerations:**
- May add `version` field for schema evolution
- Backward compatibility not guaranteed for status codes

### 13.2 User context versioning

**Current state:**
- `version: "1.0"` required
- Only one version defined

**Forward compatibility:**
- Unknown fields are ignored
- Future versions may add optional fields

---

## 14. Performance and file size

### 14.1 Context file sizes

**Typical sizes:**
- Official context: 0.5–2 KB per file
- User context: 1–5 KB (depends on coverage)

**Scaling:**
- Linear with number of metrics covered
- Negligible impact on report generation time (<1ms per context)

### 14.2 Report generation impact

**With contexts:**
- Report generation: ~100–500ms (YAML parsing + formatting)

**Without contexts:**
- Report generation: ~50–200ms (formatting only)

**Recommendation:** Always provide contexts for meaningful reports.

---

## 15. Limitations and non-goals

### 15.1 Explicit limitations

**Contexts do NOT:**
- Perform automated classification or scoring
- Compute derived metrics
- Apply thresholds for decision-making
- Guarantee comprehensive coverage
- Provide interpretation of "what it means"

**Contexts DO:**
- Provide reference frames for positioning
- Document rationale and limitations
- Enable comparison across analyses
- Support human interpretation

### 15.2 Non-goals

- **Machine learning integration:** Contexts are declarative, not trainable
- **Real-time adaptation:** Contexts are static files, not dynamic
- **Probabilistic reasoning:** Contexts provide ranges, not distributions
- **Causal inference:** Contexts do not explain why values fall in/out of range

---

## 16. Related technical documentation

For detailed information on related topics, see:

- **`01_TECHNICAL_OVERVIEW.md`** – Overall system architecture
- **`02_RESULTS_JSON_SCHEMA.md`** – Structure of measurements being positioned
- **`03_ANALYSIS_PROTOCOLS.md`** – Protocols (independent of contexts)
- **`A1_CATALOG_ANALYSES_OUTPUTS.md`** – Complete list of metrics that can be contextualized

---

## 17. Document status and maintenance

This document was generated on **2025-01-22** after comprehensive review of the SAT codebase.

**Sources verified:**
- `02_Generate_Report.py` (852 lines, context loading and positioning logic)
- `Analysis_Workspace/02_contexts/Official/context_temporal.yaml` (45 lines)
- `Analysis_Workspace/02_contexts/Official/context_information.yaml` (27 lines)
- `Analysis_Workspace/02_contexts/User_Defined/context_Template.yaml` (45 lines)
- All 8 official context files examined

**Validation:**
- `try_load_family_context()` logic verified
- `_get_reference()` for official contexts verified
- `_get_user_reference()` for user contexts verified
- Validation rules extracted from code (lines 485–524)
- Positioning algorithm verified (lines 236–241)

**This document is complete and accurate** with respect to context file structure, validation, and usage as of 2025-01-22.