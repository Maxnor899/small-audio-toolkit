"""
Generate objective analysis reports from results.json

This script produces factual, reproducible outputs based on measured values.
It does NOT perform automated classification, scoring, likelihood estimation,
or hypothesis funnels.

Outputs (4 files):
- 01_MEASUREMENT_SUMMARY.md
- 02_METHODOLOGY_AND_READING_GUIDE.md
- 03_CONTEXTUAL_POSITIONING.md
- 04_CONTEXTUAL_POSITIONING_USER.md

Usage:
  python Generate_Report.py <results.json|output_dir> \
    --protocol <analysis_protocol.yaml> \
    [--contexts-dir <OFFICIAL_CONTEXTS_DIR>] \
    [--user-context <USER_CONTEXT.yaml>]

Notes on contexts:
- Official context files are loaded per analysis family from a directory.
  - Expected file naming: context_<family>.yaml
- User context is provided as a single YAML file (official-like schema).
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


def resolve_path(p: Path, project_root: Path) -> Path:
    """Resolve a path robustly.

    - Absolute paths are returned as-is.
    - For relative paths, prefer CWD (so existing CLI habits keep working).
    - If not found, fall back to being relative to the project root (script directory).
    """
    if p.is_absolute():
        return p
    cwd_candidate = (Path.cwd() / p).resolve()
    if cwd_candidate.exists():
        return cwd_candidate
    return (project_root / p).resolve()


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
    if not contexts_dir.exists():
        return None, f"Contexts directory not found: {contexts_dir}"
    if not contexts_dir.is_dir():
        return None, f"Contexts path is not a directory: {contexts_dir}"

    path = contexts_dir / f"context_{family}.yaml"
    if not path.exists():
        return None, f"Missing context file: {path.name}"
    try:
        with path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        if not isinstance(data, dict):
            return None, f"Invalid YAML structure (expected mapping) in: {path.name}"
        return data, None
    except Exception as e:
        return None, f"Failed to load context file {path.name}: {e}"


def iter_result_methods(results: dict):
    """Yield (family, method_dict) for each method result present in results.json."""
    analyses = results.get("analyses")
    if isinstance(analyses, list):
        for entry in analyses:
            if not isinstance(entry, dict):
                continue
            fam = entry.get("family")
            if not isinstance(fam, str):
                fam = "unknown"
            yield fam, entry
        return

    families = results.get("families")
    if isinstance(families, dict):
        for fam, fam_data in families.items():
            if not isinstance(fam, str):
                continue
            if not isinstance(fam_data, dict):
                continue
            methods = fam_data.get("methods")
            if isinstance(methods, list):
                for m in methods:
                    if isinstance(m, dict):
                        yield fam, m
        return


def format_value(v: Any) -> str:
    if isinstance(v, float):
        if v != v:  # NaN
            return "NaN"
        if v == float("inf"):
            return "inf"
        if v == float("-inf"):
            return "-inf"
        return f"{v:.6g}"
    return str(v)


def _header_lines(results: dict, title: str) -> List[str]:
    md = [f"# {title}", ""]
    meta = results.get("meta")
    if isinstance(meta, dict):
        src = meta.get("source_file")
        if src:
            md.append(f"- Source: `{src}`")
        ts = meta.get("timestamp")
        if ts:
            md.append(f"- Timestamp: `{ts}`")
        md.append("")
    return md


def _file_information_lines(results: dict) -> List[str]:
    md: List[str] = []
    info = results.get("file")
    if isinstance(info, dict):
        md.append("## File Information")
        md.append("")
        for k in ["path", "format", "sample_rate", "channels", "duration_seconds"]:
            if k in info:
                md.append(f"- {k}: `{info[k]}`")
        md.append("")
    return md


def _preprocessing_lines(results: dict) -> List[str]:
    md: List[str] = []
    pre = results.get("preprocessing")
    if isinstance(pre, dict):
        md.append("## Preprocessing")
        md.append("")
        for k, v in pre.items():
            md.append(f"- {k}: `{v}`")
        md.append("")
    return md


def _extract_scalar_metrics(measurements: Any) -> List[Tuple[str, str, Any]]:
    """
    Flatten scalar metrics from various measurement shapes.

    Returns list of (scope_key, metric_name, value) where:
    - scope_key is e.g. "global", "L", "R", "L-R", "L/R", etc.
    - metric_name is the scalar key
    - value is the scalar
    """
    out: List[Tuple[str, str, Any]] = []
    if not isinstance(measurements, dict):
        return out

    for scope_key, scope_val in measurements.items():
        if isinstance(scope_val, dict):
            for metric_name, v in scope_val.items():
                if isinstance(v, (int, float, str, bool)) or v is None:
                    if isinstance(v, (list, dict)):
                        continue
                    out.append((str(scope_key), str(metric_name), v))
        else:
            if isinstance(scope_val, (int, float, str, bool)) or scope_val is None:
                out.append(("global", str(scope_key), scope_val))
    return out


def _get_ctx_method(ctx: dict, method_name: str) -> Optional[dict]:
    methods = ctx.get("methods")
    if not isinstance(methods, dict):
        return None
    v = methods.get(method_name)
    return v if isinstance(v, dict) else None


def _get_ctx_metric(ctx_method: dict, metric_name: str) -> Optional[dict]:
    metrics = ctx_method.get("metrics")
    if not isinstance(metrics, dict):
        return None
    v = metrics.get(metric_name)
    return v if isinstance(v, dict) else None


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
    md.append("This section uses **official context files** to position a selected subset of scalar metrics.")
    md.append("Contexts affect presentation only; they never affect computation.")
    md.append("")

    if not contexts_dir.exists() or not contexts_dir.is_dir():
        md.append(f"_Official contexts not available; this report was not generated._ (Invalid contexts directory: `{contexts_dir}`)")
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
            md.append(f"_Official context not available for this family; measurements are not positioned._ ({err})")
            md.append("")
            continue

        # Basic schema sanity
        if str(ctx.get("family", "")).strip() and str(ctx.get("family", "")).strip() != family:
            md.append(f"- Context warning: context `family` field is `{ctx.get('family')}` (expected `{family}`)")
            md.append("")

        # Context scope (objective) and references (if provided)
        scope = ctx.get("scope")
        if isinstance(scope, dict):
            obj = scope.get("objective")
            if isinstance(obj, str) and obj.strip():
                md.append(f"- Objective: {obj.strip()}")
            cov = scope.get("coverage")
            if isinstance(cov, str) and cov.strip():
                md.append(f"- Coverage: `{cov.strip()}`")
            rat = scope.get("rationale")
            if isinstance(rat, str) and rat.strip():
                md.append(f"- Rationale: {rat.strip()}")
            md.append("")

        refs = ctx.get("references")
        if isinstance(refs, list) and refs:
            md.append("- Documentary references:")
            for r in refs:
                if not isinstance(r, dict):
                    continue
                authors = str(r.get("authors", "")).strip()
                title = str(r.get("title", "")).strip()
                year = str(r.get("year", "")).strip()
                note = str(r.get("note", "")).strip()
                core = " — ".join([x for x in [authors, f'"{title}"' if title else "", f"({year})" if year else ""] if x])
                if note:
                    md.append(f"  - {core}. {note}")
                else:
                    md.append(f"  - {core}.")
            md.append("")

        # Collect A/B/C entries + expected/missing
        section_A: List[str] = []
        section_B: List[str] = []
        section_C: List[str] = []
        section_UNMAPPED: List[str] = []

        # Expected (from context) vs observed (from results) scalar metrics
        expected: set[tuple[str, str]] = set()
        ctx_methods = ctx.get("methods")
        if isinstance(ctx_methods, dict):
            for mname_ctx, mctx in ctx_methods.items():
                if not isinstance(mctx, dict):
                    continue
                metrics_ctx = mctx.get("metrics")
                if isinstance(metrics_ctx, dict):
                    for metric_name in metrics_ctx.keys():
                        expected.add((str(mname_ctx), str(metric_name)))

        observed: set[tuple[str, str]] = set()

        for method in methods:
            mname = str(method.get("method", "unknown"))
            meas = method.get("measurements", {})
            scalar_items = _extract_scalar_metrics(meas)
            for _scope_key, _metric_name, _value in scalar_items:
                observed.add((mname, _metric_name))

            ctx_method = _get_ctx_method(ctx, mname)
            if ctx_method is None:
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
                note_txt = (" ".join(notes)).strip() or "No note provided."

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
                    section_UNMAPPED.append(
                        f"- `{mname}` / `{scope_key}` / **{metric_name}**: {format_value(value)} "
                        f"— _invalid or missing reference.status_"
                    )

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

        md.append("**Expected by context but missing in results (not evaluated)**")
        md.append("")
        missing = sorted(expected - observed)
        if missing:
            for mname_m, metric_m in missing:
                md.append(f"- `{mname_m}`: **{metric_m}** — _missing in results.json_")
        else:
            md.append("_No expected scalar metrics were missing for this family._")
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


def user_context_family(user_ctx: dict) -> Optional[str]:
    fam = user_ctx.get("family")
    return str(fam).strip() if isinstance(fam, str) and str(fam).strip() else None


def _get_user_method_ctx(user_ctx: dict, method_name: str) -> Optional[dict]:
    methods = user_ctx.get("methods")
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
    - reference.typical_range must NOT be present
    - notes are recommended; if missing, they are flagged as an issue

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

    if "typical_range" in ref:
        issues.append("typical_range is not allowed in user contexts")

    tr = ref.get("typical_user_range")
    typical_user_range: Optional[List[float]] = None
    if isinstance(tr, list) and len(tr) == 2 and all(isinstance(x, (int, float)) for x in tr):
        typical_user_range = [float(tr[0]), float(tr[1])]
    else:
        issues.append("missing or invalid typical_user_range")

    return typical_user_range, notes, issues


def generate_user_contextual_positioning_report(results: dict, user_context_path: Optional[Path]) -> str:
    md: List[str] = []
    md += _header_lines(results, "Audio Analysis Report - Contextual Positioning (User Context)")
    md += _file_information_lines(results)
    md += _preprocessing_lines(results)

    md.append("## Contextual Positioning (User Context)")
    md.append("")
    md.append("This section uses a **user-provided context file** to position measurements against user-provided ranges.")
    md.append("Contexts affect presentation only; they never affect computation.")
    md.append("")

    if user_context_path is None:
        md.append("_User context not provided; this report was not generated._")
        md.append("")
        return "\n".join(md)

    md.append(f"- User context file: `{user_context_path}`")
    md.append("")

    user_ctx, err = try_load_user_context(user_context_path)
    if err:
        md.append(f"_User context not available; this report was not generated._ ({err})")
        md.append("")
        return "\n".join(md)

    family_target = user_context_family(user_ctx)
    if not family_target:
        md.append("_Invalid user context: missing or empty top-level `family` field; this report was not generated._")
        md.append("")
        return "\n".join(md)

    scope = user_ctx.get("scope")
    if isinstance(scope, dict):
        obj = scope.get("objective")
        if isinstance(obj, str) and obj.strip():
            md.append(f"- Objective: {obj.strip()}")
        cov = scope.get("coverage")
        if isinstance(cov, str) and cov.strip():
            md.append(f"- Coverage: `{cov.strip()}`")
        rat = scope.get("rationale")
        if isinstance(rat, str) and rat.strip():
            md.append(f"- Rationale: {rat.strip()}")
        md.append("")

    refs = user_ctx.get("references")
    if isinstance(refs, list) and refs:
        md.append("- Documentary references:")
        for r in refs:
            if not isinstance(r, dict):
                continue
            authors = str(r.get("authors", "")).strip()
            title = str(r.get("title", "")).strip()
            year = str(r.get("year", "")).strip()
            note = str(r.get("note", "")).strip()
            core = " — ".join([x for x in [authors, f'"{title}"' if title else "", f"({year})" if year else ""] if x])
            if note:
                md.append(f"  - {core}. {note}")
            else:
                md.append(f"  - {core}.")
        md.append("")

    by_family: Dict[str, List[dict]] = {}
    for family, method in iter_result_methods(results):
        by_family.setdefault(family, []).append(method)

    if not by_family:
        md.append("_No analysis results found in results.json._")
        md.append("")
        return "\n".join(md)

    if family_target not in by_family:
        md.append(f"_User context targets family `{family_target}`, but no such family was found in results.json; this report was not generated._")
        md.append("")
        return "\n".join(md)

    methods = by_family[family_target]

    md.append(f"### {family_target}")
    md.append("")

    section_USER: List[str] = []
    section_UNMAPPED: List[str] = []

    expected: set[tuple[str, str]] = set()
    ctx_methods = user_ctx.get("methods")
    if isinstance(ctx_methods, dict):
        for mname_ctx, mctx in ctx_methods.items():
            if not isinstance(mctx, dict):
                continue
            metrics_ctx = mctx.get("metrics")
            if isinstance(metrics_ctx, dict):
                for metric_name in metrics_ctx.keys():
                    expected.add((str(mname_ctx), str(metric_name)))

    observed: set[tuple[str, str]] = set()

    for method in methods:
        mname = str(method.get("method", "unknown"))
        meas = method.get("measurements", {})
        scalar_items = _extract_scalar_metrics(meas)
        for _scope_key, _metric_name, _value in scalar_items:
            observed.add((mname, _metric_name))

        mctx = _get_user_method_ctx(user_ctx, mname)
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
            note_txt = (" ".join(notes)).strip() or "No note provided."

            if issues:
                section_UNMAPPED.append(
                    f"- `{mname}` / `{scope_key}` / **{metric_name}**: {format_value(value)} "
                    f"— _invalid user context entry_ ({'; '.join(issues)}). {note_txt}"
                )
                continue

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

    md.append("**Expected by user context but missing in results (not evaluated)**")
    md.append("")
    missing = sorted(expected - observed)
    if missing:
        for mname_m, metric_m in missing:
            md.append(f"- `{mname_m}`: **{metric_m}** — _missing in results.json_")
    else:
        md.append("_No expected scalar metrics were missing for this family._")
    md.append("")
    md.append("")

    return "\n".join(md)


def generate_measurement_summary_report(results: dict) -> str:
    md: List[str] = []
    md += _header_lines(results, "Audio Analysis Report - Measurement Summary")
    md += _file_information_lines(results)
    md += _preprocessing_lines(results)

    md.append("## Measured Outputs")
    md.append("")
    md.append("This report lists measured outputs as produced by the analysis engine. No interpretation is applied.")
    md.append("")

    any_found = False
    for family, method in iter_result_methods(results):
        any_found = True
        mname = str(method.get("method", "unknown"))
        md.append(f"### {family} / {mname}")
        md.append("")
        meas = method.get("measurements", {})
        scalar_items = _extract_scalar_metrics(meas)
        if not scalar_items:
            md.append("_No scalar measurements found for this method._")
            md.append("")
            continue
        for scope_key, metric_name, value in scalar_items:
            md.append(f"- `{scope_key}` / **{metric_name}**: {format_value(value)}")
        md.append("")

    if not any_found:
        md.append("_No analysis results found in results.json._")
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
    md += _file_information_lines(results)
    md += _preprocessing_lines(results)

    md.append("## Methodology")
    md.append("")
    if protocol_path is None:
        md.append("_No protocol path provided._")
    elif protocol is None:
        md.append(f"_Protocol could not be loaded or is empty: `{protocol_path}`_")
    else:
        md.append(f"- Protocol file: `{protocol_path}`")
        md.append("- This report describes the analysis configuration used to produce results.json.")
    md.append("")

    md.append("## Context Sources")
    md.append("")
    if contexts_dir is None:
        md.append("- Official contexts: _not provided_")
    else:
        md.append(f"- Official contexts dir: `{contexts_dir}`")
    if user_context_path is None:
        md.append("- User context: _not provided_")
    else:
        md.append(f"- User context file: `{user_context_path}`")
    md.append("")

    md.append("## Reading Guide")
    md.append("")
    md.append("- Report 01 lists scalar measurements as produced by the engine.")
    md.append("- Report 02 describes the protocol and how to read outputs.")
    md.append("- Report 03 positions selected scalar metrics against official documentary ranges (if available).")
    md.append("- Report 04 positions selected scalar metrics against user-provided ranges (if a valid user context is provided).")
    md.append("")
    md.append("No automated interpretation or classification is performed.")
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
        help="User context YAML file (optional). If omitted or invalid, 04_CONTEXTUAL_POSITIONING_USER.md is generated as not generated with explanation.",
        default=None,
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()
    project_root = Path(__file__).resolve().parent

    input_path = resolve_path(Path(args.input), project_root)
    results_file = (input_path / "results.json") if input_path.is_dir() else input_path
    if not results_file.exists():
        raise SystemExit(f"Error: File not found: {results_file}")

    results = load_json(results_file)

    protocol_path = resolve_path(Path(args.protocol), project_root) if args.protocol else None
    protocol = try_load_yaml(protocol_path)

    contexts_dir = resolve_path(Path(args.contexts_dir), project_root) if args.contexts_dir else None
    user_context_path = resolve_path(Path(args.user_context), project_root) if args.user_context else None

    out_dir = results_file.parent

    r1 = generate_measurement_summary_report(results)
    r2 = generate_methodology_and_reading_guide(results, protocol_path, contexts_dir, user_context_path, protocol)

    if contexts_dir is not None and contexts_dir.exists() and contexts_dir.is_dir():
        r3 = generate_contextual_positioning_report(results, contexts_dir)
    else:
        r3 = "\n".join(
            _header_lines(results, "Audio Analysis Report - Contextual Positioning")
            + [
                "",
                "_Official contexts not available; this report was not generated._",
                f"- contexts_dir: `{contexts_dir}`",
                "",
            ]
        )

    r4 = generate_user_contextual_positioning_report(results, user_context_path)

    (out_dir / "01_MEASUREMENT_SUMMARY.md").write_text(r1, encoding="utf-8")
    (out_dir / "02_METHODOLOGY_AND_READING_GUIDE.md").write_text(r2, encoding="utf-8")
    (out_dir / "03_CONTEXTUAL_POSITIONING.md").write_text(r3, encoding="utf-8")
    (out_dir / "04_CONTEXTUAL_POSITIONING_USER.md").write_text(r4, encoding="utf-8")

    print("✅ Report generation complete!")


if __name__ == "__main__":
    main()
