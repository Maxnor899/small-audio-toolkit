#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
decode_ook_integrated.py

Décodage OOK "intégré" (fenêtré) :
- Band-pass autour d'une porteuse (par défaut 393 Hz)
- Enveloppe (Hilbert)
- Intégration de l'énergie sur fenêtres de durée Ts (symbol period)
- Seuil sur énergie par fenêtre (k-means 2 classes + fallback)
- Symboles: H (high energy) / L (low energy)
- Séparateurs: runs longs de L -> '|'
- Triplets: groupage par 3 symboles H/L au sein de chaque chunk (séparé par '|')

Dépendances:
  pip install numpy scipy soundfile matplotlib

Usage:
  python decode_ook_integrated.py lsig.flac --out decode_int_diff --fc 393 --domain diff
  python decode_ook_integrated.py lsig.flac --out decode_int_sum  --fc 393 --domain sum

Options utiles:
  --ts_ms 60           (force Ts en ms)
  --ts_min_ms 30 --ts_max_ms 120  (auto recherche)
  --sep_run 6          (nombre de fenêtres L consécutives pour un séparateur)
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import List, Tuple, Dict, Any, Optional

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
    """Mini k-means 1D (k=2): retourne (c_low, c_high, labels 0/1)."""
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

    if c2 < c1:
        c1, c2 = c2, c1
        lab = 1 - lab

    return c1, c2, lab


def window_mean(x: np.ndarray, win: int) -> np.ndarray:
    """Mean par fenêtres non chevauchées."""
    n = len(x)
    m = n // win
    if m <= 0:
        return np.array([], dtype=np.float64)
    xx = x[: m * win].reshape(m, win)
    return xx.mean(axis=1)


def majority_filter_bits(bits: np.ndarray, k: int = 3) -> np.ndarray:
    """Filtrage majoritaire simple sur bits 0/1."""
    bits = np.asarray(bits, dtype=np.int8)
    if bits.size < k or k <= 1:
        return bits
    pad = k // 2
    b = np.pad(bits, (pad, pad), mode="edge")
    out = np.empty_like(bits)
    for i in range(bits.size):
        out[i] = 1 if np.sum(b[i:i+k]) > (k // 2) else 0
    return out


def runs(values: np.ndarray) -> List[Tuple[int, int]]:
    """Run-length encode d'une suite 0/1. Renvoie (val, length)."""
    v = np.asarray(values, dtype=np.int8)
    if v.size == 0:
        return []
    out: List[Tuple[int, int]] = []
    cur = int(v[0])
    ln = 1
    for x in v[1:]:
        x = int(x)
        if x == cur:
            ln += 1
        else:
            out.append((cur, ln))
            cur = x
            ln = 1
    out.append((cur, ln))
    return out


# -------------------------
# Integrated OOK decoding
# -------------------------

def score_bimodality(c_low: float, c_high: float, x: np.ndarray) -> float:
    """Score heuristique: séparation relative des clusters."""
    x = np.asarray(x, dtype=np.float64)
    if not np.isfinite(c_low) or not np.isfinite(c_high) or c_high <= c_low or x.size < 10:
        return -1.0
    sep = (c_high - c_low)
    sd = np.std(x) + 1e-12
    return float(sep / sd)


def choose_ts_samples(env: np.ndarray, fs: float, ts_min_ms: float, ts_max_ms: float) -> Tuple[int, Dict[str, Any]]:
    """
    Auto-choix de Ts par balayage (fenêtrage + score de bimodalité).
    On teste des Ts de 30 à 120ms typiquement.
    """
    dbg: Dict[str, Any] = {"candidates": []}
    best_ts = None
    best_score = -1e9

    # pas de 1 ms
    for ts_ms in range(int(ts_min_ms), int(ts_max_ms) + 1):
        ts = int(round((ts_ms / 1000.0) * fs))
        if ts < 8:
            continue
        e = window_mean(env, ts)
        if e.size < 50:
            continue

        c1, c2, _ = kmeans_1d_2clusters(e)
        s = score_bimodality(c1, c2, e)

        # pénalise les Ts absurdes avec trop peu de fenêtres
        s2 = s + 0.05 * np.log10(e.size)

        dbg["candidates"].append({"ts_ms": ts_ms, "ts_samples": ts, "score": float(s2), "c_low": float(c1), "c_high": float(c2), "n_windows": int(e.size)})
        if s2 > best_score:
            best_score = s2
            best_ts = ts

    if best_ts is None:
        # fallback "raisonnable"
        best_ts = int(round(0.06 * fs))  # 60ms

    dbg["best"] = {"ts_samples": int(best_ts), "score": float(best_score)}
    return int(best_ts), dbg


def decode_integrated_ook(
    x: np.ndarray,
    fs: float,
    fc: float,
    rel_bw: float,
    ts_samples: Optional[int],
    ts_min_ms: float,
    ts_max_ms: float,
    sep_run: int,
    majority_k: int,
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Retourne result + debug.
    result contient symbols, triplets, etc.
    """

    # Normalisation robuste (pour rendre l'enveloppe exploitable)
    x = np.asarray(x, dtype=np.float64)
    x = x - np.mean(x)
    x = x / (np.std(x) + 1e-12)

    x_bp = bandpass(x, fs, fc, rel_bw=rel_bw, order=4)
    env = np.abs(hilbert(x_bp))

    auto_dbg = None
    if ts_samples is None:
        ts_samples, auto_dbg = choose_ts_samples(env, fs, ts_min_ms, ts_max_ms)

    energies = window_mean(env, ts_samples)

    # seuil par fenêtre (kmeans + fallback)
    c_low, c_high, _ = kmeans_1d_2clusters(energies)
    if (not np.isfinite(c_low)) or (not np.isfinite(c_high)) or (c_high <= c_low):
        thr = float(np.median(energies) + 0.5 * np.std(energies))
        thr_mode = "fallback(median+0.5*std)"
    else:
        thr = float(0.5 * (c_low + c_high))
        thr_mode = "kmeans(midpoint)"

    bits = (energies > thr).astype(np.int8)  # 1=High, 0=Low
    bits_f = majority_filter_bits(bits, k=majority_k)

    # Runs pour générer symboles + séparateurs
    r = runs(bits_f)

    # Symboles par fenêtre: H/L
    symbols_windows = "".join("H" if b else "L" for b in bits_f)

    # Symbol stream compressé avec séparateurs:
    # - on convertit les runs: High run -> "H"*len ; Low run -> "L"*len ou " | " si long
    parts: List[str] = []
    for val, ln in r:
        if val == 1:
            parts.append("H" * ln)
        else:
            if ln >= sep_run:
                parts.append("|")
            else:
                parts.append("L" * ln)
    symbols = "".join(parts)

    # Triplets
    triplets: List[str] = []
    for chunk in symbols.split("|"):
        chunk = "".join(c for c in chunk if c in ("H", "L"))
        usable = len(chunk) - (len(chunk) % 3)
        for i in range(0, usable, 3):
            triplets.append(chunk[i:i+3])

    result: Dict[str, Any] = {
        "fs_hz": float(fs),
        "fc_hz": float(fc),
        "rel_bw": float(rel_bw),
        "ts_samples": int(ts_samples),
        "ts_ms": float(1000.0 * ts_samples / fs),
        "threshold": float(thr),
        "threshold_mode": thr_mode,
        "energy_centers": {"low": float(c_low), "high": float(c_high)},
        "counts": {
            "n_windows": int(energies.size),
            "high_windows": int(np.sum(bits_f == 1)),
            "low_windows": int(np.sum(bits_f == 0)),
            "separators": int(symbols.count("|")),
            "triplets": int(len(triplets)),
        },
        "symbols_windows": symbols_windows,
        "symbols": symbols,
        "triplets": triplets,
    }

    debug: Dict[str, Any] = {
        "x_bp": x_bp,
        "env": env,
        "energies": energies,
        "bits_raw": bits,
        "bits_f": bits_f,
        "auto_ts_debug": auto_dbg,
    }
    return result, debug


# -------------------------
# Outputs
# -------------------------

def save_plots(out_dir: Path, fs: float, ts_samples: int, x_bp: np.ndarray, env: np.ndarray, energies: np.ndarray, bits_f: np.ndarray, prefix: str) -> None:
    ensure_dir(out_dir)

    # 1) bandpassed + env (first 6s)
    n = min(len(x_bp), int(fs * 6))
    t = np.arange(n) / fs

    fig, ax = plt.subplots(figsize=(12, 3))
    ax.plot(t, x_bp[:n])
    ax.set_title(f"{prefix} Bandpassed (first 6s)")
    ax.set_xlabel("Time (s)")
    fig.savefig(out_dir / f"{prefix}_bandpassed.png", dpi=160, bbox_inches="tight")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(12, 3))
    ax.plot(t, env[:n])
    ax.set_title(f"{prefix} Envelope (first 6s)")
    ax.set_xlabel("Time (s)")
    fig.savefig(out_dir / f"{prefix}_envelope.png", dpi=160, bbox_inches="tight")
    plt.close(fig)

    # 2) window energies + bits (first 300 windows)
    m = min(len(energies), 300)
    tw = (np.arange(m) * ts_samples) / fs

    fig, ax = plt.subplots(figsize=(12, 3))
    ax.plot(tw, energies[:m])
    ax.set_title(f"{prefix} Window energies (first {m} windows)")
    ax.set_xlabel("Time (s)")
    fig.savefig(out_dir / f"{prefix}_energies.png", dpi=160, bbox_inches="tight")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(12, 2.5))
    ax.plot(tw, bits_f[:m])
    ax.set_ylim(-0.2, 1.2)
    ax.set_title(f"{prefix} H/L decisions per window (first {m} windows)")
    ax.set_xlabel("Time (s)")
    fig.savefig(out_dir / f"{prefix}_bits.png", dpi=160, bbox_inches="tight")
    plt.close(fig)


def write_report(out_dir: Path, src: str, domain: str, res: Dict[str, Any]) -> None:
    md: List[str] = []
    md.append("# Integrated OOK Decode Report")
    md.append("")
    md.append("This report decodes a weak-contrast OOK-like signal by integrating envelope energy over symbol-sized windows.")
    md.append("It outputs H/L symbols and chunk separators ('|'), then groups H/L into triplets.")
    md.append("")
    md.append("## Input")
    md.append(f"- file: `{src}`")
    md.append(f"- domain: `{domain}`")
    md.append(f"- sample_rate: {res['fs_hz']:.3f} Hz")
    md.append(f"- carrier_fc: {res['fc_hz']:.3f} Hz (rel_bw={res['rel_bw']})")
    md.append("")
    md.append("## Windowing")
    md.append(f"- Ts: {res['ts_samples']} samples ({res['ts_ms']:.2f} ms)")
    md.append("")
    md.append("## Thresholding on window energies")
    md.append(f"- centers: low={res['energy_centers']['low']}, high={res['energy_centers']['high']}")
    md.append(f"- threshold: {res['threshold']} ({res['threshold_mode']})")
    md.append("")
    md.append("## Counts")
    for k, v in res["counts"].items():
        md.append(f"- {k}: {v}")
    md.append("")
    md.append("## Symbol stream (compressed with '|')")
    sym = res.get("symbols", "")
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
    trips = res.get("triplets", [])
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
    md.append("## Plots")
    md.append("- `*_bandpassed.png`")
    md.append("- `*_envelope.png`")
    md.append("- `*_energies.png`")
    md.append("- `*_bits.png`")
    md.append("")

    (out_dir / "INTEGRATED_OOK_REPORT.md").write_text("\n".join(md), encoding="utf-8")


def write_csv(out_dir: Path, energies: np.ndarray, bits_f: np.ndarray) -> None:
    p = out_dir / "window_energies.csv"
    lines = ["index,energy,bit"]
    for i, (e, b) in enumerate(zip(energies, bits_f)):
        lines.append(f"{i},{float(e)},{int(b)}")
    p.write_text("\n".join(lines), encoding="utf-8")


# -------------------------
# Main
# -------------------------

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("audio_file", type=str)
    ap.add_argument("--out", type=str, default="decode_integrated")
    ap.add_argument("--fc", type=float, default=393.0)
    ap.add_argument("--domain", type=str, default="diff", choices=["sum", "diff", "left", "right"])
    ap.add_argument("--rel_bw", type=float, default=0.05)

    ap.add_argument("--ts_ms", type=float, default=0.0, help="Force Ts in ms (0 = auto).")
    ap.add_argument("--ts_min_ms", type=float, default=30.0)
    ap.add_argument("--ts_max_ms", type=float, default=120.0)

    ap.add_argument("--sep_run", type=int, default=6, help="Low-run length (in windows) to insert '|'.")
    ap.add_argument("--majority_k", type=int, default=3, help="Majority filter size on window bits (odd >=1).")

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

    ts_samples = None
    if args.ts_ms and args.ts_ms > 0:
        ts_samples = int(round((args.ts_ms / 1000.0) * fs))

    res, dbg = decode_integrated_ook(
        sig,
        fs=float(fs),
        fc=float(args.fc),
        rel_bw=float(args.rel_bw),
        ts_samples=ts_samples,
        ts_min_ms=float(args.ts_min_ms),
        ts_max_ms=float(args.ts_max_ms),
        sep_run=int(args.sep_run),
        majority_k=int(args.majority_k if args.majority_k >= 1 else 1),
    )

    # outputs
    write_report(out_dir, src=str(in_path), domain=args.domain, res=res)
    (out_dir / "symbols_HL.txt").write_text(res.get("symbols", ""), encoding="utf-8")
    (out_dir / "symbols_per_window.txt").write_text(res.get("symbols_windows", ""), encoding="utf-8")
    (out_dir / "triplets.txt").write_text("\n".join(res.get("triplets", [])), encoding="utf-8")
    write_csv(out_dir, dbg["energies"], dbg["bits_f"])

    prefix = f"fc_{args.fc:.3f}_{args.domain}_Ts{res['ts_ms']:.1f}ms"
    save_plots(out_dir, fs=float(fs), ts_samples=int(res["ts_samples"]), x_bp=dbg["x_bp"], env=dbg["env"], energies=dbg["energies"], bits_f=dbg["bits_f"], prefix=prefix)

    # si auto Ts, dump un petit résumé
    if dbg.get("auto_ts_debug") is not None:
        best = dbg["auto_ts_debug"].get("best", {})
        (out_dir / "auto_ts_best.txt").write_text(str(best), encoding="utf-8")

    print(f"Wrote: {out_dir / 'INTEGRATED_OOK_REPORT.md'}")
    print(f"Wrote: {out_dir / 'symbols_HL.txt'}")
    print(f"Wrote: {out_dir / 'triplets.txt'}")
    print(f"Wrote: {out_dir / 'window_energies.csv'}")


if __name__ == "__main__":
    main()
