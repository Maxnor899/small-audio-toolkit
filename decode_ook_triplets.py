#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
decode_ook_triplets.py

Décodage OOK "TP-style" (symbolique):
1) Band-pass autour d'une porteuse (par défaut 393 Hz)
2) Enveloppe (Hilbert) + lissage
3) Seuillage auto (k-means 2 classes) + fallback robuste
4) Nettoyage anti-grésillement (suppression de segments trop courts)
5) Run-length encoding -> durées ON/OFF
6) Clustering des durées ON (court/long) -> H/L
7) Clustering des durées OFF (court/long) -> séparateur '|'
8) Sortie: symbols_HL.txt + triplets.txt + rapport Markdown + plots

Dépendances:
  pip install numpy scipy soundfile matplotlib

Usage recommandé (domaine diff):
  python decode_ook_triplets.py lsig.flac --out decode_ook_diff --fc 393 --domain diff --smooth_ms 5 --min_seg_ms 3
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import List, Tuple, Dict, Any

import numpy as np
import soundfile as sf
from scipy.signal import butter, filtfilt, hilbert
import matplotlib.pyplot as plt


# -------------------------
# Helpers
# -------------------------

def ensure_dir(p: Path) -> Path:
    p.mkdir(parents=True, exist_ok=True)
    return p


def moving_average(x: np.ndarray, win: int) -> np.ndarray:
    win = max(1, int(win))
    if win == 1:
        return x
    k = np.ones(win, dtype=np.float64) / win
    return np.convolve(x, k, mode="same")


def butter_bandpass(low_hz: float, high_hz: float, fs: float, order: int = 4):
    nyq = 0.5 * fs
    lo = max(1e-9, low_hz / nyq)
    hi = min(0.999999, high_hz / nyq)
    if hi <= lo:
        raise ValueError(f"Invalid bandpass: low={low_hz} high={high_hz} fs={fs}")
    b, a = butter(order, [lo, hi], btype="band")
    return b, a


def bandpass(x: np.ndarray, fs: float, fc: float, rel_bw: float = 0.05, order: int = 4) -> np.ndarray:
    bw = max(1.0, abs(fc) * rel_bw)
    lo = max(0.5, fc - bw)
    hi = fc + bw
    b, a = butter_bandpass(lo, hi, fs, order=order)
    return filtfilt(b, a, x).astype(np.float64)


def kmeans_1d_2clusters(x: np.ndarray, iters: int = 30) -> Tuple[float, float, np.ndarray]:
    """
    Mini k-means 1D (k=2).
    Retourne (c_low, c_high, labels) où labels vaut 0 (cluster bas) ou 1 (cluster haut).
    """
    x = np.asarray(x, dtype=np.float64)
    if x.size == 0:
        return float("nan"), float("nan"), np.array([], dtype=np.int64)

    c1 = float(np.percentile(x, 30))
    c2 = float(np.percentile(x, 70))

    for _ in range(iters):
        d1 = np.abs(x - c1)
        d2 = np.abs(x - c2)
        lab = (d2 < d1).astype(np.int64)
        if np.any(lab == 0):
            c1 = float(np.mean(x[lab == 0]))
        if np.any(lab == 1):
            c2 = float(np.mean(x[lab == 1]))

    # forcer c1<c2
    if c2 < c1:
        c1, c2 = c2, c1
        lab = 1 - lab

    return c1, c2, lab


def run_length_encode(mask01: np.ndarray) -> List[Tuple[int, int]]:
    """
    mask01: array 0/1
    retourne une liste de tuples (value, length_samples)
    """
    m = np.asarray(mask01).astype(np.int8)
    if m.size == 0:
        return []
    out: List[Tuple[int, int]] = []
    cur = int(m[0])
    ln = 1
    for v in m[1:]:
        v = int(v)
        if v == cur:
            ln += 1
        else:
            out.append((cur, ln))
            cur = v
            ln = 1
    out.append((cur, ln))
    return out


# -------------------------
# Core decoding
# -------------------------

def decode_ook_to_symbols_and_triplets(
    x: np.ndarray,
    fs: float,
    fc: float,
    rel_bw: float,
    smooth_ms: float,
    min_seg_ms: float,
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Retourne:
      result: dict (symbols, triplets, counts, thresholds, centers, etc.)
      debug: dict (x_bp, env_s, clean_mask, rle2, on/off lens, etc.)
    """

    # Normalisation robuste (très important pour domain diff)
    x = np.asarray(x, dtype=np.float64)
    x = x - np.mean(x)
    x = x / (np.std(x) + 1e-12)

    # 1) band-pass
    x_bp = bandpass(x, fs, fc, rel_bw=rel_bw, order=4)

    # 2) enveloppe
    z = hilbert(x_bp)
    env = np.abs(z)

    # 3) lissage enveloppe
    smooth_win = max(1, int(round((smooth_ms / 1000.0) * fs)))
    env_s = moving_average(env, smooth_win)
    if np.std(env_s) < 1e-4:
        raise RuntimeError("Envelope contrast too low: OOK not directly observable in this domain.")
    
    # 4) seuillage auto (kmeans) + fallback
    c_low, c_high, _ = kmeans_1d_2clusters(env_s)

    if (not np.isfinite(c_low)) or (not np.isfinite(c_high)) or (c_high <= c_low):
        thr = float(np.median(env_s) + 0.5 * np.std(env_s))
        thr_mode = "fallback(median+0.5*std)"
    else:
        thr = float(0.5 * (c_low + c_high))
        thr_mode = "kmeans(midpoint)"

    mask = (env_s > thr).astype(np.int8)  # 1=ON, 0=OFF

    # 5) nettoyage segments trop courts (anti-grésillement)
    rle = run_length_encode(mask)
    min_len = int(round((min_seg_ms / 1000.0) * fs))

    clean_mask = np.zeros_like(mask)
    idx = 0
    for val, ln in rle:
        if ln < min_len:
            val = 1 - val
        clean_mask[idx:idx + ln] = val
        idx += ln

    rle2 = run_length_encode(clean_mask)

    # 6) durées ON/OFF
    on_lens = np.array([ln for val, ln in rle2 if val == 1], dtype=np.float64)
    off_lens = np.array([ln for val, ln in rle2 if val == 0], dtype=np.float64)

    result: Dict[str, Any] = {
        "fc_hz": float(fc),
        "fs_hz": float(fs),
        "threshold": thr,
        "threshold_mode": thr_mode,
        "env_centers": {"low": float(c_low), "high": float(c_high)},
        "smooth_win_samples": int(smooth_win),
        "min_seg_samples": int(min_len),
        "counts": {
            "on_segments": int(on_lens.size),
            "off_segments": int(off_lens.size),
        },
        "symbols": "",
        "triplets": [],
        "duration_centers": {"on": None, "off": None},
        "duration_thresholds": {"on_thr": None, "off_thr": None},
    }

    debug: Dict[str, Any] = {
        "x_bp": x_bp,
        "env_s": env_s,
        "mask": mask,
        "clean_mask": clean_mask,
        "rle2": rle2,
        "on_lens": on_lens,
        "off_lens": off_lens,
    }

    # Pas assez de segments -> on s’arrête proprement
    if on_lens.size < 10 or off_lens.size < 10:
        return result, debug

    # 7) clustering durées ON (court/long) et OFF (court/long)
    on_c1, on_c2, _ = kmeans_1d_2clusters(on_lens)
    off_c1, off_c2, _ = kmeans_1d_2clusters(off_lens)

    on_thr = float(0.5 * (on_c1 + on_c2))
    off_thr = float(0.5 * (off_c1 + off_c2))

    result["duration_centers"]["on"] = {"short": float(on_c1), "long": float(on_c2)}
    result["duration_centers"]["off"] = {"short": float(off_c1), "long": float(off_c2)}
    result["duration_thresholds"]["on_thr"] = on_thr
    result["duration_thresholds"]["off_thr"] = off_thr

    # 8) mapping segments -> symbol stream
    parts: List[str] = []
    sep_count = 0
    hl_count = 0

    for val, ln in rle2:
        if val == 1:
            sym = "H" if float(ln) <= on_thr else "L"
            parts.append(sym)
            hl_count += 1
        else:
            # séparateur sur OFF long
            if float(ln) >= off_thr:
                parts.append("|")
                sep_count += 1

    symbols = "".join(parts)
    result["symbols"] = symbols
    result["counts"]["symbols_HL"] = int(hl_count)
    result["counts"]["separators"] = int(sep_count)

    # 9) triplets
    triplets: List[str] = []
    for chunk in symbols.split("|"):
        chunk = "".join([c for c in chunk if c in ("H", "L")])
        # group by 3
        usable = len(chunk) - (len(chunk) % 3)
        for i in range(0, usable, 3):
            triplets.append(chunk[i:i + 3])

    result["triplets"] = triplets
    return result, debug


# -------------------------
# Outputs
# -------------------------

def save_plots(out_dir: Path, fs: float, x_bp: np.ndarray, env_s: np.ndarray, clean_mask: np.ndarray, prefix: str) -> None:
    ensure_dir(out_dir)
    n = min(len(x_bp), int(fs * 6))  # 6 seconds
    t = np.arange(n) / fs

    fig, ax = plt.subplots(figsize=(12, 3))
    ax.plot(t, x_bp[:n])
    ax.set_title(f"{prefix} Bandpassed signal (first 6s)")
    ax.set_xlabel("Time (s)")
    fig.savefig(out_dir / f"{prefix}_bandpassed.png", dpi=160, bbox_inches="tight")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(12, 3))
    ax.plot(t, env_s[:n])
    ax.set_title(f"{prefix} Envelope (smoothed, first 6s)")
    ax.set_xlabel("Time (s)")
    fig.savefig(out_dir / f"{prefix}_envelope.png", dpi=160, bbox_inches="tight")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(12, 2.5))
    ax.plot(t, clean_mask[:n])
    ax.set_title(f"{prefix} OOK mask (ON=1, first 6s)")
    ax.set_xlabel("Time (s)")
    fig.savefig(out_dir / f"{prefix}_mask.png", dpi=160, bbox_inches="tight")
    plt.close(fig)


def write_report(out_dir: Path, src: str, domain: str, result: Dict[str, Any]) -> None:
    md: List[str] = []
    md.append("# OOK Triplets Decode Report")
    md.append("")
    md.append("This report extracts an OOK-like symbolic stream (H/L + separators) from a narrowband carrier, then groups symbols by triplets.")
    md.append("It does not assert meaning; it only converts the waveform into a representation suitable for TP-style decoding.")
    md.append("")
    md.append("## Input")
    md.append(f"- file: `{src}`")
    md.append(f"- domain: `{domain}`")
    md.append(f"- sample_rate: {result['fs_hz']:.3f} Hz")
    md.append(f"- carrier_fc: {result['fc_hz']:.3f} Hz")
    md.append("")
    md.append("## Thresholding")
    md.append(f"- env centers: low={result['env_centers']['low']}, high={result['env_centers']['high']}")
    md.append(f"- threshold: {result['threshold']} ({result['threshold_mode']})")
    md.append(f"- smooth_win_samples: {result['smooth_win_samples']}")
    md.append(f"- min_seg_samples: {result['min_seg_samples']}")
    md.append("")
    md.append("## Duration clustering")
    md.append(f"- ON centers: {result['duration_centers']['on']}")
    md.append(f"- OFF centers: {result['duration_centers']['off']}")
    md.append(f"- ON thr: {result['duration_thresholds']['on_thr']}")
    md.append(f"- OFF thr: {result['duration_thresholds']['off_thr']}")
    md.append("")
    md.append("## Counts")
    for k, v in result["counts"].items():
        md.append(f"- {k}: {v}")
    md.append("")

    md.append("## Symbol stream (H/L with '|' separators)")
    sym = result.get("symbols", "")
    md.append("")
    if not sym:
        md.append("_No symbols produced (insufficient segments or thresholding failed)._")
    else:
        md.append("```")
        if len(sym) > 4000:
            md.append(sym[:2000])
            md.append("... (truncated) ...")
            md.append(sym[-2000:])
        else:
            md.append(sym)
        md.append("```")
    md.append("")

    md.append("## Triplets")
    trips = result.get("triplets", [])
    if not trips:
        md.append("_No triplets produced._")
    else:
        md.append("```")
        line: List[str] = []
        for i, tri in enumerate(trips, 1):
            line.append(tri)
            if i % 40 == 0:
                md.append(" ".join(line))
                line = []
        if line:
            md.append(" ".join(line))
        md.append("```")
    md.append("")

    (out_dir / "OOK_TRIPLETS_REPORT.md").write_text("\n".join(md), encoding="utf-8")


# -------------------------
# Main
# -------------------------

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("audio_file", type=str)
    ap.add_argument("--out", type=str, default="decode_ook")
    ap.add_argument("--fc", type=float, default=393.0)
    ap.add_argument("--domain", type=str, default="diff", choices=["sum", "diff", "left", "right"])
    ap.add_argument("--rel_bw", type=float, default=0.05)
    ap.add_argument("--smooth_ms", type=float, default=5.0)
    ap.add_argument("--min_seg_ms", type=float, default=3.0)
    args = ap.parse_args()

    in_path = Path(args.audio_file)
    out_dir = ensure_dir(Path(args.out))

    audio, fs = sf.read(str(in_path), always_2d=True)
    audio = audio.astype(np.float64)

    left = audio[:, 0]
    right = audio[:, 1] if audio.shape[1] > 1 else audio[:, 0]
    summ = 0.5 * (left + right)
    diff = 0.5 * (left - right)

    if args.domain == "left":
        sig = left
    elif args.domain == "right":
        sig = right
    elif args.domain == "sum":
        sig = summ
    else:
        sig = diff

    result, debug = decode_ook_to_symbols_and_triplets(
        sig,
        fs=float(fs),
        fc=float(args.fc),
        rel_bw=float(args.rel_bw),
        smooth_ms=float(args.smooth_ms),
        min_seg_ms=float(args.min_seg_ms),
    )

    # Write outputs
    write_report(out_dir, src=str(in_path), domain=args.domain, result=result)

    (out_dir / "symbols_HL.txt").write_text(result.get("symbols", ""), encoding="utf-8")
    (out_dir / "triplets.txt").write_text("\n".join(result.get("triplets", [])), encoding="utf-8")

    prefix = f"fc_{args.fc:.3f}_{args.domain}"
    save_plots(out_dir, fs=float(fs), x_bp=debug["x_bp"], env_s=debug["env_s"], clean_mask=debug["clean_mask"], prefix=prefix)

    print(f"Wrote: {out_dir / 'OOK_TRIPLETS_REPORT.md'}")
    print(f"Wrote: {out_dir / 'symbols_HL.txt'}")
    print(f"Wrote: {out_dir / 'triplets.txt'}")
    print(f"Plots: {out_dir / (prefix + '_bandpassed.png')}")


if __name__ == "__main__":
    main()
