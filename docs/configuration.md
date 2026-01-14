# Configuration Reference 

This document defines the **configuration contract** as implemented by the current codebase.

It documents:

* required keys
* keys that have a **direct effect** on execution
* keys that are **accepted/validated but currently unused** (explicitly marked)

No undocumented key is relied upon by the engine.

---

## Root structure

```yaml
version: "1.0"
channels:
analyses:
preprocessing:   # optional
visualization:   # optional
output:          # optional
```

### Required root keys

| Key        | Type   | Required | Notes                                                               |
| ---------- | ------ | -------- | ------------------------------------------------------------------- |
| `version`  | string | ✅        | Required by validation. Stored in run metadata as `config_version`. |
| `channels` | dict   | ✅        | Must contain `channels.analyze`.                                    |
| `analyses` | dict   | ✅        | May be empty, but must be a dictionary.                             |

---

## channels

### channels.analyze

Select channels to analyze.

| Key       | Type         | Required | Description                              |
| --------- | ------------ | -------- | ---------------------------------------- |
| `analyze` | list[string] | ✅        | List of channels to extract and analyze. |

Allowed values:

* `left`
* `right`
* `mono`
* `sum`
* `difference`

---

## preprocessing (optional)

### preprocessing.normalize

Global level normalization applied **before** analysis.

| Key            | Type   | Default | Effect                                                            |
| -------------- | ------ | ------: | ----------------------------------------------------------------- |
| `enabled`      | bool   | `false` | If true, normalization is applied per channel.                    |
| `method`       | string | `"rms"` | `"rms"` or `"lufs"` (LUFS uses simplified RMS approximation).     |
| `target_level` | float  | `-20.0` | Target level in dB (or LUFS target for the simplified LUFS path). |

---

### preprocessing.segmentation

Temporal segmentation used to define `context.segments`.

| Key                | Type   |    Default | Effect                                                                             |
| ------------------ | ------ | ---------: | ---------------------------------------------------------------------------------- |
| `enabled`          | bool   |    `false` | If false, a single segment covering the whole signal is used.                      |
| `method`           | string | `"energy"` | `"energy"` or `"spectral"` (both are fixed-duration segmentation in current code). |
| `segment_duration` | float  |      `1.0` | Segment size in seconds.                                                           |

---

### preprocessing.silence_detection (accepted but currently unused)

| Key            | Type  | Default | Effect                                            |
| -------------- | ----- | ------: | ------------------------------------------------- |
| `enabled`      | bool  | `false` | **No effect in the current runner** (not called). |
| `threshold_db` | float | `-40.0` | Validated only.                                   |
| `min_duration` | float |   `0.1` | Validated only.                                   |

Notes:

* The silence detection implementation exists (`Preprocessor.detect_silence`) but is not invoked by the current pipeline.
* If provided, this block is preserved in metadata (`metadata.preprocessing`).

---

## analyses (required)

`analyses` is a dictionary of categories. Each category follows the same structure:

```yaml
analyses:
  <category_name>:
    enabled: true|false
    methods:
      - name: <registry_identifier>
        params: { ... }
```

### Category behavior

* If `enabled` is false or missing → the category is skipped.
* If `enabled` is true → `methods` must be a list.
* Each method entry must be a dict containing `name`.
* `params` is optional and defaults to `{}`.
* Runtime parameters are computed as:

  * `merged_params = {**registry.default_params, **params}`

### Validated categories

The validator knows these categories:

* `preprocessing`
* `temporal`
* `spectral`
* `time_frequency`
* `modulation`
* `information`
* `inter_channel`
* `steganography`
* `meta_analysis`

Unknown categories are not rejected; they trigger a warning during validation.

---

## visualization (optional)

### visualization.enabled

| Key       | Type | Default | Effect                                                            |
| --------- | ---- | ------: | ----------------------------------------------------------------- |
| `enabled` | bool | `false` | If true, the runner generates images in `output/visualizations/`. |

### visualization.formats

| Key       | Type         |   Default | Effect                                            |
| --------- | ------------ | --------: | ------------------------------------------------- |
| `formats` | list[string] | `["png"]` | Output formats for figures (`png`, `svg`, `pdf`). |

### visualization.dpi

| Key   | Type | Default | Effect                                 |
| ----- | ---- | ------: | -------------------------------------- |
| `dpi` | int  |   `150` | Raster resolution when saving figures. |

### visualization.figsize

| Key       | Type         |   Default | Effect                                              |
| --------- | ------------ | --------: | --------------------------------------------------- |
| `figsize` | list[number] | `[12, 8]` | Matplotlib figure size in inches `[width, height]`. |

---

## output (optional)

### output.save_raw_data

| Key             | Type | Default | Effect                                                      |
| --------------- | ---- | ------: | ----------------------------------------------------------- |
| `save_raw_data` | bool |  `true` | If true, saves `results.json` (without visualization data). |

### output.save_config

| Key           | Type | Default | Effect                                                       |
| ------------- | ---- | ------: | ------------------------------------------------------------ |
| `save_config` | bool |  `true` | If true, saves `config_used.json` (the full config as used). |

### output.export_formats (accepted but currently unused)

| Key              | Type         |  Default | Effect                                                |
| ---------------- | ------------ | -------: | ----------------------------------------------------- |
| `export_formats` | list[string] | *(none)* | **No effect in the current runner** (validated only). |

Notes:

* The validator checks `export_formats` values (`json`, `csv`), but the runner always writes JSON only.

---

## Minimal working configuration example

```yaml
version: "1.0"

channels:
  analyze: ["left", "right", "difference"]

analyses:
  temporal:
    enabled: true
    methods:
      - name: "autocorrelation"
        params:
          max_lag: 2000
          max_samples: 50000

visualization:
  enabled: true
  formats: ["png"]
  dpi: 150

output:
  save_raw_data: true
  save_config: true
```
