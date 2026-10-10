"""Create Figure 5.2 for the main fuel--food--inflation PCMCI+ pathways."""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "results" / "corrected_model"
FIGURES = RESULTS / "figures"
INPUT = RESULTS / "pcmci_to_dml_mapping.csv"
OUTPUT = FIGURES / "figure_5_2_pcmci_main_fuel_food_inflation_relationships.png"

DISPLAY = {
    "pms": "PMS petrol price",
    "ago": "AGO diesel price",
    "food": "Kano food CPI",
    "inflation": "Kano headline inflation",
}
POSITIONS = {
    "pms": (0.18, 0.72),
    "ago": (0.18, 0.37),
    "food": (0.51, 0.55),
    "inflation": (0.84, 0.55),
}


def add_node(ax, x: float, y: float, label: str, color: str) -> None:
    width, height = 0.225, 0.125
    patch = FancyBboxPatch(
        (x - width / 2, y - height / 2), width, height,
        boxstyle="round,pad=0.014,rounding_size=0.02",
        transform=ax.transAxes, linewidth=1.9, edgecolor="#1f4e79",
        facecolor=color, zorder=3,
    )
    ax.add_patch(patch)
    ax.text(x, y, label, transform=ax.transAxes, ha="center", va="center",
            fontsize=12, fontweight="bold", color="#17365d", zorder=4)


def main() -> None:
    links = pd.read_csv(INPUT)
    FIGURES.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(14, 8), dpi=220)
    fig.patch.set_facecolor("white")
    ax.set_axis_off()
    fig.suptitle("Figure 5.2: PCMCI+ Results for the Main Fuel–Food–Inflation Relationships",
                 fontsize=18.5, fontweight="bold", color="#17365d", y=0.965)
    ax.text(0.5, 0.902,
            "Nominal PCMCI+ relationships selected for effect estimation; none remains statistically supported after BH-FDR correction",
            transform=ax.transAxes, ha="center", fontsize=11.7, color="#4f4f4f")

    add_node(ax, *POSITIONS["pms"], DISPLAY["pms"], "#dbeaf7")
    add_node(ax, *POSITIONS["ago"], DISPLAY["ago"], "#dbeaf7")
    add_node(ax, *POSITIONS["food"], DISPLAY["food"], "#fce5cd")
    add_node(ax, *POSITIONS["inflation"], DISPLAY["inflation"], "#fce5cd")

    label_positions = {
        ("pms", "food"): (0.385, 0.825),
        ("ago", "food"): (0.385, 0.260),
        ("food", "inflation"): (0.675, 0.685),
    }
    for _, row in links.iterrows():
        treatment, outcome = row["Treatment"], row["Outcome"]
        start, end = POSITIONS[treatment], POSITIONS[outcome]
        arrow = FancyArrowPatch(
            start, end, transform=ax.transAxes, arrowstyle="-|>", mutation_scale=19,
            linewidth=2.5, linestyle="--", color="#c26a00", shrinkA=28, shrinkB=28,
            zorder=2,
        )
        ax.add_patch(arrow)
        mid_x, mid_y = label_positions[(treatment, outcome)]
        label = (f"Lag {int(row['PCMCI_Lag'])}  |  r = {row['PCMCI_Statistic']:.3f}\n"
                 f"raw p = {row['PCMCI_P']:.3f}  |  BH-FDR q = {row['PCMCI_Q']:.3f}")
        ax.text(mid_x, mid_y, label, transform=ax.transAxes, ha="center", va="center",
                fontsize=10.3, fontweight="semibold", color="#7a3d00",
                bbox={"boxstyle": "round,pad=0.30", "facecolor": "white", "edgecolor": "#e4bb8d"},
                zorder=5)

    ax.text(0.5, 0.145,
            "Dashed arrows denote nominal (raw p < 0.05) temporal associations. They are exploratory and are not BH-FDR-supported PCMCI+ discoveries.",
            transform=ax.transAxes, ha="center", fontsize=10.6, color="#4f4f4f")
    ax.text(0.5, 0.095,
            "PCMCI+ statistics are partial correlations conditional on the algorithm's selected temporal parents; they are not causal-effect estimates.",
            transform=ax.transAxes, ha="center", fontsize=10.6, color="#4f4f4f")
    ax.text(0.5, 0.035, "Source: Author's analysis (2026).",
            transform=ax.transAxes, ha="center", fontsize=10.8, fontstyle="italic", color="#4f4f4f")

    fig.savefig(OUTPUT, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Saved {OUTPUT}")


if __name__ == "__main__":
    main()
