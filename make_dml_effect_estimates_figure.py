"""Create Figure 5.3 from the selected LinearDML effect estimates."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "results" / "corrected_model"
INPUT = RESULTS / "dml_effects.csv"
OUTPUT = RESULTS / "figures" / "figure_5_3_dml_effect_estimates_selected_relationships.png"

PATHWAYS = [
    ("pms", "food", "PMS petrol price → Kano food CPI"),
    ("ago", "food", "AGO diesel price → Kano food CPI"),
    ("food", "inflation", "Kano food CPI → Kano headline inflation"),
]


def p_text(value: float) -> str:
    return "p < 0.001" if value < 0.001 else f"p = {value:.3f}"


def main() -> None:
    effects = pd.read_csv(INPUT)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(1, 3, figsize=(16, 7.6), dpi=220)
    fig.patch.set_facecolor("white")
    fig.suptitle("Figure 5.3: DML Effect Estimates for the Selected Fuel–Food–Inflation Relationships",
                 fontsize=18, fontweight="bold", color="#17365d", y=0.965)
    fig.text(0.5, 0.905,
             "LinearDML estimates with 95% confidence intervals; each panel uses its own effect scale",
             ha="center", fontsize=11.8, color="#4f4f4f")

    for ax, (treatment, outcome, title) in zip(axes, PATHWAYS):
        row = effects[(effects["Treatment"] == treatment) & (effects["Outcome"] == outcome)].iloc[0]
        estimate, lower, upper = row["Effect"], row["CI_Lower"], row["CI_Upper"]
        left_error, right_error = estimate - lower, upper - estimate

        ax.axvline(0, color="#7f7f7f", linewidth=1.2, linestyle="--", zorder=0)
        ax.errorbar(estimate, 0, xerr=[[left_error], [right_error]], fmt="o",
                    color="#b35a00", ecolor="#b35a00", elinewidth=3, capsize=7,
                    markersize=10, zorder=3)
        margin = max((upper - lower) * 0.45, abs(estimate) * 0.35)
        ax.set_xlim(min(0, lower) - margin, upper + margin)
        ax.set_ylim(-0.85, 0.85)
        ax.set_yticks([])
        ax.set_title(title, fontsize=12.3, fontweight="bold", color="#17365d", pad=16)
        ax.set_xlabel("LinearDML effect estimate", fontsize=10.8)
        ax.grid(axis="x", color="#d9e2f3", linewidth=0.8)
        for spine in ("top", "right", "left"):
            ax.spines[spine].set_visible(False)

        stats = (
            f"Lag: {int(row['Lag'])} months\n"
            f"N = {int(row['N'])}\n"
            f"Effect = {estimate:.5f}\n"
            f"95% CI: [{lower:.5f}, {upper:.5f}]\n"
            f"SE = {row['SE']:.5f}; {p_text(row['P_value'])}"
        )
        ax.text(0.5, 0.10, stats, transform=ax.transAxes, ha="center", va="bottom",
                fontsize=10.2, color="#4f4f4f",
                bbox={"boxstyle": "round,pad=0.40", "facecolor": "#f7fbff", "edgecolor": "#a6bddb"})

    fig.text(0.5, 0.105,
             "Note: DML estimates are exploratory conditional effect estimates. The selected relationships met the nominal PCMCI+ significance criterion but did not remain statistically supported after the BH-FDR correction.",
             ha="center", fontsize=10.2, color="#4f4f4f", fontweight="semibold", wrap=True)
    fig.text(0.5, 0.060, "Source: Author's analysis (2026).",
             ha="center", fontsize=10.8, color="#4f4f4f", fontstyle="italic")
    fig.subplots_adjust(left=0.06, right=0.97, top=0.80, bottom=0.23, wspace=0.34)
    fig.savefig(OUTPUT, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Saved {OUTPUT}")


if __name__ == "__main__":
    main()
