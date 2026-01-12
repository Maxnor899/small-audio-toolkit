# Configuration Format

## Overview

The pipeline is entirely driven by a YAML configuration file that declares:

- Preprocessing steps to apply
- Channels to analyze
- Analysis categories to activate
- Methods to execute in each category
- Method-specific parameters

The configuration file is versioned and saved with results to ensure reproducibility.

## File Structure

```yaml
version: "1.0"

preprocessing:
  normalize:
    enabled: true
    method: "rms"  # or "lufs"
    target_level: -20.0
  
  silence_detection:
    enabled: true
    threshold_db: -40.0
    min_duration: 0.1

  segmentation:
    enabled: false

channels:
  analyze: ["left", "right", "sum", "difference"]
  # Options: "left", "right", "mono", "sum", "difference"

analyses:
  temporal:
    enabled: true
    methods:
      - name: "envelope"
        params:
          method: "hilbert"
      
      - name: "autocorrelation"
        params:
          max_lag: 1000
  
  spectral:
    enabled: true
    methods:
      - name: "fft_global"
        params:
          window: "hann"
      
      - name: "peak_detection"
        params:
          prominence: 10.0
          distance: 100
  
  time_frequency:
    enabled: true
    methods:
      - name: "stft"
        params:
          n_fft: 2048
          hop_length: 512
          window: "hann"
      
      - name: "cqt"
        params:
          n_bins: 84
          bins_per_octave: 12
  
  modulation:
    enabled: false
  
  information:
    enabled: true
    methods:
      - name: "shannon_entropy"
        params:
          window_size: 1024
      
      - name: "compression_ratio"
        params:
          algorithm: "gzip"
  
  inter_channel:
    enabled: true
    methods:
      - name: "cross_correlation"
        params: {}
      
      - name: "phase_difference"
        params:
          frequency_bands: [[100, 500], [500, 2000], [2000, 8000]]
  
  steganography:
    enabled: false
  
  meta_analysis:
    enabled: false

visualization:
  enabled: true
  formats: ["png"]
  dpi: 300

output:
  save_raw_data: true
  save_config: true
  export_formats: ["json"]
```

## Configuration Sections

### Preprocessing

Optional preprocessing steps applied before analysis.

```yaml
preprocessing:
  normalize:
    enabled: bool
    method: "rms" | "lufs"
    target_level: float
  
  silence_detection:
    enabled: bool
    threshold_db: float
    min_duration: float  # seconds
  
  segmentation:
    enabled: bool
    method: "energy" | "spectral"
    segment_duration: float  # seconds
```

### Channels

Defines which channels to analyze.

```yaml
channels:
  analyze: list[str]
  # Options:
  # - "left": left channel
  # - "right": right channel
  # - "mono": average of all channels
  # - "sum": L + R
  # - "difference": L - R
```

### Analyses

Each analysis category can be enabled/disabled and configured independently.

#### Temporal Analysis

```yaml
temporal:
  enabled: bool
  methods:
    - name: "envelope"
      params:
        method: "hilbert" | "rms"
        window_size: int  # for rms
    
    - name: "autocorrelation"
      params:
        max_lag: int
        normalize: bool
    
    - name: "pulse_detection"
      params:
        threshold: float
        min_distance: int
```

#### Spectral Analysis

```yaml
spectral:
  enabled: bool
  methods:
    - name: "fft_global"
      params:
        window: "hann" | "hamming" | "blackman"
    
    - name: "peak_detection"
      params:
        prominence: float
        distance: int
        height: float
    
    - name: "harmonic_analysis"
      params:
        fundamental_range: [float, float]
        max_harmonics: int
    
    - name: "cepstrum"
      params: {}
```

#### Time-Frequency Analysis

```yaml
time_frequency:
  enabled: bool
  methods:
    - name: "stft"
      params:
        n_fft: int
        hop_length: int
        window: str
    
    - name: "cqt"
      params:
        n_bins: int
        bins_per_octave: int
    
    - name: "wavelet"
      params:
        wavelet: "morlet" | "mexicanhat"
        scales: list[int]
```

#### Modulation Analysis

```yaml
modulation:
  enabled: bool
  methods:
    - name: "am_detection"
      params:
        carrier_range: [float, float]
    
    - name: "fm_detection"
      params:
        method: "hilbert" | "instantaneous"
    
    - name: "phase_analysis"
      params: {}
```

#### Information Analysis

```yaml
information:
  enabled: bool
  methods:
    - name: "shannon_entropy"
      params:
        window_size: int
        normalize: bool
    
    - name: "local_entropy"
      params:
        window_size: int
        hop_length: int
    
    - name: "compression_ratio"
      params:
        algorithm: "gzip" | "lz77"
```

#### Inter-Channel Analysis

```yaml
inter_channel:
  enabled: bool
  methods:
    - name: "cross_correlation"
      params:
        max_lag: int
    
    - name: "phase_difference"
      params:
        frequency_bands: list[list[float]]
    
    - name: "time_delay"
      params: {}
```

### Visualization

```yaml
visualization:
  enabled: bool
  formats: list[str]  # ["png", "svg", "pdf"]
  dpi: int
  figsize: [float, float]  # width, height in inches
```

### Output

```yaml
output:
  save_raw_data: bool
  save_config: bool
  export_formats: list[str]  # ["json", "csv"]
```

## Parameter Types

- `bool`: true/false
- `int`: integer value
- `float`: floating point value
- `str`: string value
- `list[T]`: list of type T

## Validation

The configuration is validated at load time. Invalid configurations will raise descriptive errors before execution begins.

## Examples

See `examples/config_example.yaml` for a complete working example.

## Best Practices

1. Start with a minimal configuration and add analyses progressively
2. Document why each analysis is enabled
3. Version your configuration files
4. Keep parameter values within reasonable ranges for your sample rate
5. Disable visualization during batch processing for performance
