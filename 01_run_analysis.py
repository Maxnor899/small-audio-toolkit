#!/usr/bin/env python3

import sys
from pathlib import Path

from audio_toolkit.config.loader import ConfigLoader
from audio_toolkit.engine.runner import AnalysisRunner


def _find_default_config(project_root: Path) -> Path:
    candidates = [
        project_root / "config_complete.yaml",
        project_root / "examples" / "config_example.yaml",
    ]
    for p in candidates:
        if p.exists():
            return p
    raise FileNotFoundError(
        "No default config found. Expected one of: "
        "config_complete.yaml or examples/config_example.yaml"
    )


def main():
    if len(sys.argv) < 2:
        print("Usage: python run_analysis.py <audio_file> [--config path/to/config.yaml] [--output path/to/output_dir]")
        sys.exit(1)

    audio_file = Path(sys.argv[1])
    if not audio_file.exists():
        print(f"File not found: {audio_file}")
        sys.exit(1)

    # Parse optional args (simple, no external deps)
    project_root = Path(__file__).resolve().parent
    config_path = None
    output_dir = None

    args = sys.argv[2:]
    i = 0
    while i < len(args):
        if args[i] == "--config" and i + 1 < len(args):
            config_path = Path(args[i + 1])
            i += 2
        elif args[i] == "--output" and i + 1 < len(args):
            output_dir = Path(args[i + 1])
            i += 2
        else:
            print(f"Unknown argument: {args[i]}")
            sys.exit(1)

    if config_path is None:
        config_path = _find_default_config(project_root)

    if not config_path.is_absolute():
        config_path = (project_root / config_path).resolve()

    config = ConfigLoader.load(config_path)

    runner = AnalysisRunner(config)

    if output_dir is None:
        output_dir = project_root / "output" / audio_file.stem

    runner.run(audio_file, output_dir)


if __name__ == "__main__":
    main()
