#!/usr/bin/env python3

import argparse
import sys
from pathlib import Path

from audio_toolkit.config.loader import ConfigLoader
from audio_toolkit.engine.runner import AnalysisRunner


def resolve_path(p: Path, project_root: Path) -> Path:
    if p.is_absolute():
        return p

    cwd_candidate = (Path.cwd() / p).resolve()
    if cwd_candidate.exists():
        return cwd_candidate

    return (project_root / p).resolve()


def find_default_config(project_root: Path) -> Path:
    baseline = (
        project_root
        / "Analysis_Workspace"
        / "01_protocols"
        / "01_Baseline"
        / "protocol_baseline_full.yaml"
    )

    if baseline.exists():
        return baseline

    raise FileNotFoundError(
        "No default protocol found.\n"
        "Expected:\n"
        f"  {baseline}\n"
        "Provide --config <path/to/protocol.yaml>."
    )


def main(argv=None) -> int:
    project_root = Path(__file__).resolve().parent

    parser = argparse.ArgumentParser(
        description="Run SAT analysis on an audio file using a protocol YAML."
    )
    parser.add_argument("audio_file", type=Path, help="Input audio file")
    parser.add_argument("--config", type=Path, help="Protocol YAML file")
    parser.add_argument("--output", type=Path, help="Output directory")
    args = parser.parse_args(argv)

    audio_file = resolve_path(args.audio_file, project_root)
    if not audio_file.exists():
        print(f"Audio file not found: {audio_file}", file=sys.stderr)
        return 1

    if args.config is None:
        config_path = find_default_config(project_root)
    else:
        config_path = resolve_path(args.config, project_root)

    if not config_path.exists():
        print(f"Config file not found: {config_path}", file=sys.stderr)
        return 1

    output_dir = args.output
    if output_dir is None:
        output_dir = project_root / "output" / audio_file.stem
    output_dir = resolve_path(output_dir, project_root)

    # Ensure output dir exists
    output_dir.mkdir(parents=True, exist_ok=True)

    # Archive the protocol used for this run (traceability only)
    protocol_dst = output_dir / "analysis_protocol_used.yaml"
    shutil.copy2(config_path, protocol_dst)
    
    config = ConfigLoader.load(config_path)
    runner = AnalysisRunner(config)
    runner.run(audio_file, output_dir)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
