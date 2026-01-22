# 05 – Extending SAT

## 1. Purpose and scope

This document provides technical guidance for developers who wish to extend SAT by:
- Adding new analysis methods
- Adding visualization support
- Creating new analysis categories
- Contributing to the codebase

**Document scope:**
- **Technical procedures:** How to extend SAT (steps, code patterns, integration points)
- **Project conventions:** Guidelines for maintainability and consistency (marked as such)
- **Workflow guidance:** Contribution process (section 10)

**This document does NOT:**
- Define runtime guarantees (see `01_TECHNICAL_OVERVIEW.md`)
- Specify output schemas (see `02_RESULTS_JSON_SCHEMA.md`)
- Document protocol structure (see `03_ANALYSIS_PROTOCOLS.md`)

**Target audience:** Python developers familiar with signal processing and SAT's architecture (see `01_TECHNICAL_OVERVIEW.md`).

---

## 2. Prerequisites

### 2.1 Required knowledge

Before extending SAT, you should understand:

- **SAT architecture** (separation of computation, configuration, reporting)
- **Analysis context** (`AnalysisContext` immutable object)
- **Result structure** (`AnalysisResult` dataclass)
- **Registry mechanism** (import-time side-effect registration)

**Required reading:** `01_TECHNICAL_OVERVIEW.md` sections 4-5.

### 2.2 Development environment

**Required:**
- Python 3.9+
- All dependencies from `requirements.txt`
- Git (for version control)

**Recommended:**
- IDE with Python type checking (VS Code, PyCharm)
- pytest (for testing, though tests are not currently included)

---

## 3. Adding a new analysis method

### 3.1 Step-by-step guide

#### Step 1: Choose the appropriate category

Determine which category your method belongs to:

| Category | Purpose | Examples |
|----------|---------|----------|
| `temporal` | Time-domain patterns | Envelope, autocorrelation, pulse detection |
| `spectral` | Frequency-domain characteristics | FFT, peak detection, spectral centroid |
| `time_frequency` | Joint time-frequency analysis | STFT, wavelets, band stability |
| `modulation` | AM/FM/chirp detection | Amplitude modulation, frequency modulation |
| `information` | Entropy and information metrics | Shannon entropy, mutual information |
| `inter_channel` | Stereo relationships | Cross-correlation, phase difference |
| `steganography` | Hidden data detection | LSB analysis, statistical anomalies |
| `meta_analysis` | Higher-order statistics | Stability scores, segment clustering |

**If unsure:** Choose the category closest to your method's primary domain. Creating new categories is discouraged unless absolutely necessary (see section 4).

#### Step 2: Create the analysis function

**Location:** `audio_toolkit/analyses/<category>.py`

**Note:** The following template illustrates a **typical implementation pattern** (per-channel iteration, scalar measurements). This is not mandatory - methods may use global measurements, inter-channel analysis, or other patterns as needed.

**Template (typical pattern, non-mandatory):**
```python
def my_new_method(context: AnalysisContext, params: Dict[str, Any]) -> AnalysisResult:
    """
    Brief description of what this method computes.
    
    Args:
        context: Analysis context containing audio data and metadata
        params: Method-specific parameters (with defaults)
        
    Returns:
        AnalysisResult with measurements, metrics, and optional visualization_data
    """
    # Extract params with defaults
    param1 = params.get('param1', default_value1)
    param2 = params.get('param2', default_value2)
    
    # Initialize result containers
    measurements = {}
    metrics = {}
    visualization_data = {}
    
    # Iterate over all channels
    for channel_name, audio_data in context.audio_data.items():
        
        # Perform analysis
        result_value = compute_something(audio_data, param1, param2)
        
        # Store measurements (per-channel)
        measurements[channel_name] = {
            'metric1': float(result_value),
            'metric2': int(another_value),
            'metric3': list(array_value)  # Limit to ~20 elements if array
        }
        
        # Store visualization data (if applicable)
        visualization_data[channel_name] = {
            'x_axis': x_data,
            'y_axis': y_data
        }
    
    # Store global metrics (method-level, not per-channel)
    metrics = {
        'param1': param1,
        'param2': param2,
        'sample_rate': context.sample_rate
    }
    
    logger.info(f"Computed my_new_method for {len(context.audio_data)} channels")
    
    return AnalysisResult(
        method='my_new_method',
        measurements=measurements,
        metrics=metrics,
        visualization_data=visualization_data
    )
```

#### Step 3: Register the method

**Location:** End of `audio_toolkit/analyses/<category>.py`

```python
# At the end of the module file
register_method(
    "my_new_method",           # Identifier (used in protocols)
    "temporal",                 # Category
    my_new_method,              # Function reference
    "Brief description"         # Human-readable description
)
```

**Registration rules:**
1. Method identifier must be unique across all categories
2. Identifier must be lowercase with underscores (snake_case)
3. Registration must occur at module level (not inside functions)

#### Step 4: Update the category module imports (if needed)

**If you created a new module file:**

Edit `audio_toolkit/analyses/__init__.py`:
```python
from . import temporal  # noqa: F401
from . import spectral  # noqa: F401
# ... existing imports ...
from . import my_new_module  # noqa: F401  # ADD THIS
```

**Note:** The `# noqa: F401` comment suppresses "unused import" warnings. This is intentional (side-effect registration).

### 3.2 Implementation guidelines

#### 3.2.1 Measurements structure

**Per-channel measurements (most common):**
```python
measurements = {
    "left": {
        "mean": 0.5,
        "std": 0.1,
        "peak_count": 15
    },
    "right": {
        "mean": 0.6,
        "std": 0.12,
        "peak_count": 17
    }
}
```

**Global measurements (inter-channel or global properties):**
```python
measurements = {
    "global": {
        "total_events": 50,
        "channel_correlation": 0.85,
        "sync_offset": 123  # samples
    }
}
```

**Best practices:**
- Use scalar types (int, float, bool, str) for top-level metrics
- **Strongly recommended:** Limit arrays to ~20 elements for readability and report compatibility (large arrays go in `visualization_data`)
- Use float() for NumPy float types to ensure JSON serialization
- Avoid nested dicts beyond 2 levels deep

**Note:** Array length is not enforced by the engine, but long arrays in measurements can impact report generation and human readability.

#### 3.2.2 Metrics vs measurements

**`measurements`** (required):
- Raw analysis outputs
- Can be nested (per-channel, per-segment)
- Can include arrays (but keep short)

**`metrics`** (optional):
- Scalar metadata about the analysis
- Configuration values, sample rate, method parameters
- NOT per-channel (method-level only)

**Example:**
```python
measurements = {
    "left": {"rms": 0.5, "peak": 0.9},
    "right": {"rms": 0.6, "peak": 0.95}
}

metrics = {
    "window_size": 1024,
    "method": "hann",
    "sample_rate": 48000
}
```

#### 3.2.3 Performance considerations

**Critical:** Many analysis methods can be O(n²) or worse. Always include performance limits.

**Template:**
```python
def expensive_method(context: AnalysisContext, params: Dict[str, Any]) -> AnalysisResult:
    max_samples = params.get('max_samples', 50000)  # CRITICAL: limit samples
    
    measurements = {}
    
    for channel_name, audio_data in context.audio_data.items():
        # Limit samples for performance
        if len(audio_data) > max_samples:
            audio_subset = audio_data[:max_samples]
            logger.warning(
                f"{method_name}: using first {max_samples} samples "
                f"(out of {len(audio_data)}) for {channel_name}"
            )
        else:
            audio_subset = audio_data
        
        # Perform analysis on subset
        result = compute_expensive_operation(audio_subset)
        
        measurements[channel_name] = {
            'result': result,
            'samples_analyzed': len(audio_subset)
        }
    
    return AnalysisResult(...)
```

**Why this matters:**
- 48 kHz × 60s = 2.88M samples
- Autocorrelation on 2.88M samples ≈ 8.3 trillion operations
- With `max_samples: 100000` → ~10 seconds

**Recommendation:** Default `max_samples` to 50,000–100,000 for O(n²) algorithms.

#### 3.2.4 Error handling

**Best practice:** Let exceptions propagate. The runner will catch and serialize them.

**What you should NOT do:**
```python
# BAD: Silent failure
try:
    result = risky_operation()
except:
    result = None  # Lost error information
```

**What you SHOULD do:**
```python
# GOOD: Let exception propagate
result = risky_operation()
# Runner catches, logs, and serializes error in results.json
```

**When to handle errors internally:**
- Recoverable errors (e.g., fallback to default value)
- Per-channel errors in multi-channel analysis

**Example (partial failure):**
```python
for channel_name, audio_data in context.audio_data.items():
    try:
        result = compute(audio_data)
        measurements[channel_name] = {'value': result}
    except ZeroDivisionError:
        measurements[channel_name] = {}  # Empty indicates failure
        logger.warning(f"Failed to compute for {channel_name}: division by zero")
```

---

## 4. Adding visualization support

### 4.1 When to add visualization

**Add visualization if:**
- Method produces temporal or spectral patterns
- Visual inspection aids interpretation
- Data dimensionality is 1D or 2D

**Skip visualization if:**
- Method produces only scalar values
- Data is high-dimensional (>3D)
- Visualization would be trivial (e.g., single bar chart)

### 4.2 Step-by-step guide

#### Step 1: Populate `visualization_data` in analysis function

```python
def my_method(context: AnalysisContext, params: Dict[str, Any]) -> AnalysisResult:
    # ... analysis code ...
    
    visualization_data = {}
    
    for channel_name, audio_data in context.audio_data.items():
        # Prepare plot-ready data
        visualization_data[channel_name] = {
            'x_axis': x_data.tolist(),  # Convert NumPy to list if needed
            'y_axis': y_data.tolist(),
            'threshold': threshold_value
        }
    
    return AnalysisResult(
        method='my_method',
        measurements=measurements,
        visualization_data=visualization_data  # Include this
    )
```

**Guidelines:**
- Store only data needed for plotting (not intermediate results)
- Use serializable types (lists, floats, ints)
- Downsample large arrays (e.g., limit to 10,000 points)

#### Step 2: Create a plotting function

**Location:** `audio_toolkit/visualization/plots.py`

```python
def plot_my_method(
    x_data: np.ndarray,
    y_data: np.ndarray,
    threshold: float,
    output_path: Path,
    title: str,
    figsize: tuple = (12, 6),
    dpi: int = 150,
    formats: list = ["png"]
) -> None:
    """
    Plot results from my_method.
    
    Args:
        x_data: X-axis data
        y_data: Y-axis data
        threshold: Threshold line to plot
        output_path: Output file path (without extension)
        title: Plot title
        figsize: Figure size in inches
        dpi: Dots per inch
        formats: Output formats (png, svg, pdf)
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Plot main data
    ax.plot(x_data, y_data, linewidth=0.8, color='blue', label='Data')
    
    # Plot threshold
    ax.axhline(threshold, color='red', linestyle='--', label='Threshold')
    
    # Styling
    ax.set_title(title)
    ax.set_xlabel("X Label")
    ax.set_ylabel("Y Label")
    ax.legend()
    ax.grid(True, alpha=0.25)
    
    fig.tight_layout()
    
    # Save
    save_figure(fig, output_path, formats, dpi)
    plt.close(fig)
```

**Guidelines:**
- Use `save_figure()` helper (handles multiple formats)
- Always `plt.close(fig)` to free memory
- Use consistent styling (grid, tight_layout, alpha=0.25)

#### Step 3: Add method to Visualizer class

**Location:** `audio_toolkit/visualization/plots.py`, inside `Visualizer` class

```python
class Visualizer:
    # ... existing methods ...
    
    def plot_my_method(self, x_data, y_data, threshold, output_path, title):
        plot_my_method(
            x_data, y_data, threshold,
            output_path, title,
            self.figsize, self.dpi, self.formats
        )
```

**Note:** The wrapper method delegates to the standalone function, passing config (figsize, dpi, formats).

#### Step 4: Hook into the runner

**Location:** `audio_toolkit/engine/runner.py`, inside `_generate_method_visualization()`

```python
def _generate_method_visualization(self, method: str, viz_data: Dict, viz_dir: Path) -> None:
    # ... existing method blocks ...
    
    # Add your method
    elif method == "my_method":
        for channel, data in viz_data.items():
            if all(k in data for k in ["x_axis", "y_axis", "threshold"]):
                self.visualizer.plot_my_method(
                    np.asarray(data["x_axis"]),
                    np.asarray(data["y_axis"]),
                    float(data["threshold"]),
                    viz_dir / f"my_method_{channel}",
                    f"My Method - {channel}"
                )
```

**Guidelines:**
- Use `if all(k in data for k in [...])` to check required keys
- Convert data to NumPy arrays with `np.asarray()`
- Use consistent naming: `<method>_<channel>.<format>`

### 4.3 Visualization best practices

**Do:**
- Use consistent color schemes (blue for data, red for thresholds/anomalies)
- Add grid with `alpha=0.25` for readability
- Use `fig.tight_layout()` to prevent label clipping
- Limit plot complexity (avoid cluttered plots)

**Don't:**
- Use RGB tuples directly (use named colors or hex)
- Plot millions of points (downsample first)
- Use interactive backends (use `matplotlib.use("Agg")`)
- Forget to close figures (`plt.close(fig)`)

---

## 5. Creating a new analysis category

**Warning:** Creating a new category requires modifications to core schema and package structure. This section documents the technical procedure. For project conventions on when to create categories, see section 5.6.

### 5.1 Technical requirements

**A new category requires:**
- A new module file in `audio_toolkit/analyses/`
- Update to `VALID_CATEGORIES` in `config/schema.py`
- Import in `analyses/__init__.py`
- Official context file in `Analysis_Workspace/02_contexts/Official/`
- Documentation in `A1_CATALOG_ANALYSES_OUTPUTS.md`

### 5.2 Step-by-step guide

#### Step 1: Create the module file

**Location:** `audio_toolkit/analyses/my_new_category.py`

```python
"""
My new category analysis methods.
"""

from typing import Dict, Any
import numpy as np

from ..engine.context import AnalysisContext
from ..engine.results import AnalysisResult
from ..engine.registry import register_method
from ..utils.logging import get_logger

logger = get_logger(__name__)


def method1(context: AnalysisContext, params: Dict[str, Any]) -> AnalysisResult:
    # Implementation
    pass


def method2(context: AnalysisContext, params: Dict[str, Any]) -> AnalysisResult:
    # Implementation
    pass


# Register methods
register_method("method1", "my_new_category", method1, "Description 1")
register_method("method2", "my_new_category", method2, "Description 2")
```

#### Step 2: Update schema

**Location:** `audio_toolkit/config/schema.py`

```python
VALID_CATEGORIES: Set[str] = {
    "preprocessing",
    "temporal",
    "spectral",
    "time_frequency",
    "modulation",
    "information",
    "inter_channel",
    "steganography",
    "meta_analysis",
    "my_new_category"  # ADD THIS
}
```

#### Step 3: Update analyses package

**Location:** `audio_toolkit/analyses/__init__.py`

```python
from . import temporal  # noqa: F401
from . import spectral  # noqa: F401
# ... existing imports ...
from . import my_new_category  # noqa: F401  # ADD THIS
```

#### Step 4: Create official context file

**Location:** `Analysis_Workspace/02_contexts/Official/context_my_new_category.yaml`

```yaml
family: my_new_category

scope:
  coverage: partial
  objective: >
    Brief description of what this category measures.
  rationale: >
    Explanation of scope and limitations.

references:
  - authors: "Your Name"
    title: "Reference Paper"
    year: 2025
    note: "Brief note about relevance."

methods:
  method1:
    metrics:
      metric1:
        reference:
          status: B
          typical_range: [0.0, 1.0]
        notes:
          - "Explanation of metric1."
```

#### Step 5: Document the category

Update `A1_CATALOG_ANALYSES_OUTPUTS.md` (or create it) with your methods.

### 5.6 Project conventions (non-technical guidance)

**Note:** This subsection describes project conventions, not runtime guarantees. The engine will accept any category name in `VALID_CATEGORIES`.

**Recommended category creation criteria:**
- Methods don't fit existing categories semantically
- You have 3+ related methods
- The methods share common preprocessing or conceptual patterns

**Discouraged scenarios:**
- Only 1-2 methods (consider adding to closest existing category)
- One-off experimental methods (consider `meta_analysis` category)
- Category name overlaps with existing category scope

**Rationale:** Excessive category proliferation makes protocol authoring harder and dilutes category semantics. However, this is a convention, not a technical constraint.

---

## 6. Stability rules and backward compatibility

### 6.1 Breaking vs non-breaking changes

**Breaking changes (require major version bump):**
- Removing a method
- Changing method identifier (name)
- Changing required params (removing defaults)
- Changing measurement structure (renaming keys)
- Changing category for existing methods

**Non-breaking changes (allowed in minor versions):**
- Adding new methods
- Adding new optional params
- Adding new measurement keys (additive only)
- Improving performance without changing outputs
- Fixing bugs in calculations

### 6.2 Deprecation process

**If you must break something:**

1. Mark as deprecated in code:
```python
def old_method(context: AnalysisContext, params: Dict[str, Any]) -> AnalysisResult:
    logger.warning("Method 'old_method' is deprecated and will be removed in v2.0. Use 'new_method' instead.")
    # ... existing implementation ...
```

2. Document in release notes
3. Wait at least one minor version before removal
4. Provide migration guide

### 6.3 Metric name stability

**Critical:** Metric names are referenced by context files. Changing a metric name breaks contextualization.

**If you must rename a metric:**
- Support both names for at least one version
- Emit deprecation warning when old name is used in contexts
- Update all official context files

---

## 7. Testing and validation

### 7.1 Manual testing

**Minimal test protocol:**

1. Create a test protocol YAML:
```yaml
version: "1.0"
channels:
  analyze: ["mono"]

analyses:
  my_category:
    enabled: true
    methods:
      - name: my_new_method
        params:
          param1: 42

visualization:
  enabled: true

output:
  save_raw_data: true
  save_config: true
```

2. Run analysis on a test file:
```bash
python 01_run_analysis.py test_audio.flac --config test_protocol.yaml --output test_output
```

3. Verify outputs:
   - `results.json` contains expected measurements
   - Visualizations are generated (if enabled)
   - No errors in console output

4. Generate report:
```bash
python 02_Generate_Report.py test_output
```

5. Verify reports:
   - Measurements appear in `01_MEASUREMENT_SUMMARY.md`
   - If context provided, positioning appears in `03_CONTEXTUAL_POSITIONING.md`

### 7.2 Validation checklist

**Before committing:**
- [ ] Method executes without errors on mono audio
- [ ] Method executes without errors on stereo audio
- [ ] Measurements are serializable (no NumPy types in results.json)
- [ ] Visualization generates (if applicable)
- [ ] Logging provides useful information
- [ ] Performance is acceptable (< 1 minute per minute of audio)
- [ ] Documentation updated (docstrings, context files)

---

## 8. Code style and conventions

### 8.1 Naming conventions

**Methods:** `lowercase_with_underscores`
- Good: `spectral_centroid`, `cross_correlation`, `lsb_analysis`
- Bad: `SpectralCentroid`, `cross-correlation`, `LSBAnalysis`

**Categories:** `lowercase_with_underscores`
- Good: `time_frequency`, `inter_channel`
- Bad: `TimeFrequency`, `inter-channel`

**Measurements:** `lowercase_with_underscores`
- Good: `envelope_mean`, `peak_frequency`, `autocorr_max`
- Bad: `envelopeMean`, `peakFreq`, `autocorrMax`

### 8.2 Type hints

**Required:**
- Function signatures (params and return type)
- Public API methods

**Example:**
```python
def my_method(context: AnalysisContext, params: Dict[str, Any]) -> AnalysisResult:
    max_samples: int = params.get('max_samples', 50000)
    threshold: float = params.get('threshold', 0.5)
    # ...
```

### 8.3 Docstrings

**Required for all public functions:**

```python
def my_method(context: AnalysisContext, params: Dict[str, Any]) -> AnalysisResult:
    """
    Brief one-line description.
    
    Longer explanation if needed. Can span multiple lines.
    Explain what the method does, not how it works.
    
    Args:
        context: Analysis context containing audio data and metadata
        params: Method-specific parameters:
            - param1 (int): Description, default: 1024
            - param2 (float): Description, default: 0.5
        
    Returns:
        AnalysisResult with measurements and optional visualization_data
        
    Raises:
        ValueError: If param1 is negative
    """
```

### 8.4 Logging

**Use structured logging:**
```python
logger.info(f"Starting {method_name} analysis")
logger.debug(f"Using parameters: {params}")
logger.warning(f"Large file detected, limiting to {max_samples} samples")
logger.error(f"Failed to process channel {channel_name}: {e}")
```

**Log levels:**
- `DEBUG`: Detailed diagnostic information
- `INFO`: Informational messages (method start/complete)
- `WARNING`: Recoverable issues (sampling limits, fallbacks)
- `ERROR`: Errors that prevent method completion

---

## 9. Common pitfalls and how to avoid them

### 9.1 Pitfall: NumPy types in measurements

**Problem:** JSON serialization fails with NumPy types.

**Example (BAD):**
```python
measurements[channel] = {
    'mean': np.mean(data)  # Returns np.float64
}
```

**Solution:**
```python
measurements[channel] = {
    'mean': float(np.mean(data))  # Convert to Python float
}
```

### 9.2 Pitfall: Unbounded computation

**Problem:** Method runs for hours on long files.

**Example (BAD):**
```python
def slow_method(context, params):
    for channel, data in context.audio_data.items():
        result = expensive_operation(data)  # No limit!
```

**Solution:**
```python
def fast_method(context, params):
    max_samples = params.get('max_samples', 50000)
    for channel, data in context.audio_data.items():
        subset = data[:max_samples] if len(data) > max_samples else data
        result = expensive_operation(subset)
```

### 9.3 Pitfall: Modifying context

**Problem:** Context is supposed to be immutable.

**Example (BAD):**
```python
def bad_method(context, params):
    context.audio_data['left'] = normalize(context.audio_data['left'])  # Mutation!
```

**Solution:**
```python
def good_method(context, params):
    normalized = normalize(context.audio_data['left'])  # Create new array
    result = analyze(normalized)
```

### 9.4 Pitfall: Silent failures

**Problem:** Errors are swallowed, making debugging impossible.

**Example (BAD):**
```python
try:
    result = compute()
except:
    result = None  # What went wrong?
```

**Solution:**
```python
try:
    result = compute()
except SpecificException as e:
    logger.error(f"Computation failed: {e}")
    raise  # Let runner handle it
```

---

## 10. Contributing to SAT (workflow guidance)

**Note:** This section describes contribution workflow and conventions, not runtime behavior or technical guarantees. The engine does not enforce these rules - they are project governance.

### 10.1 Contribution workflow

1. **Fork the repository**
2. **Create a feature branch:** `git checkout -b feature/my-new-method`
3. **Implement your changes** (follow this guide)
4. **Test thoroughly** (section 7)
5. **Commit with clear messages:** `git commit -m "Add spectral_kurtosis method to spectral category"`
6. **Push to your fork:** `git push origin feature/my-new-method`
7. **Open a pull request** with description of changes

### 10.2 Pull request checklist

- [ ] Code follows style guide (section 8)
- [ ] Method is registered in registry
- [ ] Docstrings are complete
- [ ] Context file created (if new method)
- [ ] Tested on mono and stereo audio
- [ ] No breaking changes (or clearly documented)
- [ ] Visualization added (if applicable)
- [ ] Logging is informative
- [ ] Performance is acceptable

---

## 11. Related technical documentation

For detailed information on related topics, see:

- **`01_TECHNICAL_OVERVIEW.md`** – System architecture and design principles
- **`02_RESULTS_JSON_SCHEMA.md`** – Structure of AnalysisResult measurements
- **`03_ANALYSIS_PROTOCOLS.md`** – How methods are configured and executed
- **`A1_CATALOG_ANALYSES_OUTPUTS.md`** – Complete catalog of existing methods

---

## 12. Document status and maintenance

This document was generated on **2025-01-22** after comprehensive review of the SAT codebase.

**Sources verified:**
- `audio_toolkit/analyses/temporal.py` (262 lines, example implementation)
- `audio_toolkit/engine/registry.py` (172 lines, registration mechanism)
- `audio_toolkit/engine/runner.py` (679 lines, visualization hookup)
- `audio_toolkit/visualization/plots.py` (1408 lines, Visualizer class)
- Multiple analysis modules examined for patterns

**This document provides complete guidance** for extending SAT with new methods, visualizations, and categories as of 2025-01-22.