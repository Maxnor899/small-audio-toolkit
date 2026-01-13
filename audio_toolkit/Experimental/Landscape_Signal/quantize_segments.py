#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
quantize_segments.py

Quantification (discrétisation) des durées de segments (sortie segmentation morphologique).
Entrée: segments.csv (colonnes: id,start_s,end_s,duration_s,start_idx,end_idx)

Sorties:
- duration_clusters.csv         (classes A,B,C... avec stats)
- symbols_sequence.txt          (séquence A B C ... + runs)
- QUANTIZATION_REPORT.md
- duration_hist.png
- duration_scatter.png

Dépendances:
  pip install numpy matplotlib
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import List, Tuple, Dict, Any

import numpy as np
import matplotlib.pyplot as plt


# -------------------------
# IO
# -------------------------

def ensure_dir(p: Path) -> Path:
    p.mkdir(parents=True, exist_ok=True)
    return p


def read_segments_csv(path: Path) -> List[Dict[str, Any]]:
    lines = path.read_text(encoding="utf-8").strip().splitlines()
    if not lines:
        return []
    header = [h.strip() for h in lines[0].split(",")]
    out = []
    for ln in lines[1:]:
        if not ln.strip():
            continue
        parts = [p.strip() for p in ln.split(",")]
        row = dict(zip(header, parts))
        # cast
        row["id"] = int(row["id"])
        row["start_s"] = float(row["start_s"])
        row["end_s"] = float(row["end_s"])
        row["duration_s"] = float(row["duration_s"])
        row["start_idx"] = int(row["start_idx"])
        row["end_idx"] = int(row["end_idx"])
        out.append(row)
    return out


def write_csv(path: Path, header: List[str], rows: List[List[Any]]) -> None:
    lines = [",".join(header)]
    for r in rows:
        lines.append(",".join(str(x) for x in r))
    path.write_text("\n".join(lines), encoding="utf-8")


# -------------------------
# Clustering (k-means 1D)
# -------------------------

def kmeans_1d(x: np.ndarray, k: int, iters: int = 50, seed: int = 0) -> Tuple[np.ndarray, np.ndarray]:
    """
    Simple k-means 1D.
    Returns:
      centers (k,), labels (n,)
    """
    x = np.asarray(x, dtype=np.float64)
    n = x.size
    if n == 0:
        return np.array([], dtype=np.float64), np.array([], dtype=np.int64)

    rng = np.random.default_rng(seed)

    # init centers via quantiles (stable)
    qs = np.linspace(0.1, 0.9, k)
    centers = np.quantile(x, qs).astype(np.float64)

    for _ in range(iters):
        # assign
        d = np.abs(x[:, None] - centers[None, :])
        labels = np.argmin(d, axis=1)

        new_centers = centers.copy()
        for i in range(k):
            if np.any(labels == i):
                new_centers[i] = np.mean(x[labels == i])

        # converge
        if np.allclose(new_centers, centers, rtol=0, atol=1e-9):
            centers = new_centers
            break
        centers = new_centers

    # sort centers and remap labels accordingly
    order = np.argsort(centers)
    centers_sorted = centers[order]

    # remap labels
    inv = np.empty_like(order)
    inv[order] = np.arange(k)
    labels_sorted = inv[labels]

    return centers_sorted, labels_sorted.astype(np.int64)


def silhouette_1d(x: np.ndarray, labels: np.ndarray, centers: np.ndarray) -> float:
    """
    Silhouette score approximé (distance abs).
    Suffisant pour choisir k.
    """
    x = np.asarray(x, dtype=np.float64)
    labels = np.asarray(labels, dtype=np.int64)
    k = centers.size
    n = x.size
    if n < 3 or k < 2:
        return -1.0

    # Precompute cluster members
    clusters = [x[labels == i] for i in range(k)]
    if any(len(c) == 0 for c in clusters):
        return -1.0

    # For each point: a = mean dist to same cluster; b = min mean dist to other cluster
    s_vals = []
    for i in range(n):
        ci = labels[i]
        xi = x[i]
        same = clusters[ci]
        if len(same) <= 1:
            continue
        a = np.mean(np.abs(same - xi))
        b = np.inf
        for cj in range(k):
            if cj == ci:
                continue
            other = clusters[cj]
            b = min(b, np.mean(np.abs(other - xi)))
        if not np.isfinite(b) or max(a, b) < 1e-12:
            continue
        s = (b - a) / max(a, b)
        s_vals.append(s)

    if not s_vals:
        return -1.0
    return float(np.mean(s_vals))


# -------------------------
# Symbol sequence
# -------------------------

def label_to_symbol(idx: int) -> str:
    # A, B, C...
    return chr(ord("A") + idx)


def run_length_symbols(symbols: List[str]) -> List[Tuple[str, int]]:
    if not symbols:
        return []
    out = []
    cur = symbols[0]
    ln = 1
    for s in symbols[1:]:
        if s == cur:
            ln += 1
        else:
            out.append((cur, ln))
            cur = s
            ln = 1
    out.append((cur, ln))
    return out


# -------------------------
# Plots
# -------------------------

def save_plots(out_dir: Path, durations: np.ndarray, labels: np.ndarray, centers: np.ndarray):
    ensure_dir(out_dir)

    # histogram
    fig, ax = plt.subplots(figsize=(10, 3))
    ax.hist(durations, bins=40)
    ax.set_title("Segment duration histogram")
    ax.set_xlabel("duration (s)")
    fig.savefig(out_dir / "duration_hist.png", dpi=160, bbox_inches="tight")
    plt.close(fig)

    # scatter over index
    fig, ax = plt.subplots(figsize=(12, 3))
    ax.scatter(np.arange(len(durations)), durations, s=12)
    ax.set_title("Segment durations over time (by segment index)")
    ax.set_xlabel("segment index")
    ax.set_ylabel("duration (s)")
    fig.savefig(out_dir / "duration_scatter.png", dpi=160, bbox_inches="tight")
    plt.close(fig)

    # centers lines
    fig, ax = plt.subplots(figsize=(10, 3))
    ax.scatter(durations, labels, s=12)
    ax.set_title("Durations vs cluster label")
    ax.set_xlabel("duration (s)")
    ax.set_ylabel("cluster (0..k-1)")
    for i, c in enumerate(centers):
        ax.axvline(c, linestyle="--")
    fig.savefig(out_dir / "duration_clusters.png", dpi=160, bbox_inches="tight")
    plt.close(fig)


# -------------------------
# Main
# -------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("segments_csv", type=str, help="Path to segments.csv (from segment_morpho_timeline.py)")
    ap.add_argument("--out", type=str, default="", help="Output folder (default: alongside segments.csv)")
    ap.add_argument("--k", type=int, default=0, help="Force number of duration classes (0 = auto choose)")
    ap.add_argument("--k_min", type=int, default=3, help="Min k for auto")
    ap.add_argument("--k_max", type=int, default=8, help="Max k for auto")
    ap.add_argument("--min_dur", type=float, default=0.0, help="Drop segments shorter than this (s)")
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    seg_path = Path(args.segments_csv)
    segs = read_segments_csv(seg_path)
    if not segs:
        raise SystemExit("segments.csv is empty or unreadable.")

    # filter
    segs = [s for s in segs if s["duration_s"] >= float(args.min_dur)]
    if not segs:
        raise SystemExit("No segments left after filtering min_dur.")

    durations = np.array([s["duration_s"] for s in segs], dtype=np.float64)

    out_dir = Path(args.out) if args.out else seg_path.parent / "quantized"
    ensure_dir(out_dir)

    # choose k
    if args.k and args.k > 0:
        k = int(args.k)
        centers, labels = kmeans_1d(durations, k=k, seed=int(args.seed))
        best_sil = silhouette_1d(durations, labels, centers)
        choose_info = {"mode": "forced", "k": k, "silhouette": best_sil}
    else:
        best = None
        for k_try in range(int(args.k_min), int(args.k_max) + 1):
            centers_t, labels_t = kmeans_1d(durations, k=k_try, seed=int(args.seed))
            sil = silhouette_1d(durations, labels_t, centers_t)
            # prefer higher silhouette, slight penalty for big k to avoid over-splitting
            score = sil - 0.03 * (k_try - int(args.k_min))
            cand = (score, sil, k_try, centers_t, labels_t)
            if best is None or cand[0] > best[0]:
                best = cand

        assert best is not None
        _, sil, k, centers, labels = best
        choose_info = {"mode": "auto", "k": int(k), "silhouette": float(sil), "k_min": int(args.k_min), "k_max": int(args.k_max)}

    # symbols per segment
    symbols = [label_to_symbol(int(l)) for l in labels]
    rle = run_length_symbols(symbols)

    # cluster stats
    cluster_rows = []
    for i in range(int(k)):
        vals = durations[labels == i]
        cluster_rows.append([
            label_to_symbol(i),
            i,
            float(centers[i]),
            float(np.mean(vals)) if vals.size else "",
            float(np.median(vals)) if vals.size else "",
            float(np.std(vals)) if vals.size else "",
            int(vals.size),
            float(np.min(vals)) if vals.size else "",
            float(np.max(vals)) if vals.size else "",
        ])

    write_csv(
        out_dir / "duration_clusters.csv",
        ["symbol", "cluster_id", "center_s", "mean_s", "median_s", "std_s", "count", "min_s", "max_s"],
        cluster_rows
    )

    # sequence outputs
    (out_dir / "symbols_sequence.txt").write_text(" ".join(symbols), encoding="utf-8")
    (out_dir / "symbols_runs.txt").write_text("\n".join([f"{s} x{n}" for s, n in rle]), encoding="utf-8")

    # report
    md = []
    md.append("# Duration Quantization Report")
    md.append("")
    md.append("This converts segment durations into discrete symbol classes (A,B,C...).")
    md.append("")
    md.append("## Input")
    md.append(f"- segments_csv: `{seg_path}`")
    md.append(f"- segment_count_used: {len(segs)}")
    md.append(f"- duration_range_s: [{durations.min():.4f}, {durations.max():.4f}]")
    md.append("")
    md.append("## k selection")
    for kx, vx in choose_info.items():
        md.append(f"- {kx}: {vx}")
    md.append("")
    md.append("## Classes")
    md.append("| symbol | center (s) | count | min | max | median | std |")
    md.append("|:--:|---:|---:|---:|---:|---:|---:|")
    for row in cluster_rows:
        sym, _, center, mean, med, std, cnt, mn, mx = row
        md.append(f"| {sym} | {center:.4f} | {cnt} | {mn:.4f} | {mx:.4f} | {med:.4f} | {std:.4f} |")
    md.append("")
    md.append("## Sequence (symbols)")
    md.append("```")
    seq = " ".join(symbols)
    if len(seq) > 4000:
        md.append(seq[:2000])
        md.append("... (truncated) ...")
        md.append(seq[-2000:])
    else:
        md.append(seq)
    md.append("```")
    md.append("")
    md.append("## Runs (RLE)")
    md.append("```")
    md.extend([f"{s} x{n}" for s, n in rle])
    md.append("```")
    md.append("")
    md.append("## Outputs")
    md.append("- duration_clusters.csv")
    md.append("- symbols_sequence.txt")
    md.append("- symbols_runs.txt")
    md.append("- duration_hist.png / duration_scatter.png / duration_clusters.png")
    md.append("")

    (out_dir / "QUANTIZATION_REPORT.md").write_text("\n".join(md), encoding="utf-8")

    # plots
    save_plots(out_dir, durations, labels, centers)

    print(f"Wrote: {out_dir / 'QUANTIZATION_REPORT.md'}")
    print(f"Wrote: {out_dir / 'duration_clusters.csv'}")
    print(f"Wrote: {out_dir / 'symbols_sequence.txt'}")
    print(f"Wrote: {out_dir / 'symbols_runs.txt'}")


if __name__ == "__main__":
    main()
