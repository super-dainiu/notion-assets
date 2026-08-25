#!/usr/bin/env python3
"""Build the terminal q/context figure for the 2026-08-25 daily note."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch


OUT = Path(__file__).resolve().parent
BLUE = "#0072B2"
ORANGE = "#E69F00"
GREEN = "#009E73"
PURPLE = "#CC79A7"
GREY = "#68707A"
LIGHT = "#EEF2F5"


def box(ax, xy, width, height, title, subtitle, color):
    patch = FancyBboxPatch(
        xy,
        width,
        height,
        boxstyle="round,pad=0.025,rounding_size=0.04",
        facecolor=color,
        edgecolor="none",
        alpha=0.14,
    )
    ax.add_patch(patch)
    ax.text(xy[0] + 0.04, xy[1] + height * 0.64, title, color=color,
            fontsize=14, weight="bold", va="center")
    ax.text(xy[0] + 0.04, xy[1] + height * 0.30, subtitle, color=GREY,
            fontsize=10.5, va="center")


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

    fig = plt.figure(figsize=(13.2, 6.4))
    grid = fig.add_gridspec(1, 2, width_ratios=[0.92, 1.5], wspace=0.23)
    mechanism = fig.add_subplot(grid[0, 0])
    results = fig.add_subplot(grid[0, 1])

    mechanism.set_xlim(0, 1)
    mechanism.set_ylim(0, 1)
    mechanism.axis("off")
    mechanism.set_title("What can survive the interaction metric?", loc="left", weight="bold")
    box(mechanism, (0.03, 0.67), 0.92, 0.19, r"Shared mutation effect  $q_m$",
        r"Useful for general response, but $D(q_m)=0$", BLUE)
    box(mechanism, (0.03, 0.39), 0.92, 0.19, r"Drug-specific gain  $b_d q_m$",
        r"The same mutation signal can be scaled by drug: $D(b_dq_m)\ne0$", GREEN)
    box(mechanism, (0.03, 0.11), 0.92, 0.19, r"Context residual  $r_{md}$",
        r"Direct mutation–drug information: $D(r_{md})\ne0$", ORANGE)
    mechanism.annotate(
        "combine only after\nheld-fold predictions exist",
        xy=(0.50, 0.37), xytext=(0.50, 0.335), ha="center", va="top",
        color=GREY, fontsize=9.5,
    )

    labels = [
        "Terminal context*",
        "Fixed q*",
        "Fixed q + context*",
        "Strict nested q†",
        "Nested q + context*",
    ]
    fold_values = np.array(
        [
            [0.12982154, 0.12229669, 0.19283197],
            [0.17342012, 0.15388359, 0.21707448],
            [0.18268913, 0.16226060, 0.23759058],
            [0.19732846, 0.17270324, 0.18777173],
            [0.19225128, 0.18019529, 0.24713335],
        ]
    )
    means = fold_values.mean(axis=1)
    colors = [ORANGE, BLUE, PURPLE, BLUE, GREEN]
    y = np.arange(len(labels))
    results.barh(y, means, color=colors, alpha=0.78, height=0.58, zorder=2)
    offsets = np.array([-0.13, 0.0, 0.13])
    fold_markers = ["o", "s", "D"]
    for fold in range(3):
        results.scatter(
            fold_values[:, fold], y + offsets[fold], marker=fold_markers[fold],
            s=38, facecolor="white", edgecolor="#263238", linewidth=1.05,
            zorder=4, label=f"Fold {fold}",
        )
    for yi, value in zip(y, means):
        results.text(value + 0.004, yi, f"{value:.3f}", va="center", weight="bold")
    results.set_yticks(y, labels)
    results.invert_yaxis()
    results.set_xlim(0, 0.275)
    results.set_xlabel("Within-drug mutant macro Spearman (equal fold mean)")
    results.set_title("Context is complementary, but not yet stable", loc="left", weight="bold")
    results.grid(axis="x", color="#E3E7EA", lw=0.8, zorder=0)
    results.legend(frameon=False, ncol=3, loc="lower right", bbox_to_anchor=(1.0, -0.20))
    results.text(
        0.0, -0.29,
        "† mechanically strict nested OOF inside the current adaptive study    "
        "* post-selection diagnostic on the same site folds",
        transform=results.transAxes, color=GREY, fontsize=9.2, va="top",
    )

    fig.suptitle(
        "Drug-specific gain survives centering; context adds complementary signal",
        x=0.04, y=0.985, ha="left", fontsize=18, weight="bold",
    )
    fig.text(
        0.99, 0.012,
        "Terminal hash-bound artifacts; drug is the context and mutant protein is the ranked item",
        ha="right", color=GREY, fontsize=9.2,
    )
    fig.subplots_adjust(left=0.04, right=0.985, bottom=0.20, top=0.88)
    stem = OUT / "fig_2026_08_25_q_context_terminal"
    fig.savefig(stem.with_suffix(".png"), dpi=300, bbox_inches="tight")
    fig.savefig(stem.with_suffix(".pdf"), bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    build()
