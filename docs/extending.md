# Extending the Pipeline

This guide explains how to add new analysis methods to the pipeline without modifying the core engine.

## Overview

Adding a new analysis method requires three steps:

1. Implement the analysis function
2. Register it in the registry
3. Activate it in a configuration file

The engine requires no modification.

## Step 1: Implement the Analysis Function

### Function Signature

```python
from typing import Dict, Any
from audio_toolkit.engine.context import AnalysisContext
from audio_toolkit.engine.results import AnalysisResult

def my_analysis(context: AnalysisContext, params: Dict[str, Any]) -> AnalysisResult:
    """
    Brief description of what this analysis does.
    
    Args:
        context: Analysis context containing audio data and metadata
        params: Method-specific parameters from configuration
    
    Returns:
        AnalysisResult containing measurements and metrics
    """
    # Implementation here
    pass
```

### Context Structure

The `AnalysisContext` provides:

```python
context.audio_data: Dict[str, np.ndarray]  # Audio per channel
context.sample_rate: int                    # Sample rate in Hz
context.segments: List[Tuple[int, int]]     # Temporal segments (if any)
context.metadata: Dict[str, Any]            # Execution metadata
```

### Parameter Handling

```python
def my_analysis(context: AnalysisContext, params: Dict[str, Any]) -> AnalysisResult:
    # Extract parameters with defaults
    window_size = params.get('window_size', 1024)
    threshold = params.get('threshold', 0.5)
    
    # Validate parameters
    if window_size <= 0:
        raise ValueError("window_size must be positive")
    
    # Perform analysis
    result = compute_something(context.audio_data, window_size, threshold)
    
    # Return structured result
    return AnalysisResult(
        method="my_analysis",
        measurements={"value": result},
        metrics={"derived_metric": result * 2},
        anomaly_score=compute_anomaly(result)
    )
```

### Result Structure

```python
AnalysisResult(
    method: str,                      # Method identifier
    measurements: Dict[str, Any],     # Raw measurements
    metrics: Dict[str, Any],          # Derived metrics
    anomaly_score: Optional[float],   # 0-1 score if applicable
    visualization_data: Optional[Dict] # Data for plotting
)
```

## Step 2: Register the Method

### In the Appropriate Module

Add your function to the relevant analysis module (e.g., `analyses/temporal.py`):

```python
# analyses/temporal.py

def my_new_temporal_analysis(context: AnalysisContext, params: Dict[str, Any]) -> AnalysisResult:
    """Implementation here"""
    pass

# Register the method
from audio_toolkit.engine.registry import register_method

register_method(
    identifier="my_new_temporal_analysis",
    category="temporal",
    function=my_new_temporal_analysis,
    description="Brief description of the method",
    default_params={
        "window_size": 1024,
        "threshold": 0.5
    }
)
```

### Registry Properties

Each registered method has:

- `identifier`: Unique string used in configuration
- `category`: Analysis category (temporal, spectral, etc.)
- `function`: The actual implementation
- `description`: Human-readable description
- `default_params`: Default parameter values

## Step 3: Activate in Configuration

Add the method to your YAML configuration:

```yaml
analyses:
  temporal:
    enabled: true
    methods:
      - name: "my_new_temporal_analysis"
        params:
          window_size: 2048
          threshold: 0.7
```

## Best Practices

### Parameter Validation

Always validate parameters at the start of your function:

```python
def my_analysis(context: AnalysisContext, params: Dict[str, Any]) -> AnalysisResult:
    # Validate required parameters
    if 'required_param' not in params:
        raise ValueError("required_param must be specified")
    
    # Validate parameter ranges
    window_size = params.get('window_size', 1024)
    if window_size < 16 or window_size > context.audio_data['left'].size:
        raise ValueError(f"window_size must be between 16 and {context.audio_data['left'].size}")
```

### Channel Handling

Process all requested channels:

```python
def my_analysis(context: AnalysisContext, params: Dict[str, Any]) -> AnalysisResult:
    measurements = {}
    
    for channel_name, audio_data in context.audio_data.items():
        result = process_channel(audio_data, params)
        measurements[channel_name] = result
    
    return AnalysisResult(
        method="my_analysis",
        measurements=measurements
    )
```

### Error Handling

Handle edge cases gracefully:

```python
def my_analysis(context: AnalysisContext, params: Dict[str, Any]) -> AnalysisResult:
    try:
        result = risky_computation(context.audio_data)
    except ZeroDivisionError:
        # Return safe fallback
        return AnalysisResult(
            method="my_analysis",
            measurements={"error": "Zero division encountered"},
            anomaly_score=None
        )
```

### Documentation

Document your method thoroughly:

```python
def my_analysis(context: AnalysisContext, params: Dict[str, Any]) -> AnalysisResult:
    """
    Compute something interesting from audio data.
    
    This method analyzes [specific property] by applying [technique].
    
    Args:
        context: Analysis context
        params: Configuration parameters:
            - window_size (int): Size of analysis window (default: 1024)
            - threshold (float): Detection threshold (default: 0.5)
    
    Returns:
        AnalysisResult with measurements:
            - value: Primary measurement
            - confidence: Confidence score (0-1)
    
    Raises:
        ValueError: If parameters are invalid
    
    References:
        - Author et al. (2020). "Paper Title". Journal.
    """
    pass
```

## Example: Complete New Method

Here's a complete example of adding a new spectral method:

```python
# analyses/spectral.py

import numpy as np
from scipy import signal
from audio_toolkit.engine.context import AnalysisContext
from audio_toolkit.engine.results import AnalysisResult
from audio_toolkit.engine.registry import register_method

def spectral_rolloff(context: AnalysisContext, params: Dict[str, Any]) -> AnalysisResult:
    """
    Compute spectral rolloff frequency.
    
    The spectral rolloff is the frequency below which a specified percentage
    of the total spectral energy is contained.
    
    Args:
        context: Analysis context
        params: Configuration parameters:
            - rolloff_percent (float): Percentage threshold (default: 0.85)
            - n_fft (int): FFT size (default: 2048)
    
    Returns:
        AnalysisResult with rolloff frequencies per channel
    """
    # Extract parameters
    rolloff_percent = params.get('rolloff_percent', 0.85)
    n_fft = params.get('n_fft', 2048)
    
    # Validate
    if not 0 < rolloff_percent < 1:
        raise ValueError("rolloff_percent must be between 0 and 1")
    
    measurements = {}
    
    for channel_name, audio_data in context.audio_data.items():
        # Compute spectrum
        freqs, spectrum = signal.periodogram(
            audio_data,
            fs=context.sample_rate,
            nfft=n_fft
        )
        
        # Compute cumulative energy
        cumulative_energy = np.cumsum(spectrum)
        total_energy = cumulative_energy[-1]
        
        # Find rolloff frequency
        rolloff_idx = np.where(cumulative_energy >= rolloff_percent * total_energy)[0]
        if len(rolloff_idx) > 0:
            rolloff_freq = freqs[rolloff_idx[0]]
        else:
            rolloff_freq = freqs[-1]
        
        measurements[channel_name] = {
            "rolloff_frequency": rolloff_freq,
            "relative_position": rolloff_freq / (context.sample_rate / 2)
        }
    
    return AnalysisResult(
        method="spectral_rolloff",
        measurements=measurements,
        metrics={"average_rolloff": np.mean([m["rolloff_frequency"] for m in measurements.values()])}
    )

# Register the method
register_method(
    identifier="spectral_rolloff",
    category="spectral",
    function=spectral_rolloff,
    description="Compute spectral rolloff frequency",
    default_params={
        "rolloff_percent": 0.85,
        "n_fft": 2048
    }
)
```

Then activate in configuration:

```yaml
analyses:
  spectral:
    enabled: true
    methods:
      - name: "spectral_rolloff"
        params:
          rolloff_percent: 0.90
          n_fft: 4096
```

## Testing Your Method

Create a simple test configuration and run:

```bash
python -m audio_toolkit.main \
  --audio test_signal.wav \
  --config test_config.yaml \
  --output test_output/
```

Verify the JSON output contains your method's results.

## Contributing Methods

When contributing new methods to the project:

1. Ensure validity
2. Provide references where applicable
3. Include comprehensive documentation
4. Add appropriate default parameters
5. Handle edge cases gracefully
6. Follow the existing code style

## Categories

Methods should be added to the appropriate category:

- `temporal`: Time-domain analysis
- `spectral`: Frequency-domain analysis
- `time_frequency`: Combined time-frequency analysis
- `modulation`: Modulation detection and analysis
- `information`: Information theory metrics
- `inter_channel`: Multi-channel analysis
- `steganography`: Steganographic detection
- `meta_analysis`: Higher-level analysis patterns

Create a new category only if your method doesn't fit existing ones.
