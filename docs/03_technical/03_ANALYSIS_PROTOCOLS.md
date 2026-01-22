# 03 – Analysis Protocols

## 1. Purpose and role

Analysis protocols are **YAML configuration files** that define:
- Which analyses are executed
- Which audio channels are analyzed
- How audio is preprocessed
- Visualization and output settings

**Key properties:**
- Declarative (no procedural logic)
- Validated at load time by `ConfigLoader`
- Consumed exclusively by `01_run_analysis.py`
- Independent of context files (contexts are for reporting only)

**Location:** Protocols are typically stored in `Analysis_Workspace/01_protocols/`.

---

## 2. Minimal valid protocol

The **absolute minimum** required for a valid protocol:

```yaml
version: "1.0"

channels:
  analyze:
    - left

analyses:
  temporal:
    enabled: true
    methods:
      - name: envelope
```

**Required top-level keys:**
- `version` (string)
- `channels` (object with `analyze` array)
- `analyses` (object with at least one category)

**All other sections are optional.**

---

## 3. Top-level structure

A complete protocol has the following top-level sections:

```yaml
version: "<version_string>"

channels: { ... }

preprocessing: { ... }      # Optional

analyses: { ... }

visualization: { ... }      # Optional

output: { ... }             # Optional
```

### 3.1 Execution order

When `01_run_analysis.py` loads a protocol:

1. **Validation**: `ConfigLoader.validate()` checks all required keys and values
2. **Audio loading**: File is loaded via `soundfile`
3. **Channel extraction**: Channels listed in `channels.analyze` are extracted
4. **Preprocessing**: Normalization and segmentation (if enabled)
5. **Analysis execution**: Methods from enabled categories are executed
6. **Visualization**: Plots generated (if `visualization.enabled: true`)
7. **Output**: `results.json` and optionally `config_used.json` are saved

---

## 4. Version field

### 4.1 Syntax

```yaml
version: "1.0"
```

**Type:** String (quoted)

**Required:** Yes

**Purpose:** Indicates the protocol schema version. Currently, only `"1.0"` is defined.

### 4.2 Validation

- Must be present
- Must be a string
- No semantic validation (any string accepted)
- Stored in `metadata.config_version` in `results.json`

### 4.3 Usage

The version field is **informational**. It does not affect execution behavior but allows:
- Protocol evolution tracking
- Backward compatibility detection (future use)
- Reproducibility (recorded in results.json)

---

## 5. Channels section

### 5.1 Purpose

Defines which audio channels to analyze.

### 5.2 Syntax

```yaml
channels:
  analyze:
    - left
    - right
    - mono
    - sum
    - difference
```

**`analyze`** (array of strings, required):
- List of channel names to extract and analyze
- Cannot be empty
- Order does not matter

### 5.3 Valid channel names

| Channel | Description | Availability |
|---------|-------------|--------------|
| `left` | Left channel | Always (mono files → duplicated) |
| `right` | Right channel | Stereo files only |
| `mono` | Mono mix (average of all channels) | Always |
| `sum` | L + R | Stereo files only |
| `difference` | L - R | Stereo files only |

### 5.4 Validation rules

**Enforced by `ConfigLoader._validate_channels()`:**

1. `channels` must be a dictionary
2. `channels.analyze` must be present
3. `channels.analyze` must be a list
4. `channels.analyze` cannot be empty
5. All channel names must be in `VALID_CHANNELS` set

**Raises `ValueError` if validation fails.**

### 5.5 Examples

**Minimal (mono analysis):**
```yaml
channels:
  analyze:
    - mono
```

**Stereo analysis:**
```yaml
channels:
  analyze:
    - left
    - right
```

**Stereo with derived channels:**
```yaml
channels:
  analyze:
    - left
    - right
    - sum
    - difference
```

### 5.6 Runtime behavior

**If mono file + `right` requested:**
- `ChannelProcessor.extract_channels()` duplicates mono data to `right`
- No error, but logged as warning

**If mono file + `sum` or `difference` requested:**
- Raises `ValueError`: `"Cannot compute 'sum': need stereo audio"`

---

## 6. Preprocessing section

### 6.1 Purpose

Defines optional preprocessing steps applied to audio before analysis.

### 6.2 Syntax

```yaml
preprocessing:
  normalize:
    enabled: true
    method: rms           # or 'lufs'
    target_level: -20.0   # in dB
  
  segmentation:
    enabled: true
    method: energy        # or 'spectral'
    segment_duration: 1.0 # in seconds
```

**Both subsections (`normalize`, `segmentation`) are optional.**

### 6.3 Normalization

**Purpose:** Standardize audio levels for cross-file comparison.

#### 6.3.1 Normalization parameters

**`enabled`** (boolean, default: `false`)
- If `false`, no normalization is applied

**`method`** (string, default: `"rms"`)
- `"rms"`: Root Mean Square normalization
- `"lufs"`: Simplified LUFS approximation (uses RMS internally with warning)

**`target_level`** (float, default: `-20.0`)
- Target level in dB
- Typical range: `-30.0` to `-6.0`

#### 6.3.2 Validation

**Enforced by `ConfigLoader._validate_preprocessing()`:**

1. `method` must be in `VALID_NORMALIZATION_METHODS` (`{"rms", "lufs"}`)
2. If invalid method → `ValueError`

**No validation of `target_level` value** (any float accepted).

#### 6.3.3 Examples

**RMS normalization (recommended):**
```yaml
preprocessing:
  normalize:
    enabled: true
    method: rms
    target_level: -20.0
```

**LUFS normalization (simplified):**
```yaml
preprocessing:
  normalize:
    enabled: true
    method: lufs
    target_level: -23.0
```

**Important:** Current LUFS implementation is a simplified RMS approximation. For production-grade ITU-R BS.1770-4 LUFS, consider using `pyloudnorm` externally.

**Disabled:**
```yaml
preprocessing:
  normalize:
    enabled: false
```

### 6.4 Segmentation

**Purpose:** Divide audio into temporal segments for segment-wise analysis.

#### 6.4.1 Segmentation parameters

**`enabled`** (boolean, default: `false`)
- If `false`, audio is treated as a single segment

**`method`** (string, default: `"energy"`)
- `"energy"`: Fixed-duration energy-based segmentation
- `"spectral"`: Fixed-duration spectral-based segmentation

**`segment_duration`** (float, default: `1.0`)
- Segment duration in seconds
- Segments shorter than half this duration are discarded (spectral method only)

#### 6.4.2 Validation

**Enforced by `Preprocessor.segment_audio()`:**

1. `method` must be in `{"energy", "spectral"}`
2. If invalid method → `ValueError`

**No validation of `segment_duration` value** (any positive float accepted).

#### 6.4.3 Examples

**Energy-based segmentation:**
```yaml
preprocessing:
  segmentation:
    enabled: true
    method: energy
    segment_duration: 1.0
```

**Spectral-based segmentation:**
```yaml
preprocessing:
  segmentation:
    enabled: true
    method: spectral
    segment_duration: 2.0
```

**Disabled (default):**
```yaml
preprocessing:
  segmentation:
    enabled: false
```

#### 6.4.4 Runtime behavior

**When enabled:**
- Segments computed from first channel
- Applied to all channels
- Stored in `AnalysisContext.segments` as `List[Tuple[int, int]]` (sample indices)

**When disabled:**
- Single segment: `[(0, len(audio))]`

**Note:** Most current analysis methods ignore segments and operate on full channels. Future methods may use segment information.

---

## 7. Analyses section

### 7.1 Purpose

Defines which analysis methods to execute, organized by category.

### 7.2 Syntax

```yaml
analyses:
  <category>:
    enabled: true|false
    methods:
      - name: <method_name>
        params:
          <param_key>: <param_value>
          ...
      - name: <method_name>  # params optional
```

### 7.3 Valid categories

From `config/schema.py::VALID_CATEGORIES`:

| Category | Module | Methods Available |
|----------|--------|-------------------|
| `temporal` | `temporal.py` | 4 methods |
| `spectral` | `spectral.py` | 9 methods |
| `time_frequency` | `time_frequency.py` | 3 methods |
| `modulation` | `modulation.py` | 5 methods |
| `information` | `information.py` | 5 methods |
| `inter_channel` | `inter_channel.py` | 4 methods |
| `steganography` | `steganography.py` | 5 methods |
| `meta_analysis` | `meta_analysis.py` | 4 methods |

**Special category:** `preprocessing` is listed in `VALID_CATEGORIES` but is handled separately (not an analysis category).

### 7.4 Category structure

Each category is an object with:

**`enabled`** (boolean, required)
- If `false`, entire category is skipped
- All methods in category are ignored

**`methods`** (array of objects, required if `enabled: true`)
- List of methods to execute
- Each method is an object with `name` and optional `params`

### 7.5 Method structure

Each method object has:

**`name`** (string, required)
- Method identifier
- Must match a registered method in the registry
- See `A1_CATALOG_ANALYSES_OUTPUTS.md` for complete list

**`params`** (object, optional)
- Method-specific parameters
- Merged with default params from registry
- Protocol params override defaults

### 7.6 Validation rules

**Enforced by `ConfigLoader._validate_analyses()`:**

1. `analyses` must be a dictionary
2. Unknown categories → **Warning logged, not error**
3. Each category config must be a dictionary
4. If `enabled: true`, `methods` must be a list
5. Each method must be a dictionary with `name` field

**Not validated:**
- Method name existence (checked at runtime against registry)
- Param keys/values (method-specific, validated by method code)

### 7.7 Examples

**Single category, single method:**
```yaml
analyses:
  temporal:
    enabled: true
    methods:
      - name: envelope
```

**Single category, multiple methods with params:**
```yaml
analyses:
  spectral:
    enabled: true
    methods:
      - name: fft_global
        params:
          window: hann
      
      - name: peak_detection
        params:
          prominence: 0.05
          distance: 50
      
      - name: spectral_centroid
```

**Multiple categories:**
```yaml
analyses:
  temporal:
    enabled: true
    methods:
      - name: envelope
      - name: autocorrelation
        params:
          max_lag: 5000
          max_samples: 100000
  
  spectral:
    enabled: true
    methods:
      - name: fft_global
  
  information:
    enabled: false  # Category disabled
```

### 7.8 Method execution order

**Execution order:**
1. Categories processed in arbitrary order (dict iteration)
2. Within a category, methods executed in listed order
3. Each method isolated (failure does not stop others)

**Critical:** Consumers MUST NOT rely on category execution order, even if current implementations preserve insertion order. This is not a contractual guarantee and may change in future implementations.

**Practical implication:** Methods should be independent and not depend on results from other categories.

### 7.9 Disabled categories

**Best practice:**
```yaml
analyses:
  steganography:
    enabled: false
```

**Alternative (implicit disable):**
- Omit the category entirely from `analyses` section
- Equivalent to `enabled: false`

---

## 8. Visualization section

### 8.1 Purpose

Controls visualization generation during analysis execution.

### 8.2 Syntax

```yaml
visualization:
  enabled: true
  formats:
    - png
    - svg
    - pdf
  dpi: 150
  figsize: [12, 8]
```

**All fields optional.** If `visualization` section omitted, defaults to `enabled: false`.

### 8.3 Parameters

**`enabled`** (boolean, default: `false`)
- If `true`, visualizations generated during analysis
- If `false`, no plots created (faster execution)

**`formats`** (array of strings, default: `["png"]`)
- Output formats for plots
- Valid values: `"png"`, `"svg"`, `"pdf"`
- Multiple formats allowed

**`dpi`** (integer, default: `100`)
- Dots per inch for raster formats (png)
- Higher values → larger file size, better quality
- Typical range: `72` to `300`

**`figsize`** (array of 2 numbers, default: `[10, 6]`)
- Figure size in inches: `[width, height]`
- Affects plot dimensions and readability

### 8.4 Validation

**Enforced by `ConfigLoader._validate_visualization()`:**

1. `formats` must be a list
2. Each format must be in `VALID_VISUALIZATION_FORMATS` (`{"png", "svg", "pdf"}`)
3. If invalid format → `ValueError`

**Not validated:**
- `dpi` value (any integer accepted)
- `figsize` structure (any array accepted)

### 8.5 Examples

**Enabled with defaults:**
```yaml
visualization:
  enabled: true
```

**High-quality PNG output:**
```yaml
visualization:
  enabled: true
  formats: ["png"]
  dpi: 300
  figsize: [16, 10]
```

**Multiple formats:**
```yaml
visualization:
  enabled: true
  formats:
    - png
    - svg
  dpi: 150
```

**Disabled (default):**
```yaml
visualization:
  enabled: false
```

Or omit section entirely.

### 8.6 Output location

Plots saved to: `<output_dir>/visualizations/`

**Naming convention:**
- Basic plots: `waveform_<channel>.png`, `spectrum_<channel>.png`
- Method plots: `<method_name>_<channel>.png`

---

## 9. Output section

### 9.1 Purpose

Controls output file generation and format.

### 9.2 Syntax

```yaml
output:
  save_raw_data: true
  save_config: true
  export_formats:
    - json
    - csv
```

**All fields optional.** Defaults to `save_raw_data: true`, others `false`.

### 9.3 Parameters

**`save_raw_data`** (boolean, default: `true`)
- If `true`, writes `results.json`
- **Critical:** Setting `save_raw_data: false` makes the analysis effectively non-auditable and incompatible with reporting. Without `results.json`, the reporting script (`02_Generate_Report.py`) cannot function, and no record of measurements exists.

**`save_config`** (boolean, default: `false`)
- If `true`, writes `config_used.json` (copy of loaded protocol)
- Useful for reproducibility

**`export_formats`** (array of strings, default: `["json"]`)
- Output formats for results
- Valid values: `"json"`, `"csv"`
- **Note:** CSV export is experimental/incomplete. CSV export is not guaranteed to cover all measurements and may omit complex nested structures.

### 9.4 Validation

**Enforced by `ConfigLoader._validate_output()`:**

1. `export_formats` must be a list
2. Each format must be in `VALID_EXPORT_FORMATS` (`{"json", "csv"}`)
3. If invalid format → `ValueError`

**Not validated:**
- `save_raw_data` type (any value accepted, coerced to bool)
- `save_config` type (any value accepted, coerced to bool)

### 9.5 Examples

**Standard output (results.json only):**
```yaml
output:
  save_raw_data: true
  save_config: false
```

**Full output (results + config):**
```yaml
output:
  save_raw_data: true
  save_config: true
```

**No output (not recommended):**
```yaml
output:
  save_raw_data: false
```

### 9.6 Output files

**Generated files:**
- `results.json` (if `save_raw_data: true`)
- `config_used.json` (if `save_config: true`)
- `visualizations/*.png` (if `visualization.enabled: true`)

**Location:** `<output_dir>` specified via `--output` CLI arg or default `output/<audio_stem>/`

---

## 10. Complete example protocols

### 10.1 Minimal protocol

```yaml
version: "1.0"

channels:
  analyze:
    - mono

analyses:
  temporal:
    enabled: true
    methods:
      - name: envelope
```

### 10.2 Baseline protocol (comprehensive)

```yaml
version: "1.0"

channels:
  analyze:
    - left
    - right
    - difference

preprocessing:
  normalize:
    enabled: true
    method: rms
    target_level: -20.0

analyses:
  temporal:
    enabled: true
    methods:
      - name: envelope
        params:
          method: hilbert
      - name: autocorrelation
        params:
          max_lag: 5000
          max_samples: 100000

  spectral:
    enabled: true
    methods:
      - name: fft_global
        params:
          window: hann
      - name: peak_detection
      - name: spectral_centroid

  information:
    enabled: true
    methods:
      - name: shannon_entropy
      - name: local_entropy

visualization:
  enabled: true
  formats: ["png"]
  dpi: 150

output:
  save_raw_data: true
  save_config: true
```

### 10.3 Focused protocol (single category)

```yaml
version: "1.0"

channels:
  analyze:
    - left
    - right

preprocessing:
  normalize:
    enabled: false

analyses:
  information:
    enabled: true
    methods:
      - name: shannon_entropy
      - name: local_entropy
        params:
          window_size: 1024
          hop_length: 512
      - name: compression_ratio
      - name: mutual_information
        params:
          num_bins: 64

visualization:
  enabled: true
  formats: ["png"]

output:
  save_raw_data: true
  save_config: true
```

---

## 11. Protocol validation and error handling

### 11.1 Validation stages

**Stage 1: YAML parsing** (by PyYAML)
- Syntax errors → `yaml.YAMLError`
- Example: malformed YAML, invalid indentation

**Stage 2: Structure validation** (by `ConfigLoader.validate()`)
- Missing required keys → `ValueError`
- Invalid types → `ValueError`
- Invalid enum values → `ValueError`

**Stage 3: Runtime validation** (by analysis engine)
- Unknown method names → Warning logged, method skipped
- Invalid params → Caught by method, logged as error in results
- File I/O errors → `FileNotFoundError`, `RuntimeError`

### 11.2 Validation guarantees

**Guaranteed to be validated:**
- Required top-level keys (`version`, `channels`, `analyses`)
- `channels.analyze` is non-empty list of valid channel names
- Normalization method in `{"rms", "lufs"}`
- Visualization formats in `{"png", "svg", "pdf"}`
- Output formats in `{"json", "csv"}`

**Not validated (passed to runtime):**
- Method names (checked against registry at execution)
- Method params (method-specific, validated by method code)
- Numeric parameter ranges (e.g., `target_level`, `dpi`)

### 11.3 Error messages

**Missing required key:**
```
ValueError: Missing required configuration key: 'channels'
```

**Invalid channel:**
```
ValueError: Invalid channel 'center'. Valid channels: {'left', 'right', 'mono', 'sum', 'difference'}
```

**Invalid normalization method:**
```
ValueError: Invalid normalization method 'peak'. Valid methods: {'rms', 'lufs'}
```

**Unknown category (warning only):**
```
WARNING: Unknown analysis category 'custom_category'. Valid categories: {...}
```

### 11.4 Best practices

**Do:**
- Validate protocols with small test files before large runs
- Check logs for warnings about unknown categories/methods
- Use `save_config: true` to archive exact protocol used

**Don't:**
- Assume all params are validated (some are runtime-only)
- Rely on specific error message text (may change)
- Use protocols with `save_raw_data: false` (loses results)

---

## 12. Protocol organization conventions

### 12.1 Directory structure

**Recommended layout:**
```
Analysis_Workspace/
└── 01_protocols/
    ├── 01_Baseline/
    │   └── protocol_baseline_full.yaml
    └── 02_Focused/
        ├── 01_temporal.yaml
        ├── 02_spectral.yaml
        ├── 05_information.yaml
        └── custom_protocol.yaml
```

**Conventions:**
- `01_Baseline/`: Comprehensive protocols testing all/most methods
- `02_Focused/`: Category-specific protocols for targeted analysis

### 12.2 Naming conventions

**Filename patterns:**
- `protocol_<purpose>.yaml` (e.g., `protocol_baseline_full.yaml`)
- `<category>.yaml` (e.g., `temporal.yaml`, `information.yaml`)
- `<use_case>.yaml` (e.g., `morse_encoding_oriented.yaml`)

**Version in filename:**
- Not recommended (version in YAML is sufficient)
- Exception: major schema changes may warrant `_v2.yaml` suffix

---

## 13. Protocol vs context files

### 13.1 Relationship

| Aspect | Protocols | Contexts |
|--------|-----------|----------|
| **Purpose** | Define analysis execution | Define reference ranges |
| **Consumed by** | `01_run_analysis.py` | `02_Generate_Report.py` |
| **Location** | `01_protocols/` | `02_contexts/` |
| **Format** | YAML | YAML |
| **Affects computation** | Yes | No |
| **Affects presentation** | No | Yes |

### 13.2 Independence

**Critical:** Protocols and contexts are **completely independent**.

- Changing a context does NOT require re-running analysis
- Changing a protocol DOES require re-running analysis
- Same `results.json` can be re-reported with different contexts

---

## 14. Performance considerations

### 14.1 Performance-critical parameters

**In method params:**
- `max_samples` (autocorrelation, cross_correlation, etc.)
  - Higher values → longer runtime, more accuracy
  - Default: 50000–100000
  - Recommendation: Keep defaults unless specific need

**In preprocessing:**
- `segment_duration` (segmentation)
  - Smaller values → more segments, longer runtime
  - Default: 1.0s
  - Recommendation: Use 1.0–5.0s

**In visualization:**
- `dpi`
  - Higher values → larger files, longer I/O
  - Default: 100–150
  - Recommendation: 150 for reports, 300 for publication

### 14.2 Execution time estimates

**Important:** These estimates depend heavily on audio duration, sample rate, hardware specifications, and the specific set of enabled methods. Use as rough guidelines only.

**Minimal protocol (1 category, 1 method):**
- ~5–30 seconds per minute of audio

**Baseline protocol (all categories):**
- ~10–15 minutes per minute of audio (with performance limits)
- Without `max_samples` limits: hours to days

**With visualization enabled:**
- +50% execution time (plot generation)

---

## 15. Schema evolution and stability

### 15.1 Stability guarantees

**Stable (will not change):**
- Required top-level keys: `version`, `channels`, `analyses`
- `channels.analyze` structure
- Category names (temporal, spectral, etc.)
- Validation behavior for invalid enum values

**May change (backward-compatible additions):**
- New optional top-level sections
- New valid channel types
- New normalization methods
- New categories

**Breaking changes (require version bump):**
- Removing required keys
- Changing validation semantics
- Renaming categories

### 15.2 Forward compatibility

**Current behavior:**
- Unknown categories → Warning, not error
- Unknown top-level keys → Ignored
- Unknown params → Passed to methods (method decides)

**Recommendation:**
- Avoid using undocumented keys (may conflict with future additions)
- Stick to documented enum values

---

## 16. Related technical documentation

For detailed information on related topics, see:

- **`01_TECHNICAL_OVERVIEW.md`** – Overall system architecture
- **`02_RESULTS_JSON_SCHEMA.md`** – Output structure produced by protocol execution
- **`04_CONTEXT_FILES_TECHNICAL.md`** – Context files for reporting (independent of protocols)
- **`A1_CATALOG_ANALYSES_OUTPUTS.md`** – Complete list of method names and params

---

## 17. Document status and maintenance

This document was generated on **2025-01-22** after comprehensive review of the SAT codebase.

**Sources verified:**
- `audio_toolkit/config/schema.py` (47 lines)
- `audio_toolkit/config/loader.py` (196 lines)
- `audio_toolkit/engine/runner.py` (679 lines, preprocessing section)
- `audio_toolkit/audio/preprocessing.py` (205 lines)
- `Analysis_Workspace/01_protocols/01_Baseline/protocol_baseline_full.yaml` (116 lines)
- `Analysis_Workspace/01_protocols/02_Focused/05_information.yaml` (37 lines)

**Validation:**
- All constants from `schema.py` verified
- All validation rules from `loader.py` documented
- All examples tested against actual protocol files
- Segmentation methods verified in `preprocessing.py`

**This document is complete and accurate** with respect to the protocol schema and validation system as of 2025-01-22.