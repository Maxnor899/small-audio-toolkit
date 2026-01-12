from pathlib import Path
from audio_toolkit.config.loader import ConfigLoader
from audio_toolkit.engine.runner import AnalysisRunner
from audio_toolkit.utils.logging import setup_logging

# Active les logs AVANT tout
setup_logging(verbose=True)

# Import des modules d'analyses
import audio_toolkit.analyses.temporal
import audio_toolkit.analyses.spectral

# Charge la config
config = ConfigLoader.load(Path('examples/config_example.yaml'))

# Lance l'analyse
try:
    runner = AnalysisRunner(config)
    runner.run(
        audio_path=Path('lsig.flac'),
        output_path=Path('results')
    )
    print("\n✓ Analyse terminée !")
except Exception as e:
    print(f"\n✗ ERREUR : {e}")
    import traceback
    traceback.print_exc()