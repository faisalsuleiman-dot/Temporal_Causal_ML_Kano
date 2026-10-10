"""Create Figure 5.6 for selected PCMCI+ relationships across maximum-lag windows."""

import csv
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "results" / "corrected_model"
INPUT = RESULTS / "table_5_8_pcmci_sensitivity_maximum_lag_windows.csv"
OUTPUT = RESULTS / "figures" / "figure_5_6_pcmci_selected_relationships_lag_sensitivity.png"

STYLE = {
    "PMS petrol price → Kano food CPI": ("#4c78a8", "o"),
    "AGO diesel price → Kano food CPI": ("#f28e2b", "s"),
    "Kano food CPI → Kano headline inflation": ("#59a14f", "^"),
}


def main() -> None:
    with INPUT.open(newline="", encoding="utf-8") as handle:
        records = list(csv.DictReader(handle))

    grouped = defaultdict(list)
    for row in records:
        if row["PCMCI+ partial correlation"] != "Not tested":
            grouped[row["Selected relationship"]].append(row)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    fig, (ax_stat, ax_q) = plt.subplots(1, 2, figsize=(15, 7.7), dpi=220)
    fig.patch.set_facecolor("white")
    fig.suptitle("Figure 5.6: PCMCI+ Sensitivity of the Selected Relationships Across Maximum Lag Windows",
                 fontsize=17.5, fontweight="bold", color="#17365d", y=0.965)
    fig.text(0.5, 0.905,
             "Selected relationship lag is held fixed while the PCMCI+ maximum lag window varies",
             ha="center", fontsize=11.7, color="#4f4f4f")

    for relationship, rows in grouped.items():
        rows.sort(key=lambda row: int(row["Maximum lag window (months)"]))
        x = [int(row["Maximum lag window (months)"]) for row in rows]
        statistics = [float(row["PCMCI+ partial correlation"]) for row in rows]
        q_values = [float(row["BH-FDR q-value"]) for row in rows]
        color, marker = STYLE[relationship]
        ax_stat.plot(x, statistics, color=color, marker=marker, linewidth=2.5, markersize=8, label=relationship)
        ax_q.plot(x, q_values, color=color, marker=marker, linewidth=2.5, markersize=8, label=relationship)

    for ax in (ax_stat, ax_q):
        ax.set_xticks([3, 6, 9])
        ax.set_xlabel("Maximum lag window (months)", fontsize=11.5)
        ax.grid(color="#d9e2f3", linewidth=0.8)
        ax.spines[["top", "right"]].set_visible(False)
        ax.tick_params(labelsize=10.5)
    ax_stat.set_ylabel("PCMCI+ partial correlation", fontsize=11.5)
    ax_stat.set_title("Conditional association statistic", fontsize=12.5, fontweight="bold", color="#17365d", pad=12)
    ax_stat.set_ylim(0.15, 0.38)

    ax_q.axhline(0.05, color="#b35a00", linewidth=1.8, linestyle="--", label="BH-FDR threshold (q = 0.05)")
    ax_q.set_ylabel("BH-FDR q-value", fontsize=11.5)
    ax_q.set_title("Multiplicity-adjusted evidence", fontsize=12.5, fontweight="bold", color="#17365d", pad=12)
    ax_q.set_ylim(0, 0.95)

    handles, labels = ax_q.get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=2, frameon=False, fontsize=10.2,
               bbox_to_anchor=(0.5, 0.155))
    fig.text(0.5, 0.105,
             "The AGO → Food CPI lag-5 relationship is not evaluated at the 3-month maximum window. All displayed q-values exceed 0.05.",
             ha="center", fontsize=10.5, color="#4f4f4f")
    fig.text(0.5, 0.060, "Source: Author's analysis (2026).",
             ha="center", fontsize=10.8, color="#4f4f4f", fontstyle="italic")
    fig.subplots_adjust(left=0.08, right=0.98, top=0.79, bottom=0.29, wspace=0.25)
    fig.savefig(OUTPUT, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Saved {OUTPUT}")


if __name__ == "__main__":
    main()
