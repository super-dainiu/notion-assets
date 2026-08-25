#!/usr/bin/env python3
"""Build the candidate-set audit figure for the 2026-08-25 daily note."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


OUT = Path(__file__).resolve().parent
BLUE = "#0072B2"
GREEN = "#009E73"
ORANGE = "#E69F00"
GREY = "#68707A"
LIGHT = "#E5E9EC"
RED = "#C44E52"


def build() -> None:
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 10.5,
            "axes.titlesize": 13,
            "axes.labelsize": 11,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "savefig.facecolor": "white",
        }
    )

    q_mean = 0.1859344767
    adaptive_mean = 0.2066864394
    reference_mean = 0.2085463264
    adaptive_delta = np.array([0.0042002387, 0.0134856881, 0.0445699613])
    reference_delta = np.array([-0.0040948374, 0.0204094709, 0.0515209156])

    labels = [
        "Strict nested q",
        "Adaptive global gate\nheld-set ranks",
        "Fixed 60:40 fusion\ncrossfold-reference ECDF",
    ]
    means = np.array([q_mean, adaptive_mean, reference_mean])
    colors = [BLUE, GREEN, ORANGE]

    fig, axes = plt.subplots(
        1, 2, figsize=(12.4, 5.45), gridspec_kw={"width_ratios": [1.0, 1.2]}
    )

    ax = axes[0]
    y = np.arange(len(labels))
    bars = ax.barh(y, means, color=colors, alpha=0.84, height=0.58, zorder=2)
    ax.set_yticks(y, labels)
    ax.invert_yaxis()
    ax.set_xlim(0.17, 0.216)
    ax.set_xlabel("Equal-fold macro Spearman")
    ax.set_title("The average fusion gain survives", loc="left", weight="bold")
    ax.grid(axis="x", color=LIGHT, lw=0.8, zorder=0)
    for bar, value in zip(bars, means):
        ax.text(
            value + 0.0008,
            bar.get_y() + bar.get_height() / 2,
            f"{value:.4f}",
            va="center",
            weight="bold",
            fontsize=10,
        )
    ax.text(
        0.01,
        -0.20,
        "The reference-CDF arm never uses the held candidate distribution.",
        transform=ax.transAxes,
        color=GREY,
        fontsize=9.2,
    )

    ax = axes[1]
    folds = np.arange(3)
    ax.axhline(0, color="#929AA1", lw=1.1, zorder=1)
    ax.axhspan(-0.009, 0, color="#F6D8D0", alpha=0.52, zorder=0)
    methods = [
        ("Adaptive gate, held-set ranks", adaptive_delta, GREEN, "s", -0.08),
        ("Fixed 60:40, reference ECDF", reference_delta, ORANGE, "o", 0.08),
    ]
    for label, delta, color, marker, offset in methods:
        x = folds + offset
        ax.plot(x, delta, color=color, lw=1.7, alpha=0.9, zorder=2)
        ax.scatter(
            x,
            delta,
            color=color,
            marker=marker,
            s=62,
            zorder=3,
            label=label,
            edgecolor="white",
            linewidth=0.7,
        )
        for xi, value in zip(x, delta):
            y_offset = 0.0028 if value >= 0 else -0.0026
            ax.text(
                xi,
                value + y_offset,
                f"{value:+.3f}",
                ha="center",
                va="bottom" if value >= 0 else "top",
                color=RED if value < 0 else color,
                fontsize=9,
                weight="bold",
            )
    ax.set_xticks(folds, ["Fold 0", "Fold 1", "Fold 2"])
    ax.set_ylim(-0.012, 0.063)
    ax.set_ylabel("Spearman change versus strict nested q")
    ax.set_title("But the every-fold claim does not survive", loc="left", weight="bold")
    ax.grid(axis="y", color=LIGHT, lw=0.8, zorder=0)
    ax.legend(frameon=False, loc="upper left")
    ax.annotate(
        "Fold 0 changes sign",
        xy=(0.08, reference_delta[0]),
        xytext=(0.45, -0.0085),
        arrowprops={"arrowstyle": "->", "color": RED, "lw": 1.1},
        color=RED,
        fontsize=9.3,
        weight="bold",
    )

    fig.suptitle(
        "q/context complementarity is promising, not yet fold-stable",
        x=0.055,
        y=0.99,
        ha="left",
        fontsize=17.5,
        weight="bold",
    )
    fig.text(
        0.99,
        0.012,
        "Crossfold references come from different fitted models: deployment-mechanics stress test, not deployable calibration. Adaptive study; no independent test.",
        ha="right",
        color=GREY,
        fontsize=8.8,
    )
    fig.subplots_adjust(left=0.20, right=0.985, bottom=0.22, top=0.84, wspace=0.31)
    stem = OUT / "fig_2026_08_25_candidate_set_audit_terminal"
    fig.savefig(stem.with_suffix(".png"), dpi=300, bbox_inches="tight")
    fig.savefig(stem.with_suffix(".pdf"), bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    build()
