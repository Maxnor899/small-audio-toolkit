"""
Configuration schema constants and validation rules.
"""

from typing import Set

VALID_CATEGORIES: Set[str] = {
    "preprocessing",
    "temporal",
    "spectral",
    "time_frequency",
    "modulation",
    "information",
    "inter_channel",
    "steganography",
    "meta_analysis"
}

VALID_CHANNELS: Set[str] = {
    "left",
    "right",
    "mono",
    "sum",
    "difference"
}

VALID_NORMALIZATION_METHODS: Set[str] = {
    "rms",
    "lufs"
}

VALID_EXPORT_FORMATS: Set[str] = {
    "json",
    "csv"
}

VALID_VISUALIZATION_FORMATS: Set[str] = {
    "png",
    "svg",
    "pdf"
}

REQUIRED_CONFIG_KEYS: Set[str] = {
    "version",
    "channels",
    "analyses"
}
