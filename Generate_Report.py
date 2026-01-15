"""
Generate objective analysis reports from results.json

This script produces factual, reproducible outputs based on measured values.
It does NOT perform automated classification, scoring, likelihood estimation,
or hypothesis funnels.

Outputs (3 files):
- 01_MEASUREMENT_SUMMARY.md
- 02_METHODOLOGY_AND_READING_GUIDE.md
- 03_CONTEXTUAL_POSITIONING.md

Usage:
  python Generate_Report.py <results.json|output_dir> [--protocol analysis_protocol.yaml] [--context contextual_references.yaml]
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Optional YAML support (PyYAML). Script still works without it.
try:
    import yaml  # type: ignore
except Exception:
    yaml = None  # type: ignore


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def try_load_yaml(path: Optional[Path]) -> Optional[dict]:
    if path is None or not path.exists() or yaml is None:
        return None
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data if isinstance(data, dict) else None


def format_value(value: Any, precision: int = 3) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        if abs(value) > 1e6 or (abs(value) < 1e-3 and value != 0.0):
            return f"{value:.{precision}e}"
        return f"{value:.{precision}f}"
    if isinstance(value, int):
        return str(value)
    if value is None:
        return "N/A"
    return str(value)


def _header_lines(results: dict, title: str) -> List[str]:
    md: List[str] = []
    md.append(f"# {title}")
    md.append("")
    md.append(f"**Analysis timestamp:** {results.get('timestamp', 'N/A')}")
    md.append(f"**Input file:** {results.get('metadata', {}).get('audio_file', 'N/A')}")
    md.append("")
    return md


def _file_information_lines(results: dict) -> List[str]:
    md: List[str] = []
    audio_info = results.get("metadata", {}).get("audio_info", {}) or {}
    md.append("## File Information")
    md.append("")
    if audio_info:
        if "duration" in audio_info:
            try:
                md.append(f"- Duration: {float(audio_info['duration']):.2f} seconds")
            except Exception:
                md.append(f"- Duration: {audio_info['duration']}")
        if "sample_rate" in audio_info:
            md.append(f"- Sample rate: {audio_info['sample_rate']} Hz")
        if "channels" in audio_info:
            md.append(f"- Channels: {audio_info['channels']}")
        if "format" in audio_info and "subtype" in audio_info:
            md.append(f"- Format: {audio_info['format']} / {audio_info['subtype']}")
        if "frames" in audio_info:
            md.append(f"- Total frames: {audio_info['frames']}")
    else:
        md.append("- No audio_info available in results.json")
    md.append("")
    return md


def _preprocessing_lines(results: dict) -> List[str]:
    md: List[str] = []
    preproc = results.get("metadata", {}).get("preprocessing")
    if not isinstance(preproc, dict):
        return md

    enabled_any = any(isinstance(v, dict) and v.get("enabled") for v in preproc.values())
    if not enabled_any:
        return md

    md.append("## Preprocessing Applied")
    md.append("")
    for key, settings in preproc.items():
        if isinstance(settings, dict) and settings.get("enabled", False):
            md.append(f"### {key}")
            for param, value in settings.items():
                if param != "enabled":
                    md.append(f"- {param}: {value}")
            md.append("")
    return md


def iter_result_methods(results: dict) -> List[Tuple[str, dict]]:
    out: List[Tuple[str, dict]] = []
    groups = results.get("results", {})
    if not isinstance(groups, dict):
        return out
    for family, methods in groups.items():
        if isinstance(methods, list):
            for m in methods:
                if isinstance(m, dict):
                    out.append((str(family), m))
    return out


def summarize_method_measurements(measurements: dict, max_items: int = 12) -> List[str]:
    lines: List[str] = []
    if not isinstance(measurements, dict):
        return lines

    for key, data in measurements.items():
        # Typical: channel -> dict(metrics)
        if isinstance(data, dict):
            # band dict-of-dicts
            if data and all(isinstance(v, dict) for v in data.values()):
                shown = 0
                for subk, subd in data.items():
                    if not isinstance(subd, dict):
                        continue
                    picks = []
                    for mk, mv in subd.items():
                        if isinstance(mv, (int, float)):
                            picks.append(f"{mk}={format_value(mv)}")
                        if len(picks) >= 2:
                            break
                    if picks:
                        lines.append(f"- {key}/{subk}: " + ", ".join(picks))
                        shown += 1
                    if shown >= 6:
                        break
            else:
                items = []
                for mk, mv in data.items():
                    if isinstance(mv, (int, float, bool)) or mv is None:
                        items.append(f"{mk}={format_value(mv)}")
                    elif isinstance(mv, str) and len(mv) <= 60:
                        items.append(f"{mk}={mv}")
                    if len(items) >= max_items:
                        break
                if items:
                    lines.append(f"- {key}: " + ", ".join(items))
        else:
            lines.append(f"- {key}: {format_value(data)}")

    return lines


def generate_measurement_summary_report(results: dict) -> str:
    md: List[str] = []
    md += _header_lines(results, "Audio Analysis Report - Measurement Summary")
    md += _file_information_lines(results)
    md += _preprocessing_lines(results)

    md.append("## Measurement Summary")
    md.append("")
    md.append("This document lists measured outputs for each analysis method.")
    md.append("It does not apply thresholds, scoring, or interpretation rules.")
    md.append("")

    methods = iter_result_methods(results)
    if not methods:
        md.append("_No analysis results found in results.json._")
        md.append("")
        return "\n".join(md)

    for family, method in methods:
        mname = str(method.get("method", "unknown"))
        md.append(f"### {family} / {mname}")
        md.append("")
        meas = method.get("measurements", {})
        lines = summarize_method_measurements(meas)
        if lines:
            md.extend(lines)
        else:
            md.append("_No measurements available for this method._")
        md.append("")

    return "\n".join(md)


def _cmp_statement(value: float, ref: dict) -> Optional[str]:
    # Accept several bound key styles
    candidates = [
        ("typical_min", "typical_max"),
        ("min", "max"),
        ("low", "high"),
    ]
    lo = hi = None
    for a, b in candidates:
        if a in ref and b in ref and isinstance(ref[a], (int, float)) and isinstance(ref[b], (int, float)):
            lo, hi = float(ref[a]), float(ref[b])
            break
    if lo is None or hi is None:
        return None
    if value < lo:
        return f"below the reference interval [{format_value(lo)}, {format_value(hi)}]"
    if value > hi:
        return f"above the reference interval [{format_value(lo)}, {format_value(hi)}]"
    return f"within the reference interval [{format_value(lo)}, {format_value(hi)}]"


def generate_methodology_and_reading_guide(
    results: dict,
    protocol_path: Optional[Path],
    context_path: Optional[Path],
    protocol: Optional[dict],
    context: Optional[dict],
) -> str:
    md: List[str] = []
    md += _header_lines(results, "Audio Analysis Report - Methodology and Reading Guide")

    md.append("## Purpose")
    md.append("")
    md.append("This document explains how to read the analysis outputs produced by this tool.")
    md.append("The tool generates **measurements** and **visualizations** only.")
    md.append("It does not classify signals, infer intent, or decide whether a signal is meaningful.")
    md.append("")

    md.append("## Two separate configuration roles")
    md.append("")
    md.append("### 1) Analysis protocol")
    md.append("Defines what is measured and how (methods, channels, parameters).")
    md.append(f"- Protocol file: `{protocol_path.name}`" if protocol_path else "- Protocol file: _not provided_")
    md.append("")
    md.append("### 2) Contextual references")
    md.append("Provides external reference ranges, notes, and sources used only for contextual positioning.")
    md.append("It never affects measurements.")
    md.append(f"- Context file: `{context_path.name}`" if context_path else "- Context file: _not provided_")
    md.append("")

    md.append("## Reading principles")
    md.append("")
    md.append("- Prefer comparisons within the same run (same config, same tool version).")
    md.append("- Use multiple independent measurements rather than relying on a single metric.")
    md.append("- Treat plots as descriptive views; visualization scaling can affect perception.")
    md.append("- A lack of notable observations is a valid and expected outcome.")
    md.append("")

    md.append("## Documentation")
    md.append("")
    md.append("See:")
    md.append("- `docs/analysis_explanations/00_README.md`")
    md.append("- `docs/analysis_explanations/01_METHODOLOGY.md`")
    md.append("- `docs/analysis_explanations/02_CONTEXTUAL_REFERENCES.md`")
    md.append("- `docs/analysis_explanations/03_OBSERVATION_LIMITS.md`")
    md.append("- `docs/analysis_explanations/families/`")
    md.append("")

    # High-level counts only (no YAML dump)
    if isinstance(protocol, dict):
        md.append("## Protocol summary (high-level)")
        md.append("")
        for k in ("families", "methods", "channels", "analyses"):
            if k in protocol:
                v = protocol[k]
                if isinstance(v, dict):
                    md.append(f"- {k}: {len(v)} keys")
                elif isinstance(v, list):
                    md.append(f"- {k}: {len(v)} entries")
                else:
                    md.append(f"- {k}: {format_value(v)}")
        md.append("")

    if isinstance(context, dict):
        md.append("## Context summary (high-level)")
        md.append("")
        fams = context.get("families")
        md.append(f"- families: {len(fams)}" if isinstance(fams, dict) else "- families: (not found)")
        md.append("")

    return "\n".join(md)


def generate_contextual_positioning_report(results: dict, context: Optional[dict]) -> str:
    md: List[str] = []
    md += _header_lines(results, "Audio Analysis Report - Contextual Positioning")
    md += _file_information_lines(results)
    md += _preprocessing_lines(results)

    md.append("## Contextual Positioning")
    md.append("")
    md.append("This section positions measured values against *external contextual references* when available.")
    md.append("It does not classify signals, infer intent, or provide conclusions.")
    md.append("")

    if not isinstance(context, dict):
        md.append("_No contextual reference file was provided (or it could not be loaded)._")
        md.append("")
        return "\n".join(md)

    families = context.get("families")
    if not isinstance(families, dict):
        md.append("_Context file loaded, but no `families:` mapping was found._")
        md.append("")
        return "\n".join(md)

    # Build index of measured scalar values
    measured: Dict[Tuple[str, str, str, str], Any] = {}
    for family, method in iter_result_methods(results):
        mname = str(method.get("method", ""))
        meas = method.get("measurements", {})
        if not isinstance(meas, dict):
            continue
        for ch, data in meas.items():
            if isinstance(data, dict):
                for mk, mv in data.items():
                    measured[(family, mname, str(ch), str(mk))] = mv

    applied_any = False

    for fam_name, fam_ref in families.items():
        if not isinstance(fam_ref, dict):
            continue
        methods_ref = fam_ref.get("methods")
        if not isinstance(methods_ref, dict):
            continue

        fam_has_meas = any(k[0] == fam_name for k in measured.keys())
        if not fam_has_meas:
            continue

        md.append(f"### {fam_name}")
        md.append("")

        for meth_name, meth_ref in methods_ref.items():
            if not isinstance(meth_ref, dict):
                continue
            meth_has_meas = any(k[0] == fam_name and k[1] == meth_name for k in measured.keys())
            if not meth_has_meas:
                continue

            md.append(f"#### {meth_name}")
            md.append("")
            note = meth_ref.get("note") or meth_ref.get("notes")
            if isinstance(note, str) and note.strip():
                md.append(f"*Note:* {note.strip()}")
                md.append("")

            metrics_ref = meth_ref.get("metrics")
            if not isinstance(metrics_ref, dict):
                md.append("_No metric references found for this method in the context file._")
                md.append("")
                continue

            for metric_name, metric_ref in metrics_ref.items():
                if not isinstance(metric_ref, dict):
                    continue

                channels = sorted({k[2] for k in measured.keys()
                                   if k[0] == fam_name and k[1] == meth_name and k[3] == metric_name})
                if not channels:
                    continue

                md.append(f"**{metric_name}**")
                md.append("")
                unit = metric_ref.get("unit")
                source = metric_ref.get("source")
                if isinstance(unit, str) and unit.strip():
                    md.append(f"- Unit (reference): {unit.strip()}")
                if isinstance(source, str) and source.strip():
                    md.append(f"- Source: {source.strip()}")
                md.append("")

                for ch in channels:
                    v = measured.get((fam_name, meth_name, ch, metric_name))
                    if isinstance(v, (int, float)):
                        stmt = _cmp_statement(float(v), metric_ref)
                        if stmt:
                            md.append(f"- {ch}: {format_value(v)} → {stmt}")
                            applied_any = True
                        else:
                            md.append(f"- {ch}: {format_value(v)} (no numeric interval available in reference entry)")
                    else:
                        md.append(f"- {ch}: {format_value(v)} (non-numeric or unavailable)")
                md.append("")

        md.append("")

    if not applied_any:
        md.append("_Context file loaded, but no comparable numeric intervals were applied (schema mismatch or references are notes-only)._")
        md.append("")

    return "\n".join(md)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Generate objective analysis reports from results.json")
    p.add_argument("input", help="results.json file OR output directory containing results.json")
    p.add_argument("--protocol", help="analysis_protocol.yaml (optional)")
    p.add_argument("--context", help="contextual_references.yaml (optional)")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    input_path = Path(args.input)
    results_file = input_path / "results.json" if input_path.is_dir() else input_path
    if not results_file.exists():
        raise SystemExit(f"Error: File not found: {results_file}")

    results = load_json(results_file)

    protocol_path = Path(args.protocol) if args.protocol else None
    context_path = Path(args.context) if args.context else None

    protocol = try_load_yaml(protocol_path)
    context = try_load_yaml(context_path)

    out_dir = results_file.parent

    r1 = generate_measurement_summary_report(results)
    r2 = generate_methodology_and_reading_guide(results, protocol_path, context_path, protocol, context)
    r3 = generate_contextual_positioning_report(results, context)

    (out_dir / "01_MEASUREMENT_SUMMARY.md").write_text(r1, encoding="utf-8")
    (out_dir / "02_METHODOLOGY_AND_READING_GUIDE.md").write_text(r2, encoding="utf-8")
    (out_dir / "03_CONTEXTUAL_POSITIONING.md").write_text(r3, encoding="utf-8")

    print("✅ Report generation complete!")


if __name__ == "__main__":
    main()
