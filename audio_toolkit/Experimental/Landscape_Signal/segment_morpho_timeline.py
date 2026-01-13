#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
segment_morpho_timeline.py

Segmentation morphologique temporelle d'une "ligne" spectrale (ex: 393 Hz).
But: découper le signal en chunks structurés (présence/absence d'énergie autour de fc),
sans supposer une modulation classique (AM/FM/phase).

Dépendances:
  pip install numpy scipy soundfile matplotlib

Usage:
  python segment_morpho_timeline.py lsig.flac --out seg393_diff --fc 393 --domain diff
  python segment_morpho_timeline.py lsig.flac --out seg393_sum  --fc 393 --domain sum

Sorties:
  - SEGMENT_REPORT.md
  - segments.csv
  - band_energy.csv
  - plots: band_energy.png, mask_raw.png, mask_morph.png, spectrogram_roi.png
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, Any, List, Tuple

import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt

from scipy.signal import stft
from scipy.ndimage import binary_closing, binary_opening


# -------------------------
# Helpers
# -------------------------

def ensure_dir(p: Path) -> Path:
    p.mkdir(parents=True, exist_ok=True)
    return p


def robust_z(x: np.ndarray) -> np.ndarray:
    """Z-score robuste via median/MAD."""
    x = np.asarray(x, dtype=np.float64)
    med = np.median(x)
    mad = np.median(np.abs(x - med)) + 1e-12
    return (x - med) / (1.4826 * mad + 1e-12)


def contiguous_segments(mask: np.ndarray, t: np.ndarray) -> List[Dict[str, Any]]:
    """
    mask: bool array length N
    t: time array length N (timestamps aligned to mask)
    returns list of segments dicts with start/end/duration, idx ranges
    """
    mask = np.asarray(mask).astype(bool)
    if mask.size == 0:
        return []

    # transitions
    m = mask.astype(np.int8)
    dm = np.diff(m, prepend=m[0])
    # start where 0->1, end where 1->0
    starts = np.where(dm == 1)[0]
    ends = np.where(dm == -1)[0] - 1

    # if mask starts True, prepend start 0
    if mask[0]:
        starts = np.r_[0, starts]
    # if mask ends True, append last index
    if mask[-1]:
        ends = np.r_[ends, mask.size - 1]

    segs: List[Dict[str, Any]] = []
    for s, e in zip(starts, ends):
        if e < s:
            continue
        t0 = float(t[s])
        t1 = float(t[e])
        segs.append({
            "start_idx": int(s),
            "end_idx": int(e),
            "start_s": t0,
            "end_s": t1,
            "duration_s": float(max(0.0, t1 - t0)),
        })
    return segs


def write_csv(path: Path, header: List[str], rows: List[List[Any]]) -> None:
    lines = [",".join(header)]
    for r in rows:
        lines.append(",".join(str(x) for x in r))
    path.write_text("\n".join(lines), encoding="utf-8")


# -------------------------
# Core
# -------------------------

def extract_band_energy(
    x: np.ndarray,
    fs: float,
    fc: float,
    rel_bw: float,
    nperseg: int,
    noverlap: int,
    window: str,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, Dict[str, Any]]:
    """
    Returns:
      t_stft: times
      band_energy: energy over time within [fc-bw, fc+bw]
      roi_spec: spectrogram magnitude for ROI freqs x times (for plotting)
      meta: dict info incl. freq axis and ROI bounds
    """
    # STFT
    f, t, Z = stft(
        x,
        fs=fs,
        window=window,
        nperseg=nperseg,
        noverlap=noverlap,
        boundary=None,
        padded=False,
    )
    mag = np.abs(Z)  # (freq, time)

    bw = max(1.0, abs(fc) * rel_bw)
    f_lo = max(0.0, fc - bw)
    f_hi = fc + bw

    idx = np.where((f >= f_lo) & (f <= f_hi))[0]
    if idx.size < 3:
        # widen a little if resolution too coarse
        idx = np.where((f >= fc - 2*bw) & (f <= fc + 2*bw))[0]

    if idx.size == 0:
        # no bins, return empty
        return t, np.zeros_like(t), np.zeros((0, len(t))), {"f": f, "f_lo": f_lo, "f_hi": f_hi, "idx": idx}

    roi = mag[idx, :]
    # energy proxy: mean magnitude in the band (could also do sum of squares)
    band_energy = np.mean(roi, axis=0)

    meta = {"f": f, "f_lo": float(f_lo), "f_hi": float(f_hi), "idx": idx}
    return t, band_energy, roi, meta


def threshold_energy(
    e: np.ndarray,
    method: str,
    q: float,
    zthr: float,
) -> Tuple[np.ndarray, Dict[str, Any]]:
    """
    Returns mask_raw (bool) + info.
    method:
      - "quantile": threshold = quantile(e, q)
      - "robust_z": threshold on robust z-score > zthr
      - "hybrid": robust z-score > zthr OR e > quantile(e,q)
    """
    e = np.asarray(e, dtype=np.float64)
    info: Dict[str, Any] = {"method": method, "q": q, "zthr": zthr}

    if e.size == 0:
        return np.zeros(0, dtype=bool), info

    ez = robust_z(e)
    tq = float(np.quantile(e, q))
    info["thr_quantile"] = tq
    info["ez_median"] = float(np.median(ez))
    info["ez_std"] = float(np.std(ez))

    if method == "quantile":
        mask = e > tq
        info["thr_used"] = tq
    elif method == "robust_z":
        mask = ez > zthr
        info["thr_used"] = zthr
    else:  # hybrid
        mask = (ez > zthr) | (e > tq)
        info["thr_used"] = {"quantile": tq, "robust_z": zthr}

    return mask.astype(bool), info


def morph_clean_mask(
    mask: np.ndarray,
    close_len: int,
    open_len: int,
) -> np.ndarray:
    """
    Morphologie 1D sur le masque binaire:
      - closing comble petits trous
      - opening enlève petits éclats
    close_len/open_len sont en nombre de frames STFT.
    """
    m = np.asarray(mask).astype(bool)
    if m.size == 0:
        return m

    if close_len > 1:
        m = binary_closing(m, structure=np.ones(close_len, dtype=bool))
    if open_len > 1:
        m = binary_opening(m, structure=np.ones(open_len, dtype=bool))
    return m


def save_plots(
    out_dir: Path,
    t: np.ndarray,
    band_energy: np.ndarray,
    mask_raw: np.ndarray,
    mask_m: np.ndarray,
    roi: np.ndarray,
    meta: Dict[str, Any],
    fc: float,
    domain: str,
):
    ensure_dir(out_dir)

    # 1) energy curve
    fig, ax = plt.subplots(figsize=(12, 3))
    ax.plot(t, band_energy)
    ax.set_title(f"Band energy around {fc:.1f} Hz ({domain})")
    ax.set_xlabel("Time (s)")
    fig.savefig(out_dir / "band_energy.png", dpi=160, bbox_inches="tight")
    plt.close(fig)

    # 2) masks
    fig, ax = plt.subplots(figsize=(12, 2.3))
    ax.plot(t, mask_raw.astype(int))
    ax.set_ylim(-0.2, 1.2)
    ax.set_title("Raw binary mask (before morphology)")
    ax.set_xlabel("Time (s)")
    fig.savefig(out_dir / "mask_raw.png", dpi=160, bbox_inches="tight")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(12, 2.3))
    ax.plot(t, mask_m.astype(int))
    ax.set_ylim(-0.2, 1.2)
    ax.set_title("Morphologically cleaned mask")
    ax.set_xlabel("Time (s)")
    fig.savefig(out_dir / "mask_morph.png", dpi=160, bbox_inches="tight")
    plt.close(fig)

    # 3) spectrogram ROI (freq bins x time)
    if roi.size > 0:
        fig, ax = plt.subplots(figsize=(12, 3.2))
        # log display for readability
        img = np.log10(roi + 1e-12)
        ax.imshow(
            img,
            aspect="auto",
            origin="lower",
            extent=[float(t[0]), float(t[-1]), meta["f_lo"], meta["f_hi"]],
        )
        ax.set_title(f"Spectrogram ROI around {fc:.1f} Hz (log scale)")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Frequency (Hz)")
        fig.savefig(out_dir / "spectrogram_roi.png", dpi=160, bbox_inches="tight")
        plt.close(fig)


def write_report(
    out_dir: Path,
    src: str,
    domain: str,
    fc: float,
    rel_bw: float,
    stft_cfg: Dict[str, Any],
    thr_info: Dict[str, Any],
    close_len: int,
    open_len: int,
    segs: List[Dict[str, Any]],
):
    md: List[str] = []
    md.append("# Morphological Timeline Segmentation Report")
    md.append("")
    md.append("This report segments time into 'chunks' based on the presence of a narrowband spectral line around a carrier frequency.")
    md.append("It uses binary thresholding on band energy followed by 1D morphological cleaning (closing/opening).")
    md.append("")
    md.append("## Input")
    md.append(f"- file: `{src}`")
    md.append(f"- domain: `{domain}`")
    md.append(f"- fc: {fc:.3f} Hz (rel_bw={rel_bw})")
    md.append("")
    md.append("## STFT configuration")
    for k, v in stft_cfg.items():
        md.append(f"- {k}: {v}")
    md.append("")
    md.append("## Thresholding")
    for k, v in thr_info.items():
        md.append(f"- {k}: {v}")
    md.append("")
    md.append("## Morphology")
    md.append(f"- closing_len_frames: {close_len}")
    md.append(f"- opening_len_frames: {open_len}")
    md.append("")
    md.append("## Segments")
    md.append(f"- count: {len(segs)}")
    md.append("")
    if segs:
        md.append("| # | start (s) | end (s) | duration (s) |")
        md.append("|---:|---:|---:|---:|")
        for i, s in enumerate(segs, 1):
            md.append(f"| {i} | {s['start_s']:.3f} | {s['end_s']:.3f} | {s['duration_s']:.3f} |")
    else:
        md.append("_No segments found. Try adjusting threshold/morphology parameters._")
    md.append("")
    md.append("## Outputs")
    md.append("- `segments.csv`: list of segments")
    md.append("- `band_energy.csv`: band energy + raw/morph masks")
    md.append("- `band_energy.png`, `mask_raw.png`, `mask_morph.png`, `spectrogram_roi.png`")
    md.append("")

    (out_dir / "SEGMENT_REPORT.md").write_text("\n".join(md), encoding="utf-8")


# -------------------------
# Main
# -------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("audio_file", type=str)

    ap.add_argument("--out", type=str, default="seg_out")
    ap.add_argument("--fc", type=float, default=393.0)
    ap.add_argument("--rel_bw", type=float, default=0.03, help="Relative BW around fc (default 0.03 = ±3%).")

    ap.add_argument("--domain", type=str, default="diff", choices=["sum", "diff", "left", "right"])

    ap.add_argument("--nperseg", type=int, default=4096)
    ap.add_argument("--noverlap", type=int, default=3072)
    ap.add_argument("--window", type=str, default="hann")

    ap.add_argument("--thr_method", type=str, default="hybrid", choices=["quantile", "robust_z", "hybrid"])
    ap.add_argument("--thr_q", type=float, default=0.80, help="Quantile for threshold (default 0.80).")
    ap.add_argument("--thr_z", type=float, default=1.0, help="Robust z threshold (default 1.0).")

    ap.add_argument("--close_frames", type=int, default=5, help="Closing length in STFT frames (default 5).")
    ap.add_argument("--open_frames", type=int, default=3, help="Opening length in STFT frames (default 3).")

    ap.add_argument("--min_seg_s", type=float, default=0.10, help="Drop segments shorter than this (seconds).")

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
        x = left
    elif args.domain == "right":
        x = right
    elif args.domain == "sum":
        x = summ
    else:
        x = diff

    # optional: normalize lightly (helps comparisons)
    x = x - np.mean(x)
    x = x / (np.std(x) + 1e-12)

    # band energy over time
    t, band_e, roi, meta = extract_band_energy(
        x=x,
        fs=float(fs),
        fc=float(args.fc),
        rel_bw=float(args.rel_bw),
        nperseg=int(args.nperseg),
        noverlap=int(args.noverlap),
        window=str(args.window),
    )

    # threshold -> raw mask
    mask_raw, thr_info = threshold_energy(
        band_e,
        method=str(args.thr_method),
        q=float(args.thr_q),
        zthr=float(args.thr_z),
    )

    # morphology cleaning
    mask_m = morph_clean_mask(mask_raw, close_len=int(args.close_frames), open_len=int(args.open_frames))

    # segments
    segs = contiguous_segments(mask_m, t=t)

    # drop tiny segments
    segs2 = [s for s in segs if s["duration_s"] >= float(args.min_seg_s)]

    # save csv
    seg_rows = [[i+1, s["start_s"], s["end_s"], s["duration_s"], s["start_idx"], s["end_idx"]] for i, s in enumerate(segs2)]
    write_csv(out_dir / "segments.csv", ["id", "start_s", "end_s", "duration_s", "start_idx", "end_idx"], seg_rows)

    be_rows = [[i, float(ti), float(ei), int(mask_raw[i]), int(mask_m[i])] for i, (ti, ei) in enumerate(zip(t, band_e))]
    write_csv(out_dir / "band_energy.csv", ["frame", "time_s", "band_energy", "mask_raw", "mask_morph"], be_rows)

    # plots + report
    save_plots(out_dir, t, band_e, mask_raw, mask_m, roi, meta, fc=float(args.fc), domain=str(args.domain))

    stft_cfg = {"nperseg": int(args.nperseg), "noverlap": int(args.noverlap), "window": str(args.window), "frames": int(len(t))}
    write_report(
        out_dir,
        src=str(in_path),
        domain=str(args.domain),
        fc=float(args.fc),
        rel_bw=float(args.rel_bw),
        stft_cfg=stft_cfg,
        thr_info=thr_info,
        close_len=int(args.close_frames),
        open_len=int(args.open_frames),
        segs=segs2,
    )

    print(f"Wrote: {out_dir / 'SEGMENT_REPORT.md'}")
    print(f"Wrote: {out_dir / 'segments.csv'}")
    print(f"Wrote: {out_dir / 'band_energy.csv'}")


if __name__ == "__main__":
    main()
