"""Create Figure 5.5 from chronological DML nuisance-model R² diagnostics."""

import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "results" / "corrected_model"
INPUT = RESULTS / "nuisance_metrics.csv"
OUTPUT = RESULTS / "figures" / "figure_5_5_dml_nuisance_model_r2_chronological_diagnostic.png"

PATHWAYS = [
    ("pms", "food", "PMS petrol price → Kano food CPI"),
    ("ago", "food", "AGO diesel price → Kano food CPI"),
    ("food", "inflation", "Kano food CPI → Kano headline inflation"),
]


def main() -> None:
    with INPUT.open(newline="", encoding="utf-8") as handle:
        records = list(csv.DictReader(handle))

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    fig, axes = plt.subplots(1, 3, figsize=(16, 8), dpi=220)
    fig.patch.set_facecolor("white")
    fig.suptitle("Figure 5.5: DML Nuisance-Model R² Results for the Chronological Diagnostic",
                 fontsize=18, fontweight="bold", color="#17365d", y=0.965)
    fig.text(0.5, 0.905,
             "Chronological 80/20 held-out diagnostic; each pathway panel uses its own R² scale",
             ha="center", fontsize=11.8, color="#4f4f4f")

    learners = ["Ridge", "RandomForest"]
    x = np.arange(len(learners))
    width = 0.34
    for ax, (treatment, outcome, title) in zip(axes, PATHWAYS):
        subset = {
            item["Learner"]: item
            for item in records
            if item["Treatment"] == treatment and item["Outcome"] == outcome
        }
        outcome_r2 = [float(subset[learner]["R2_Y"]) for learner in learners]
        treatment_r2 = [float(subset[learner]["R2_T"]) for learner in learners]
        bars_y = ax.bar(x - width / 2, outcome_r2, width, label="Outcome nuisance R²",
                        color="#4c78a8", edgecolor="#244c70")
        bars_t = ax.bar(x + width / 2, treatment_r2, width, label="Treatment nuisance R²",
                        color="#d04f45", edgecolor="#8f3028")
        ax.axhline(0, color="#555555", linewidth=1.1)
        ax.set_xticks(x, ["Ridge", "Random Forest"])
        ax.set_title(title, fontsize=11.8, fontweight="bold", color="#17365d", pad=14)
        ax.set_ylabel("Held-out R²", fontsize=10.8)
        ax.grid(axis="y", color="#d9e2f3", linewidth=0.8)
        ax.set_axisbelow(True)
        ax.spines[["top", "right"]].set_visible(False)
        values = outcome_r2 + treatment_r2
        lower = min(values) - max(0.25, abs(min(values)) * 0.15)
        ax.set_ylim(lower, 0.25)
        for bars in (bars_y, bars_t):
            for bar in bars:
                value = bar.get_height()
                ax.text(bar.get_x() + bar.get_width() / 2, value / 2,
                        f"{value:.3f}", ha="center", va="center", fontsize=9.2,
                        color="white", fontweight="bold")

    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=2, frameon=False, fontsize=11,
               bbox_to_anchor=(0.5, 0.175))
    fig.text(0.5, 0.120,
             "All held-out R² values are below zero, indicating limited nuisance-model performance on the later observations.",
             ha="center", fontsize=10.7, color="#4f4f4f")
    fig.text(0.5, 0.070, "Source: Author's analysis (2026).",
             ha="center", fontsize=10.8, color="#4f4f4f", fontstyle="italic")
    fig.subplots_adjust(left=0.07, right=0.98, top=0.80, bottom=0.29, wspace=0.32)
    fig.savefig(OUTPUT, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Saved {OUTPUT}")


if __name__ == "__main__":
    main()
