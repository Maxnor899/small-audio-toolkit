#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
decode_audio_payload.py

Autoportant: charge un FLAC/WAV, extrait une/plusieurs porteuses probables,
tente des décodages (DPSK/BPSK/QPSK, FSK, OOK/ASK), et génère un rapport Markdown.

Dépendances: numpy, scipy, soundfile, matplotlib
  pip install numpy scipy soundfile matplotlib

Usage:
  python decode_audio_payload.py lsig.flac --out decode_out
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional

import numpy as np
import soundfile as sf

from scipy.signal import butter, filtfilt, hilbert, medfilt
import matplotlib.pyplot as plt


# ----------------------------
# Utilities
# ----------------------------

def ensure_dir(p: Path) -> Path:
    p.mkdir(parents=True, exist_ok=True)
    return p


def rms(x: np.ndarray) -> float:
    x = np.asarray(x, dtype=np.float64)
    return float(np.sqrt(np.mean(x * x) + 1e-12))


def normalize_rms(x: np.ndarray, target_db: float = -20.0) -> np.ndarray:
    """RMS normalize to target dBFS (approx)."""
    x = np.asarray(x, dtype=np.float64)
    target = 10 ** (target_db / 20.0)
    g = target / (rms(x) + 1e-12)
    return x * g


def butter_bandpass(low_hz: float, high_hz: float, fs: float, order: int = 4) -> Tuple[np.ndarray, np.ndarray]:
    nyq = 0.5 * fs
    low = max(1e-9, low_hz / nyq)
    high = min(0.999999, high_hz / nyq)
    if high <= low:
        raise ValueError(f"Invalid bandpass: low={low_hz} high={high_hz} fs={fs}")
    b, a = butter(order, [low, high], btype="band")
    return b, a


def bandpass(x: np.ndarray, fs: float, center_hz: float, rel_bw: float = 0.05, order: int = 4) -> np.ndarray:
    """Band-pass around center_hz with relative bandwidth (±rel_bw*center)."""
    bw = max(1.0, abs(center_hz) * rel_bw)
    lo = max(0.5, center_hz - bw)
    hi = center_hz + bw
    b, a = butter_bandpass(lo, hi, fs, order=order)
    return filtfilt(b, a, x).astype(np.float64)


def moving_average(x: np.ndarray, win: int) -> np.ndarray:
    win = max(1, int(win))
    if win == 1:
        return x
    k = np.ones(win, dtype=np.float64) / win
    return np.convolve(x, k, mode="same")


def bits_to_bytes(bits: np.ndarray) -> bytes:
    bits = np.asarray(bits).astype(np.uint8)
    n = (len(bits) // 8) * 8
    bits = bits[:n]
    if n == 0:
        return b""
    by = np.packbits(bits.reshape(-1, 8), axis=1, bitorder="big").flatten()
    return bytes(by.tolist())


def shannon_entropy_bits(bits: np.ndarray) -> float:
    bits = np.asarray(bits).astype(np.uint8)
    if bits.size == 0:
        return float("nan")
    p1 = float(bits.mean())
    p0 = 1.0 - p1
    def h(p):
        return 0.0 if p <= 1e-12 else -p * math.log2(p)
    return h(p0) + h(p1)


def guess_file_signatures(blob: bytes) -> List[str]:
    """Tiny signature sniffing (non exhaustive)."""
    sigs = []
    if blob.startswith(b"PK\x03\x04"):
        sigs.append("ZIP (PK\\x03\\x04)")
    if blob.startswith(b"\x89PNG\r\n\x1a\n"):
        sigs.append("PNG")
    if blob.startswith(b"%PDF"):
        sigs.append("PDF")
    if blob.startswith(b"RIFF") and blob[8:12] == b"WAVE":
        sigs.append("WAV (RIFF/WAVE)")
    if blob.startswith(b"\x1f\x8b"):
        sigs.append("GZIP")
    if blob.startswith(b"OggS"):
        sigs.append("OGG")
    if blob[:3] == b"ID3":
        sigs.append("MP3 (ID3)")
    return sigs


# ----------------------------
# Symbol timing estimation (simple & robust-ish)
# ----------------------------

def estimate_symbol_period_from_phase_jumps(phase: np.ndarray, fs: float) -> Dict[str, Any]:
    """
    Estimate symbol period Ts from phase jumps:
    - unwrap phase
    - compute abs(dphi)
    - detect "events" where abs(dphi) exceeds a robust threshold
    - look at histogram of inter-event intervals
    """
    ph = np.unwrap(phase.astype(np.float64))
    dphi = np.diff(ph)
    ad = np.abs(dphi)

    # Robust threshold: median + k * MAD
    med = float(np.median(ad))
    mad = float(np.median(np.abs(ad - med)) + 1e-12)
    thr = med + 8.0 * mad  # fairly strict

    idx = np.where(ad > thr)[0]
    # De-bounce: keep only events separated by >= min_sep samples
    min_sep = int(0.002 * fs)  # 2 ms
    events = []
    last = -10**9
    for i in idx.tolist():
        if i - last >= min_sep:
            events.append(i)
            last = i
    events = np.asarray(events, dtype=np.int64)

    out: Dict[str, Any] = {
        "threshold": thr,
        "event_count": int(events.size),
        "events": events,
        "best_Ts_s": None,
        "best_Ts_samples": None,
        "notes": [],
    }

    if events.size < 50:
        out["notes"].append("Not enough phase-jump events to estimate Ts reliably.")
        return out

    intervals = np.diff(events).astype(np.float64)
    # Remove tiny intervals (still possible)
    intervals = intervals[intervals > min_sep]

    if intervals.size < 50:
        out["notes"].append("Not enough stable inter-event intervals after filtering.")
        return out

    # Histogram mode
    lo = np.percentile(intervals, 5)
    hi = np.percentile(intervals, 95)
    if hi <= lo:
        out["notes"].append("Interval distribution degenerate.")
        return out

    bins = int(min(200, max(30, (hi - lo) // 2)))
    hist, edges = np.histogram(intervals, bins=bins, range=(lo, hi))
    k = int(np.argmax(hist))
    center = 0.5 * (edges[k] + edges[k + 1])

    Ts_samples = int(max(1, round(center)))
    Ts_s = Ts_samples / fs

    out["best_Ts_s"] = Ts_s
    out["best_Ts_samples"] = Ts_samples
    out["intervals_stats"] = {
        "median_samples": float(np.median(intervals)),
        "mean_samples": float(np.mean(intervals)),
        "std_samples": float(np.std(intervals)),
        "p10_samples": float(np.percentile(intervals, 10)),
        "p90_samples": float(np.percentile(intervals, 90)),
    }
    return out


def sample_at_symbol_times(x: np.ndarray, Ts: int, offset: int) -> np.ndarray:
    """Sample 1D array x every Ts samples starting at offset."""
    offset = int(max(0, min(len(x) - 1, offset)))
    idx = np.arange(offset, len(x), Ts, dtype=np.int64)
    return x[idx]


def pick_best_offset_by_cluster_separation(values: np.ndarray, Ts: int, offsets: int = 16) -> Tuple[int, float]:
    """
    Try several offsets in [0..Ts) and pick the one maximizing a simple separation metric.
    Works for phase-diff or inst-freq series.
    """
    best_off = 0
    best_score = -1.0
    for j in range(offsets):
        off = int(round(j * (Ts / offsets)))
        samp = sample_at_symbol_times(values, Ts, off)
        if samp.size < 50:
            continue
        # Score: (p90 - p10) / (std + eps) but capped
        p10 = np.percentile(samp, 10)
        p90 = np.percentile(samp, 90)
        sd = np.std(samp) + 1e-12
        score = float((p90 - p10) / sd)
        if score > best_score:
            best_score = score
            best_off = off
    return best_off, best_score


# ----------------------------
# Demodulators (hypothesis-driven)
# ----------------------------

def demod_dbpsk(phase: np.ndarray, fs: float, Ts: int, offset: int) -> np.ndarray:
    """DBPSK: bits from sign of phase difference between successive symbols."""
    ph = np.unwrap(phase.astype(np.float64))
    ph_s = sample_at_symbol_times(ph, Ts, offset)
    if ph_s.size < 3:
        return np.array([], dtype=np.uint8)
    d = np.diff(ph_s)
    # Wrap to [-pi, pi]
    d = (d + np.pi) % (2 * np.pi) - np.pi
    # Map: near 0 => 0, near pi/-pi => 1
    bits = (np.abs(d) > (np.pi / 2)).astype(np.uint8)
    return bits


def demod_dqpsk(phase: np.ndarray, fs: float, Ts: int, offset: int) -> np.ndarray:
    """
    DQPSK: 4 phase-diff states => 2 bits/symbol.
    We quantize delta phase to nearest of {0, pi/2, pi, -pi/2}.
    """
    ph = np.unwrap(phase.astype(np.float64))
    ph_s = sample_at_symbol_times(ph, Ts, offset)
    if ph_s.size < 3:
        return np.array([], dtype=np.uint8)
    d = np.diff(ph_s)
    d = (d + np.pi) % (2 * np.pi) - np.pi

    # Quantize
    refs = np.array([0.0, np.pi / 2, np.pi, -np.pi / 2], dtype=np.float64)
    idx = np.argmin(np.abs(d.reshape(-1, 1) - refs.reshape(1, -1)), axis=1)

    # Gray-ish mapping (common but not guaranteed)
    # 0 -> 00, +pi/2 -> 01, pi -> 11, -pi/2 -> 10
    mapping = {
        0: (0, 0),
        1: (0, 1),
        2: (1, 1),
        3: (1, 0),
    }
    bits = np.array([b for i in idx for b in mapping[int(i)]], dtype=np.uint8)
    return bits


def kmeans_1d_two_clusters(x: np.ndarray, iters: int = 20) -> Tuple[float, float, np.ndarray]:
    """Tiny 1D k-means (k=2) without sklearn."""
    x = np.asarray(x, dtype=np.float64)
    if x.size == 0:
        return 0.0, 0.0, np.array([], dtype=np.int64)
    c1, c2 = np.percentile(x, 25), np.percentile(x, 75)
    for _ in range(iters):
        d1 = np.abs(x - c1)
        d2 = np.abs(x - c2)
        lab = (d2 < d1).astype(np.int64)
        if np.any(lab == 0):
            c1 = float(np.mean(x[lab == 0]))
        if np.any(lab == 1):
            c2 = float(np.mean(x[lab == 1]))
    # ensure c1 < c2
    if c2 < c1:
        c1, c2 = c2, c1
        lab = 1 - lab
    return c1, c2, lab


def demod_bfsk_from_instfreq(inst_freq: np.ndarray, Ts: int, offset: int) -> np.ndarray:
    """Binary FSK by clustering instantaneous frequency samples at symbol times."""
    f_s = sample_at_symbol_times(inst_freq, Ts, offset)
    if f_s.size < 50:
        return np.array([], dtype=np.uint8)
    c1, c2, lab = kmeans_1d_two_clusters(f_s)
    # assign low freq -> 0, high -> 1
    bits = lab.astype(np.uint8)
    return bits


def demod_ook_from_envelope(envelope: np.ndarray, Ts: int, offset: int) -> np.ndarray:
    """OOK/ASK via envelope clustering at symbol times."""
    a_s = sample_at_symbol_times(envelope, Ts, offset)
    if a_s.size < 50:
        return np.array([], dtype=np.uint8)
    c1, c2, lab = kmeans_1d_two_clusters(a_s)
    bits = lab.astype(np.uint8)
    return bits


# ----------------------------
# Scoring & reporting helpers
# ----------------------------

@dataclass
class DecodeAttempt:
    name: str
    bits: np.ndarray
    Ts_samples: int
    offset: int
    meta: Dict[str, Any]

    def score(self) -> float:
        """Higher is better: prefer non-trivial entropy + compressibility-ish heuristics."""
        bits = self.bits
        if bits.size < 200:
            return -1.0
        ent = shannon_entropy_bits(bits)
        # Prefer not pure noise (entropy ~1) and not degenerate (~0)
        ent_score = 1.0 - abs(ent - 0.7)  # peak near 0.7 (heuristic)
        # Bias for balance
        p1 = float(bits.mean())
        bal = 1.0 - abs(p1 - 0.5) * 2.0  # 1 when 0.5, 0 when 0 or 1
        # Simple run-length metric: too many flips or too few flips both are suspicious
        flips = float(np.mean(bits[1:] != bits[:-1])) if bits.size > 1 else 0.0
        flip_score = 1.0 - abs(flips - 0.1)  # heuristic
        return float(ent_score + 0.5 * bal + 0.5 * flip_score)

    def summary(self) -> Dict[str, Any]:
        bits = self.bits
        blob = bits_to_bytes(bits[: 8 * 4096])  # first 4KB
        sigs = guess_file_signatures(blob)
        return {
            "name": self.name,
            "bit_len": int(bits.size),
            "Ts_samples": int(self.Ts_samples),
            "offset": int(self.offset),
            "entropy_bits": shannon_entropy_bits(bits),
            "p1": float(bits.mean()) if bits.size else float("nan"),
            "score": self.score(),
            "signatures": sigs,
            **self.meta,
        }


def save_bits_artifacts(out_dir: Path, attempt: DecodeAttempt) -> Dict[str, str]:
    """Save bits as .bin and .txt for inspection."""
    bits = attempt.bits
    paths: Dict[str, str] = {}
    if bits.size == 0:
        return paths

    base = out_dir / attempt.name.replace(" ", "_")
    # text
    txt_path = base.with_suffix(".bits.txt")
    txt_path.write_text("".join("1" if b else "0" for b in bits[:200000]), encoding="utf-8")
    paths["bits_txt"] = str(txt_path)

    # binary
    bin_path = base.with_suffix(".bin")
    bin_path.write_bytes(bits_to_bytes(bits))
    paths["bits_bin"] = str(bin_path)

    # first bytes as hex
    head = bits_to_bytes(bits[: 8 * 256])
    hex_path = base.with_suffix(".head.hex.txt")
    hex_path.write_text(head.hex(), encoding="utf-8")
    paths["head_hex"] = str(hex_path)

    return paths


def plot_quicklooks(out_dir: Path, fs: float, x: np.ndarray, env: np.ndarray, inst_f: np.ndarray, phase: np.ndarray, prefix: str) -> None:
    """Save a few quick plots (no interactive)."""
    ensure_dir(out_dir)
    n = min(len(x), int(fs * 5))  # first 5 seconds
    t = np.arange(n) / fs

    def save_fig(fig, name):
        fig.savefig(out_dir / f"{prefix}_{name}.png", dpi=150, bbox_inches="tight")
        plt.close(fig)

    fig, ax = plt.subplots(figsize=(10, 3))
    ax.plot(t, x[:n])
    ax.set_title("Bandpassed signal (first 5s)")
    ax.set_xlabel("Time (s)")
    save_fig(fig, "bandpassed")

    fig, ax = plt.subplots(figsize=(10, 3))
    ax.plot(t, env[:n])
    ax.set_title("Envelope (first 5s)")
    ax.set_xlabel("Time (s)")
    save_fig(fig, "envelope")

    fig, ax = plt.subplots(figsize=(10, 3))
    ax.plot(t, inst_f[:n])
    ax.set_title("Instantaneous frequency (first 5s)")
    ax.set_xlabel("Time (s)")
    save_fig(fig, "inst_freq")

    fig, ax = plt.subplots(figsize=(10, 3))
    ph = np.unwrap(phase[:n])
    ax.plot(t, ph)
    ax.set_title("Unwrapped phase (first 5s)")
    ax.set_xlabel("Time (s)")
    save_fig(fig, "phase_unwrapped")


# ----------------------------
# Main decoding pipeline
# ----------------------------

def decode_for_carrier(audio_mono: np.ndarray, fs: float, carrier_hz: float, out_dir: Path) -> Dict[str, Any]:
    """
    For one carrier hypothesis:
    - bandpass around carrier
    - analytic signal -> envelope, phase, inst freq
    - estimate Ts from phase jumps
    - try multiple offsets
    - run decoders: DBPSK, DQPSK, BFSK, OOK
    - rank attempts and save top artifacts
    """
    out: Dict[str, Any] = {"carrier_hz": carrier_hz, "fs": fs, "attempts": []}

    x_bp = bandpass(audio_mono, fs, carrier_hz, rel_bw=0.05, order=4)
    z = hilbert(x_bp)
    env = np.abs(z)
    ph = np.angle(z)
    # inst freq from phase derivative
    ph_u = np.unwrap(ph)
    inst_f = (fs / (2 * np.pi)) * np.diff(ph_u, prepend=ph_u[0])

    # Light smoothing to make sampling less jittery
    env_s = moving_average(env, int(0.001 * fs))          # 1 ms
    inst_f_s = medfilt(inst_f, kernel_size=max(3, int(0.001 * fs) | 1))  # odd

    plot_quicklooks(out_dir, fs, x_bp, env_s, inst_f_s, ph, prefix=f"fc_{carrier_hz:.3f}")

    timing = estimate_symbol_period_from_phase_jumps(ph, fs)
    out["timing_estimation"] = {k: (v.tolist() if isinstance(v, np.ndarray) else v) for k, v in timing.items() if k != "events"}
    # also save events count only
    out["timing_estimation"]["event_count"] = int(timing.get("event_count", 0))

    Ts = timing.get("best_Ts_samples", None)
    if Ts is None:
        # Fallback: try a small set of plausible Ts values (ms range)
        out["timing_estimation"]["notes"] = out["timing_estimation"].get("notes", []) + [
            "Falling back to heuristic Ts candidates (no reliable Ts estimate)."
        ]
        Ts_candidates = [int(fs * v) for v in [0.005, 0.01, 0.02, 0.05]]  # 5ms, 10ms, 20ms, 50ms
    else:
        Ts_candidates = [int(Ts)]
        # also try a couple harmonics/subharmonics (just in case)
        Ts_candidates += [max(1, int(Ts / 2)), int(Ts * 2)]

    attempts: List[DecodeAttempt] = []

    for Ts_c in sorted(set(Ts_candidates)):
        if Ts_c < 5 or Ts_c > int(fs * 0.5):  # ignore absurd symbol periods
            continue

        # pick offsets on the most informative signal for each demod
        # DPSK uses phase differences
        dphi = np.diff(np.unwrap(ph))
        dphi = (dphi + np.pi) % (2 * np.pi) - np.pi
        off_phi, score_phi = pick_best_offset_by_cluster_separation(dphi, Ts_c, offsets=16)

        # FSK uses inst freq
        off_f, score_f = pick_best_offset_by_cluster_separation(inst_f_s, Ts_c, offsets=16)

        # OOK uses envelope
        off_a, score_a = pick_best_offset_by_cluster_separation(env_s, Ts_c, offsets=16)

        # DBPSK
        bits = demod_dbpsk(ph, fs, Ts_c, off_phi)
        attempts.append(DecodeAttempt(
            name=f"fc_{carrier_hz:.3f}_DBPSK_Ts{Ts_c}_off{off_phi}",
            bits=bits,
            Ts_samples=Ts_c,
            offset=off_phi,
            meta={"offset_score": score_phi, "method": "DBPSK"},
        ))

        # DQPSK
        bits = demod_dqpsk(ph, fs, Ts_c, off_phi)
        attempts.append(DecodeAttempt(
            name=f"fc_{carrier_hz:.3f}_DQPSK_Ts{Ts_c}_off{off_phi}",
            bits=bits,
            Ts_samples=Ts_c,
            offset=off_phi,
            meta={"offset_score": score_phi, "method": "DQPSK"},
        ))

        # BFSK
        bits = demod_bfsk_from_instfreq(inst_f_s, Ts_c, off_f)
        attempts.append(DecodeAttempt(
            name=f"fc_{carrier_hz:.3f}_BFSK_Ts{Ts_c}_off{off_f}",
            bits=bits,
            Ts_samples=Ts_c,
            offset=off_f,
            meta={"offset_score": score_f, "method": "BFSK"},
        ))

        # OOK
        bits = demod_ook_from_envelope(env_s, Ts_c, off_a)
        attempts.append(DecodeAttempt(
            name=f"fc_{carrier_hz:.3f}_OOK_Ts{Ts_c}_off{off_a}",
            bits=bits,
            Ts_samples=Ts_c,
            offset=off_a,
            meta={"offset_score": score_a, "method": "OOK"},
        ))

    # rank
    attempts_sorted = sorted(attempts, key=lambda a: a.score(), reverse=True)
    out["attempts"] = [a.summary() for a in attempts_sorted[:50]]

    # save top-N artifacts
    keep = min(8, len(attempts_sorted))
    out["saved_artifacts"] = []
    for a in attempts_sorted[:keep]:
        art = save_bits_artifacts(out_dir, a)
        out["saved_artifacts"].append({"attempt": a.name, "paths": art, "summary": a.summary()})

    return out

def generate_markdown_report(out_path: Path, meta: Dict[str, Any], results: Dict[str, Any]) -> None:
    lines: List[str] = []
    lines.append("# Decode Report (Hypothesis-driven)")
    lines.append("")
    lines.append("This report attempts multiple demodulation hypotheses (PSK/DPSK, FSK, OOK) around detected/assumed carriers.")
    lines.append("It does **not** prove the existence of hidden information; it only surfaces structured candidates for inspection.")
    lines.append("")
    lines.append("## Input")
    lines.append(f"- File: `{meta['input_file']}`")
    lines.append(f"- Sample rate: {meta['fs']} Hz")
    lines.append(f"- Channels: {meta['channels']}")
    lines.append(f"- Duration: {meta['duration_s']:.2f} s")
    lines.append("")

    lines.append("## Carrier hypotheses")
    for c in meta["carriers_hz"]:
        lines.append(f"- {c:.3f} Hz")
    lines.append("")

    # results["per_carrier"] is actually a list of domains (sum/difference)
    for domain_block in results.get("per_carrier", []):
        domain_name = domain_block.get("domain", "unknown")
        lines.append(f"# Domain: {domain_name}")
        lines.append("")
        lines.append("This section reports decoding attempts applied to this derived signal (e.g., sum or difference).")
        lines.append("")

        for block in domain_block.get("carriers", []):
            fc = block.get("carrier_hz")
            if fc is None:
                # Skip malformed blocks gracefully
                continue

            lines.append(f"## Results for carrier {fc:.3f} Hz")
            lines.append("")

            te = block.get("timing_estimation", {})
            lines.append("### Symbol timing estimation (from phase jumps)")
            lines.append(f"- event_count: {te.get('event_count', 'N/A')}")
            lines.append(f"- best_Ts_samples: {te.get('best_Ts_samples', 'N/A')}")
            lines.append(f"- best_Ts_s: {te.get('best_Ts_s', 'N/A')}")
            if "intervals_stats" in te:
                st = te["intervals_stats"]
                lines.append(f"- interval median/mean/std (samples): {st.get('median_samples'):.1f} / {st.get('mean_samples'):.1f} / {st.get('std_samples'):.1f}")
            if te.get("notes"):
                lines.append("- notes:")
                for n in te["notes"]:
                    lines.append(f"  - {n}")
            lines.append("")

            lines.append("### Top decode candidates (ranked)")
            lines.append("")
            lines.append("| rank | method | Ts (samples) | offset | entropy(bits) | p1 | score | signatures |")
            lines.append("|---:|:--|---:|---:|---:|---:|---:|:--|")
            for i, a in enumerate(block.get("attempts", [])[:15], start=1):
                sigs = ", ".join(a.get("signatures", [])) if a.get("signatures") else ""
                ent = a.get("entropy_bits", float("nan"))
                p1 = a.get("p1", float("nan"))
                sc = a.get("score", float("nan"))
                lines.append(
                    f"| {i} | {a.get('method','')} | {a.get('Ts_samples','')} | {a.get('offset','')} | "
                    f"{float(ent):.3f} | {float(p1):.3f} | {float(sc):.3f} | {sigs} |"
                )
            lines.append("")

            if block.get("saved_artifacts"):
                lines.append("### Saved artifacts (top attempts)")
                lines.append("")
                for item in block["saved_artifacts"]:
                    summ = item.get("summary", {})
                    lines.append(f"- **{item.get('attempt','(unknown)')}**")
                    lines.append(f"  - method: {summ.get('method')}")
                    try:
                        lines.append(f"  - entropy: {float(summ.get('entropy_bits')):.3f}, p1: {float(summ.get('p1')):.3f}, score: {float(summ.get('score')):.3f}")
                    except Exception:
                        lines.append(f"  - entropy/p1/score: {summ.get('entropy_bits')}, {summ.get('p1')}, {summ.get('score')}")
                    if summ.get("signatures"):
                        lines.append(f"  - signatures: {', '.join(summ['signatures'])}")
                    for k, v in (item.get("paths") or {}).items():
                        lines.append(f"  - {k}: `{v}`")
                lines.append("")

        lines.append("")

    lines.append("## Quicklooks")
    lines.append("PNG plots were written next to artifacts (bandpassed/envelope/inst_freq/phase for first 5 seconds).")
    lines.append("")

    out_path.write_text("\n".join(lines), encoding="utf-8")

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("audio_file", type=str, help="Input audio file (FLAC/WAV).")
    ap.add_argument("--out", type=str, default="decode_out", help="Output directory.")
    ap.add_argument("--target_db", type=float, default=-20.0, help="RMS normalization target dB (optional).")
    ap.add_argument("--no_normalize", action="store_true", help="Disable RMS normalization.")
    ap.add_argument("--carriers", type=str, default="", help="Comma-separated carrier frequencies in Hz (override).")
    args = ap.parse_args()

    in_path = Path(args.audio_file)
    out_dir = ensure_dir(Path(args.out))

    x, fs = sf.read(str(in_path), always_2d=True)
    x = x.astype(np.float64)
    n = x.shape[0]
    ch = x.shape[1]
    dur = n / fs

    # Channels: left/right/sum/diff
    left = x[:, 0]
    right = x[:, 1] if ch > 1 else x[:, 0]
    summ = 0.5 * (left + right)
    diff = 0.5 * (left - right)

    if not args.no_normalize:
        left = normalize_rms(left, args.target_db)
        right = normalize_rms(right, args.target_db)
        summ = normalize_rms(summ, args.target_db)
        diff = normalize_rms(diff, args.target_db)

    # Carrier hypotheses
    if args.carriers.strip():
        carriers = [float(c.strip()) for c in args.carriers.split(",") if c.strip()]
    else:
        # From your Measurement Summary:
        # fundamental ~65.965 Hz; difference shows ~393.019 Hz.
        # We'll try both, plus a couple of simple multiples.
        carriers = [
            65.965,
            393.019,
            2 * 65.965,
            3 * 65.965,
        ]

    meta = {
        "input_file": str(in_path),
        "fs": float(fs),
        "channels": int(ch),
        "duration_s": float(dur),
        "carriers_hz": carriers,
        "notes": [
            "Carrier defaults are taken from prior measurement summary (fundamental and difference-channel peak).",
            "This is hypothesis-driven demodulation, not proof of hidden data.",
        ],
    }

    results: Dict[str, Any] = {"meta": meta, "per_carrier": []}

    # Decode on SUM and DIFF (often very informative)
    for domain_name, sig in [("sum", summ), ("difference", diff)]:
        dom_dir = ensure_dir(out_dir / domain_name)
        dom_block = {"domain": domain_name, "carriers": []}
        for fc in carriers:
            cdir = ensure_dir(dom_dir / f"fc_{fc:.3f}Hz")
            block = decode_for_carrier(sig, fs, fc, cdir)
            dom_block["carriers"].append(block)
        results["per_carrier"].append(dom_block)

    # Save JSON and Markdown
    (out_dir / "decode_results.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    generate_markdown_report(out_dir / "DECODE_REPORT.md", meta, results)

    print(f"Wrote: {out_dir / 'DECODE_REPORT.md'}")
    print(f"Wrote: {out_dir / 'decode_results.json'}")
    print(f"Artifacts in: {out_dir}")


if __name__ == "__main__":
    main()
