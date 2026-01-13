"""
Analyses package.

Importing this package registers all analysis methods into the global registry.
This is an intentional side-effect, per the project architecture.
"""

# Trigger registration of all methods via module import side-effects.
from . import temporal  # noqa: F401
from . import spectral  # noqa: F401
from . import time_frequency  # noqa: F401
from . import modulation  # noqa: F401
from . import information  # noqa: F401
from . import inter_channel  # noqa: F401
from . import steganography  # noqa: F401
from . import meta_analysis  # noqa: F401
