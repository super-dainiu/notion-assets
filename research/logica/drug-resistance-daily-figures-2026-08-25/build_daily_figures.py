#!/usr/bin/env python3
"""Build the four missing figures for the 2026-08-21--25 daily notes.

The numbers are frozen from the resistance audit artifacts described in
README.md.  The 2026-08-22 panel is explicitly a conceptual illustration.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, Rectangle


OUT = Path(__file__).resolve().parent
BLUE = "#0072B2"
ORANGE = "#E69F00"
GREEN = "#009E73"
RED = "#D55E00"
SKY = "#56B4E9"
PURPLE = "#CC79A7"
GREY = "#68707A"
LIGHT = "#EEF2F5"


def style() -> None:
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 11,
            "axes.titlesize": 16,
            "axes.labelsize": 12,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "savefig.facecolor": "white",
        }
    )


def save(fig: plt.Figure, stem: str) -> None:
    fig.savefig(OUT / f"{stem}.png", dpi=300, bbox_inches="tight")
    fig.savefig(OUT / f"{stem}.pdf", bbox_inches="tight")
    plt.close(fig)


def split_figure() -> None:
    fig, ax = plt.subplots(figsize=(10.5, 6.1))
    ax.set_xlim(0, 287)
    ax.set_ylim(-0.5, 11.6)
    ax.set_yticks(range(11))
    ax.set_yticklabels([f"Drug {i}" for i in range(1, 12)])
    ax.set_xlabel("MET kinase-domain residue sites (schematic ordering)")
    fig.suptitle(
        "Split residue sites once; keep every drug measurement together",
        x=0.075,
        y=0.98,
        ha="left",
        fontsize=17,
        weight="bold",
    )

    blocks = [(0, 229, BLUE, "Train\n229 sites"), (229, 258, ORANGE, "Validation\n29 sites"), (258, 287, GREEN, "Test\n29 sites")]
    for x0, x1, color, label in blocks:
        for drug in range(11):
            ax.add_patch(Rectangle((x0, drug - 0.38), x1 - x0, 0.76, facecolor=color, alpha=0.72, edgecolor="white", lw=0.6))
        ax.text((x0 + x1) / 2, 11.05, label, ha="center", va="bottom", color=color, weight="bold")

    ax.axvline(229, color="white", lw=2)
    ax.axvline(258, color="white", lw=2)
    fig.text(
        0.985,
        0.015,
        "All substitutions at one residue and all 11 drug contexts stay in the same partition",
        ha="right",
        color=GREY,
        fontsize=10,
    )
    ax.grid(False)
    fig.subplots_adjust(left=0.075, right=0.985, bottom=0.15, top=0.82)
    save(fig, "fig_2026_08_21_site_grouped_split")


def shared_interaction_figure() -> None:
    drugs = np.arange(1, 12)
    q = np.array([-0.55, 0.05, 0.58])
    residuals = np.array(
        [
            [0.20, -0.08, 0.02, 0.34, -0.18, -0.12, 0.10, -0.05, 0.28, -0.25, -0.06],
            [-0.22, 0.17, 0.05, -0.12, 0.25, -0.03, -0.20, 0.23, -0.06, 0.01, -0.08],
            [0.05, 0.19, -0.27, -0.04, 0.14, 0.30, -0.12, -0.22, 0.08, -0.16, 0.05],
        ]
    )
    colors = [BLUE, ORANGE, GREEN]
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.9), sharey=True)
    for idx, color in enumerate(colors):
        axes[0].plot(drugs, q[idx] + residuals[idx], marker="o", ms=4, lw=2, color=color, label=f"Mutation {idx + 1}")
        axes[1].plot(drugs, np.repeat(q[idx], len(drugs)), marker="o", ms=4, lw=2, color=color)
    axes[0].set_title("Measured: shared +\ndrug-specific", loc="left", weight="bold", fontsize=13)
    axes[1].set_title("Early model: mostly\nshared mutation effect", loc="left", weight="bold", fontsize=13)
    for ax in axes:
        ax.set_xlabel("Drug context")
        ax.set_xticks([1, 3, 5, 7, 9, 11])
        ax.axhline(0, color="#D9DEE3", lw=1)
    axes[0].set_ylabel("Response (arbitrary units)")
    axes[0].legend(frameon=False, loc="lower right")
    fig.suptitle("Why lower regression loss did not guarantee drug-specific ranking", x=0.06, ha="left", fontsize=17, weight="bold")
    fig.text(0.99, 0.01, "Conceptual illustration — not measured values", ha="right", color=GREY, fontsize=9)
    fig.subplots_adjust(left=0.08, right=0.98, bottom=0.14, top=0.77, wspace=0.22)
    save(fig, "fig_2026_08_22_shared_vs_interaction")


def baseline_figure() -> None:
    datasets = ["Coelho", "Kim"]
    boltz = np.array([0.052, 0.068])
    drugclip = np.array([0.070, 0.154])
    x = np.arange(len(datasets))
    width = 0.32
    fig, ax = plt.subplots(figsize=(8.2, 5.2))
    bars1 = ax.bar(x - width / 2, boltz, width, color=SKY, label="Boltz-2")
    bars2 = ax.bar(x + width / 2, drugclip, width, color=ORANGE, label="DrugCLIP")
    ax.bar_label(bars1, fmt="%.3f", padding=4, fontsize=11)
    ax.bar_label(bars2, fmt="%.3f", padding=4, fontsize=11)
    ax.set_xticks(x, datasets)
    ax.set_ylim(0, 0.18)
    ax.set_ylabel("Within-drug mutant macro Spearman")
    ax.set_title("Frozen representations contain weak positive resistance signal", loc="left", weight="bold")
    ax.legend(frameon=False, ncol=2, loc="upper left")
    ax.grid(axis="y", color="#E6EAED", lw=0.8)
    fig.text(
        0.985,
        0.015,
        "Preliminary cached-head audit; symmetric tuning was completed the next day",
        ha="right",
        color=GREY,
        fontsize=9,
    )
    fig.subplots_adjust(left=0.11, right=0.98, bottom=0.15, top=0.87)
    save(fig, "fig_2026_08_24_preliminary_baselines")


def current_picture_figure() -> None:
    q_transfer = np.array([0.2473369, 0.2285147, 0.2496733])
    direct = np.array([-0.1324076, -0.1335444, -0.1279451])
    labels = ["Coelho\nBoltz-2", "Coelho\nDrugCLIP", "Kim\nBoltz-2", "Kim\nDrugCLIP"]
    lr_delta = np.array([0.006289, 0.000580, -0.011163, 0.004243])
    colors = [BLUE, ORANGE, SKY, PURPLE]

    fig, axes = plt.subplots(1, 2, figsize=(11.4, 5.4))
    ax = axes[0]
    for x, values, color, label in [(0, q_transfer, GREEN, "q = f − g"), (1, direct, GREY, "Direct q head")]:
        ax.scatter(np.repeat(x, 3) + np.array([-0.045, 0, 0.045]), values, s=55, color=color, zorder=3)
        ax.hlines(np.median(values), x - 0.18, x + 0.18, color=color, lw=4, label=label)
    ax.axhline(0, color="#C9CFD4", lw=1)
    ax.set_xticks([0, 1], ["q = f − g", "Direct q head"])
    ax.set_ylabel("General-response Spearman")
    ax.set_title("Shared mutation response transfers", loc="left", weight="bold")
    ax.text(0, np.median(q_transfer) + 0.035, "median 0.247", ha="center", color=GREEN, weight="bold")
    ax.text(1, np.median(direct) - 0.055, "median −0.132", ha="center", color=GREY, weight="bold")
    ax.set_ylim(-0.23, 0.35)

    ax = axes[1]
    y = np.arange(len(labels))
    ax.axvline(0, color="#9FA7AE", lw=1)
    for yi, value, color in zip(y, lr_delta, colors):
        ax.plot([0, value], [yi, yi], color=color, lw=3)
        ax.scatter(value, yi, s=70, color=color, zorder=3)
        ax.text(value + (0.0007 if value >= 0 else -0.0007), yi, f"{value:+.4f}", ha="left" if value >= 0 else "right", va="center")
    ax.set_yticks(y, labels)
    ax.invert_yaxis()
    ax.set_xlim(-0.014, 0.009)
    ax.set_xlabel("Macro Spearman change from lower-LR expansion")
    ax.set_title("More cached-head tuning did not clear the gate", loc="left", weight="bold")
    ax.grid(axis="x", color="#E6EAED", lw=0.8)

    fig.suptitle("The shared component works; drug-specific interaction remains the bottleneck", x=0.055, ha="left", fontsize=17, weight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.92), w_pad=3.0)
    save(fig, "fig_2026_08_25_general_vs_interaction")


if __name__ == "__main__":
    style()
    split_figure()
    shared_interaction_figure()
    baseline_figure()
    current_picture_figure()
