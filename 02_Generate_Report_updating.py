"""
Generate objective analysis reports from results.json

This script produces factual, reproducible outputs based on measured values.
It does NOT perform automated classification, scoring, likelihood estimation,
or hypothesis funnels.

Outputs (3 or 4 files):
- 01_MEASUREMENT_SUMMARY.md
- 02_METHODOLOGY_AND_READING_GUIDE.md
- 03_CONTEXTUAL_POSITIONING.md
- 04_CONTEXTUAL_POSITIONING_USER.md (only if --user-context is provided)

Usage:
  python Generate_Report.py <results.json|output_dir> \
    --protocol <analysis_protocol.yaml> \
    [--contexts-dir <OFFICIAL_CONTEXTS_DIR>] \
    [--user-context <USER_CONTEXT.yaml>]

Notes on contexts:
- Official context files are loaded per analysis family from a directory.
  - Expected file naming: context_<family>.yaml
- User context is provided as a single YAML file.
- Contexts affect presentation only; they never affect computation.
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


def try_load_family_context(contexts_dir: Path, family: str) -> Tuple[Optional[dict], Optional[str]]:
    """
    Load context_<family>.yaml from contexts_dir.
    Returns (context_dict, error_message). Exactly one of them is non-None.
    """
    if yaml is None:
        return None, "PyYAML is not available; cannot load context YAML files."

    ctx_path = contexts_dir / f"context_{family}.yaml"
    if not ctx_path.exists():
        return None, f"Context file not found: {ctx_path}"

    try:
        with ctx_path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        if not isinstance(data, dict):
            return None, f"Invalid YAML structure (expected mapping) in: {ctx_path}"
        return data, None
    except Exception as e:
        return None, f"Failed to load context file {ctx_path}: {e}"


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


def generate_methodology_and_reading_guide(
    results: dict,
    protocol_path: Optional[Path],
    contexts_dir: Optional[Path],
    user_context_path: Optional[Path],
    protocol: Optional[dict],
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
    md.append("Provide external reference statuses and notes used only for report presentation.")
    md.append("They never affect measurements.")
    if contexts_dir:
        md.append(f"- Official contexts directory: `{contexts_dir}`")
    else:
        md.append("- Official contexts directory: _not provided_")
    if user_context_path:
        md.append(f"- User context file: `{user_context_path}`")
    else:
        md.append("- User context file: _not provided_")
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

    return "\n".join(md)


def _extract_scalar_metrics(measurements: Any) -> List[Tuple[str, str, Any]]:
    """
    Flatten typical measurement structure into a list of (scope_key, metric_name, value)
    where 'scope_key' is usually channel name or pair key.
    Only extracts scalar values: int/float/bool/None/short strings.
    """
    out: List[Tuple[str, str, Any]] = []
    if not isinstance(measurements, dict):
        return out

    for scope_key, data in measurements.items():
        if isinstance(data, dict):
            # Skip dict-of-dicts (bands, etc.) here; they are not scalar per-metric entries.
            if data and all(isinstance(v, dict) for v in data.values()):
                continue
            for mk, mv in data.items():
                if isinstance(mv, (int, float, bool)) or mv is None:
                    out.append((str(scope_key), str(mk), mv))
                elif isinstance(mv, str) and len(mv) <= 80:
                    out.append((str(scope_key), str(mk), mv))
        else:
            # Rare: direct scalar at top-level
            if isinstance(data, (int, float, bool)) or data is None:
                out.append((str(scope_key), str(scope_key), data))
    return out


def _get_ctx_method(ctx: dict, method_name: str) -> Optional[dict]:
    methods = ctx.get("methods")
    if not isinstance(methods, dict):
        return None
    m = methods.get(method_name)
    return m if isinstance(m, dict) else None


def _get_ctx_metric(ctx_method: dict, metric_name: str) -> Optional[dict]:
    metrics = ctx_method.get("metrics")
    if not isinstance(metrics, dict):
        return None
    m = metrics.get(metric_name)
    return m if isinstance(m, dict) else None


def _get_reference(metric_ctx: dict) -> Tuple[Optional[str], Optional[List[float]], List[str]]:
    """
    Returns (status, typical_range, notes).
    """
    notes: List[str] = []
    if isinstance(metric_ctx.get("notes"), list):
        notes = [str(x) for x in metric_ctx["notes"] if str(x).strip()]
    ref = metric_ctx.get("reference")
    if not isinstance(ref, dict):
        return None, None, notes
    status = ref.get("status")
    status_s = str(status) if isinstance(status, str) else None

    tr = ref.get("typical_range")
    typical_range: Optional[List[float]] = None
    if isinstance(tr, list) and len(tr) == 2 and all(isinstance(x, (int, float)) for x in tr):
        typical_range = [float(tr[0]), float(tr[1])]

    return status_s, typical_range, notes


def _position_against_range(value: float, lo: float, hi: float) -> str:
    if value < lo:
        return "below"
    if value > hi:
        return "above"
    return "within"


def generate_contextual_positioning_report(results: dict, contexts_dir: Path) -> str:
    md: List[str] = []
    md += _header_lines(results, "Audio Analysis Report - Contextual Positioning")
    md += _file_information_lines(results)
    md += _preprocessing_lines(results)

    md.append("## Contextual Positioning")
    md.append("")
    md.append("This section uses **context files** to organize measurements into:")
    md.append("- metrics with reference zones (status **A**)")
    md.append("- metrics without reference zones (status **B**/**C**)")
    md.append("")
    md.append("Contexts affect presentation only; they never affect computation.")
    md.append("")

    if not contexts_dir.exists():
        md.append(f"_Contexts directory not found: `{contexts_dir}`_")
        md.append("")
        return "\n".join(md)

    # Group results by family/method
    by_family: Dict[str, List[dict]] = {}
    for family, method in iter_result_methods(results):
        by_family.setdefault(family, []).append(method)

    if not by_family:
        md.append("_No analysis results found in results.json._")
        md.append("")
        return "\n".join(md)

    # Build report per family
    for family, methods in by_family.items():
        md.append(f"### {family}")
        md.append("")

        ctx, err = try_load_family_context(contexts_dir, family)
        if err:
            md.append(f"- Context: _not available_ ({err})")
            md.append("")
            # Still list methods/metrics briefly to avoid silent omission
            for method in methods:
                mname = str(method.get("method", "unknown"))
                md.append(f"#### {mname}")
                md.append("")
                md.append("_No context available for this family; measurements cannot be organized into A/B/C._")
                md.append("")
            md.append("")
            continue

        # Basic schema sanity
        if str(ctx.get("family", "")).strip() and str(ctx.get("family", "")).strip() != family:
            md.append(f"- Context warning: context `family` field is `{ctx.get('family')}` (expected `{family}`)")
            md.append("")

        # Collect A and B/C entries
        section_A: List[str] = []
        section_B: List[str] = []
        section_C: List[str] = []
        section_UNMAPPED: List[str] = []

        for method in methods:
            mname = str(method.get("method", "unknown"))
            meas = method.get("measurements", {})
            scalar_items = _extract_scalar_metrics(meas)

            ctx_method = _get_ctx_method(ctx, mname)
            if ctx_method is None:
                # No method context: everything becomes unmapped but still visible.
                for scope_key, metric_name, value in scalar_items:
                    section_UNMAPPED.append(
                        f"- `{mname}` / `{scope_key}` / **{metric_name}**: {format_value(value)} "
                        f"— _not covered by context (missing method entry)_"
                    )
                continue

            for scope_key, metric_name, value in scalar_items:
                metric_ctx = _get_ctx_metric(ctx_method, metric_name)
                if metric_ctx is None:
                    section_UNMAPPED.append(
                        f"- `{mname}` / `{scope_key}` / **{metric_name}**: {format_value(value)} "
                        f"— _not covered by context (missing metric entry)_"
                    )
                    continue

                status, typical_range, notes = _get_reference(metric_ctx)
                note_txt = (" ".join(notes)).strip()
                if not note_txt:
                    note_txt = "No note provided."

                # Status routing
                if status == "A" and typical_range and isinstance(value, (int, float)):
                    lo, hi = typical_range
                    pos = _position_against_range(float(value), lo, hi)
                    section_A.append(
                        f"- `{mname}` / `{scope_key}`: **{metric_name}** = {format_value(value)} "
                        f"(reference [{format_value(lo)}, {format_value(hi)}]) → **{pos}**. "
                        f"{note_txt}"
                    )
                elif status == "A" and typical_range and not isinstance(value, (int, float)):
                    section_A.append(
                        f"- `{mname}` / `{scope_key}`: **{metric_name}** = {format_value(value)} "
                        f"(reference [{format_value(typical_range[0])}, {format_value(typical_range[1])}]) "
                        f"— _non-numeric value; no positioning applied_. {note_txt}"
                    )
                elif status == "B":
                    section_B.append(
                        f"- `{mname}` / `{scope_key}`: **{metric_name}** = {format_value(value)} "
                        f"— {note_txt}"
                    )
                elif status == "C":
                    section_C.append(
                        f"- `{mname}` / `{scope_key}`: **{metric_name}** = {format_value(value)} "
                        f"— {note_txt}"
                    )
                else:
                    # Unknown or missing status
                    section_UNMAPPED.append(
                        f"- `{mname}` / `{scope_key}` / **{metric_name}**: {format_value(value)} "
                        f"— _invalid or missing reference.status_"
                    )

        # Render family sections
        md.append("#### 3.A Metrics with reference zones (Status A)")
        md.append("")
        if section_A:
            md.extend(section_A)
        else:
            md.append("_No status A metrics were applicable for this family._")
        md.append("")

        md.append("#### 3.B Metrics without reference zones")
        md.append("")
        md.append("**Status B — context-dependent (no stable zone)**")
        md.append("")
        if section_B:
            md.extend(section_B)
        else:
            md.append("_No status B metrics listed for this family._")
        md.append("")

        md.append("**Status C — descriptive only (no stable zone)**")
        md.append("")
        if section_C:
            md.extend(section_C)
        else:
            md.append("_No status C metrics listed for this family._")
        md.append("")

        md.append("**Unmapped / missing context coverage**")
        md.append("")
        if section_UNMAPPED:
            md.extend(section_UNMAPPED)
        else:
            md.append("_No unmapped scalar metrics for this family._")
        md.append("")

        md.append("")

    return "\n".join(md)


def try_load_user_context(user_context_path: Path) -> Tuple[Optional[dict], Optional[str]]:
    """Load a single user context YAML file.

    Returns (context_dict, error_message). Exactly one of them is non-None.
    """
    if yaml is None:
        return None, "PyYAML is not available; cannot load user context YAML file."
    if not user_context_path.exists():
        return None, f"User context file not found: {user_context_path}"
    try:
        with user_context_path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        if not isinstance(data, dict):
            return None, f"Invalid YAML structure (expected mapping) in: {user_context_path}"
        return data, None
    except Exception as e:
        return None, f"Failed to load user context file {user_context_path}: {e}"


def _get_user_family_ctx(user_ctx: dict, family: str) -> Optional[dict]:
    v = user_ctx.get(family)
    return v if isinstance(v, dict) else None


def _get_user_method_ctx(user_family_ctx: dict, method_name: str) -> Optional[dict]:
    methods = user_family_ctx.get("methods")
    if not isinstance(methods, dict):
        return None
    v = methods.get(method_name)
    return v if isinstance(v, dict) else None


def _get_user_metric_ctx(user_method_ctx: dict, metric_name: str) -> Optional[dict]:
    metrics = user_method_ctx.get("metrics")
    if not isinstance(metrics, dict):
        return None
    v = metrics.get(metric_name)
    return v if isinstance(v, dict) else None


def _get_user_reference(metric_ctx: dict) -> Tuple[Optional[List[float]], List[str], List[str]]:
    """Return (typical_user_range, notes, issues).

    User rules:
    - reference.status must be exactly 'USER'
    - reference.typical_user_range must be a 2-number list
    - notes must be a non-empty list

    This function never raises; it collects issues to be reported.
    """
    issues: List[str] = []

    notes_raw = metric_ctx.get("notes")
    notes: List[str] = []
    if isinstance(notes_raw, list):
        notes = [str(x) for x in notes_raw if str(x).strip()]
    if not notes:
        issues.append("missing or empty notes")

    ref = metric_ctx.get("reference")
    if not isinstance(ref, dict):
        issues.append("missing reference section")
        return None, notes, issues

    status = ref.get("status")
    if not (isinstance(status, str) and status == "USER"):
        issues.append("reference.status must be USER")

    tr = ref.get("typical_user_range")
    typical_user_range: Optional[List[float]] = None
    if isinstance(tr, list) and len(tr) == 2 and all(isinstance(x, (int, float)) for x in tr):
        typical_user_range = [float(tr[0]), float(tr[1])]
    else:
        issues.append("missing or invalid typical_user_range")

    return typical_user_range, notes, issues


def generate_user_contextual_positioning_report(results: dict, user_context_path: Path) -> str:
    md: List[str] = []
    md += _header_lines(results, "Audio Analysis Report - Contextual Positioning (User Context)")
    md += _file_information_lines(results)
    md += _preprocessing_lines(results)

    md.append("## Contextual Positioning (User Context)")
    md.append("")
    md.append("This section uses a **user-provided context file** to position measurements against user-provided ranges.")
    md.append("Contexts affect presentation only; they never affect computation.")
    md.append(f"- User context file: `{user_context_path}`")
    md.append("")

    user_ctx, err = try_load_user_context(user_context_path)
    if err:
        md.append(f"_User context not available_ ({err})")
        md.append("")
        return "\n".join(md)

    # Group results by family/method
    by_family: Dict[str, List[dict]] = {}
    for family, method in iter_result_methods(results):
        by_family.setdefault(family, []).append(method)

    if not by_family:
        md.append("_No analysis results found in results.json._")
        md.append("")
        return "\n".join(md)

    for family, methods in by_family.items():
        md.append(f"### {family}")
        md.append("")

        family_ctx = _get_user_family_ctx(user_ctx, family)
        if family_ctx is None:
            md.append("- User context: _not covered_ (missing family entry)")
            md.append("")
            for method in methods:
                mname = str(method.get("method", "unknown"))
                md.append(f"#### {mname}")
                md.append("")
                md.append("_No user context available for this family; measurements cannot be positioned against user-provided ranges._")
                md.append("")
            md.append("")
            continue

        section_USER: List[str] = []
        section_UNMAPPED: List[str] = []

        for method in methods:
            mname = str(method.get("method", "unknown"))
            meas = method.get("measurements", {})
            scalar_items = _extract_scalar_metrics(meas)

            mctx = _get_user_method_ctx(family_ctx, mname)
            if mctx is None:
                for scope_key, metric_name, value in scalar_items:
                    section_UNMAPPED.append(
                        f"- `{mname}` / `{scope_key}` / **{metric_name}**: {format_value(value)} "
                        f"— _not covered by user context (missing method entry)_"
                    )
                continue

            for scope_key, metric_name, value in scalar_items:
                metric_ctx = _get_user_metric_ctx(mctx, metric_name)
                if metric_ctx is None:
                    section_UNMAPPED.append(
                        f"- `{mname}` / `{scope_key}` / **{metric_name}**: {format_value(value)} "
                        f"— _not covered by user context (missing metric entry)_"
                    )
                    continue

                tr, notes, issues = _get_user_reference(metric_ctx)
                note_txt = (" ".join(notes)).strip()
                if not note_txt:
                    note_txt = "No note provided."

                if issues:
                    section_UNMAPPED.append(
                        f"- `{mname}` / `{scope_key}` / **{metric_name}**: {format_value(value)} "
                        f"— _invalid user context entry_ ({'; '.join(issues)}). {note_txt}"
                    )
                    continue

                # Valid user reference
                assert tr is not None
                lo, hi = tr
                if isinstance(value, (int, float)):
                    pos = _position_against_range(float(value), lo, hi)
                    section_USER.append(
                        f"- `{mname}` / `{scope_key}`: **{metric_name}** = {format_value(value)} "
                        f"(user-provided range [{format_value(lo)}, {format_value(hi)}]) → **{pos}**. "
                        f"{note_txt}"
                    )
                else:
                    section_UNMAPPED.append(
                        f"- `{mname}` / `{scope_key}`: **{metric_name}** = {format_value(value)} "
                        f"(user-provided range [{format_value(lo)}, {format_value(hi)}]) "
                        f"— _non-numeric value; no positioning applied_. {note_txt}"
                    )

        md.append("#### 4.USER Metrics with user-provided ranges (Status USER)")
        md.append("")
        if section_USER:
            md.extend(section_USER)
        else:
            md.append("_No applicable user-range metrics were found for this family._")
        md.append("")

        md.append("**Unmapped / missing / invalid user context coverage**")
        md.append("")
        if section_UNMAPPED:
            md.extend(section_UNMAPPED)
        else:
            md.append("_No unmapped scalar metrics for this family._")
        md.append("")
        md.append("")

    return "\n".join(md)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Generate objective analysis reports from results.json")
    p.add_argument("input", help="results.json file OR output directory containing results.json")
    p.add_argument("--protocol", required=True, help="analysis_protocol.yaml (required)")
    p.add_argument(
        "--contexts-dir",
        help="Directory containing family context files (context_<family>.yaml).",
        default=None,
    )
    p.add_argument(
        "--user-context",
        help="User context YAML file (optional). Used to generate 04_CONTEXTUAL_POSITIONING_USER.md.",
        default=None,
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()
    input_path = Path(args.input)
    results_file = input_path / "results.json" if input_path.is_dir() else input_path
    if not results_file.exists():
        raise SystemExit(f"Error: File not found: {results_file}")

    results = load_json(results_file)

    protocol_path = Path(args.protocol) if args.protocol else None
    protocol = try_load_yaml(protocol_path)

    contexts_dir = Path(args.contexts_dir) if args.contexts_dir else None
    user_context_path = Path(args.user_context) if args.user_context else None

    out_dir = results_file.parent

    r1 = generate_measurement_summary_report(results)
    r2 = generate_methodology_and_reading_guide(results, protocol_path, contexts_dir, user_context_path, protocol)

    if contexts_dir is not None:
        r3 = generate_contextual_positioning_report(results, contexts_dir)
    else:
        r3 = "\n".join(
            _header_lines(results, "Audio Analysis Report - Contextual Positioning")
            + ["", "_No official contexts directory provided; contextual positioning (official) was not generated._", ""]
        )

    (out_dir / "01_MEASUREMENT_SUMMARY.md").write_text(r1, encoding="utf-8")
    (out_dir / "02_METHODOLOGY_AND_READING_GUIDE.md").write_text(r2, encoding="utf-8")
    (out_dir / "03_CONTEXTUAL_POSITIONING.md").write_text(r3, encoding="utf-8")

    if user_context_path is not None:
        r4 = generate_user_contextual_positioning_report(results, user_context_path)
        (out_dir / "04_CONTEXTUAL_POSITIONING_USER.md").write_text(r4, encoding="utf-8")

    print("✅ Report generation complete!")


if __name__ == "__main__":
    main()
