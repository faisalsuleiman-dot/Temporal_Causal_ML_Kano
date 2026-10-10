"""Create Figure 5.4: mean PCMCI+ simulation performance across ten replications."""

import csv
import statistics
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "results" / "corrected_model"
INPUT = RESULTS / "simulation_metrics.csv"
OUTPUT = RESULTS / "figures" / "figure_5_4_mean_pcmci_simulation_performance.png"

METRICS = [
    ("Precision", "Precision", "#4c78a8"),
    ("Recall", "Recall", "#59a14f"),
    ("F1", "F1-score", "#9c755f"),
    ("FDR", "False discovery rate\n(FDR)", "#d04f45"),
]


def main() -> None:
    with INPUT.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    labels = [label for _, label, _ in METRICS]
    means = [statistics.mean(float(row[key]) for row in rows) for key, _, _ in METRICS]
    colors = [color for _, _, color in METRICS]

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(11.5, 7.5), dpi=220)
    fig.patch.set_facecolor("white")
    bars = ax.bar(labels, means, color=colors, edgecolor="#244c70", linewidth=1.1, width=0.62)
    ax.set_ylim(0, 1.10)
    ax.set_ylabel("Mean performance value", fontsize=12)
    ax.set_yticks([i / 10 for i in range(0, 11, 2)])
    ax.grid(axis="y", color="#d9e2f3", linewidth=0.9)
    ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(axis="x", labelsize=12)
    ax.tick_params(axis="y", labelsize=11)

    for bar, mean in zip(bars, means):
        ax.text(bar.get_x() + bar.get_width() / 2, mean + 0.035, f"{mean:.3f}",
                ha="center", va="bottom", fontsize=13, fontweight="bold", color="#17365d")

    ax.set_title("Figure 5.4: Mean PCMCI+ Simulation Performance Across Ten Replications",
                 fontsize=17, fontweight="bold", color="#17365d", pad=24)
    ax.text(0.5, 1.01,
            "Means calculated from 10 simulation replications (500 observations per replication)",
            transform=ax.transAxes, ha="center", fontsize=11.5, color="#4f4f4f")
    fig.text(0.5, 0.085,
             "Higher values are favourable for Precision, Recall and F1-score; lower values are favourable for the false discovery rate.",
             ha="center", fontsize=10.7, color="#4f4f4f")
    fig.text(0.5, 0.040, "Source: Author's analysis (2026).",
             ha="center", fontsize=10.8, color="#4f4f4f", fontstyle="italic")
    fig.subplots_adjust(top=0.82, bottom=0.21, left=0.12, right=0.97)
    fig.savefig(OUTPUT, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Saved {OUTPUT}")


if __name__ == "__main__":
    main()
