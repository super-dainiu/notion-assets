#!/usr/bin/env python3
"""Build the terminal cross-fitted q/context gate figure for 2026-08-25."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


OUT = Path(__file__).resolve().parent
BLUE = "#0072B2"
ORANGE = "#E69F00"
GREEN = "#009E73"
PURPLE = "#CC79A7"
GREY = "#68707A"
LIGHT = "#E5E9EC"


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

    q = np.array([0.1973284598, 0.1727032357, 0.1877717346])
    fixed = np.array([0.1922512773, 0.1801952864, 0.2471333549])
    global_gate = np.array([0.2015286985, 0.1861889238, 0.2323416959])
    drug_gate = np.array([0.1929636604, 0.1802703612, 0.2466184032])

    labels = ["Strict nested q", "Fixed 50:50", "Cross-fitted global", "Drug-specific hierarchical"]
    arrays = [q, fixed, global_gate, drug_gate]
    means = np.array([values.mean() for values in arrays])
    colors = [BLUE, PURPLE, GREEN, ORANGE]

    fig, axes = plt.subplots(1, 2, figsize=(12.4, 5.5), gridspec_kw={"width_ratios": [1.0, 1.25]})

    ax = axes[0]
    y = np.arange(len(labels))
    bars = ax.barh(y, means, color=colors, alpha=0.82, height=0.58, zorder=2)
    ax.set_yticks(y, labels)
    ax.invert_yaxis()
    ax.set_xlim(0.16, 0.216)
    ax.set_xlabel("Equal-fold macro Spearman")
    ax.set_title("The three hybrids have the same mean", loc="left", weight="bold")
    ax.grid(axis="x", color=LIGHT, lw=0.8, zorder=0)
    for bar, value in zip(bars, means):
        ax.text(value + 0.0011, bar.get_y() + bar.get_height() / 2, f"{value:.4f}",
                va="center", weight="bold", fontsize=10)
    ax.text(
        0.02, -0.18,
        "Mean score alone cannot choose the gate.",
        transform=ax.transAxes, color=GREY, fontsize=9.5,
    )

    ax = axes[1]
    folds = np.arange(3)
    methods = [
        ("Fixed 50:50", fixed - q, PURPLE, "o"),
        ("Cross-fitted global", global_gate - q, GREEN, "s"),
        ("Drug-specific hierarchical", drug_gate - q, ORANGE, "^"),
    ]
    ax.axhline(0, color="#929AA1", lw=1.1, zorder=1)
    ax.axhspan(-0.005, 0, color="#F6D8D0", alpha=0.45, zorder=0)
    offsets = [-0.12, 0.0, 0.12]
    label_offsets = [
        [-0.0036, 0.0025, 0.0025],
        [0.0028, 0.0028, 0.0028],
        [0.0028, -0.0038, -0.0038],
    ]
    for method_index, (offset, (label, delta, color, marker)) in enumerate(zip(offsets, methods)):
        x = folds + offset
        ax.plot(x, delta, color=color, lw=1.7, alpha=0.9, zorder=2)
        ax.scatter(x, delta, color=color, marker=marker, s=58, zorder=3, label=label,
                   edgecolor="white", linewidth=0.7)
        for fold_index, (xi, value) in enumerate(zip(x, delta)):
            text_offset = label_offsets[method_index][fold_index]
            ax.text(xi, value + text_offset, f"{value:+.3f}",
                    ha="center", va="bottom" if text_offset >= 0 else "top", color=color,
                    fontsize=8.8, weight="bold")
    ax.set_xticks(folds, ["Fold 0", "Fold 1", "Fold 2"])
    ax.set_ylim(-0.012, 0.068)
    ax.set_ylabel("Spearman change versus strict nested q")
    ax.set_title("Only the global cross-fit improves every fold", loc="left", weight="bold")
    ax.grid(axis="y", color=LIGHT, lw=0.8, zorder=0)
    ax.legend(frameon=False, ncol=1, loc="upper left")
    ax.text(
        0.99, -0.18,
        "Selected q weights: 0.6, 0.6, 0.7; context receives the remainder.",
        transform=ax.transAxes, ha="right", color=GREY, fontsize=9.5,
    )

    fig.suptitle(
        "A small global q/context gate is more stable than drug-specific gating",
        x=0.055, y=0.99, ha="left", fontsize=17.5, weight="bold",
    )
    fig.text(
        0.99, 0.012,
        "Other-fold labels fit each gate; own-fold labels are excluded. Adaptive-study diagnostic, not independent confirmation.",
        ha="right", color=GREY, fontsize=9.2,
    )
    fig.subplots_adjust(left=0.19, right=0.985, bottom=0.22, top=0.86, wspace=0.30)
    stem = OUT / "fig_2026_08_25_crossfit_gate_terminal"
    fig.savefig(stem.with_suffix(".png"), dpi=300, bbox_inches="tight")
    fig.savefig(stem.with_suffix(".pdf"), bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    build()
