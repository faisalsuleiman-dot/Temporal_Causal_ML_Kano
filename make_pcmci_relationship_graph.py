"""Create Figure 5.1 from the primary FDR-supported PCMCI+ results."""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "results" / "corrected_model"
FIGURES = RESULTS / "figures"
INPUT = RESULTS / "pcmci_fdr_significant_links.csv"
OUTPUT = FIGURES / "figure_5_1_pcmci_temporal_relationship_graph.png"


DISPLAY_NAMES = {
    "m2": "Broad money supply (M2)",
    "fx": "NGN/USD exchange rate",
    "tariff": "KEDCO electricity tariff",
    "inflation": "Kano headline inflation",
}

POSITIONS = {
    "m2": (0.17, 0.67),
    "fx": (0.50, 0.67),
    "tariff": (0.83, 0.67),
    "inflation": (0.50, 0.24),
}


def column(frame: pd.DataFrame, *names: str) -> str:
    for name in names:
        if name in frame.columns:
            return name
    raise KeyError(f"Expected one of {names}; found {list(frame.columns)}")


def q_text(value: float) -> str:
    return "q < 0.001" if value < 0.001 else f"q = {value:.3f}"


def add_node(ax, x: float, y: float, label: str) -> None:
    width, height = 0.255, 0.115
    patch = FancyBboxPatch(
        (x - width / 2, y - height / 2), width, height,
        boxstyle="round,pad=0.012,rounding_size=0.018",
        linewidth=1.8, edgecolor="#1f4e79", facecolor="#dbeaf7",
        transform=ax.transAxes, zorder=3,
    )
    ax.add_patch(patch)
    ax.text(x, y, label, transform=ax.transAxes, ha="center", va="center",
            fontsize=11.2, fontweight="semibold", color="#17365d", zorder=4,
            wrap=True)


def add_arrow(ax, start, end, label: str, rad: float = 0.0) -> None:
    arrow = FancyArrowPatch(
        start, end, transform=ax.transAxes, arrowstyle="-|>",
        mutation_scale=18, linewidth=2.4, color="#b35a00",
        connectionstyle=f"arc3,rad={rad}", shrinkA=26, shrinkB=26, zorder=2,
    )
    ax.add_patch(arrow)
    x = (start[0] + end[0]) / 2
    y = (start[1] + end[1]) / 2 + (0.075 if rad >= 0 else -0.075)
    ax.text(x, y, label, transform=ax.transAxes, ha="center", va="center",
            fontsize=10.2, color="#7a3d00", fontweight="semibold",
            bbox={"boxstyle": "round,pad=0.26", "facecolor": "white", "edgecolor": "#e4bb8d"},
            zorder=5)


def main() -> None:
    links = pd.read_csv(INPUT)
    cause_col = column(links, "Cause", "cause", "Source", "source")
    effect_col = column(links, "Effect", "effect", "Target", "target")
    lag_col = column(links, "Lag", "lag")
    stat_col = column(links, "Statistic", "Stat", "stat", "val")
    q_col = column(links, "BH_FDR_Q", "q_value", "q", "FDR_q", "p_value_fdr")

    FIGURES.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(14, 8), dpi=220)
    fig.patch.set_facecolor("white")
    ax.set_axis_off()

    fig.suptitle("Figure 5.1: PCMCI+ Temporal Relationship Graph",
                 fontsize=20, fontweight="bold", color="#17365d", y=0.965)
    ax.text(0.5, 0.90, "Primary BH-FDR-supported temporal relationships (maximum lag = 6 months)",
            transform=ax.transAxes, ha="center", fontsize=12.3, color="#4f4f4f")

    variables = set(links[cause_col]).union(links[effect_col])
    for variable in sorted(variables):
        add_node(ax, *POSITIONS[variable], DISPLAY_NAMES[variable])

    for _, row in links.iterrows():
        cause, effect = row[cause_col], row[effect_col]
        label = f"Lag {int(row[lag_col])}  |  r = {row[stat_col]:.3f}  |  {q_text(row[q_col])}"
        if cause == effect:
            x, y = POSITIONS[cause]
            loop = FancyArrowPatch(
                (x + 0.08, y + 0.045), (x - 0.08, y + 0.045), transform=ax.transAxes,
                arrowstyle="-|>", mutation_scale=18, linewidth=2.4, color="#b35a00",
                connectionstyle="arc3,rad=1.35", zorder=2,
            )
            ax.add_patch(loop)
            ax.text(x, y + 0.20, label, transform=ax.transAxes, ha="center", va="center",
                    fontsize=10.2, color="#7a3d00", fontweight="semibold",
                    bbox={"boxstyle": "round,pad=0.26", "facecolor": "white", "edgecolor": "#e4bb8d"},
                    zorder=5)
        else:
            add_arrow(ax, POSITIONS[cause], POSITIONS[effect], label)

    ax.text(0.5, 0.055,
            "Arrows indicate lagged conditional associations identified by PCMCI+. Only links with BH-FDR q < 0.05 are displayed.",
            transform=ax.transAxes, ha="center", fontsize=10.7, color="#4f4f4f")
    ax.text(0.5, 0.015, "Source: Author's analysis (2026).",
            transform=ax.transAxes, ha="center", fontsize=10.5, fontstyle="italic", color="#4f4f4f")

    fig.savefig(OUTPUT, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Saved {OUTPUT}")


if __name__ == "__main__":
    main()
