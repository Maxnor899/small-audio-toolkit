from pathlib import Path
from audio_toolkit.config.loader import ConfigLoader
from audio_toolkit.engine.runner import AnalysisRunner
from audio_toolkit.utils.logging import setup_logging

setup_logging(verbose=True)

# Import des modules d'analyses
import audio_toolkit.analyses.temporal
import audio_toolkit.analyses.spectral
import audio_toolkit.analyses.time_frequency      # ← NOUVEAU
import audio_toolkit.analyses.modulation          # ← NOUVEAU
import audio_toolkit.analyses.inter_channel       # ← NOUVEAU

# Charge la config
config = ConfigLoader.load(Path('examples/config_example.yaml'))

# Lance l'analyse
runner = AnalysisRunner(config)
runner.run(
    audio_path=Path('lsig.flac'),
    output_path=Path('results')
)

print("\n✓ Analyse terminée !")