print("Test 1: Import Path...")
from pathlib import Path
print("✓ Path OK")

print("Test 2: Import yaml...")
import yaml
print("✓ yaml OK")

print("Test 3: Import numpy...")
import numpy as np
print("✓ numpy OK")

print("Test 4: Import scipy...")
import scipy
print("✓ scipy OK")

print("Test 5: Import matplotlib...")
import matplotlib
print("✓ matplotlib OK")

print("Test 6: Import soundfile...")
import soundfile
print("✓ soundfile OK")

print("Test 7: Import audio_toolkit.audio.loader...")
from audio_toolkit.audio.loader import AudioLoader
print("✓ audio_toolkit.audio.loader OK")

print("Test 8: Import audio_toolkit.analyses.temporal...")
import audio_toolkit.analyses.temporal
print("✓ audio_toolkit.analyses.temporal OK")

print("\nTous les imports OK!")